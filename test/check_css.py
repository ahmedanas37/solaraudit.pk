import os
import re

def check_css():
    css_path = os.path.join(os.path.dirname(__file__), "..", "css", "style.min.css")
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()

    workspace = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    all_classes = set()
    for root, dirs, files in os.walk(workspace):
        if any(x in root for x in [".git", "__pycache__", ".agents", "test", "node_modules"]):
            continue
        for fname in files:
            if fname.endswith((".html", ".js")):
                with open(os.path.join(root, fname), "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    for match in re.finditer(r'class=["\']([^"\']+)["\']', content):
                        for c in match.group(1).split():
                            all_classes.add(c)

    print(f"Total unique classes found: {len(all_classes)}")
    custom_classes = {"tool-card", "stat-value", "touch-target", "bill-val", "card-val", "green", "card-sub", "cta-btn", "attribution", "header", "brand", "brand-icon", "brand-title", "brand-sub", "badge", "field", "label-row", "grid", "card", "card-label", "widget-box"}

    missing = []
    for c in sorted(all_classes):
        if c in custom_classes:
            continue
        # Check standard tailwind escaped form
        esc = c.replace(":", "\\:").replace("[", "\\[").replace("]", "\\]").replace("/", "\\/").replace(".", "\\.").replace("%", "\\%")
        if f".{esc}" not in css and f"{esc}{{" not in css and f"{esc}:" not in css and f"{esc}," not in css:
            missing.append(c)

    print(f"Missing classes ({len(missing)}):", missing)
    return len(missing) == 0

if __name__ == "__main__":
    check_css()
