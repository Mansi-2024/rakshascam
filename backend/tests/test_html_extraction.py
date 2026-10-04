"""Unit tests for structured HTML extraction, links, contact signals, and factual claims."""

import pytest
from app.services.html_extractor import extract_html_information

SAMPLE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Apex Global Wealth Advisors | Secure Returns</title>
  <meta name="description" content="Premier wealth management advisory with SEBI authorized brokers offering guaranteed returns.">
  <link rel="canonical" href="https://example.com/canonical-home">
</head>
<body>
  <h1>Apex Global Wealth Advisors Private Limited</h1>
  <p>
    Welcome to our premier trading community. We promise guaranteed returns of 30% monthly with guaranteed profit on all institutional allocations.
    Act now—this is a limited time opportunity to double your money safely with risk-free investment plans.
  </p>
  <div class="regulatory">
    <p>Our advisors are SEBI registered under Intermediary Code INA000012345. CIN: U67120MH2020PTC123456.</p>
    <p>We are a government approved entity authorized for portfolio operations.</p>
  </div>
  <div class="contact">
    <p>Reach us at support@example.com or director@apexwealth.co.in</p>
    <a href="mailto:queries@example.com">Send Query</a>
    <p>Helpline: +91 98765 12345 or call 022-26543210</p>
  </div>
  <nav>
    <a href="/plans">Internal Plans</a>
    <a href="https://example.com/team">About Our Team</a>
    <a href="https://thirdparty-payment.test/checkout">External Gateway</a>
    <a href="javascript:void(0)">Ignored Script Link</a>
  </nav>
</body>
</html>
"""


def test_html_title_extraction():
    """10. Test that page title is correctly extracted and stripped."""
    page, _, _, _ = extract_html_information(SAMPLE_HTML, "https://example.com")
    assert page.title == "Apex Global Wealth Advisors | Secure Returns"
    assert page.language == "en"
    assert page.canonical_url == "https://example.com/canonical-home"


def test_meta_description_extraction():
    """11. Test that meta description is extracted accurately."""
    page, _, _, _ = extract_html_information(SAMPLE_HTML, "https://example.com")
    assert page.description == "Premier wealth management advisory with SEBI authorized brokers offering guaranteed returns."


def test_link_extraction():
    """12. Test link extraction, relative URL resolution, and internal vs external classification."""
    _, links, _, _ = extract_html_information(SAMPLE_HTML, "https://example.com")

    urls = [link.url for link in links]
    assert "https://example.com/plans" in urls
    assert "https://example.com/team" in urls
    assert "https://thirdparty-payment.test/checkout" in urls

    # Check internal flag
    internal_map = {link.url: link.internal for link in links}
    assert internal_map["https://example.com/plans"] is True
    assert internal_map["https://example.com/team"] is True
    assert internal_map["https://thirdparty-payment.test/checkout"] is False

    # Check that javascript: was skipped
    assert not any("javascript:" in link.url for link in links)


def test_email_extraction():
    """13. Test extraction of emails from both body text and mailto: href attributes."""
    _, _, contacts, _ = extract_html_information(SAMPLE_HTML, "https://example.com")

    assert "support@example.com" in contacts.emails
    assert "director@apexwealth.co.in" in contacts.emails
    assert "queries@example.com" in contacts.emails
    assert len(contacts.phone_numbers) >= 1


def test_financial_phrase_extraction():
    """14. Test deterministic detection of financial claims without verdict generation."""
    _, _, _, refs = extract_html_information(SAMPLE_HTML, "https://example.com")

    claims = [item.phrase.lower() for item in refs.financial_claims]
    assert "guaranteed returns" in claims
    assert "guaranteed profit" in claims
    assert "act now" in claims
    assert "limited time" in claims
    assert "double your money" in claims
    assert "risk-free investment" in claims

    # Confirm all have proper category and source
    for item in refs.financial_claims:
        assert item.category == "financial_claim"
        assert item.source == "page_text"
        assert item.context is not None


def test_regulatory_phrase_extraction():
    """15. Test detection of regulatory mentions and registration number formats."""
    _, _, _, refs = extract_html_information(SAMPLE_HTML, "https://example.com")

    reg_phrases = [item.phrase.lower() for item in refs.regulatory_mentions]
    assert "sebi registered" in reg_phrases
    assert "government approved" in reg_phrases
    assert "authorized" in reg_phrases

    # Test registration numbers
    reg_codes = [item.phrase for item in refs.registration_numbers]
    assert "INA000012345" in reg_codes
    assert "U67120MH2020PTC123456" in reg_codes

    # Test entity detection
    entity_names = [item.phrase for item in refs.entities]
    assert any("Apex Global Wealth Advisors Private Limited" in name for name in entity_names)
