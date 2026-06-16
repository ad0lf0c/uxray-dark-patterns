import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright


def normalize_url(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        return "https://" + url
    return url


def safe_name(url: str) -> str:
    parsed = urlparse(url)
    domain = parsed.netloc.replace(":", "_")
    domain = re.sub(r"[^a-zA-Z0-9._-]", "_", domain)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{domain}_{timestamp}"


def main():
    parser = argparse.ArgumentParser(description="UX-Ray evidence collector")
    parser.add_argument("url", help="Website URL to analyze")
    parser.add_argument("--headful", action="store_true", help="Open browser visibly")
    args = parser.parse_args()

    url = normalize_url(args.url)
    output_dir = Path("evidence") / safe_name(url)
    output_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=not args.headful,
            args=[
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",
            ],
        )

        context = browser.new_context(
            viewport={"width": 1440, "height": 1200},
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        )

        page = context.new_page()

        print(f"[+] Opening: {url}")
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(5000)

        title = page.title()
        final_url = page.url

        print(f"[+] Title: {title}")
        print(f"[+] Final URL: {final_url}")

        page.screenshot(path=output_dir / "screenshot.png", full_page=True)

        html = page.content()
        (output_dir / "page.html").write_text(html, encoding="utf-8")

        visible_text = page.locator("body").inner_text(timeout=10000)
        (output_dir / "visible_text.txt").write_text(visible_text, encoding="utf-8")

        buttons = page.eval_on_selector_all(
            "button, input[type=button], input[type=submit], a",
            """
            els => els.map((el, index) => {
                const rect = el.getBoundingClientRect();
                const style = window.getComputedStyle(el);
                return {
                    index,
                    tag: el.tagName.toLowerCase(),
                    text: (el.innerText || el.value || el.getAttribute('aria-label') || '').trim(),
                    href: el.href || null,
                    type: el.getAttribute('type') || null,
                    id: el.id || null,
                    class: el.className || null,
                    visible: !!(rect.width && rect.height),
                    x: Math.round(rect.x),
                    y: Math.round(rect.y),
                    width: Math.round(rect.width),
                    height: Math.round(rect.height),
                    color: style.color,
                    backgroundColor: style.backgroundColor,
                    fontSize: style.fontSize,
                    fontWeight: style.fontWeight
                }
            })
            """
        )

        forms = page.eval_on_selector_all(
            "form",
            """
            forms => forms.map((form, index) => {
                return {
                    index,
                    action: form.action || null,
                    method: form.method || null,
                    text: form.innerText.trim().slice(0, 1000),
                    inputs: Array.from(form.querySelectorAll('input, select, textarea')).map(input => ({
                        tag: input.tagName.toLowerCase(),
                        type: input.getAttribute('type') || null,
                        name: input.getAttribute('name') || null,
                        placeholder: input.getAttribute('placeholder') || null,
                        checked: input.checked || false,
                        value: input.value || null
                    }))
                }
            })
            """
        )

        checkboxes = page.eval_on_selector_all(
            "input[type=checkbox], input[type=radio]",
            """
            els => els.map((el, index) => {
                const label = el.labels && el.labels.length > 0
                    ? Array.from(el.labels).map(l => l.innerText).join(" ")
                    : "";
                return {
                    index,
                    type: el.type,
                    name: el.name || null,
                    checked: el.checked,
                    label: label.trim(),
                    id: el.id || null
                }
            })
            """
        )

        dark_pattern_keywords = [
            "accept all", "reject all", "manage options", "cookies",
            "only today", "limited time", "last chance", "only", "left",
            "don't miss", "no thanks", "i don't want", "continue without",
            "free trial", "cancel anytime", "subscribe", "unsubscribe",
            "aceitar tudo", "rejeitar", "gerir opções", "cookies",
            "última oportunidade", "tempo limitado", "restam", "subscrever",
            "cancelar", "não quero", "continuar sem"
        ]

        lower_text = visible_text.lower()
        keyword_hits = [kw for kw in dark_pattern_keywords if kw in lower_text]

        summary = {
            "url_requested": url,
            "url_final": final_url,
            "title": title,
            "output_dir": str(output_dir),
            "stats": {
                "visible_text_chars": len(visible_text),
                "buttons_links_count": len(buttons),
                "forms_count": len(forms),
                "checkboxes_radios_count": len(checkboxes),
                "keyword_hits_count": len(keyword_hits),
            },
            "keyword_hits": keyword_hits,
            "files": {
                "screenshot": "screenshot.png",
                "html": "page.html",
                "visible_text": "visible_text.txt",
                "buttons": "buttons.json",
                "forms": "forms.json",
                "checkboxes": "checkboxes.json",
                "summary": "summary.json"
            }
        }

        (output_dir / "buttons.json").write_text(
            json.dumps(buttons, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        (output_dir / "forms.json").write_text(
            json.dumps(forms, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        (output_dir / "checkboxes.json").write_text(
            json.dumps(checkboxes, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        (output_dir / "summary.json").write_text(
            json.dumps(summary, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        browser.close()

    print("\n[+] Evidence collected successfully.")
    print(f"[+] Output folder: {output_dir}")
    print("[+] Generated:")
    print("    - screenshot.png")
    print("    - page.html")
    print("    - visible_text.txt")
    print("    - buttons.json")
    print("    - forms.json")
    print("    - checkboxes.json")
    print("    - summary.json")


if __name__ == "__main__":
    main()
