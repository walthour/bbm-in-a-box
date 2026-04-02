#!/usr/bin/env python3
"""
Scrape a landing page and extract copy structure for analysis.

Usage:
    python3 website-copywriting-analysis/scripts/analyze.py <url>
    python3 website-copywriting-analysis/scripts/analyze.py https://example.com/sales-page

Output:
    .tmp/wireframe.md
"""

import os
import sys
import re
import json
from urllib.parse import urlparse

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: Required packages not installed.")
    print("Run: pip install requests beautifulsoup4")
    sys.exit(1)

OUTPUT_DIR = ".tmp"


def clean_text(text):
    """Clean extracted text - normalize whitespace, remove excess newlines."""
    if not text:
        return ""
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_hero_section(soup):
    """Extract likely hero section content."""
    hero = {
        "headline": None,
        "subheadline": None,
        "cta": None
    }

    # Look for hero section by common class/id names
    hero_selectors = [
        'header', '[class*="hero"]', '[id*="hero"]',
        '[class*="banner"]', '[class*="masthead"]',
        '[class*="above-fold"]', 'section:first-of-type'
    ]

    hero_section = None
    for selector in hero_selectors:
        try:
            hero_section = soup.select_one(selector)
            if hero_section:
                break
        except:
            continue

    # Extract headline (h1 priority, then h2)
    h1 = soup.find('h1')
    if h1:
        hero["headline"] = clean_text(h1.get_text())

    # Look for subheadline near h1
    if h1:
        # Check next sibling or nearby p/h2
        next_elem = h1.find_next_sibling(['p', 'h2', 'div'])
        if next_elem and len(clean_text(next_elem.get_text())) < 300:
            hero["subheadline"] = clean_text(next_elem.get_text())

    # Extract first prominent CTA
    cta_selectors = [
        'a[class*="cta"]', 'a[class*="button"]', 'button[class*="cta"]',
        'a[class*="btn"]', 'button[class*="btn"]',
        '[class*="hero"] a', '[class*="hero"] button'
    ]

    for selector in cta_selectors:
        try:
            cta = soup.select_one(selector)
            if cta:
                cta_text = clean_text(cta.get_text())
                if cta_text and len(cta_text) < 50:
                    hero["cta"] = cta_text
                    break
        except:
            continue

    return hero


def extract_headings(soup):
    """Extract all headings in order."""
    headings = []
    for tag in soup.find_all(['h1', 'h2', 'h3']):
        text = clean_text(tag.get_text())
        if text and len(text) > 2:
            headings.append({
                "level": tag.name,
                "text": text
            })
    return headings


def extract_ctas(soup):
    """Extract all call-to-action buttons/links."""
    ctas = []
    seen = set()

    # Look for buttons and CTA-style links
    for elem in soup.find_all(['button', 'a']):
        classes = ' '.join(elem.get('class', []))

        # Filter for likely CTAs
        is_cta = any(x in classes.lower() for x in ['cta', 'btn', 'button', 'submit', 'buy', 'get', 'start'])

        if is_cta or elem.name == 'button':
            text = clean_text(elem.get_text())
            if text and len(text) < 50 and text not in seen:
                seen.add(text)
                ctas.append(text)

    return ctas


def extract_testimonials(soup):
    """Extract testimonial/social proof sections."""
    testimonials = []

    # Look for testimonial containers
    testimonial_selectors = [
        '[class*="testimonial"]', '[class*="review"]',
        '[class*="quote"]', '[class*="social-proof"]',
        'blockquote'
    ]

    for selector in testimonial_selectors:
        try:
            for elem in soup.select(selector):
                text = clean_text(elem.get_text())
                if text and 20 < len(text) < 500:
                    testimonials.append(text[:300] + "..." if len(text) > 300 else text)
        except:
            continue

    return testimonials[:5]  # Limit to 5


def extract_bullet_lists(soup):
    """Extract bullet point lists (likely benefits/features)."""
    bullet_lists = []

    for ul in soup.find_all(['ul', 'ol']):
        items = []
        for li in ul.find_all('li', recursive=False):
            text = clean_text(li.get_text())
            if text and 5 < len(text) < 200:
                items.append(text)

        if 2 <= len(items) <= 15:
            bullet_lists.append(items)

    return bullet_lists[:5]  # Limit to 5 lists


def extract_sections(soup):
    """Try to identify distinct page sections."""
    sections = []

    # Look for semantic sections
    for section in soup.find_all(['section', 'div']):
        classes = ' '.join(section.get('class', []))
        section_id = section.get('id', '')

        # Look for section-like containers
        if any(x in classes.lower() or x in section_id.lower() for x in
               ['section', 'block', 'module', 'container', 'component']):

            # Get section heading if present
            heading = section.find(['h2', 'h3'])
            heading_text = clean_text(heading.get_text()) if heading else None

            if heading_text:
                sections.append(heading_text)

    return sections[:15]  # Limit


def extract_pricing(soup):
    """Extract pricing information if present."""
    pricing = []

    # Look for price patterns
    price_pattern = re.compile(r'\$[\d,]+(?:\.\d{2})?|\d+(?:,\d{3})*(?:\.\d{2})?\s*(?:USD|dollars?)', re.I)

    # Look in likely pricing areas
    pricing_selectors = [
        '[class*="price"]', '[class*="pricing"]',
        '[class*="cost"]', '[class*="offer"]'
    ]

    for selector in pricing_selectors:
        try:
            for elem in soup.select(selector):
                text = elem.get_text()
                matches = price_pattern.findall(text)
                pricing.extend(matches)
        except:
            continue

    # Also search full page
    full_text = soup.get_text()
    all_prices = price_pattern.findall(full_text)

    return list(set(pricing + all_prices))[:10]


