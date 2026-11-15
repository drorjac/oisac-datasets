"""Read remote files without downloading them: a seekable file over HTTP range requests.

Zenodo and 4TU.ResearchData both answer range requests, so `zipfile` can read the table of
contents of a multi-GB archive and pull out one member with a few small requests.
"""
from __future__ import annotations

import io
import zipfile

import requests

UA = {"User-Agent": "oisac-datasets/0.1 (+https://github.com/drorjac/oisac-datasets)"}


class HTTPRangeFile(io.RawIOBase):
    """A read-only, seekable file whose bytes come from HTTP range requests."""

    def __init__(self, url: str, size: int | None = None, block: int = 1 << 20,
                 session: requests.Session | None = None):
        self.url, self.block = url, block
        self.s = session or requests.Session()
        self.s.headers.update(UA)
        if size is None:
            r = self.s.get(url, headers={"Range": "bytes=0-0"}, stream=True, timeout=60)
            r.raise_for_status()
            if r.status_code != 206:
                r.close()
                raise OSError(f"server does not support range requests: {url}")
            size = int(r.headers["Content-Range"].rsplit("/", 1)[1])
            self.url = r.url  # keep the redirect target
            r.close()
        self.size, self.pos = size, 0
        self._cache: dict[int, bytes] = {}
        self.requests = 0

    def readable(self): return True
    def seekable(self): return True
    def tell(self): return self.pos

    def seek(self, off, whence=io.SEEK_SET):
        self.pos = {io.SEEK_SET: off, io.SEEK_CUR: self.pos + off, io.SEEK_END: self.size + off}[whence]
        return self.pos

    def _get_block(self, i: int) -> bytes:
        if i not in self._cache:
            a = i * self.block
            b = min(a + self.block, self.size) - 1
            r = self.s.get(self.url, headers={"Range": f"bytes={a}-{b}"}, timeout=120)
            r.raise_for_status()
            self.requests += 1
            if len(self._cache) > 64:
                self._cache.clear()
            self._cache[i] = r.content
        return self._cache[i]

    def read(self, n=-1):
        if n is None or n < 0:
            n = self.size - self.pos
        n = max(0, min(n, self.size - self.pos))
        out = bytearray()
        while n:
            i, o = divmod(self.pos, self.block)
            chunk = self._get_block(i)[o:o + n]
            if not chunk:
                break
            out += chunk
            self.pos += len(chunk)
            n -= len(chunk)
        return bytes(out)

    def readinto(self, b):
        data = self.read(len(b))
        b[:len(data)] = data
        return len(data)


def remote_zip(url: str, size: int | None = None) -> zipfile.ZipFile:
    """Open a remote zip archive for listing and for extracting single members."""
    return zipfile.ZipFile(HTTPRangeFile(url, size=size))
