import os
import re
import json
import xml.etree.ElementTree as ET

WORKSPACE = r"c:\Users\Anas\Documents\antigravity\excited-davinci"

def test_sitemap_and_robots():
    print("Testing sitemap.xml and robots.txt...")
    robots_path = os.path.join(WORKSPACE, "robots.txt")
    sitemap_path = os.path.join(WORKSPACE, "sitemap.xml")
    
    assert os.path.exists(robots_path), "robots.txt missing!"
    assert os.path.exists(sitemap_path), "sitemap.xml missing!"
    
    with open(robots_path, "r", encoding="utf-8") as f:
        r_text = f.read()
        assert "Sitemap: https://solaraudit.online/sitemap.xml" in r_text, "Sitemap directive missing in robots.txt"
    
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    # xml namespace
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [loc.text for loc in root.findall("sm:url/sm:loc", ns)]
    
    expected_urls = [
        "https://solaraudit.online/",
        "https://solaraudit.online/ke-bill-calculator.html",
        "https://solaraudit.online/lesco-solar-calculator.html",
        "https://solaraudit.online/5kw-solar-system-pakistan.html",
        "https://solaraudit.online/solar-quote-validator.html",
        "https://solaraudit.online/about.html",
        "https://solaraudit.online/privacy-policy.html",
        "https://solaraudit.online/terms.html"
    ]
    
    for u in expected_urls:
        assert u in urls, f"Missing {u} in sitemap.xml"
    print(f"[PASS] Sitemap validated with {len(urls)} URLs.")

def test_html_pages_and_schemas():
    print("Testing HTML pages and JSON-LD schemas...")
    html_files = [
        "index.html",
        "ke-bill-calculator.html",
        "lesco-solar-calculator.html",
        "5kw-solar-system-pakistan.html",
        "solar-quote-validator.html",
        "about.html",
        "privacy-policy.html",
        "terms.html"
    ]
    
    for fname in html_files:
        path = os.path.join(WORKSPACE, fname)
        assert os.path.exists(path), f"{fname} does not exist!"
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Check canonical
        assert '<link rel="canonical"' in content, f"Canonical tag missing in {fname}"
        
        # Check OG image
        assert 'og:image' in content, f"og:image missing in {fname}"
        
        # Extract and validate all application/ld+json blocks
        schema_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
        assert len(schema_matches) > 0, f"No JSON-LD schema found in {fname}"
        
        for idx, s in enumerate(schema_matches):
            try:
                data = json.loads(s.strip())
                assert "@context" in data, f"@context missing in schema #{idx} of {fname}"
            except Exception as e:
                raise AssertionError(f"Invalid JSON in schema #{idx} of {fname}: {e}")
                
        print(f"[PASS] {fname}: Valid HTML, canonical, OG tags, and {len(schema_matches)} JSON-LD schema(s).")

def test_og_image():
    print("Testing og-image.png...")
    og_path = os.path.join(WORKSPACE, "og-image.png")
    assert os.path.exists(og_path), "og-image.png missing!"
    size = os.path.getsize(og_path)
    assert size > 20000, f"og-image.png is suspiciously small ({size} bytes)"
    print(f"[PASS] og-image.png exists ({size} bytes).")

if __name__ == "__main__":
    test_sitemap_and_robots()
    test_html_pages_and_schemas()
    test_og_image()
    print("\nALL PYTHON INTEGRITY TESTS PASSED!")
