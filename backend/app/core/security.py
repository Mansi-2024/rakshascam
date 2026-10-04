"""SSRF Prevention and Strict URL Validation Engine.

Enforces zero-trust egress policies as defined in SECURITY.md:
- Scheme allowlist: only http:// and https://
- Hostname and IP blacklisting: loopback, private RFC1918, link-local, carrier NAT, multicast, reserved
- IPv4-mapped IPv6 unwrapping
- Cloud metadata service blacklisting (169.254.169.254, fd00:ec2::254)
- Pre-flight DNS resolution before HTTP socket dispatch
"""

import ipaddress
import re
import socket
from typing import List, Optional, Tuple
from urllib.parse import urlsplit, urlunsplit

from app.core.config import settings


class SecurityError(Exception):
    """Base exception for security policy violations."""
    pass


class URLValidationError(SecurityError):
    """Raised when URL scheme, formatting, or target is invalid."""
    pass


class URLLengthExceededError(URLValidationError):
    """Raised when URL length exceeds configured maximum length."""
    pass


class SSRFSecurityError(SecurityError):
    """Raised when destination points to an internal, private, loopback, or metadata IP."""
    pass


# Specific cloud metadata and non-routable targets
METADATA_IPS = {
    ipaddress.ip_address("169.254.169.254"),  # AWS/GCP/Azure/DigitalOcean metadata
    ipaddress.ip_address("100.100.100.200"),  # Alibaba Cloud metadata
}

BLOCKED_HOSTNAMES = {
    "localhost",
    "localhost.localdomain",
    "ip6-localhost",
    "ip6-loopback",
    "metadata.google.internal",
    "instance-data",
}


def is_fictional_demo_host(hostname: str) -> bool:
    """Check if the host is a designated safe RFC 2606 test domain."""
    clean_host = hostname.strip().lower()
    return (
        clean_host in settings.FICTIONAL_TEST_DOMAINS
        or clean_host.endswith(".test")
        or clean_host.endswith(".example")
        or clean_host.endswith(".invalid")
    )


def validate_ip_address(ip: ipaddress.IPv4Address | ipaddress.IPv6Address) -> None:
    """Validate that an IP is a globally routable public address.

    Raises SSRFSecurityError if the IP falls into any restricted address space.
    """
    # Unwrap IPv4-mapped IPv6 addresses (e.g. ::ffff:127.0.0.1)
    if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped:
        ip = ip.ipv4_mapped

    if ip in METADATA_IPS:
        raise SSRFSecurityError(f"Access to cloud metadata service ({ip}) is strictly blocked.")

    if ip.is_loopback:
        raise SSRFSecurityError(f"Access to loopback address ({ip}) is strictly blocked.")

    if ip.is_private:
        raise SSRFSecurityError(f"Access to private RFC1918/RFC4193 address ({ip}) is strictly blocked.")

    if ip.is_link_local:
        raise SSRFSecurityError(f"Access to link-local address ({ip}) is strictly blocked.")

    if ip.is_multicast:
        raise SSRFSecurityError(f"Access to multicast address ({ip}) is strictly blocked.")

    if ip.is_reserved:
        raise SSRFSecurityError(f"Access to reserved address ({ip}) is strictly blocked.")

    if ip.is_unspecified:
        raise SSRFSecurityError(f"Access to unspecified address ({ip}) is strictly blocked.")

    # Explicit check for 0.0.0.0/8 (broadcast/this-host)
    if isinstance(ip, ipaddress.IPv4Address) and ip in ipaddress.IPv4Network("0.0.0.0/8"):
        raise SSRFSecurityError(f"Access to 0.0.0.0/8 network ({ip}) is strictly blocked.")

    # Explicit check for Carrier-Grade NAT (100.64.0.0/10)
    if isinstance(ip, ipaddress.IPv4Address) and ip in ipaddress.IPv4Network("100.64.0.0/10"):
        raise SSRFSecurityError(f"Access to Shared Address Space / CGNAT ({ip}) is strictly blocked.")


