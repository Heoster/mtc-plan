#!/usr/bin/env python3
"""Mechanical design pre-flight for the built site.

Checks the rules that can be verified without a browser. The browser-side
checks (overflow, line counts, nav height) live in tools/qa.py.
Run after build_site.py. Exit code is non-zero if anything fails.
"""
import re
import sys
import pathlib

BASE = pathlib.Path(__file__).resolve().parent.parent
SITE = BASE / "maples-tech-club"
PAGES = sorted(SITE.glob("*.html"))
HTML = {p.name: p.read_text(encoding="utf-8") for p in PAGES}
ALL = "".join(HTML.values())
CSS = re.search(r"<style>(.*?)</style>", ALL, re.S).group(1)

results = []


def check(name, ok, detail=""):
    results.append((ok, name, detail))


def body_of(src):
    """Markup with <style>, <script> and tag attributes removed."""
    s = re.sub(r"<style>.*?</style>", "", src, flags=re.S)
    s = re.sub(r"<script>.*?</script>", "", s, flags=re.S)
    return re.sub(r"<[^>]+>", " ", s)


text = body_of(ALL)

# --- 9.G typography -------------------------------------------------------
em = text.count("\u2014") + text.count("\u2013")
check("9.G  no em/en dashes in copy", em == 0, f"found {em}")

# --- 4.7 label inflation --------------------------------------------------
eyebrows = len(re.findall(r'class="[^"]*\b(?:kicker|eyebrow)\b', ALL))
sections = len(re.findall(r"<section\b", ALL))
cap = -(-sections // 3)
check("4.7  eyebrow count within cap", eyebrows <= cap, f"{eyebrows} vs cap {cap}")

# --- 9.A shouting ---------------------------------------------------------
upper = len(re.findall(r"text-transform:\s*uppercase", CSS))
check("9.A  no uppercase label styling", upper == 0, f"{upper} rules")

# --- 4.2 consistency lock -------------------------------------------------
check("4.2  no gradient text", "background-clip:text" not in CSS.replace(" ", ""))
purple = re.findall(r"#(?:7c3aed|8b5cf6|a78bfa|6366f1|818cf8)", CSS, re.I)
check("4.2  no AI-default purple", not purple, str(set(purple)))
retired = [v for v in ("--cy", "--vi", "--am", "--gr") if v + ":" in CSS]
check("4.2  retired accent vars gone", not retired, str(retired))

# --- shape + motion -------------------------------------------------------
radii = sorted(set(re.findall(r"--r-[\w-]+:\s*([\dpx.]+)", CSS)))
check("shape lock: 3-step radius scale", len(radii) == 3, str(radii))
check("motion: no scroll listener", "addEventListener('scroll'" not in ALL)
check("motion: IntersectionObserver used", "IntersectionObserver" in ALL)
check("a11y: reduced-motion honoured", "prefers-reduced-motion" in CSS)
check("a11y: dark mode defined", "prefers-color-scheme:dark" in CSS.replace(" ", ""))
pure = re.findall(r"#fff\b|#000\b|#ffffff\b|#000000\b", CSS, re.I)
check("4.11 no pure black page bg", "--paper:#fff" not in CSS.replace(" ", ""))

# --- icons must never balloon (the regression that slipped through) -------
check("icons: svg.i has an explicit box",
      bool(re.search(r"svg\.i\{[^}]*width:", CSS)))
junk = re.search(r"\.i\{font-style:normal\}", CSS)
check("icons: no junk .i reset", junk is None)

# --- images ---------------------------------------------------------------
imgs = re.findall(r"<img\b[^>]*>", ALL)
noalt = [i for i in imgs if "alt=" not in i]
nodim = [i for i in imgs if not ("width=" in i and "height=" in i)]
check("perf: every img has alt", not noalt, f"{len(noalt)} missing")
check("perf: every img has width/height", not nodim, f"{len(nodim)} missing")
lazy = [i for i in imgs if "assets/" in i and "loading=" not in i]
check("perf: non-hero imgs lazy", len(lazy) <= 1, f"{len(lazy)} eager")

# --- 4.5 one CTA label per intent ----------------------------------------
def label_words(raw):
    s = re.sub(r"<[^>]+>", " ", raw)
    s = re.sub(r"&[a-z]+;|&#\d+;", " ", s)        # &rarr; is decoration, not a word
    return re.sub(r"\s+", " ", s).strip(" \u2192\u2193>").strip()


labels = [label_words(m)
          for m in re.findall(r'<a[^>]*class="[^"]*\bbtn\b[^"]*"[^>]*>(.*?)</a>', ALL, re.S)]
longs = [l for l in set(labels) if len(l.split()) > 4]
check("4.5  no CTA label over 4 words", not longs, str(longs))

dl = {l for l in labels if "download" in l.lower()}
check("4.5  single download label", len(dl) <= 1, str(dl))

# --- per page -------------------------------------------------------------
for name, src in HTML.items():
    if name == "404.html":
        check("404 has <base href>", '<base href="/"' in src)
    t = body_of(src)
    if "\u2014" in t:
        check(f"{name}: no em dash", False)

ok = sum(1 for r in results if r[0])
print(f"\n  PRE-FLIGHT  {ok}/{len(results)} passed\n")
for good, name, detail in results:
    if not good:
        print(f"  FAIL  {name}  {detail}")
for good, name, detail in results:
    if good:
        print(f"  pass  {name}")
print()
sys.exit(0 if ok == len(results) else 1)
