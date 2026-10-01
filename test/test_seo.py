import os
import re
import json
import xml.etree.ElementTree as ET

WORKSPACE = r"c:\Users\Anas\Documents\antigravity\excited-davinci"

def test_sitemap_and_robots():
    print(">>> Testing sitemap.xml and robots.txt...")
    robots_path = os.path.join(WORKSPACE, "robots.txt")
    sitemap_path = os.path.join(WORKSPACE, "sitemap.xml")
    
    assert os.path.exists(robots_path), "robots.txt missing!"
    assert os.path.exists(sitemap_path), "sitemap.xml missing!"
    
    with open(robots_path, "r", encoding="utf-8") as f:
        r_text = f.read()
        assert "Sitemap: https://solaraudit.online/sitemap.xml" in r_text, "Sitemap directive missing in robots.txt"
    
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [loc.text for loc in root.findall("sm:url/sm:loc", ns)]
    
    # Requirement: Strictly EXCLUDE embed.html and widget.html from sitemap.xml
    assert "https://solaraudit.online/embed.html" not in urls, "embed.html MUST be excluded from sitemap.xml!"
    assert "https://solaraudit.online/widget.html" not in urls, "widget.html MUST be excluded from sitemap.xml!"

    expected_urls = [
        "https://solaraudit.online/",
        "https://solaraudit.online/3kw-solar-system-pakistan.html",
        "https://solaraudit.online/5kw-solar-system-pakistan.html",
        "https://solaraudit.online/10kw-solar-system-pakistan.html",
        "https://solaraudit.online/15kw-20kw-solar-system-pakistan.html",
        "https://solaraudit.online/solar-panels-for-ac-pakistan.html",
        "https://solaraudit.online/solar-batteries-pakistan.html",
        "https://solaraudit.online/solar-quote-validator.html",
        "https://solaraudit.online/ke-bill-calculator.html",
        "https://solaraudit.online/lesco-solar-calculator.html",
        "https://solaraudit.online/iesco-solar-calculator.html",
        "https://solaraudit.online/mepco-solar-calculator.html",
        "https://solaraudit.online/gepco-solar-calculator.html",
        "https://solaraudit.online/fesco-solar-calculator.html",
        "https://solaraudit.online/pesco-solar-calculator.html",
        "https://solaraudit.online/about.html",
        "https://solaraudit.online/privacy-policy.html",
        "https://solaraudit.online/terms.html"
    ]
    
    for u in expected_urls:
        assert u in urls, f"Missing {u} in sitemap.xml"
    print(f"[PASS] Sitemap validated with {len(urls)} URLs. embed.html & widget.html excluded.")

def test_distinct_seo_metadata_and_h1():
    print("\n>>> Testing distinctness of all 14 satellite pages + index.html...")
    calculator_pages = [
        "index.html",
        "3kw-solar-system-pakistan.html",
        "5kw-solar-system-pakistan.html",
        "10kw-solar-system-pakistan.html",
        "15kw-20kw-solar-system-pakistan.html",
        "solar-panels-for-ac-pakistan.html",
        "solar-batteries-pakistan.html",
        "solar-quote-validator.html",
        "ke-bill-calculator.html",
        "lesco-solar-calculator.html",
        "iesco-solar-calculator.html",
        "mepco-solar-calculator.html",
        "gepco-solar-calculator.html",
        "fesco-solar-calculator.html",
        "pesco-solar-calculator.html"
    ]

    h1_map = {}
    title_map = {}
    desc_map = {}

    for fname in calculator_pages:
        path = os.path.join(WORKSPACE, fname)
        assert os.path.exists(path), f"File {fname} missing!"
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract H1
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
        assert h1_match, f"No <h1> found in {fname}"
        h1_text = re.sub(r'\s+', ' ', h1_match.group(1)).strip()
        assert h1_text not in h1_map, f"Duplicate <h1> detected! '{h1_text}' in {fname} and {h1_map.get(h1_text)}"
        h1_map[h1_text] = fname

        # Extract Title
        title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
        assert title_match, f"No <title> found in {fname}"
        title_text = title_match.group(1).strip()
        assert title_text not in title_map, f"Duplicate <title> in {fname} and {title_map.get(title_text)}"
        title_map[title_text] = fname

        # Extract Meta Description
        desc_match = re.search(r'<meta name="description" content="(.*?)">', content)
        assert desc_match, f"No meta description found in {fname}"
        desc_text = desc_match.group(1).strip()
        assert desc_text not in desc_map, f"Duplicate description in {fname} and {desc_map.get(desc_text)}"
        desc_map[desc_text] = fname

        # Check Schema.org JSON-LD
        schemas = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
        assert len(schemas) > 0, f"No JSON-LD schema found in {fname}"
        for idx, s in enumerate(schemas):
            data = json.loads(s.strip())
            assert "@context" in data, f"@context missing in schema #{idx} of {fname}"
            if "@graph" in data:
                types = [item.get("@type") for item in data["@graph"]]
                assert "WebApplication" in types, f"WebApplication schema missing in {fname}"
                assert "FAQPage" in types, f"FAQPage schema missing in {fname}"

        # Check Canonical
        assert f'<link rel="canonical" href="https://solaraudit.online/{"" if fname == "index.html" else fname}">' in content, f"Canonical tag incorrect in {fname}"

        # Check Mobile Sticky Summary Bar
        assert 'id="stickyMobileSummary"' in content, f"Sticky Mobile Summary Bar missing in {fname}"
        assert 'id="mobileStickyKw"' in content, f"Mobile sticky kW readout missing in {fname}"

        # Check Performance: NO Tailwind CDN and NO jsPDF in head
        assert 'cdn.tailwindcss.com' not in content, f"cdn.tailwindcss.com still present in {fname}!"
        assert 'cdnjs.cloudflare.com/ajax/libs/jspdf' not in content, f"Synchronous jsPDF still in {fname}!"
        assert 'css/style.min.css?v=2026.2' in content, f"Compiled css/style.min.css?v=2026.2 missing in {fname}"

    print(f"[PASS] All {len(calculator_pages)} pages verified with 100% unique <h1> headers, unique <title>s, unique descriptions, and valid schemas!")