def extract_meta(soup, url):
    """Extract meta information."""
    meta = {
        "url": url,
        "title": None,
        "description": None
    }

    # Title
    title_tag = soup.find('title')
    if title_tag:
        meta["title"] = clean_text(title_tag.get_text())

    # Meta description
    desc_tag = soup.find('meta', attrs={'name': 'description'})
    if desc_tag:
        meta["description"] = desc_tag.get('content', '')

    return meta


def scrape_landing_page(url):
    """Main scraping function."""

    # Validate URL
    parsed = urlparse(url)
    if not parsed.scheme:
        url = 'https://' + url

    print(f"Scraping: {url}")

    # Fetch page
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        sys.exit(1)

    # Parse HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Remove script/style elements
    for element in soup(['script', 'style', 'noscript', 'iframe']):
        element.decompose()

    # Extract all components
    data = {
        "meta": extract_meta(soup, url),
        "hero": extract_hero_section(soup),
        "headings": extract_headings(soup),
        "ctas": extract_ctas(soup),
        "sections": extract_sections(soup),
        "bullet_lists": extract_bullet_lists(soup),
        "testimonials": extract_testimonials(soup),
        "pricing": extract_pricing(soup)
    }

    return data


def format_output(data):
    """Format extracted data as markdown for analysis."""
    lines = []

    lines.append("# Landing Page Analysis")
    lines.append("")
    lines.append(f"**URL:** {data['meta']['url']}")
    if data['meta']['title']:
        lines.append(f"**Page Title:** {data['meta']['title']}")
    if data['meta']['description']:
        lines.append(f"**Meta Description:** {data['meta']['description']}")
    lines.append("")

    # Hero Section
    lines.append("## Hero Section")
    lines.append("")
    if data['hero']['headline']:
        lines.append(f"**Headline:** {data['hero']['headline']}")
    if data['hero']['subheadline']:
        lines.append(f"**Subheadline:** {data['hero']['subheadline']}")
    if data['hero']['cta']:
        lines.append(f"**Primary CTA:** {data['hero']['cta']}")
    lines.append("")

    # Page Structure (Headings)
    lines.append("## Page Structure (Headings)")
    lines.append("")
    for h in data['headings']:
        indent = "  " * (int(h['level'][1]) - 1)
        lines.append(f"{indent}- [{h['level'].upper()}] {h['text']}")
    lines.append("")

    # Section Flow
    if data['sections']:
        lines.append("## Section Flow")
        lines.append("")
        for i, section in enumerate(data['sections'], 1):
            lines.append(f"{i}. {section}")
        lines.append("")

    # CTAs Found
    if data['ctas']:
        lines.append("## CTAs Found")
        lines.append("")
        for cta in data['ctas']:
            lines.append(f"- {cta}")
        lines.append("")

    # Bullet Lists (Benefits/Features)
    if data['bullet_lists']:
        lines.append("## Bullet Lists (Potential Benefits/Features)")
        lines.append("")
        for i, bullets in enumerate(data['bullet_lists'], 1):
            lines.append(f"### List {i}")
            for bullet in bullets:
                lines.append(f"- {bullet}")
            lines.append("")

    # Testimonials
    if data['testimonials']:
        lines.append("## Social Proof / Testimonials")
        lines.append("")
        for t in data['testimonials']:
            lines.append(f"> {t}")
            lines.append("")

    # Pricing
    if data['pricing']:
        lines.append("## Pricing Found")
        lines.append("")
        for price in data['pricing']:
            lines.append(f"- {price}")
        lines.append("")

    # Analysis Prompts
    lines.append("---")
    lines.append("")
    lines.append("## Analysis Prompts")
    lines.append("")
    lines.append("Use this extracted structure to analyze:")
    lines.append("")
    lines.append("1. **StoryBrand Elements**: Is the customer clearly the hero? Is the brand positioned as guide?")
    lines.append("2. **Hormozi Value Equation**: How does the page address Dream Outcome, Likelihood, Time, Effort?")
    lines.append("3. **CRO Flow**: Does each section answer one question? Are CTAs well-placed?")
    lines.append("4. **Headline Strength**: Is it specific? Does it promise transformation?")
    lines.append("5. **Missing Elements**: What's absent that could improve conversions?")
    lines.append("")

    return "\n".join(lines)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Scrape a landing page and extract copy structure.")
    parser.add_argument("url", help="URL to scrape")
    parser.add_argument("--output", default=".tmp/wireframe.md", help="Output markdown file path")
    parser.add_argument("--json", default=".tmp/analysis.json", help="Output JSON file path")

    args = parser.parse_args()

    url = args.url

    # Ensure URL has scheme
    parsed = urlparse(url)
    if not parsed.scheme:
        url = 'https://' + url

    # Ensure output directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    os.makedirs(os.path.dirname(args.json), exist_ok=True)

    # Scrape
    data = scrape_landing_page(url)

    # Format output
    output = format_output(data)

    # Save Markdown
    with open(args.output, "w") as f:
        f.write(output)

    print(f"\n✅ Scraped successfully!")
    print(f"📄 Wireframe saved to: {args.output}")

    # Save JSON
    with open(args.json, "w") as f:
        json.dump(data, f, indent=2)
    print(f"📊 Analysis data saved to: {args.json}")

    # Print summary
    print(f"\n--- Summary ---")
    if data['hero']['headline']:
        print(f"Headline: {data['hero']['headline'][:80]}...")
    print(f"Headings found: {len(data['headings'])}")
    print(f"CTAs found: {len(data['ctas'])}")
    print(f"Bullet lists: {len(data['bullet_lists'])}")
    print(f"Testimonials: {len(data['testimonials'])}")


if __name__ == "__main__":
    main()
