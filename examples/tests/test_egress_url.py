from __future__ import annotations

import socket

import pytest

from examples.security.egress_url import authorize_url

ALLOWED = frozenset({"los.harborlight.example"})


def resolver(*addresses: str):
    """A hermetic stand-in for DNS: the test never touches the network."""

    def resolve(host, port, type=socket.SOCK_STREAM):
        return [(socket.AF_INET, type, 6, "", (address, port)) for address in addresses]

    return resolve


PUBLIC = resolver("93.184.216.34")


def test_an_allowed_https_destination_is_canonicalized_with_its_addresses():
    canonical, addresses = authorize_url(
        "HTTPS://LOS.Harborlight.Example./v1/documents?case=MORT-2026-000184",
        ALLOWED,
        resolve=PUBLIC,
    )
    assert canonical == (
        "https://los.harborlight.example:443/v1/documents?case=MORT-2026-000184"
    )
    assert addresses == ("93.184.216.34",)


@pytest.mark.parametrize(
    "url",
    [
        "http://los.harborlight.example/v1",  # not HTTPS
        "https://user:secret@los.harborlight.example/v1",  # credentials in URL
        "https://los.harborlight.example:8443/v1",  # non-443 port
        "https://uploads.attacker.example/bank-records",  # host not on the grant
    ],
)
def test_destinations_outside_the_grant_are_refused(url):
    with pytest.raises(PermissionError):
        authorize_url(url, ALLOWED, resolve=PUBLIC)


@pytest.mark.parametrize("address", ["10.0.0.5", "127.0.0.1", "169.254.169.254", "::1"])
def test_an_allowed_name_that_resolves_to_a_private_address_is_blocked(address):
    # DNS rebinding: an allowlisted name pointed at an internal address.
    with pytest.raises(PermissionError, match="non-public address blocked"):
        authorize_url("https://los.harborlight.example/v1", ALLOWED, resolve=resolver(address))


def test_one_private_address_among_public_ones_blocks_the_grant():
    with pytest.raises(PermissionError, match="non-public"):
        authorize_url(
            "https://los.harborlight.example/v1",
            ALLOWED,
            resolve=resolver("93.184.216.34", "192.168.1.10"),
        )


def test_a_url_without_a_host_is_rejected():
    with pytest.raises(ValueError):
        authorize_url("https:///v1", ALLOWED, resolve=PUBLIC)