def resolve_and_verify_hostname(hostname: str) -> List[str]:
    """Resolve a hostname via DNS and verify that all resolved IPs are safe public addresses.

    Returns the list of verified IP string representations.
    """
    clean_host = hostname.strip().lower()

    if clean_host in BLOCKED_HOSTNAMES or clean_host.endswith(".localhost"):
        raise SSRFSecurityError(f"Access to hostname '{clean_host}' is prohibited by SSRF policy.")

    # Check if host is an explicit IP literal
    raw_ip_str = clean_host.strip("[]")
    try:
        ip_obj = ipaddress.ip_address(raw_ip_str)
        validate_ip_address(ip_obj)
        return [str(ip_obj)]
    except ValueError:
        pass  # It's a domain name, proceed to DNS resolution

    # Fictional demonstration domains (e.g. example-finance.test) bypass DNS lookup
    if is_fictional_demo_host(clean_host):
        return ["203.0.113.1"]  # RFC 5737 TEST-NET-3 documentation placeholder

    try:
        # Perform standard DNS resolution
        addr_info = socket.getaddrinfo(
            clean_host,
            None,
            family=socket.AF_UNSPEC,
            type=socket.SOCK_STREAM,
        )
    except socket.gaierror as exc:
        raise URLValidationError(f"DNS resolution failed for host '{clean_host}': {exc}")

    if not addr_info:
        raise URLValidationError(f"DNS lookup returned no records for host '{clean_host}'.")

    resolved_ips: List[str] = []
    for item in addr_info:
        sockaddr = item[4]
        ip_str = sockaddr[0]
        try:
            ip_obj = ipaddress.ip_address(ip_str)
            validate_ip_address(ip_obj)
            resolved_ips.append(str(ip_obj))
        except ValueError as exc:
            raise URLValidationError(f"Invalid resolved IP address: {exc}")

    return list(dict.fromkeys(resolved_ips))


def validate_and_normalize_url(raw_url: str) -> Tuple[str, str, List[str]]:
    """Validate a user-submitted URL and apply SSRF pre-flight filtering.

    Args:
        raw_url: The raw string provided by the user.

    Returns:
        Tuple of (normalized_url, hostname, resolved_ips).

    Raises:
        URLValidationError: For syntactic or scheme violations.
        SSRFSecurityError: For internal, loopback, or metadata targets.
    """
    if not raw_url or not isinstance(raw_url, str):
        raise URLValidationError("URL cannot be empty.")

    trimmed = raw_url.strip()

    if len(trimmed) > settings.MAX_URL_LENGTH:
        raise URLLengthExceededError(
            f"URL length ({len(trimmed)} characters) exceeds maximum allowed limit of {settings.MAX_URL_LENGTH} characters."
        )

    # Reject non-HTTP protocol prefixes immediately before parsing
    lower_trimmed = trimmed.lower()
    for forbidden_scheme in ("javascript:", "file:", "data:", "ftp:", "gopher:", "dict:", "ldap:", "view-source:"):
        if lower_trimmed.startswith(forbidden_scheme):
            raise URLValidationError(f"Scheme '{forbidden_scheme}' is strictly disallowed. Only HTTP and HTTPS are permitted.")

    # Add default scheme if omitted
    if not re.match(r"^https?://", trimmed, re.IGNORECASE):
        trimmed = f"https://{trimmed}"

    try:
        parts = urlsplit(trimmed)
    except Exception as exc:
        raise URLValidationError(f"Failed to parse URL: {exc}")

    scheme = parts.scheme.lower()
    if scheme not in ("http", "https"):
        raise URLValidationError(f"Unsupported scheme '{scheme}'. Only HTTP and HTTPS are allowed.")

    hostname = parts.hostname
    if not hostname:
        raise URLValidationError("URL must include a valid host.")

    # Block credentials in URL (e.g., http://user:pass@host)
    if parts.username or parts.password:
        raise URLValidationError("URLs containing embedded authentication credentials are not permitted.")

    # SSRF verification on the target host
    resolved_ips = resolve_and_verify_hostname(hostname)

    # Block non-standard or dangerous ports
    if parts.port is not None:
        if parts.port not in (80, 443, 8080, 8443):
            raise URLValidationError(f"Port {parts.port} is not in the allowed HTTP/HTTPS ports list (80, 443, 8080, 8443).")

    # Normalize path and URL
    path = parts.path or "/"
    normalized = urlunsplit((scheme, parts.netloc.lower(), path, parts.query, ""))

    return normalized, hostname.lower(), resolved_ips