def test_disco_contextual_links():
    print("\n>>> Testing contextual editorial links to regional DISCOs...")
    disco_pages = [
        "lesco-solar-calculator.html",
        "mepco-solar-calculator.html",
        "iesco-solar-calculator.html",
        "gepco-solar-calculator.html",
        "fesco-solar-calculator.html"
    ]
    for dp in disco_pages:
        path = os.path.join(WORKSPACE, dp)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        # Verify that each regional DISCO page links to other regional DISCO pages
        links_found = [other for other in disco_pages if other in content and other != dp]
        assert len(links_found) >= 2, f"{dp} lacks contextual editorial links to other DISCOs! Found only {links_found}"
    print("[PASS] Regional DISCO contextual cross-links verified.")

def test_widget_optimization():
    print("\n>>> Testing widget.html optimization...")
    widget_path = os.path.join(WORKSPACE, "widget.html")
    assert os.path.exists(widget_path)
    with open(widget_path, "r", encoding="utf-8") as f:
        w_text = f.read()
    
    assert "cdn.tailwindcss.com" not in w_text, "Tailwind CDN must not be in widget.html"
    assert "js/tariff-data.js?v=2026.2" in w_text, "widget.html must link to js/tariff-data.js?v=2026.2"
    assert "js/calculator-engine.js?v=2026.2" in w_text, "widget.html must link to js/calculator-engine.js?v=2026.2"
    
    # Check file size reduction: must be under 15KB (was 42KB)
    w_size = os.path.getsize(widget_path)
    print(f"widget.html size: {w_size} bytes ({w_size/1024:.1f} KB)")
    assert w_size < 15000, f"widget.html is too large: {w_size} bytes"
    print("[PASS] widget.html is lightweight and cleanly linked.")

def test_deployment_hardening():
    print("\n>>> Testing .cpanel.yml and deploy.php hardening...")
    cpanel_path = os.path.join(WORKSPACE, ".cpanel.yml")
    deploy_path = os.path.join(WORKSPACE, "deploy.php")
    
    with open(cpanel_path, "r", encoding="utf-8") as f:
        c_text = f.read()
    assert ".htaccess" in c_text, ".htaccess missing in .cpanel.yml"
    assert "*.txt" in c_text, "*.txt verification files missing in .cpanel.yml"
    assert "deploy.php" in c_text, "deploy.php missing in .cpanel.yml"

    with open(deploy_path, "r", encoding="utf-8") as f:
        d_text = f.read()
    assert "/home/zynk/.deploy_secret" in d_text, "deploy.php does not check /home/zynk/.deploy_secret"
    print("[PASS] Deployment configurations hardened.")

if __name__ == "__main__":
    test_sitemap_and_robots()
    test_distinct_seo_metadata_and_h1()
    test_disco_contextual_links()
    test_widget_optimization()
    test_deployment_hardening()
    print("\n========================================================")
    print("ALL SEO, PERFORMANCE & DEPLOYMENT INTEGRITY TESTS PASSED!")
    print("========================================================")
