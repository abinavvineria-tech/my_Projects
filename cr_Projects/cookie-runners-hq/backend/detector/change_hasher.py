"""Change hasher — produces deterministic content hashes for scraped content."""
import hashlib


def hash_content(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def hash_html(html: str) -> str:
    # Strip whitespace to avoid hash flapping from formatting changes
    stripped = " ".join(html.split())
    return hashlib.sha256(stripped.encode("utf-8")).hexdigest()
