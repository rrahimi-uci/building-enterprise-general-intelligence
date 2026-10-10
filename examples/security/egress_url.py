"""Default-deny URL authorization for an egress grant.

The egress proxy canonicalizes a destination before it opens a connection:
HTTPS only, no credentials in the URL, port 443, a host on the grant's
allowlist, and only public addresses. It returns the canonical URL and the
resolved addresses. The proxy must connect only to those addresses for this
grant; resolving the name again at connect time reopens DNS rebinding.
"""
from __future__ import annotations

import ipaddress
import socket
from typing import Callable
from urllib.parse import urlsplit, urlunsplit

Resolver = Callable[..., list]

# --8<-- example:start


def authorize_url(
    raw_url: str,
    allowed_hosts: frozenset[str],
    *,
    resolve: Resolver = socket.getaddrinfo,
) -> tuple[str, tuple[str, ...]]:
    parsed = urlsplit(raw_url)
    if parsed.scheme.lower() != "https" or parsed.username or parsed.password:
        raise PermissionError("invalid egress URL")
    if not parsed.hostname:
        raise ValueError("host required")
    host = parsed.hostname.encode("idna").decode("ascii").rstrip(".").lower()
    port = parsed.port or 443
    if port != 443 or host not in allowed_hosts:
        raise PermissionError("destination outside egress grant")
    addresses: set[str] = set()
    for item in resolve(host, port, type=socket.SOCK_STREAM):
        address = ipaddress.ip_address(item[4][0])
        if not address.is_global:
            raise PermissionError(f"non-public address blocked: {address}")
        addresses.add(address.compressed)
    canonical = urlunsplit(("https", f"{host}:443", parsed.path or "/", parsed.query, ""))
    # Connect only to these addresses; a second lookup reopens DNS rebinding.
    return canonical, tuple(sorted(addresses))


# --8<-- example:end
