#!/usr/bin/env python3
"""Generates the multi-page Maples Tech Club website into ./maples-tech-club/."""
import os, re, shutil, html

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "maples-tech-club")
os.makedirs(OUT, exist_ok=True)

PDF = "Maples_Tech_Club_Proposal_Principal.pdf"


# Always rebuild the PDF first, so the site never ships a stale or wrongly
# dated copy. If reportlab is missing we carry on with whatever PDF is there.
def _rebuild_pdf():
    import subprocess, sys
    builder = os.path.join(BASE, "build_pdf.py")
    if not os.path.exists(builder):
        return
    r = subprocess.run([sys.executable, builder], capture_output=True, text=True)
    if r.returncode == 0:
        print("  PDF rebuilt")
    else:
        print("  ! PDF not rebuilt, using the existing file:",
              (r.stderr or "").strip().splitlines()[-1:] or "unknown error")


_rebuild_pdf()


# Page count is read from the built PDF so the site can never quote a stale number.
def _pdf_pages(path, default=13):
    try:
        m = re.search(rb"/Count\s+(\d+)", open(path, "rb").read())
        return int(m.group(1)) if m else default
    except Exception:
        return default

NP = _pdf_pages(os.path.join(BASE, PDF))

# ══════════════════════════════════════════════════════════════════ CSS
CSS = r"""
/* ============================================================================
   Maples Tech Club - design system
   Redesign mode: overhaul. Content and IA preserved, visual language replaced.

   Dials: DESIGN_VARIANCE 6 / MOTION_INTENSITY 4 / VISUAL_DENSITY 4
   Trust-first institutional audience (a Principal) pulls the dials down;
   redesign-overhaul pushes variance and motion back up by two.

   Palette is inherited from the PDF, not invented: #0f4c81 is the ACCENT
   constant in build_pdf.py, commented there as "deep institutional blue", and
   #c2410c already appears in the same document. Navy carries structure, burnt
   orange is the single accent. One accent, whole page, both themes.
   ========================================================================== */

/* Geist Variable, SIL Open Font License 1.1, subset to Latin plus the few
   symbols this site uses. Embedded as a data URI so the page makes zero
   network requests for type: no FOUT, no layout shift, works offline. */
@font-face{
  font-family:"Geist";
  src:url(data:font/woff2;base64,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) format("woff2-variations");
  font-weight:100 900;
  font-style:normal;
  font-display:swap;
}

:root{
  color-scheme: light dark;

  /* neutrals - cool, so they sit with the navy rather than fighting it */
  --paper:#f6f7f9;
  --surface:#ffffff;
  --surface-2:#f0f3f7;
  --ink:#0c1b2a;
  --body:#44525f;
  --muted:#6b7b8c;
  --line:#dde3ea;
  --line-strong:#c6d0db;

  /* brand - structure */
  --brand:#0f4c81;
  --brand-deep:#0c2136;
  --brand-soft:#e9eff6;

  /* accent - exactly one, used everywhere */
  --accent:#c2410c;
  --accent-ink:#9a340a;
  --accent-soft:#fcf0e8;

  /* semantic, kept inside the same family */
  --good:#0f766e;
  --good-soft:#e7f3f1;
  --warn:#8a5a0b;
  --warn-soft:#fbf2e2;

  /* shape - documented 3 step scale, applied everywhere.
     panels 12, controls 8, chips 6. No exceptions. */
  --r-panel:12px;
  --r-control:8px;
  --r-chip:6px;

  --ease:cubic-bezier(.16,1,.3,1);
  --shadow:0 1px 2px rgba(12,33,54,.04), 0 8px 24px -12px rgba(12,33,54,.14);
  --shadow-lift:0 2px 4px rgba(12,33,54,.05), 0 18px 40px -18px rgba(12,33,54,.22);
  --maxw:1180px;
}

@media (prefers-color-scheme: dark){
  :root{
    --paper:#0b1420;
    --surface:#111e2d;
    --surface-2:#16263a;
    --ink:#e9eef4;
    --body:#b2bfcd;
    --muted:#8294a7;
    --line:#1f3148;
    --line-strong:#2c4259;

    --brand:#6aa6dd;
    --brand-deep:#081623;
    --brand-soft:#13293f;

    --accent:#fb923c;
    --accent-ink:#fdba74;
    --accent-soft:#2b1a0e;

    --good:#5eead4;
    --good-soft:#102b2a;
    --warn:#fcd34d;
    --warn-soft:#2a2210;

    --shadow:0 1px 2px rgba(0,0,0,.3), 0 8px 24px -12px rgba(0,0,0,.6);
    --shadow-lift:0 2px 4px rgba(0,0,0,.35), 0 18px 40px -18px rgba(0,0,0,.7);
  }
}

*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
@media (prefers-reduced-motion: reduce){html{scroll-behavior:auto}}

body{
  margin:0;
  background:var(--paper);
  color:var(--body);
  font-family:"Geist",ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  font-size:16.5px;
  line-height:1.65;
  font-feature-settings:"ss01","cv01";
  -webkit-font-smoothing:antialiased;
  text-rendering:optimizeLegibility;
}

/* figures line up in columns without pulling in a second type family */
.mono,.stat b,.row span:last-child,table td:last-child,.num{
  font-variant-numeric:tabular-nums lining-nums;
}

h1,h2,h3,h4{color:var(--ink);margin:0 0 .5em;font-weight:620;letter-spacing:-.022em;line-height:1.14}
h1{font-size:clamp(1.95rem,1.1rem + 2.7vw,3.05rem);letter-spacing:-.034em;line-height:1.05;font-weight:640}
h2{font-size:clamp(1.6rem,1.05rem + 1.9vw,2.45rem);letter-spacing:-.028em;line-height:1.1}
h3{font-size:1.16rem;letter-spacing:-.014em;font-weight:620}
h4{font-size:1rem;font-weight:620;letter-spacing:-.01em}
p{margin:0 0 1.05em;max-width:68ch}
a{color:var(--brand);text-decoration-color:color-mix(in srgb,var(--brand) 32%,transparent);text-underline-offset:3px}
a:hover{text-decoration-color:currentColor}
strong,b{color:var(--ink);font-weight:620}
small{font-size:.86rem}
hr,.hr{border:0;border-top:1px solid var(--line);margin:34px 0}
img{max-width:100%;height:auto;display:block}
::selection{background:color-mix(in srgb,var(--accent) 22%,transparent);color:var(--ink)}

:focus-visible{outline:2.5px solid var(--accent);outline-offset:3px;border-radius:3px}

.wrap{width:100%;max-width:var(--maxw);margin-inline:auto;padding-inline:28px}

/* sections. Density 4 = standard rhythm, not an art gallery. */
section{padding:74px 0}
section.band{padding:74px 0;background:var(--surface-2);border-block:1px solid var(--line)}
.sec,.anchor{scroll-margin-top:92px}

/* ---------------------------------------------------------------- nav ---- */
.nav{
  position:sticky;top:0;z-index:50;
  background:color-mix(in srgb,var(--paper) 86%,transparent);
  backdrop-filter:saturate(1.6) blur(14px);
  -webkit-backdrop-filter:saturate(1.6) blur(14px);
  border-bottom:1px solid var(--line);
}
@media (prefers-reduced-transparency: reduce){.nav{background:var(--paper);backdrop-filter:none;-webkit-backdrop-filter:none}}
.navin{
  max-width:var(--maxw);margin-inline:auto;padding:0 28px;
  height:68px;display:flex;align-items:center;gap:22px;justify-content:space-between;
}
.brand{display:flex;align-items:center;gap:11px;text-decoration:none;color:var(--ink);flex:0 0 auto}
.logo{width:34px;height:34px;flex:0 0 auto}
.bname{font-weight:640;font-size:.97rem;letter-spacing:-.02em;color:var(--ink);line-height:1.15}
.bsub{font-size:.715rem;color:var(--muted);letter-spacing:.005em}
.links{display:flex;align-items:center;gap:3px;flex:0 1 auto;min-width:0}
.links a{
  color:var(--body);text-decoration:none;font-size:.885rem;font-weight:520;
  padding:8px 11px;border-radius:var(--r-control);white-space:nowrap;
  transition:color .18s var(--ease),background .18s var(--ease);
}
.links a:hover{color:var(--ink);background:var(--surface-2)}
.links a.on{color:var(--ink);background:var(--surface-2);font-weight:580}
.links a.cta{
  background:var(--brand);color:#fff;font-weight:580;margin-left:7px;
  box-shadow:0 1px 2px rgba(12,33,54,.16);
}
.links a.cta:hover{background:var(--brand-deep);color:#fff}
@media (prefers-color-scheme: dark){
  .links a.cta{background:var(--brand);color:#06121e}
  .links a.cta:hover{background:#8dbce8;color:#06121e}
}
.logo .lsq{fill:var(--brand)}
.logo .lmk{fill:#fff}
@media (prefers-color-scheme: dark){.logo .lmk{fill:#06121e}}
footer .logo .lsq{fill:#fff}
footer .logo .lmk{fill:var(--brand-deep)}
.burger{
  display:none;background:var(--surface);border:1px solid var(--line-strong);
  color:var(--ink);font-size:1.1rem;line-height:1;padding:9px 12px;
  border-radius:var(--r-control);cursor:pointer;
}

/* --------------------------------------------------------------- hero ---- */
/* Variance 6: asymmetric 1.08fr / .92fr, not a centred stack. */
.hero{padding:58px 0 66px;position:relative;overflow:hidden}
.hero::after{
  content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;
  background:
    radial-gradient(70ch 40ch at 82% 8%, color-mix(in srgb,var(--brand) 7%,transparent), transparent 70%),
    radial-gradient(50ch 30ch at 4% 96%, color-mix(in srgb,var(--accent) 5%,transparent), transparent 70%);
}
.hero h1{margin-bottom:.42em;max-width:20ch}
.hero .lead{font-size:clamp(1.02rem,.96rem + .34vw,1.17rem);color:var(--body);max-width:52ch;margin-bottom:26px}
.split{display:grid;grid-template-columns:1.08fr .92fr;gap:56px;align-items:start}
.hero .split{grid-template-columns:1.2fr .8fr;gap:46px}
.split.mid{align-items:center}
.hero figure{margin:0;position:relative}
.hero figure img{
  width:100%;aspect-ratio:16/10;object-fit:cover;
  border-radius:var(--r-panel);border:1px solid var(--line);box-shadow:var(--shadow-lift);
}
.fig{margin:0}
.fig figcaption{margin-top:10px;font-size:.84rem;color:var(--muted)}
.fig img{width:100%;aspect-ratio:16/10;object-fit:cover;border-radius:var(--r-panel);
  border:1px solid var(--line);box-shadow:var(--shadow);max-height:440px}
figcaption{font-size:.8rem;color:var(--muted);margin-top:10px;max-width:46ch}

.lead{font-size:1.06rem;color:var(--body);max-width:64ch}

/* ------------------------------------------------------------- labels ---- */
/* Eyebrow restraint (4.7). These survive only as small component labels, never
   as uppercase wide tracking section eyebrows. No uppercase, no letterspacing. */
.kicker,.eyebrow{
  display:block;font-size:.76rem;font-weight:600;color:var(--accent);
  letter-spacing:0;text-transform:none;margin-bottom:9px;
}


/* .grad used to paint an AI cyan-indigo-violet gradient across 18 headings.
   Neutralised to the single page accent. */
.grad{color:var(--accent);background:none;-webkit-text-fill-color:currentColor}

.shead{margin-bottom:30px;max-width:62ch}
.shead p{color:var(--body);margin-bottom:0}
.shead h2{margin-bottom:.34em}

/* ------------------------------------------------------------ buttons ---- */
.btns{display:flex;flex-wrap:wrap;gap:11px;align-items:center}
.btn{
  --bg:var(--surface); --fg:var(--ink); --bd:var(--line-strong);
  display:inline-flex;align-items:center;justify-content:center;gap:8px;
  padding:11px 19px;border-radius:var(--r-control);
  background:var(--bg);color:var(--fg);border:1px solid var(--bd);
  font-size:.925rem;font-weight:580;line-height:1.25;text-decoration:none;
  white-space:nowrap;                      /* CTA must never wrap (4.5) */
  cursor:pointer;
  transition:transform .16s var(--ease),box-shadow .2s var(--ease),
             background .2s var(--ease),border-color .2s var(--ease);
}
.btn:hover{transform:translateY(-1px);box-shadow:var(--shadow);text-decoration:none}
.btn:active{transform:translateY(1px) scale(.992)}
.btn-p,.b1{--bg:var(--brand); --fg:#fff; --bd:var(--brand)}
.btn-p:hover,.b1:hover{--bg:var(--brand-deep); --bd:var(--brand-deep)}
@media (prefers-color-scheme: dark){
  .btn-p,.b1{--fg:#06121e}
  .btn-p:hover,.b1:hover{--bg:#8dbce8; --bd:#8dbce8; --fg:#06121e}
}
.b2{--bg:var(--surface); --fg:var(--ink); --bd:var(--line-strong)}
.btn-s{padding:8px 14px;font-size:.855rem}
.btn.cta{--bg:var(--accent); --fg:#fff; --bd:var(--accent)}
.btn.cta:hover{--bg:var(--accent-ink); --bd:var(--accent-ink)}

/* --------------------------------------------------------------- grid ---- */
.grid{display:grid;gap:18px}
.g2{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}
.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
/* Variance 6: the three up grid is deliberately uneven so it does not read as
   the stock three identical feature cards (9.C). */
.g3.uneven{grid-template-columns:1.25fr 1fr 1fr}
.lnkgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(248px,1fr));gap:14px}

/* -------------------------------------------------------------- cards ---- */
.card{
  background:var(--surface);border:1px solid var(--line);
  border-radius:var(--r-panel);padding:24px 24px 22px;
  transition:border-color .2s var(--ease),box-shadow .2s var(--ease),transform .2s var(--ease);
}
.card > :last-child{margin-bottom:0}
.card h3,.card h4{margin-bottom:.4em}
a.card,.card.lnk{text-decoration:none;display:block;color:var(--body)}
a.card:hover,.card.lnk:hover{border-color:var(--line-strong);box-shadow:var(--shadow);transform:translateY(-2px)}
.card.tw{border-left:3px solid var(--accent)}
.hpanel{
  background:var(--surface);border:1px solid var(--line);
  border-radius:var(--r-panel);padding:22px 24px;box-shadow:var(--shadow);
}

/* rows: one hairline between items, never top and bottom on every row (9.F) */
.row{
  display:flex;justify-content:space-between;align-items:baseline;gap:18px;
  padding:11px 0;border-bottom:1px solid var(--line);
}
.row:last-child{border-bottom:0}
.row > span:first-child{color:var(--muted);font-size:.9rem}
.row > span:last-child{color:var(--ink);font-weight:580;text-align:right;font-size:.92rem}
.row .free,.free{color:var(--good);font-weight:620}
.row .paid,.paid{color:var(--accent)}

.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--line);
  border:1px solid var(--line);border-radius:var(--r-panel);overflow:hidden}
.stat{background:var(--surface);padding:19px 20px}
.stat b{display:block;color:var(--ink);font-size:1.5rem;font-weight:640;letter-spacing:-.03em;line-height:1.15}
.stat span{display:block;color:var(--muted);font-size:.79rem;margin-top:3px}

/* -------------------------------------------------------------- chips ---- */
.tags,.pills{display:flex;flex-wrap:wrap;gap:7px;margin-top:13px}
.pill{
  display:inline-flex;align-items:center;gap:6px;
  padding:4px 10px;border-radius:var(--r-chip);
  font-size:.785rem;font-weight:540;line-height:1.45;
  background:var(--surface-2);color:var(--body);border:1px solid var(--line);
  white-space:normal;
}
.pill.p-c,.pill.p-a{background:var(--brand-soft);color:var(--brand);border-color:transparent}
.pill.p-v,.pill.p-g{background:var(--accent-soft);color:var(--accent-ink);border-color:transparent}
@media (prefers-color-scheme: dark){.pill.p-v,.pill.p-g{color:var(--accent)}}
.mono{
  font-family:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace;
  font-size:.86em;background:var(--surface-2);border:1px solid var(--line);
  border-radius:var(--r-chip);padding:2px 5px;color:var(--ink);
}

/* ----------------------------------------------------- numbered steps ---- */
.steps{list-style:none;margin:0;padding:0 0 0 0;display:grid;gap:26px}
.step{position:relative;padding-left:52px}
.step .num{
  position:absolute;left:0;top:1px;width:32px;height:32px;border-radius:50%;
  display:grid;place-items:center;font-size:.86rem;font-weight:620;
  background:var(--brand-soft);color:var(--brand);border:1px solid transparent;
}
.step h4{margin-bottom:.3em}
.step p{margin-bottom:.5em}
.step::before{
  content:"";position:absolute;left:15.5px;top:38px;bottom:-26px;width:1px;background:var(--line);
}
.step:last-child::before{display:none}

/* -------------------------------------------------------------- notes ---- */
.note{
  background:var(--brand-soft);border-left:3px solid var(--brand);
  border-radius:0 var(--r-panel) var(--r-panel) 0;
  padding:18px 22px;margin:22px 0;
}
.note > :last-child{margin-bottom:0}
.note h4{margin-bottom:.35em}
.note.warn{background:var(--warn-soft);border-left-color:var(--warn)}
.note.good{background:var(--good-soft);border-left-color:var(--good)}
.note.disc{background:var(--surface-2);border-left-color:var(--line-strong)}
.warn{color:var(--warn)}
.good{color:var(--good)}
.no{color:var(--accent)}

.u{text-decoration:underline;text-underline-offset:3px}

/* ------------------------------------------------------------- tables ---- */
table{width:100%;border-collapse:collapse;font-size:.91rem;margin:18px 0}
th,td{text-align:left;padding:11px 14px;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--ink);font-weight:620;font-size:.84rem;background:var(--surface-2)}
tr:last-child td{border-bottom:0}

/* ------------------------------------------------------------- tocbar ---- */
.tocbar{
  display:flex;flex-wrap:wrap;gap:7px;padding:14px 0 0;
}
.tocbar a{
  font-size:.83rem;font-weight:540;text-decoration:none;color:var(--body);
  padding:6px 11px;border:1px solid var(--line);border-radius:var(--r-chip);
  background:var(--surface);transition:all .18s var(--ease);
}
.tocbar a:hover{color:var(--ink);border-color:var(--line-strong);background:var(--surface-2)}

/* ------------------------------------------------------------- footer ---- */
/* The single deliberate colour block on the page, at the very end. */
footer{background:var(--brand-deep);color:#9fb3c6;padding:56px 0 26px;border-top:1px solid var(--line)}
footer .brand,footer .bname{color:#fff}
footer .bsub{color:#8ba1b6}
footer h4{color:#fff;font-size:.9rem;margin-bottom:.8em}
footer a{color:#c3d3e2;text-decoration:none}
footer a:hover{color:#fff;text-decoration:underline}
footer p{color:#9fb3c6}
.fgrid{display:grid;grid-template-columns:1.5fr 1fr 1fr;gap:38px}
.fgrid a{display:block;padding:3.5px 0;font-size:.9rem}
.fbot{
  margin-top:34px;padding-top:20px;border-top:1px solid rgba(255,255,255,.1);
  font-size:.82rem;color:#8ba1b6;display:flex;flex-wrap:wrap;gap:12px;justify-content:space-between;
}
.fbot p{margin:0;color:#8ba1b6;font-size:.82rem}

/* ------------------------------------------------------------- motion ---- */
/* Motion intensity 4: entry cascade and hover feedback only. No scroll
   hijack, no parallax, no infinite loops. Driven by IntersectionObserver,
   never by a scroll listener (5.D). */
.rv{opacity:0;transform:translateY(14px);transition:opacity .62s var(--ease),transform .62s var(--ease)}
.rv.in{opacity:1;transform:none}
@media (prefers-reduced-motion: reduce){
  .rv{opacity:1;transform:none;transition:none}
  *,*::before,*::after{animation-duration:.001ms !important;animation-iteration-count:1 !important;
    transition-duration:.001ms !important;scroll-behavior:auto !important}
}

/* --------------------------------------------------------- responsive ---- */
@media (max-width:1000px){
  .fgrid{grid-template-columns:1fr 1fr;gap:28px}
  .g3,.g3.uneven{grid-template-columns:1fr 1fr}
  .stats{grid-template-columns:1fr 1fr}
}
/* icons are sized at the source: an inline svg with no width attribute
   expands to its container, so every context gets an explicit box */
svg.i{width:18px;height:18px;flex:none;vertical-align:-.17em;
  fill:none;stroke:currentColor;stroke-width:1.7;
  stroke-linecap:round;stroke-linejoin:round}
.btn svg.i{width:16px;height:16px}
.eyebrow svg.i,.kicker svg.i{width:14px;height:14px;stroke:var(--accent)}
.ic{display:inline-flex;align-items:center;justify-content:center;
  width:40px;height:40px;margin-bottom:14px;
  border-radius:var(--r-control);background:var(--brand-soft);
  border:1px solid var(--line);color:var(--brand)}
.ic svg.i{width:20px;height:20px;stroke:var(--brand)}
.card.tw .ic{background:var(--accent-soft);border-color:var(--accent-soft);
  color:var(--accent-ink)}
.card.tw .ic svg.i{stroke:var(--accent-ink)}
.lnk svg.i{width:17px;height:17px;stroke:var(--brand)}
.pill svg.i{width:13px;height:13px}

@media (max-width:860px){
  .burger{display:block}
  .links{
    display:none;position:absolute;top:68px;left:0;right:0;
    flex-direction:column;align-items:stretch;gap:2px;
    background:var(--surface);border-bottom:1px solid var(--line);
    padding:12px 20px 18px;box-shadow:var(--shadow-lift);
  }
  .links.open{display:flex}
  .links a{padding:11px 12px;font-size:.96rem}
  .links a.cta{margin-left:0;margin-top:7px;text-align:center;justify-content:center}
  .split,.split.mid{grid-template-columns:1fr;gap:34px}
  .hero{padding:44px 0 56px}
  .hero h1{max-width:none}
  .hero .lead{max-width:none}
}
@media (max-width:860px){
  /* these tables carry real comparison data, so they scroll rather than
     reflow into something unreadable */
  table{display:block;width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch}
  table thead,table tbody{display:table;width:100%;min-width:520px}
  .mono{overflow-wrap:anywhere}
  .pill{overflow-wrap:anywhere}
}
@media (max-width:720px){
  section,section.band{padding:52px 0}
  .wrap{padding-inline:20px}
  .navin{padding:0 20px}
  .g2,.g3,.g3.uneven,.lnkgrid{grid-template-columns:1fr}
  .fgrid{grid-template-columns:1fr;gap:24px}
  .card{padding:20px}
  .steps{gap:22px}
}
@media (max-width:480px){
  body{font-size:16px}
  .stats{grid-template-columns:1fr}
  .btn{width:100%}
  .btns{gap:9px}
  .row{flex-direction:column;align-items:flex-start;gap:2px}
  .row > span:last-child{text-align:left}
  .fbot{flex-direction:column;gap:6px}
}

@media print{
  .nav,.burger,.tocbar,.btns{display:none}
  body{background:#fff;color:#000;font-size:11pt}
  section{padding:18px 0}
  .rv{opacity:1;transform:none}
}

"""

LOGO = """<svg class="logo" viewBox="0 0 40 40" role="img" aria-label="Maples Tech Club">
<rect class="lsq" x="1" y="1" width="38" height="38" rx="9"/>
<path class="lmk" d="M10.5 28.5V12h3.4l6.1 9.4 6.1-9.4h3.4v16.5h-3.5v-10l-5 7.6h-2l-5-7.6v10z"/>
</svg>"""

def ic(p):
    return f'<svg class="i" viewBox="0 0 24 24" aria-hidden="true">{p}</svg>'

I_CODE   = ic('<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>')
I_CHIP   = ic('<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>')
I_BRAIN  = ic('<path d="M12 5a3 3 0 0 0-6 0 3 3 0 0 0-1 5.8A3 3 0 0 0 7 17a3 3 0 0 0 5 2.2V5z"/><path d="M12 5a3 3 0 0 1 6 0 3 3 0 0 1 1 5.8A3 3 0 0 1 17 17a3 3 0 0 1-5 2.2"/>')
I_PEN    = ic('<path d="M12 19l7-7 3 3-7 7-3-3z"/><path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18z"/><path d="M2 2l7.586 7.586"/><circle cx="11" cy="11" r="2"/>')
I_SHIELD = ic('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>')
I_TROPHY = ic('<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M6 3h12v6a6 6 0 0 1-12 0z"/><path d="M9 21h6M12 15v6"/>')
I_MAIL   = ic('<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 7l-10 6L2 7"/>')
I_CLOUD  = ic('<path d="M18 17h-7a5 5 0 1 1 1-9.9A6 6 0 1 1 18 17z"/>')
I_GIT    = ic('<circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9v3a3 3 0 0 1-3 3H9"/><path d="M6 15V6"/>')
I_GLOBE  = ic('<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20 15 15 0 0 1 0-20z"/>')
I_RUPEE  = ic('<path d="M6 3h12M6 8h12M6 13h5a5 5 0 0 0 0-10"/><path d="M6 13l8 8"/>')
I_USERS  = ic('<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>')
I_DOC    = ic('<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><path d="M8 13h8M8 17h6"/>')
I_DOWN   = ic('<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><path d="M12 15V3"/>')
I_SPARK  = ic('<path d="M12 2l2.2 6.4L21 11l-6.8 2.6L12 20l-2.2-6.4L3 11l6.8-2.6z"/>')
I_BOOK   = ic('<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>')
I_CHART  = ic('<path d="M3 3v18h18"/><path d="M7 15l4-5 3 3 5-7"/>')
I_LOCK   = ic('<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>')

PAGES = [("index.html","Home"),("about.html","The Club"),("benefits.html","Benefits"),
         ("registration.html","Registration"),("join.html","Join Us"),("proposal.html","For the Principal")]

def nav(cur):
    out = []
    for f, t in PAGES:
        cls = ' class="cta"' if f == "proposal.html" else (' class="on"' if f == cur else "")
        out.append(f'<a href="{f}"{cls}>{t}</a>')
    return "\n      ".join(out)

FOOT = f"""
<footer>
  <div class="wrap">
    <div class="fgrid">
      <div>
        <a class="brand" href="index.html" style="margin-bottom:12px">{LOGO}
          <span><span class="bname">Maples Tech Club</span><br>
          <span class="bsub">Maples Academy &middot; Khatauli</span></span></a>
        <p style="font-size:14px;max-width:34ch">A student-run technology society proposed for
        Maples Academy, Khatauli, Uttar Pradesh - teaching computing, AI, robotics and design
        by building real things.</p>
        <p style="font-size:13.5px;color:var(--tx3);margin-top:8px">
        Motto - <em>Learn it. Build it. Ship it.</em></p>
      </div>
      <div><h5>The Club</h5><ul>
        <li><a href="about.html">Purpose &amp; vision</a></li>
        <li><a href="about.html#squads">The six squads</a></li>
        <li><a href="about.html#structure">Structure</a></li>
        <li><a href="about.html#calendar">Annual calendar</a></li>
        <li><a href="join.html">Selection process</a></li>
        <li><a href="join.html#conduct">Code of conduct</a></li>
      </ul></div>
      <div><h5>Benefits</h5><ul>
        <li><a href="benefits.html#school">For the school</a></li>
        <li><a href="benefits.html#students">For students</a></li>
        <li><a href="benefits.html#learn">Free learning</a></li>
        <li><a href="benefits.html#ai">AI tools</a></li>
        <li><a href="registration.html">Registration roadmap</a></li>
        <li><a href="registration.html#domain">Activating our domain</a></li>
      </ul></div>
      <div><h5>Official portals</h5><ul>
        <li><a href="https://edu.google.com/workspace-for-education/editions/education-fundamentals/" target="_blank" rel="noopener">Google for Education</a></li>
        <li><a href="https://www.microsoft.com/en-in/education/products/office" target="_blank" rel="noopener">Microsoft 365 Education</a></li>
        <li><a href="https://github.com/education" target="_blank" rel="noopener">GitHub Education</a></li>
        <li><a href="https://support.google.com/a/answer/7667994" target="_blank" rel="noopener">Google Admin Console</a></li>
        <li><a href="https://aim.gov.in/atl.php" target="_blank" rel="noopener">Atal Tinkering Labs</a></li>
        <li><a href="{PDF}" download>Download proposal PDF</a></li>
      </ul></div>
    </div>
    <div class="disc"><strong>Please note.</strong> This website is a student proposal prepared by
      Harsh (Class XII, Roll No. 13) to support an application to the Principal. The Maples Tech Club is
      <em>proposed</em> and not yet a sanctioned body of the school, and this site is not an official
      publication of Maples Academy. Every programme listed is described from its provider's own
      published information at the time of writing; eligibility rules, features and fees change, so
      please confirm on the official links before acting.</div>
    <div class="fbot">
      <span>Proposal prepared by <strong style="color:var(--tx2)">Harsh</strong>, Class XII, Roll No. 13,
        Maples Academy, Khatauli, Muzaffarnagar, Uttar Pradesh.</span>
      <span>Built by the students it is meant for.</span>
    </div>
  </div>
</footer>
""" + """
<script>
(function(){
  var b=document.querySelector('.burger'), n=document.querySelector('nav.links');
  if(b&&n){b.addEventListener('click',function(){
    n.classList.toggle('open');
    b.setAttribute('aria-expanded', n.classList.contains('open'));
  });}

  // Entry reveal. MOTION_INTENSITY 4: content arrives once, then stays put.
  // IntersectionObserver, never a scroll listener. Honours reduced motion,
  // and if the API is missing everything is simply shown.
  var items = document.querySelectorAll('.rv');
  var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(still || !('IntersectionObserver' in window)){
    for(var i=0;i<items.length;i++) items[i].classList.add('in');
    return;
  }
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, {rootMargin:'0px 0px -8% 0px', threshold:0.12});
  items.forEach(function(el){ io.observe(el); });
})();
</script>
"""

def page(fname, title, desc, body):
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} &middot; Maples Tech Club, Maples Academy Khatauli</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="author" content="Harsh, Class XII, Roll No. 13, Maples Academy Khatauli">
<meta name="theme-color" content="#f6f7f9" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0b1420" media="(prefers-color-scheme: dark)">
<style>{CSS}</style>
</head>
<body>
<header class="nav">
  <div class="navin">
    <a class="brand" href="index.html">{LOGO}
      <span><span class="bname">Maples Tech Club</span><br>
      <span class="bsub">Maples Academy &middot; Khatauli</span></span></a>
    <button class="burger" aria-label="Menu" aria-expanded="false">&#9776;</button>
    <nav class="links">
      {nav(fname)}
    </nav>
  </div>
</header>
<main>
{body}
</main>
{FOOT}
</body>
</html>"""
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(doc)
    return len(doc)


# ══════════════════════════════════════════════════════════════════ 1. HOME
home = f"""
<section class="hero"><div class="wrap">
  <div class="split mid">
    <div>
      <span class="eyebrow">Proposed for session 2026-27. Not yet approved.</span>
      <h1>Students who <span class="grad">build things</span>, not just study them.</h1>
      <p class="lead">A technology club for Maples Academy, running on software the school
      already qualifies for at no cost.</p>
      <div class="btns">
        <a class="btn btn-p" href="{PDF}" download>{I_DOWN} Download the proposal</a>
        <a class="btn btn-s" href="benefits.html">See every benefit &rarr;</a>
      </div>
    </div>
    <figure>
      <img src="assets/hero-lab.jpg" width="1376" height="768" fetchpriority="high"
           decoding="async" alt="Students at desktop computers in a school computer
           laboratory, one leaning across to help another.">
    </figure>
  </div>
</div></section>

<section class="band rv"><div class="wrap">
  <div class="split rv">
    <div>
      <h2>What it costs the school</h2>
      <p>Nothing. Every programme named on this site is the provider\u2019s own free offer to
      verified schools, and Maples Academy already owns the one thing they all ask for: a
      domain. The only real cost is a teacher\u2019s time.</p>
      <div class="btns"><a class="btn btn-s" href="registration.html">How registration works &rarr;</a></div>
    </div>
    <div class="hpanel">
      <div class="kicker">The proposal in numbers</div>
      <div class="row"><span>Cost to the school, per year</span><span class="free">&#8377;0</span></div>
      <div class="row"><span>Licence cost of all software</span><span class="free">&#8377;0</span></div>
      <div class="row"><span>Domain to buy</span><span class="free">None - already owned</span></div>
      <div class="row"><span>Teachers required</span><span>1&ndash;2 <small>(advisor + coordinator)</small></span></div>
      <div class="row"><span>Lab time required</span><span>2 hours / week</span></div>
      <div class="row"><span>Open to</span><span>Classes VI &ndash; XII</span></div>
      <div class="row"><span>Domain squads</span><span>6</span></div>
      <div class="row"><span>Government grant possible</span><span class="paid">up to &#8377;20 lakh</span></div>
    </div>
  </div>
  <div class="stats">
    <div class="stat"><b class="grad">&#8377;0</b><span>Google Workspace<br>for Education</span></div>
    <div class="stat"><b class="grad">&#8377;0</b><span>Microsoft 365<br>Education A1</span></div>
    <div class="stat"><b class="grad">&#8377;0</b><span>GitHub Education<br>&amp; Student Pack</span></div>
    <div class="stat"><b class="grad">1</b><span>domain, already<br>owned by the school</span></div>
  </div>
</div></section>

<section class="rv" style="padding-top:8px"><div class="wrap">
  <div class="note vi">
    <h4>The single idea behind this whole proposal</h4>
    <p>Google, Microsoft, GitHub, Canva, Figma, JetBrains and dozens of others give their software
    to schools and school students <strong>free</strong>. They all check eligibility the same way:
    through an <strong>official school email address on the school's own domain</strong>.
    <strong>Maples Academy already owns that domain.</strong> It is
    <span class="mono">mapleskhatauli.com</span>, and it is sitting there unused for this purpose.
    Verify it once with Google as a recognised school, open the Admin Console, and every door on
    this website opens at once. There is nothing to buy.</p>
  </div>
</div></section>

<section class="anchor rv"><div class="wrap">
  <div class="shead">
    <h2>Six squads. One rule: <span class="grad">finish something</span>.</h2>
    <p>Every member ends every term holding something they actually made - a working website, a
    program, a robot that moves, a poster, a short film, a data chart. Theory is taught in service
    of the thing being built, never instead of it.</p>
  </div>
  <div class="grid g3">
    <div class="card"><div class="ic">{I_CODE}</div><h3>Web &amp; App Development</h3>
      <p>HTML, CSS, JavaScript, Git and GitHub, hosting and responsive design.</p>
      <div class="tags"><span class="pill p-c">Builds the school website</span></div></div>
    <div class="card vi"><div class="ic">{I_BRAIN}</div><h3>AI &amp; Data</h3>
      <p>Python, data handling, charts and statistics, introductory machine learning, prompt
      literacy and AI ethics.</p>
      <div class="tags"><span class="pill p-v">CBSE AI skill subject support</span></div></div>
    <div class="card gr"><div class="ic">{I_CHIP}</div><h3>Robotics, IoT &amp; Electronics</h3>
      <p>Circuits, sensors, Arduino, micro:bit, 3D design and printing, automation.</p>
      <div class="tags"><span class="pill p-g">Science exhibition</span></div></div>
    <div class="card am"><div class="ic">{I_PEN}</div><h3>Design &amp; Digital Media</h3>
      <p>Graphic design, typography, posters and magazine layout, photography, video editing.</p>
      <div class="tags"><span class="pill p-a">Annual Day coverage</span></div></div>
    <div class="card"><div class="ic">{I_SHIELD}</div><h3>Cyber Safety &amp; Digital Citizenship</h3>
      <p>Passwords and 2FA, phishing and fraud, privacy, safe social media, fact-checking.</p>
      <div class="tags"><span class="pill p-c">School-wide awareness</span></div></div>
    <div class="card vi"><div class="ic">{I_TROPHY}</div><h3>Competitive Programming</h3>
      <p>Problem solving, algorithms, data structures, olympiad and aptitude preparation.</p>
      <div class="tags"><span class="pill p-v">Olympiads &amp; contests</span></div></div>
  </div>
  <div class="btns"><a class="btn btn-s" href="about.html">Read the club charter &rarr;</a></div>
</div></section>

<section class="rv"><div class="wrap">
  <div class="shead">
    <h2>Four reasons a principal should say yes</h2>
  </div>
  <div class="grid g2">
    <div class="card gr"><div class="ic">{I_RUPEE}</div><h3>It costs the school nothing</h3>
      <p>Not one rupee. The school already owns <span class="mono">mapleskhatauli.com</span>, so
      there is no domain to buy and no yearly fee to find. Every software licence described here is
      free to verified schools.</p></div>
    <div class="card"><div class="ic">{I_CLOUD}</div><h3>The school gains real infrastructure</h3>
      <p>Official email for every teacher and student, Google Classroom, Microsoft Teams, cloud storage,
      a website that is actually kept up to date and an online notice board. The school keeps full
      administrative control of every account.</p></div>
    <div class="card vi"><div class="ic">{I_BOOK}</div><h3>It matches CBSE and NEP 2020</h3>
      <p>CBSE now examines Artificial Intelligence and Information Technology as skill subjects, and
      the National Education Policy 2020 places explicit emphasis on coding, computational thinking
      and experiential learning. This club is the practical wing of that.</p></div>
    <div class="card am"><div class="ic">{I_TROPHY}</div><h3>Students leave with proof, not just marks</h3>
      <p>A published project, a GitHub profile, a competition certificate - evidence a student
      can show to a college, a scholarship committee or an employer. Marks alone no longer
      distinguish anyone.</p></div>
  </div>
</div></section>

<section class="rv"><div class="wrap">
  <div class="shead">
    <h2>What this proposal does <em>not</em> claim</h2>
  </div>
  <div class="note warn">
    <h4>Two limits worth stating plainly</h4>
    <p><strong>1. OpenAI's free <em>ChatGPT for Teachers</em> plan is United States only.</strong>
    It is genuinely free for verified U.S. K&ndash;12 educators, but it is not available to Indian
    schools today. What <em>is</em> available to us worldwide and free is
    <a href="https://academy.openai.com/" target="_blank" rel="noopener">OpenAI Academy</a> (AI-literacy
    courses, including a K&ndash;12 educator track) plus the free tiers of ChatGPT, Google Gemini
    and Microsoft Copilot for supervised classroom use.</p>
    <p><strong>2. Most headline &ldquo;free AI for students&rdquo; offers require the student to be 18 or
    above</strong> and are usually aimed at college students. School students under 18 should use the
    free tiers, under supervision, with a teacher present.</p>
    <p>Everything else on this site is, to the best of our research, available to an eligible Indian
    CBSE school right now - and every claim links to the provider's own page so the school can
    verify it independently.</p>
  </div>
</div></section>

<section class="rv" style="padding-top:12px"><div class="wrap">
  <div class="band">
    <h2>A {NP}-page formal application, ready to print and sign</h2>
    <p class="lead" style="margin:0 auto">Complete with the club charter, a verified schedule of every
    benefit, the registration roadmap with documents and costs, the member selection process, the code
    of conduct, safeguards and a one-year target sheet the club asks to be judged against.</p>
    <div class="btns">
      <a class="btn btn-p" href="{PDF}" download>{I_DOWN} Download the proposal</a>
      <a class="btn btn-s" href="proposal.html">Read the summary online &rarr;</a>
    </div>
  </div>
</div></section>
"""

# ══════════════════════════════════════════════════════════════════ 2. ABOUT
about = f"""
<section class="hero" style="padding-bottom:26px"><div class="wrap">
  <span class="eyebrow">{I_USERS} The Club</span>
  <h1>What the <span class="grad">Maples Tech Club</span> actually is</h1>
  <p class="lead">A supervised workshop rather than a lecture class, and the place where the school's
  digital systems are looked after. This page is the club's full charter: what it is, what it is for, how
  it is structured, its six squads and its calendar.</p>
  <div class="tocbar">
    <a href="#definition">Definition</a><a href="#purpose">Purpose</a><a href="#vision">Vision &amp; mission</a>
    <a href="#structure">Structure</a><a href="#squads">The six squads</a><a href="#calendar">Calendar</a>
    <a href="#discipline">Academic discipline</a>
  </div>
</div></section>

<section class="anchor rv" id="definition" style="padding-top:20px"><div class="wrap">
  <div class="shead"><h2>A workshop, not a lecture hall</h2></div>
  <div class="split">
    <div>
      <p>The one rule that defines the Maples Tech Club is that <strong>every member ends every term
      holding something they have actually made</strong>. A working web page, a small program, a robot
      that moves, a poster, a short film, a chart, a written-up experiment. Theory is taught only as far
      as it is needed to make the thing. The club does not repeat the syllabus. It puts it to use.</p>
      <p>The club also <strong>looks after the school's digital systems</strong>. Once the registrations
      are done, the club helps maintain the school's website, its official email accounts, its Google
      Classroom spaces and its event photographs, always under the faculty advisor. So the school gets
      something back, week after week, for the two hours it gives us.</p>
      <p>It is <strong>non-commercial and non-political</strong>. No fee is charged to apply or to be
      a member, and nothing is sold.</p>
    </div>
    <div class="hpanel">
      <div class="kicker">Identity</div>
      <div class="row"><span>Name</span><span>Maples Tech Club (MTC)</span></div>
      <div class="row"><span>Institution</span><span>Maples Academy, Khatauli</span></div>
      <div class="row"><span>Motto</span><span><em>Learn it. Build it. Ship it.</em></span></div>
      <div class="row"><span>Open to</span><span>Classes VI &ndash; XII</span></div>
      <div class="row"><span>Meets</span><span>1 session &times; 2 hrs / week</span></div>
      <div class="row"><span>Proposed by</span><span>Harsh, Class XII, Roll No. 13</span></div>
      <div class="row"><span>Membership fee</span><span class="free">None</span></div>
    </div>
  </div>
</div></section>

<div class="wrap"><div class="hr"></div></div>

<section class="anchor rv" id="purpose" style="padding-top:0"><div class="wrap">
  <div class="shead"><figure class="fig" style="margin:0 0 34px">
    <img loading="lazy" src="assets/students-teach.jpg" width="1376" height="768"
         alt="An older student explaining something at a chalkboard to three younger students
         seated at desks.">
    <figcaption>Objective four: every member teaches the year below them, so the club outlives
    the students who started it.</figcaption>
  </figure>
  <h2>The nine objectives</h2>
    <p>Each objective is stated with the reason it matters specifically to Maples Academy, so the
    club can be judged against it.</p></div>
  <div class="tw"><table>
    <thead><tr><th style="width:34px">#</th><th style="width:26%">Objective</th><th>Why it matters to our school</th></tr></thead>
    <tbody>
      <tr><td><strong>1</strong></td><td><strong>Close the gap between syllabus and practice</strong></td>
        <td>CBSE now examines Artificial Intelligence and Information Technology as skill subjects. A student
        who has actually written and run code understands the paper far better than one who has memorised it.</td></tr>
      <tr><td><strong>2</strong></td><td><strong>Get the school the free digital tools it qualifies for</strong></td>
        <td>Official school email, cloud storage, Google Classroom and Microsoft Teams are available at no
        licence cost - but only to registered institutions. The club does the registration and the upkeep.</td></tr>
      <tr><td><strong>3</strong></td><td><strong>Give every member a verifiable portfolio</strong></td>
        <td>Project work hosted publicly is evidence a student can show to a college, a scholarship committee or
        an employer. Marks alone no longer set anyone apart.</td></tr>
      <tr><td><strong>4</strong></td><td><strong>Build a self-sustaining peer-teaching chain</strong></td>
        <td>Classes XI&ndash;XII train Classes VI&ndash;X. The club does not collapse when its seniors graduate,
        and no teacher gets landed with extra teaching.</td></tr>
      <tr><td><strong>5</strong></td><td><strong>Represent the school externally</strong></td>
        <td>Participation and prizes in olympiads, science fairs, hackathons and innovation challenges bring
        recognition to the institution and to Khatauli.</td></tr>
      <tr><td><strong>6</strong></td><td><strong>Digitise and support school operations</strong></td>
        <td>A maintained website, an online notice board, digital forms, event media and a results portal
        all done by students, supervised by staff, without paying a vendor.</td></tr>
      <tr><td><strong>7</strong></td><td><strong>Run the school's presence online</strong></td>
        <td>With the Principal's permission the club sets up and looks after the school's official pages on
        <strong>Facebook, Instagram</strong> and any other platform the school approves, and designs the
        posters and notices for Annual Day, Sports Day, the Science Exhibition, admissions and every other
        function. Nothing is posted or printed without the Faculty Advisor approving it in writing first.
        This work is currently either not done or paid for outside; the club does it free.</td></tr>
      <tr><td><strong>8</strong></td><td><strong>Teach digital safety and AI ethics</strong></td>
        <td>Students already use AI and social media. Structured guidance on privacy, safe conduct online,
        misinformation and honesty in their work protects the school as much as it protects them.</td></tr>
      <tr><td><strong>9</strong></td><td><strong>Widen career horizons</strong></td>
        <td>Exposure to software, data, design and hardware careers - and to the free national learning
        platforms that teach them, aimed at students who would otherwise never hear of any of it.</td></tr>
    </tbody></table></div>
</div></section>

<section class="anchor rv" id="vision"><div class="wrap">
  <div class="shead"><h2>What we are aiming at</h2></div>
  <div class="note vi">
    <h4>Vision</h4>
    <p style="font-size:18px;color:var(--tx)">No student should leave Maples Academy having only
    <em>read</em> about technology. They should leave having <em>made</em> something with it.</p>
  </div>
  <h3 style="margin-top:26px;margin-bottom:6px">Mission - the club commits to:</h3>
  <ul class="ck">
    <li><strong>Teach practical computing, AI literacy and electronics</strong> through hands-on projects,
      free of cost, to any student of the school who wishes to learn.</li>
    <li><strong>Get hold of, and look after properly,</strong> the free technology our
      school is eligible for, so that the benefit reaches every student and teacher, not just club members.</li>
    <li><strong>Create a peer-teaching chain</strong> in which senior members train junior members, so the club
      survives the departure of any individual, including its founder.</li>
    <li><strong>Represent Maples Academy</strong> in inter-school competitions, olympiads, hackathons and
      national innovation challenges.</li>
    <li><strong>Serve the school with real digital work</strong>: website, notices, results portal, event
      photography, posters and archives.</li>
    <li><strong>Promote safe, ethical and honest use</strong> of computers and artificial intelligence,
      including a firm stand against plagiarism and misuse.</li>
  </ul>
</div></section>

<div class="wrap"><div class="hr"></div></div>

<section class="anchor rv" id="structure" style="padding-top:0"><div class="wrap">
  <div class="shead"><h2>Who answers to whom</h2>
    <p>Authority flows from the Principal to the two nominated teachers, and only then to students.
    <strong>No student office-bearer holds financial or disciplinary authority, and no student is ever
    given administrator rights over a school account.</strong></p></div>
  <div class="tw"><table>
    <thead><tr><th style="width:56px">Tier</th><th style="width:19%">Office</th><th style="width:22%">Held by</th><th>Responsibility</th></tr></thead>
    <tbody>
      <tr><td><strong>1</strong></td><td><strong>Patron</strong></td><td>The Principal</td>
        <td>Approves the club, the annual plan, and any participation outside the school. The final word on everything.</td></tr>
      <tr><td><strong>2</strong></td><td><strong>Faculty Advisor</strong></td><td>One teacher nominated by the Principal</td>
        <td>Present at every session; countersigns all correspondence; answerable for discipline, attendance
        and the safety of the members.</td></tr>
      <tr><td><strong>3</strong></td><td><strong>Coordinator</strong></td><td>One teacher nominated by the Principal.
        May be the same person as the Faculty Advisor.</td>
        <td>Holds the <strong>Google Admin Console</strong> and all administrator passwords, jointly with the
        Principal. The school's verified contact for Google, Microsoft, GitHub and Canva. Creates and closes
        accounts, and is answerable for data privacy and for which apps each class may use.</td></tr>
      <tr><td><strong>4</strong></td><td><strong>Core Committee</strong></td><td>6 students of Classes XI&ndash;XII</td>
        <td>President, Vice-President, Secretary, Technical Lead, Design &amp; Media Lead, Outreach Lead.
        Plan sessions, keep the register, report monthly to the advisor.</td></tr>
      <tr><td><strong>5</strong></td><td><strong>Squad Leads</strong></td><td>6 students, one per domain</td>
        <td>Run the weekly agenda and mentoring for their own squad.</td></tr>
      <tr><td><strong>6</strong></td><td><strong>Core Members</strong></td><td>Selected students, Classes VIII&ndash;XII</td>
        <td>Attend regularly, complete term projects, mentor juniors, represent the school externally.</td></tr>
      <tr><td><strong>7</strong></td><td><strong>Open Members</strong></td><td>Any student, Classes VI&ndash;XII</td>
        <td>Attend open workshops and awareness sessions. No selection of any kind.</td></tr>
    </tbody></table></div>
  <div class="note good" style="margin-top:22px">
    <h4>Why the club will outlive its founder</h4>
    <p>Every squad has a junior deputy. The Core Committee is elected annually in Term IV. All
    documentation, credentials and project files are handed to the Faculty Advisor before the outgoing
    batch leaves, and at least 40% of every new intake is kept for Classes VI&ndash;IX.</p>
  </div>
</div></section>

<section class="anchor rv" id="squads"><div class="wrap">
  <div class="shead"><h2>The six domain squads</h2>
    <p>A member joins one squad but may attend any squad's open sessions.</p></div>
  <div class="tw"><table>
    <thead><tr><th style="width:23%">Squad</th><th style="width:38%">What members learn</th><th>A typical term project</th></tr></thead>
    <tbody>
      <tr><td><strong>Web &amp; App Development</strong></td>
        <td>HTML, CSS, JavaScript, Git and GitHub, hosting, responsive design, basic databases</td>
        <td>The official Maples Academy website and an online notice board</td></tr>
      <tr><td><strong>Artificial Intelligence &amp; Data</strong></td>
        <td>Python, data handling, charts and statistics, introductory machine learning, prompt literacy, AI ethics</td>
        <td>A data study of school attendance, or an image classifier trained on a small dataset</td></tr>
      <tr><td><strong>Robotics, IoT &amp; Electronics</strong></td>
        <td>Circuits, sensors, Arduino, micro:bit, 3D design and printing, automation</td>
        <td>An automatic water-level alarm, or a line-following robot for the science exhibition</td></tr>
      <tr><td><strong>Design &amp; Digital Media</strong></td>
        <td>Graphic design, typography, poster and magazine layout, photography, video editing</td>
        <td>The complete visual identity and coverage of the Annual Day</td></tr>
      <tr><td><strong>Cyber Safety &amp; Digital Citizenship</strong></td>
        <td>Passwords and two-factor authentication, phishing and fraud, privacy, safe social media, fact-checking</td>
        <td>A school-wide digital safety awareness drive and a parents' handout</td></tr>
      <tr><td><strong>Competitive Programming &amp; Logic</strong></td>
        <td>Problem solving, algorithms, data structures, olympiad and aptitude preparation</td>
        <td>A school coding contest and entry to national olympiads</td></tr>
    </tbody></table></div>
</div></section>

<section class="anchor rv" id="calendar"><div class="wrap">
  <div class="shead"><h2>How a year runs</h2></div>
  <div class="tw"><table>
    <thead><tr><th style="width:90px">Term</th><th style="width:150px">Period</th><th style="width:34%">Focus</th><th>Deliverable</th></tr></thead>
    <tbody>
      <tr><td><strong>Term I</strong></td><td>April &ndash; June</td>
        <td>Recruitment, induction, fundamentals, digital hygiene</td>
        <td>Every new member publishes a first small project</td></tr>
      <tr><td><strong>Term II</strong></td><td>July &ndash; September</td>
        <td>Squad specialisation; the school website goes live</td>
        <td>Live school website; inter-house coding contest</td></tr>
      <tr><td><strong>Term III</strong></td><td>October &ndash; December</td>
        <td>Competitions, science exhibition, hackathon participation</td>
        <td><strong>TechFest Maples</strong> - an open exhibition for parents and feeder schools</td></tr>
      <tr><td><strong>Term IV</strong></td><td>January &ndash; March</td>
        <td>Board-exam-light term: documentation, peer teaching, handover</td>
        <td>Annual report to the Principal; election of the next Core Committee</td></tr>
    </tbody></table></div>
</div></section>

<section class="anchor rv" id="discipline" style="padding-top:12px"><div class="wrap">
  <div class="note warn">
    <h4>Academic discipline - a binding rule of the club</h4>
    <p>The club <strong>stops completely for the four weeks before any school examination</strong> and for
    the whole of the CBSE board examination period. Coming to the club is never an excuse for falling
    behind in class. If a member's marks start dropping, the Faculty Advisor keeps them out until they
    recover. Studies come first, and that is written into the code of conduct every member signs.</p>
  </div>
  <div class="btns">
    <a class="btn btn-p" href="join.html">How to join &rarr;</a>
    <a class="btn btn-s" href="benefits.html">What the school gets &rarr;</a>
  </div>
</div></section>
"""

# ══════════════════════════════════════════════════════════════════ 3. BENEFITS
def row(name, url, what, elig, cost, cost_cls="free"):
    return f"""<tr>
      <td><strong>{name}</strong><br><a href="{url}" target="_blank" rel="noopener"
        style="font-size:12.5px;word-break:break-all">{url.replace('https://','').rstrip('/')}</a></td>
      <td>{what}</td><td>{elig}</td><td class="{cost_cls}">{cost}</td></tr>"""

benefits = f"""
<section class="hero" style="padding-bottom:26px"><div class="wrap">
  <span class="eyebrow">{I_SPARK} Benefits &amp; official links</span>
  <h1>Everything the school <span class="grad">can get free</span></h1>
  <p class="lead">Every entry below is a published programme of the named organisation, with its
  official link so the school can verify the claim independently. Nothing here requires Maples Academy
  to enter into a paid contract.</p>
  <div class="tocbar">
    <a href="#school">For the school</a><a href="#students">For students</a>
    <a href="#learn">Free learning</a><a href="#ai">AI tools</a><a href="#govt">Government schemes</a>
    <a href="#worth">What it is worth</a>
  </div>
</div></section>

<section class="anchor rv" id="school" style="padding-top:14px"><div class="wrap">
  <div class="shead"><h2>What <span class="grad">Maples Academy</span> receives</h2>
    <p>These are given to the <em>school</em>, once the school has been verified as an accredited
    institution. From there they reach every teacher and student, not just club members.</p></div>
  <div class="tw"><table>
    <thead><tr><th style="width:21%">Programme</th><th style="width:37%">What the school receives</th>
      <th style="width:26%">Eligibility</th><th style="width:16%">Cost</th></tr></thead>
    <tbody>
    {row("Google Workspace for Education Fundamentals",
         "https://edu.google.com/workspace-for-education/editions/education-fundamentals/",
         "Official school Gmail on our own domain for every student and teacher; Google Classroom; "
         "Meet; Drive; Docs, Sheets, Slides, Forms and Sites; Calendar and Chat; and a central "
         "<strong>Admin Console</strong> giving the school full control of every account, plus pooled "
         "cloud storage for the institution.",
         "Accredited K&ndash;12 schools recognised by CBSE, ICSE or a State Board, after verification by Google. "
         "<a href='https://support.google.com/a/answer/134628' target='_blank' rel='noopener'>Check the qualification rules</a>.",
         "FREE")}
    {row("Microsoft 365 Education (Office 365 A1)",
         "https://www.microsoft.com/en-in/education/products/office",
         "Web and mobile Word, Excel, PowerPoint, Outlook and OneNote; <strong>Microsoft Teams</strong> for "
         "classes; 1&nbsp;TB of OneDrive storage per user; SharePoint; School Data Sync; unlimited staff "
         "and student licences.",
         "Accredited academic institutions, after Microsoft's academic verification. "
         "<a href='https://learn.microsoft.com/en-us/microsoft-365/education/deploy/office-365-education-self-sign-up' "
         "target='_blank' rel='noopener'>Self-sign-up guide</a>.",
         "FREE<br><small>A1 tier</small>")}
    {row("GitHub Education - Teachers &amp; Schools",
         "https://github.com/education/teachers",
         "<strong>GitHub Classroom</strong> for distributing and auto-grading assignments; the "
         "<a href='https://education.github.com/toolbox' target='_blank' rel='noopener'>Teacher Toolbox</a> "
         "of professional developer tools; free GitHub Team with unlimited private repositories for verified "
         "teachers; and free hosting for the school website on "
         "<a href='https://pages.github.com/' target='_blank' rel='noopener'>GitHub Pages</a>.",
         "A currently employed teacher at an accredited institution, verified with a school email address "
         "and faculty identification. Approval is usually quick.",
         "FREE")}
    {row("Canva for Education",
         "https://www.canva.com/education/",
         "The complete Canva Pro feature set for verified K&ndash;12 teachers and, through them, their "
         "students: premium templates, brand kit, background remover and classroom assignment tools - "
         "for school notices, the magazine and event design.",
         "Verified K&ndash;12 teachers and their schools. Students receive access through a "
         "teacher-created class; they cannot enrol independently.",
         "FREE")}
    {row("Optional later: a .edu.in address - ERNET India, MeitY, Govt. of India",
         "https://registry.ernet.in/",
         "<strong>Not needed for anything else on this page.</strong> The school already owns "
         "<span class='mono'>mapleskhatauli.com</span>, and every programme listed here accepts it. A "
         "<span class='mono'>.edu.in</span> address adds academic standing and nothing else. ERNET India is "
         "the <em>exclusive</em> Government registrar for <span class='mono'>.edu.in</span>, "
         "<span class='mono'>.ac.in</span>, <span class='mono'>.res.in</span> and "
         "<span class='mono'>.school.in</span>.",
         "Primary and secondary schools affiliated to CBSE, ICSE or a recognised State Board. "
         "<a href='https://registry.ernet.in/guidelines' target='_blank' rel='noopener'>Official guidelines</a>.",
         "&asymp; &#8377;1,180<br><small>per year, only if<br>the school wants it</small>", "paid")}
    {row("Cisco Networking Academy",
         "https://www.netacad.com/",
         "Free, industry-recognised curricula in networking, cybersecurity, Python and IoT, with instructor "
         "training and student certificates of completion.",
         "Schools and teachers enrolling as an academy.",
         "FREE")}
    {row("Autodesk Education &amp; Tinkercad",
         "https://www.autodesk.com/education/edu-software/overview",
         "Free educational licences for professional design and engineering software, and "
         "<a href='https://www.tinkercad.com/' target='_blank' rel='noopener'>Tinkercad</a> - free "
         "browser-based 3D design, circuit simulation and block coding, built for school classrooms.",
         "Students and educators at accredited institutions; Tinkercad classrooms are open to schools.",
         "FREE")}
    </tbody></table></div>
</div></section>

<section class="anchor rv" id="students"><div class="wrap">
  <div class="shead"><h2>What <span class="grad">Maples students</span> receive</h2>
    <p>These become available once the school email domain exists, because almost all of them verify
    eligibility through an institutional email address - though several also accept a photograph
    of a school identity card.</p></div>
  <div class="tw"><table>
    <thead><tr><th style="width:21%">Programme</th><th style="width:37%">What a student receives</th>
      <th style="width:26%">Eligibility</th><th style="width:16%">Cost</th></tr></thead>
    <tbody>
    {row("GitHub Student Developer Pack",
         "https://education.github.com/pack",
         "A large bundle of professional developer software, cloud credits, domain names and learning "
         "subscriptions contributed by dozens of technology companies - free for as long as the "
         "student's enrolment is verified.",
         "Aged <strong>13 or above</strong>, currently enrolled in a degree- or diploma-granting programme "
         " - <strong>which expressly includes school students</strong>. Verified by school email <em>or</em> "
         "a photograph of the school identity card.",
         "FREE")}
    {row("Figma for Education",
         "https://www.figma.com/education/",
         "Free access to Figma's paid design and prototyping platform, including FigJam whiteboards - "
         "the industry standard for interface design.",
         "Verified high-school students and educators, applying with a school-issued email address. "
         "Renewed annually. Some AI features are restricted for K&ndash;12 users.",
         "FREE")}
    {row("JetBrains Educational Licence",
         "https://www.jetbrains.com/community/education/",
         "The full suite of JetBrains professional programming environments, free for the duration of "
         "study and renewable each year.",
         "Students and teachers at accredited institutions, verified by academic email address or ISIC card.",
         "FREE")}
    {row("Notion for Education",
         "https://www.notion.com/product/notion-for-education",
         "The Notion Plus plan free for individual students and teachers - notes, project planning, "
         "club documentation and knowledge management.",
         "Students and educators verifying with an education email address.",
         "FREE")}
    {row("Microsoft Learn &amp; MakeCode",
         "https://learn.microsoft.com/en-us/training/",
         "Free structured learning paths in programming, cloud computing, data and AI. "
         "<a href='https://www.microsoft.com/en-us/makecode' target='_blank' rel='noopener'>MakeCode</a> "
         "provides block-based coding for micro:bit and Minecraft.",
         "Open to all; progress and achievements are tracked against the account.",
         "FREE")}
    {row("Google for Education learning tools",
         "https://csfirst.withgoogle.com/",
         "<a href='https://csfirst.withgoogle.com/' target='_blank' rel='noopener'>CS First</a> provides free, "
         "ready-made computer-science lesson plans built for school clubs; "
         "<a href='https://applieddigitalskills.withgoogle.com/' target='_blank' rel='noopener'>Applied Digital Skills</a> "
         "and <a href='https://beinternetawesome.withgoogle.com/' target='_blank' rel='noopener'>Be Internet Awesome</a> "
         "cover digital literacy and online safety.",
         "Free and open to schools and clubs worldwide. No verification needed.",
         "FREE")}
    </tbody></table></div>
</div></section>

<section class="anchor rv" id="learn"><div class="wrap">
  <div class="shead"><h2>Free curricula the club will teach from</h2>
    <p>None of these require the school to register anything. They are simply the best free material
    available, and the club's weekly sessions will be built on them.</p></div>
  <div class="lnkgrid">
    <a class="lnk" href="https://code.org/" target="_blank" rel="noopener">{I_CODE} Code.org - full K&ndash;12 CS curriculum <span class="u">code.org</span></a>
    <a class="lnk" href="https://scratch.mit.edu/" target="_blank" rel="noopener">{I_PEN} MIT Scratch - block coding for juniors <span class="u">scratch.mit.edu</span></a>
    <a class="lnk" href="https://www.freecodecamp.org/" target="_blank" rel="noopener">{I_CODE} freeCodeCamp - web development, certified <span class="u">freecodecamp.org</span></a>
    <a class="lnk" href="https://cs50.harvard.edu/x/" target="_blank" rel="noopener">{I_BOOK} Harvard CS50x - introduction to CS <span class="u">cs50.harvard.edu</span></a>
    <a class="lnk" href="https://www.kaggle.com/learn" target="_blank" rel="noopener">{I_CHART} Kaggle Learn - Python, data, ML <span class="u">kaggle.com/learn</span></a>
    <a class="lnk" href="https://swayam.gov.in/" target="_blank" rel="noopener">{I_GLOBE} SWAYAM &amp; NPTEL - Govt. of India courses <span class="u">swayam.gov.in</span></a>
    <a class="lnk" href="https://skillsbuild.org/" target="_blank" rel="noopener">{I_SPARK} IBM SkillsBuild - free courses &amp; badges <span class="u">skillsbuild.org</span></a>
    <a class="lnk" href="https://www.arduino.cc/education" target="_blank" rel="noopener">{I_CHIP} Arduino Education - electronics projects <span class="u">arduino.cc/education</span></a>
    <a class="lnk" href="https://microbit.org/" target="_blank" rel="noopener">{I_CHIP} micro:bit - classroom hardware &amp; lessons <span class="u">microbit.org</span></a>
    <a class="lnk" href="https://www.tinkercad.com/" target="_blank" rel="noopener">{I_CHIP} Tinkercad - 3D design &amp; circuits in a browser <span class="u">tinkercad.com</span></a>
    <a class="lnk" href="https://classroom.github.com/" target="_blank" rel="noopener">{I_GIT} GitHub Classroom - assignments &amp; auto-grading <span class="u">classroom.github.com</span></a>
    <a class="lnk" href="https://cbseacademic.nic.in/" target="_blank" rel="noopener">{I_BOOK} CBSE Academic - AI &amp; IT skill syllabi <span class="u">cbseacademic.nic.in</span></a>
  </div>
</div></section>

<section class="anchor rv" id="ai"><div class="wrap">
  <div class="shead"><h2>AI tools - what is actually available to us in India</h2>
    <p>This is the section most often exaggerated online, so it is written carefully.</p></div>
  <div class="grid g2">
    <div class="card gr"><div class="ic">{I_BOOK}</div><h3>Available to us, free, today</h3>
      <ul class="ck" style="margin-bottom:0">
        <li><a href="https://academy.openai.com/" target="_blank" rel="noopener"><strong>OpenAI Academy</strong></a>
       - free AI-literacy courses worldwide, including a K&ndash;12 educator track.</li>
        <li><strong>Free tiers of ChatGPT, Google Gemini and Microsoft Copilot</strong> for supervised
          classroom demonstration, with a teacher present.</li>
        <li><a href="https://learn.microsoft.com/en-us/training/" target="_blank" rel="noopener"><strong>Microsoft Learn AI paths</strong></a>
          and <a href="https://www.kaggle.com/learn" target="_blank" rel="noopener"><strong>Kaggle Learn</strong></a>
       - free, structured, certificate-bearing.</li>
        <li><strong>CBSE's own AI skill-subject material</strong>, which the club will use to support
          classroom teaching.</li>
      </ul></div>
    <div class="card am"><div class="ic">{I_LOCK}</div><h3>Not available to us - stated plainly</h3>
      <ul class="ar" style="margin-bottom:0">
        <li><strong>OpenAI's free <em>ChatGPT for Teachers</em> plan is United States only.</strong> It is
          genuinely free for verified U.S. K&ndash;12 educators, but it is not offered to Indian schools
          at present.</li>
        <li><strong>Most headline &ldquo;free AI for students&rdquo; offers require the user to be 18 or above</strong>
          and are aimed at college students, not school students.
          <a href="https://gemini.google/students/" target="_blank" rel="noopener">Google's student offers</a>
          change periodically - always read the current eligibility.</li>
        <li><strong>ChatGPT Edu is an institutional, paid licence</strong> aimed at universities and large
          districts, not at individual schools.</li>
      </ul></div>
  </div>
  <div class="note">
    <h4>How the club will actually use AI</h4>
    <p>The club teaches students to <strong>understand</strong> AI: what these systems are, where they get
    things wrong, how to check them, and why handing in their output as your own work is dishonest. All of it
    is supervised, on approved free plans. Under the club's rules, submitting AI work without saying so is
    treated as copying. That rule is written into the
    <a href="join.html#conduct">code of conduct</a> every member signs.</p>
  </div>
</div></section>

<section class="anchor rv" id="govt"><div class="wrap">
  <div class="shead"><h2>Schemes the school itself can apply for</h2></div>
  <div class="grid g2">
    <div class="card vi"><div class="ic">{I_CHIP}</div><h3>Atal Tinkering Laboratory - up to &#8377;20 lakh</h3>
      <p>Under the Atal Innovation Mission, NITI Aayog, a selected school receives grant-in-aid of
      <strong>&#8377;10 lakh</strong> to establish the laboratory (3D printer, robotics and electronics kits,
      sensors, microcontrollers, tools) and a further <strong>&#8377;10 lakh</strong> towards operating
      expenses over five years.</p>
      <p><small>Open to schools with Classes VI&ndash;XII that can spare the built-up space AIM asks for.
      Applications open in announced windows - watch the portal.</small></p>
      <div class="tags"><a class="pill p-v" href="https://aim.gov.in/atl.php" target="_blank" rel="noopener">aim.gov.in/atl.php &rarr;</a></div></div>
    <div class="card"><div class="ic">{I_GLOBE}</div><h3>ERNET India - optional academic domain</h3>
      <p>ERNET India, an autonomous society under the Ministry of Electronics and IT, is the
      <strong>exclusive registrar</strong> for <span class="mono">.edu.in</span>,
      <span class="mono">.ac.in</span>, <span class="mono">.res.in</span> and
      <span class="mono">.school.in</span>. A CBSE-affiliated school is directly eligible.</p>
      <p><small><strong>We do not need this.</strong> The school already owns
      <span class="mono">mapleskhatauli.com</span>, which every programme here accepts. A
      <span class="mono">.edu.in</span> address is a credibility upgrade to consider later, at roughly
      &#8377;1,180 a year.</small></p>
      <div class="tags"><a class="pill p-c" href="https://registry.ernet.in/guidelines" target="_blank" rel="noopener">registry.ernet.in &rarr;</a></div></div>
  </div>
</div></section>

<section class="anchor rv" id="worth" style="padding-top:12px"><div class="wrap">
  <div class="band">
    <h2>All of the above, for <span class="grad">&#8377;0 a year</span></h2>
    <p class="lead" style="margin:0 auto">The school already owns
    <span class="mono">mapleskhatauli.com</span>, so there is no domain to buy and no yearly fee to find.
    Every software licence on this page is offered free to verified schools, with no obligation to
    upgrade and no contract committing the school to future payment. The only priced row in the table
    above is the optional <span class="mono">.edu.in</span> address, which nothing else depends on.</p>
    <div class="btns">
      <a class="btn btn-p" href="registration.html">How registration works &rarr;</a>
      <a class="btn btn-s" href="{PDF}" download>{I_DOWN} Download the proposal</a>
    </div>
  </div>
</div></section>
"""

# ══════════════════════════════════════════════════════════════════ 4. REGISTRATION
registration = f"""
<section class="hero" style="padding-bottom:26px"><div class="wrap">
  <span class="eyebrow">{I_GLOBE} Registration roadmap</span>
  <h1>How Maples Academy gets <span class="grad">registered</span></h1>
  <p class="lead">Eight phases, in order. Google, Microsoft and GitHub all verify a school through its
  <strong>domain name</strong> - and the school already owns one, so the part that normally costs
  money and takes weeks is done. Each phase is small, and the school may halt after any phase without
  loss.</p>
  <div class="tocbar">
    <a href="#domain">0&ndash;1. Our domain</a><a href="#google">2&ndash;3. Google</a>
    <a href="#microsoft">4. Microsoft</a><a href="#github">5. GitHub</a>
    <a href="#rest">6&ndash;7. The rest</a><a href="#docs">Document checklist</a>
    <a href="#optional">Optional .edu.in</a><a href="#cost">Total cost</a>
  </div>
</div></section>

<section class="anchor rv" style="padding-top:8px"><div class="wrap">
  <div class="note vi">
    <h4>Read this first</h4>
    <p>Almost every free education programme in the world verifies a school the same way: it looks for an
    <strong>institutional email address on a domain the school owns</strong>. Maples Academy already owns
    <span class="mono">mapleskhatauli.com</span>. Nothing has to be bought and nothing has to be renewed.
    What remains is to prove to Google that the domain belongs to a recognised school, and then to set up
    the Admin Console. After that the rest is form-filling.</p>
  </div>
</div></section>

<section class="anchor rv" id="domain" style="padding-top:10px"><div class="wrap">
  <figure class="fig" style="margin:0 0 34px">
    <img loading="lazy" src="assets/desk-admin.jpg" width="1376" height="768"
         alt="A school office desk with an open laptop, a tied bundle of paper files, spectacles
         and a tumbler of tea.">
    <figcaption>Most of this is paperwork done once. After that the accounts simply exist.</figcaption>
  </figure>
  <div class="shead"><h2>Activate the domain we <span class="grad">already own</span></h2>
    <p>The school owns <span class="mono">mapleskhatauli.com</span>. Google does not care what the
    suffix is. It cares that the school controls the domain and that the school is a recognised
    educational institution. Both are true today.</p></div>
  <div class="split">
    <div>
      <div class="steps">
        <div class="step"><div class="num">0</div><h4>The Principal names two teachers</h4>
          <p>A <strong>Faculty Advisor</strong> to supervise the club's sessions, and a
          <strong>Coordinator</strong> to hold the Google Admin Console and act as the school's verified
          contact. These may be the same person. A line in writing from the Principal is enough.</p></div>
        <div class="step"><div class="num">1</div><h4>Find out who controls the domain</h4>
          <p>Somebody bought <span class="mono">mapleskhatauli.com</span> and somebody renews it. The
          school office, or whoever built the present website, will have that login.
          <strong>This is the one thing to confirm before anything else starts.</strong></p></div>
        <div class="step"><div class="num">2</div><h4>Check whether email already runs on it</h4>
          <p>If the school already receives mail at an address ending in
          <span class="mono">@mapleskhatauli.com</span>, say so during the Google sign-up so the existing
          mail is not interrupted. If there is no email on the domain yet, Google simply becomes the
          school's mail provider. Either way it works - the office just has to tell the Coordinator
          which it is.</p></div>
        <div class="step"><div class="num">3</div><h4>Add Google's verification record</h4>
          <p>Google supplies a short TXT record. It is pasted into the domain's DNS settings through the
          same login found in step&nbsp;1. The existing website keeps working exactly as before; a
          verification record changes nothing a visitor can see.</p></div>
      </div>
    </div>
    <div class="hpanel">
      <div class="kicker">At a glance</div>
      <div class="row"><span>Domain</span><span class="mono">mapleskhatauli.com</span></div>
      <div class="row"><span>Already owned</span><span class="free">Yes</span></div>
      <div class="row"><span>Cost to activate</span><span class="free">&#8377;0</span></div>
      <div class="row"><span>Typical time</span><span>1 &ndash; 2 days</span></div>
      <div class="row"><span>Who does it</span><span>Coordinator,<br>helped by the club</span></div>
      <div class="row"><span>Existing website</span><span class="free">Unaffected</span></div>
      <div class="row"><span>Needed from the office</span><span>The domain login</span></div>
      <p style="margin:14px 0 0"><a class="btn btn-s" style="width:100%;justify-content:center"
        href="https://support.google.com/a/answer/60216" target="_blank" rel="noopener">How Google verifies &rarr;</a></p>
    </div>
  </div>
  <div class="note warn" style="margin-top:24px">
    <h4>What the school office must confirm first</h4>
    <p>This proposal cannot tell you two things from outside, and both should be checked before the
    Coordinator begins. <strong>One:</strong> who holds the account that
    <span class="mono">mapleskhatauli.com</span> was registered through, and whether the renewal is paid
    up. <strong>Two:</strong> whether any email is already running on that domain, because the sign-up
    asks. Neither answer blocks the plan. They only decide which path the Coordinator takes on the
    sign-up form, and five minutes with the school's records should settle both.</p>
  </div>
</div></section>

<section class="anchor rv" id="docs"><div class="wrap">
  <div class="shead"><h2>Documents to keep ready</h2>
    <p>Google, Microsoft and GitHub all ask for roughly the same proof that we are a real school. Scan
    these once, as PDFs under 2&nbsp;MB each, and the same folder serves every application.</p></div>
  <div class="grid g2">
    <div class="card"><div class="ic">{I_DOC}</div><h3>From the Principal</h3>
      <ul class="ck" style="margin-bottom:0">
        <li><strong>A line in writing from the Principal</strong> naming the Faculty Advisor and the
          Coordinator.</li>
        <li><strong>A letter on school letterhead</strong> confirming that the Coordinator is authorised
          to act for the school online. Google and Microsoft occasionally ask for this.</li>
        <li><strong>The login for the domain account</strong>, or somebody from the office available to
          add the verification record on the Coordinator's instruction.</li>
        <li><strong>Teacher identity proof</strong> - an identity card or an employment letter.
          GitHub and Canva both ask a teacher to prove employment.</li>
      </ul></div>
    <div class="card gr"><div class="ic">{I_SHIELD}</div><h3>Proof of the school's standing</h3>
      <ul class="ck" style="margin-bottom:0">
        <li><strong>Affiliation / approval / recognition letter</strong> from CBSE, ICSE, a State Board or
          other recognised authority.</li>
        <li><strong>Registration certificate</strong> establishing the legal constitution of the school or
          of its parent society or trust.</li>
        <li><strong>Address proof</strong> issued by a Government authority, and the school's telephone
          number and student and staff strength.</li>
        <li><strong>GST certificate</strong>, only if the school has one. None of the free programmes
          here require it.</li>
      </ul></div>
  </div>
  <p style="margin-top:14px;font-size:14px;color:var(--tx3)">No stamp paper, no posted originals and no
  fee are involved in any of this. Those belong only to the optional
  <a href="#optional"><span class="mono">.edu.in</span> route</a> described further down.</p>
</div></section>

<div class="wrap"><div class="hr"></div></div>

<section class="anchor rv" id="google" style="padding-top:0"><div class="wrap">
  <div class="shead"><h2>Google Workspace for Education, and the Admin Console</h2></div>
  <div class="split">
    <div>
      <ol class="no">
        <li><strong>Open the Education Fundamentals sign-up</strong> and start an application as the school's
          administrator. Supply the school's name, type, website, student and staff numbers, address,
          telephone and a contact email that is <em>not</em> on the new domain.</li>
        <li><strong>Enter <span class="mono">mapleskhatauli.com</span></strong> and prove ownership by
          adding the verification record Google provides to the domain's DNS settings.</li>
        <li><strong>Upload the accreditation document</strong> - the CBSE or Board affiliation
          certificate - when Google asks for evidence of educational status.</li>
        <li><strong>Wait for review.</strong> Google assesses eligibility; applications are typically decided
          within a couple of weeks.</li>
        <li><strong>Set up the Google Admin Console.</strong> This is phase&nbsp;3 and it is the part that
          matters most. From the Console the Coordinator issues addresses in the form
          <span class="mono">name@mapleskhatauli.com</span>, groups users by class, sets the data privacy
          and content-filtering rules, and decides which Google apps each class may use. The Console stays
          the school's permanent control panel; the Principal and the Coordinator hold its passwords.</li>
        <li><strong>Open Google Classroom</strong> for each class, and the club will run a short session
          for teachers who want one.</li>
      </ol>
      <div class="lnkgrid">
        <a class="lnk" href="https://edu.google.com/workspace-for-education/editions/education-fundamentals/" target="_blank" rel="noopener">{I_CLOUD} Education Fundamentals <span class="u">edu.google.com</span></a>
        <a class="lnk" href="https://support.google.com/a/answer/134628" target="_blank" rel="noopener">{I_SHIELD} Who qualifies <span class="u">support.google.com</span></a>
      </div>
    </div>
    <div class="hpanel">
      <div class="kicker">What the school gets</div>
      <div class="row"><span>School Gmail on our domain</span><span class="free">Yes</span></div>
      <div class="row"><span>Google Classroom</span><span class="free">Yes</span></div>
      <div class="row"><span>Meet, Drive, Docs, Forms, Sites</span><span class="free">Yes</span></div>
      <div class="row"><span>Central Admin Console</span><span class="free">Yes</span></div>
      <div class="row"><span>Users</span><span>Unlimited</span></div>
      <div class="row"><span>Price</span><span class="free">&#8377;0</span></div>
    </div>
  </div>
</div></section>

<section class="anchor rv" id="microsoft"><div class="wrap">
  <div class="shead"><h2>Microsoft 365 Education (Office 365 A1)</h2></div>
  <div class="split">
    <div>
      <ol class="no">
        <li><strong>Begin the education sign-up</strong> on the Microsoft Education site using an address on
          the school domain.</li>
        <li><strong>Complete academic verification.</strong> If the domain is not automatically recognised,
          Microsoft asks for proof of the school's academic status - supply the affiliation
          certificate. Approval can take a few business days.</li>
        <li><strong>Assign the free A1 licences</strong> from the Microsoft 365 admin centre:
          <em>Users &rarr; Active users &rarr; Assign licences</em>. There is no cap on the number of staff
          and student licences.</li>
        <li><strong>Set up Teams</strong> for classes and staff, and enable OneDrive for each user.</li>
      </ol>
      <div class="note warn">
        <p><strong>Two practical cautions.</strong> The free A1 tier gives <em>web and mobile</em> Office
        apps - installable desktop Word and Excel require the paid A3 tier. And if Microsoft asks for
        a card during sign-up as an anti-abuse check, the A1 tier itself still remains free; read each
        screen carefully before confirming anything.</p>
      </div>
      <div class="lnkgrid">
        <a class="lnk" href="https://www.microsoft.com/en-in/education/products/office" target="_blank" rel="noopener">{I_MAIL} Microsoft 365 Education <span class="u">microsoft.com</span></a>
        <a class="lnk" href="https://learn.microsoft.com/en-us/microsoft-365/education/deploy/office-365-education-self-sign-up" target="_blank" rel="noopener">{I_DOC} Self-sign-up guide <span class="u">learn.microsoft.com</span></a>
      </div>
    </div>
    <div class="hpanel">
      <div class="kicker">What the school gets</div>
      <div class="row"><span>Word, Excel, PowerPoint (web)</span><span class="free">Yes</span></div>
      <div class="row"><span>Microsoft Teams for classes</span><span class="free">Yes</span></div>
      <div class="row"><span>OneDrive per user</span><span class="free">1 TB</span></div>
      <div class="row"><span>SharePoint &amp; School Data Sync</span><span class="free">Yes</span></div>
      <div class="row"><span>Desktop Office apps</span><span class="paid">A3 tier only</span></div>
      <div class="row"><span>Price of A1</span><span class="free">&#8377;0</span></div>
    </div>
  </div>
</div></section>

<section class="anchor rv" id="github"><div class="wrap">
  <div class="shead"><h2>GitHub Education</h2>
    <p>Two separate applications: one by the teacher, one by each student.</p></div>
  <div class="grid g2">
    <div class="card"><div class="ic">{I_USERS}</div><h3>The Coordinator applies as a teacher</h3>
      <ol class="no" style="margin-bottom:0">
        <li>Create a personal GitHub account.</li>
        <li>Go to <em>Settings &rarr; Billing &amp; plans &rarr; Education benefits</em> and start an
          application as a <strong>Teacher</strong>.</li>
        <li>Select the school, allow the location prompt, and upload a photograph of the faculty identity
          card or an employment verification letter, using the school email address.</li>
        <li>On approval, open <a href="https://classroom.github.com/" target="_blank" rel="noopener">GitHub
          Classroom</a> and claim the <a href="https://education.github.com/toolbox" target="_blank" rel="noopener">Teacher Toolbox</a>.</li>
      </ol></div>
    <div class="card vi"><div class="ic">{I_GIT}</div><h3>Each student applies for the Student Pack</h3>
      <ol class="no" style="margin-bottom:0">
        <li>Be <strong>13 or older</strong> and hold a personal GitHub account (organisation accounts do
          not qualify).</li>
        <li>Apply at <a href="https://education.github.com/pack" target="_blank" rel="noopener">education.github.com/pack</a>
          and choose <em>I am a student</em>.</li>
        <li>Verify with the school email address <em>or</em> upload a dated school identity card, class
          schedule or enrolment letter.</li>
        <li>Decisions usually arrive within a few days. Verification is re-checked periodically, and
          individual partner offers renew on their own schedules.</li>
      </ol></div>
  </div>
  <div class="note">
    <p><strong>Tip that prevents most rejections:</strong> when asked for the institution, match the exact
    spelling used in GitHub's school list, and make sure the identity card photograph clearly shows the
    student's name, the school's name and a date.</p>
  </div>
</div></section>

<section class="anchor rv" id="rest"><div class="wrap">
  <div class="shead"><h2>Finishing the job</h2></div>
  <div class="grid g3">
    <div class="card am"><div class="ic">{I_PEN}</div><h3>6. Canva &amp; the rest</h3>
      <p>The Coordinator verifies as a K&ndash;12 educator at
      <a href="https://www.canva.com/education/" target="_blank" rel="noopener">canva.com/education</a> and
      creates classes to bring students in. Students separately claim
      <a href="https://www.figma.com/education/" target="_blank" rel="noopener">Figma</a>,
      <a href="https://www.jetbrains.com/community/education/" target="_blank" rel="noopener">JetBrains</a> and
      <a href="https://www.notion.com/product/notion-for-education" target="_blank" rel="noopener">Notion</a>
      with their new school email.</p></div>
    <div class="card"><div class="ic">{I_GLOBE}</div><h3>7. Refresh the school website</h3>
      <p>The Web squad maintains the official Maples Academy site on
      <span class="mono">mapleskhatauli.com</span>, hosted free on
      <a href="https://pages.github.com/" target="_blank" rel="noopener">GitHub Pages</a> if the school
      wishes to move it. All content and photographs are approved by the school before publication.</p></div>
    <div class="card gr"><div class="ic">{I_CHIP}</div><h3>Optional - Atal Tinkering Lab</h3>
      <p>When the Atal Innovation Mission next opens applications, the school management applies for the
      grant of up to <strong>&#8377;20 lakh</strong>. Watch
      <a href="https://aim.gov.in/atl.php" target="_blank" rel="noopener">aim.gov.in</a> for the window; the
      club will prepare the supporting material.</p></div>
  </div>
</div></section>

<section class="anchor rv" id="optional"><div class="wrap">
  <div class="shead"><h2>Would a <span class="grad">.edu.in</span> address be better?</h2>
    <p>This is the one question worth answering properly, because an earlier draft of this proposal was
    built around it.</p></div>
  <div class="split">
    <div>
      <p>ERNET India, an autonomous society under the Ministry of Electronics and Information Technology,
      is the <strong>exclusive registrar</strong> for <span class="mono">.edu.in</span>,
      <span class="mono">.ac.in</span>, <span class="mono">.res.in</span> and
      <span class="mono">.school.in</span>. A CBSE-affiliated school is directly eligible, and an address
      ending in <span class="mono">.edu.in</span> carries visible academic standing in India.</p>
      <p><strong>But the school does not need it.</strong> Google, Microsoft, GitHub, Canva, Figma,
      JetBrains and Notion all verify a school by checking that it controls its domain and is a recognised
      institution. None of them require a particular suffix.
      <span class="mono">mapleskhatauli.com</span> satisfies every one of them, today, at no cost.</p>
      <p>So the honest recommendation is this. Activate what the school already owns first. Get the
      accounts running, let a year pass, and see whether anyone misses the
      <span class="mono">.edu.in</span>. If the school then decides it wants that standing, the route is
      below and the earlier work is not wasted - a second domain can be added to the same Google
      Workspace without rebuilding anything.</p>
      <div class="steps" style="margin-top:18px">
        <div class="step"><div class="num">1</div><h4>Check availability</h4>
          <p>Search the name on the ERNET registry. It must match the school's full name or a recognisable
          abbreviation. Generic names and personal names are refused, and it must not resemble any
          Government body's name.</p></div>
        <div class="step"><div class="num">2</div><h4>Prepare the papers</h4>
          <p>An application letter on school letterhead and an undertaking on <strong>&#8377;100
          non-judicial stamp paper</strong>, both in ERNET's own format, signed and stamped by the Head of
          the Institution, plus the appointment letter of the administrative contact, the affiliation
          letter, the registration certificate of the school or its society, and a Government address
          proof. All as PDFs under 2&nbsp;MB.</p></div>
        <div class="step"><div class="num">3</div><h4>Apply, pay and post</h4>
          <p>Complete the online form and pay by card, net banking, NEFT or UPI. Demand drafts are no
          longer accepted. True copies of the stamped undertaking and the application letter go by post to
          ERNET India, New Delhi.</p></div>
        <div class="step"><div class="num">4</div><h4>Await manual verification</h4>
          <p>ERNET reviews the documents by hand. Allow two to four weeks. Renewal needs fresh documents,
          so keep copies of everything.</p></div>
      </div>
    </div>
    <div class="hpanel">
      <div class="kicker">If the school ever wants it</div>
      <div class="row"><span>Registrar</span><span>ERNET India (MeitY)</span></div>
      <div class="row"><span>Suffixes available</span><span>.edu.in &middot; .ac.in<br>.res.in &middot; .school.in</span></div>
      <div class="row"><span>Who is eligible</span><span>CBSE / ICSE / State Board<br>affiliated schools</span></div>
      <div class="row"><span>Indicative fee</span><span class="paid">&asymp; &#8377;1,180 / year<br><small>cheaper multi-year</small></span></div>
      <div class="row"><span>Stamp paper</span><span>&#8377;100 non-judicial</span></div>
      <div class="row"><span>Typical time</span><span>2 &ndash; 4 weeks</span></div>
      <div class="row"><span>Needed for this plan</span><span class="free">No</span></div>
      <p style="margin:14px 0 0"><a class="btn btn-s" style="width:100%;justify-content:center"
        href="https://registry.ernet.in/guidelines" target="_blank" rel="noopener">Official ERNET guidelines &rarr;</a></p>
    </div>
  </div>
  <div class="note warn" style="margin-top:24px">
    <h4>Fees change - confirm before paying</h4>
    <p>Published ERNET tariffs have varied over the years and differ between sources. The figure quoted
    here (&asymp;&nbsp;&#8377;1,180 for one year, inclusive of GST) is indicative only.
    <strong>Please confirm the current tariff on the ERNET portal at the time of applying</strong>, and
    note that registering several years at once reduces the yearly cost. A restoration fee applies if a
    domain is allowed to lapse. None of this affects the main plan, which costs nothing.</p>
  </div>
</div></section>

<section class="anchor rv" id="cost"><div class="wrap">
  <div class="shead"><h2>Sequence, owners, time and cost</h2></div>
  <div class="tw"><table>
    <thead><tr><th style="width:60px">Phase</th><th style="width:28%">Action</th><th style="width:22%">Owner</th>
      <th style="width:110px">Time</th><th>Cost</th></tr></thead>
    <tbody>
      <tr><td><strong>0</strong></td><td><strong>Permission</strong> - Principal approves the club and names the Faculty Advisor and the Coordinator</td><td>Principal</td><td>1 week</td><td class="free">Nil</td></tr>
      <tr><td><strong>1</strong></td><td><strong>Prove we own <span class="mono">mapleskhatauli.com</span></strong> by adding Google's verification record</td><td>Coordinator, with the club</td><td>1&ndash;2 days</td><td class="free">Nil</td></tr>
      <tr><td><strong>2</strong></td><td><strong>Verify our eligibility with Google</strong> - Education Fundamentals sign-up</td><td>Coordinator</td><td>2 weeks</td><td class="free">FREE</td></tr>
      <tr><td><strong>3</strong></td><td><strong>Set up the Google Admin Console</strong> - accounts, groups, privacy, app access</td><td>Coordinator, with the club</td><td>1 week</td><td class="free">FREE</td></tr>
      <tr><td><strong>4</strong></td><td><strong>Microsoft 365 Education</strong> A1 licences</td><td>Coordinator</td><td>1&ndash;2 weeks</td><td class="free">FREE</td></tr>
      <tr><td><strong>5</strong></td><td><strong>GitHub Education</strong> - teacher, then students</td><td>Coordinator, then members</td><td>1 week</td><td class="free">FREE</td></tr>
      <tr><td><strong>6</strong></td><td><strong>Canva, Figma, JetBrains, Notion</strong> and other verified programmes</td><td>Coordinator</td><td>1 week</td><td class="free">FREE</td></tr>
      <tr><td><strong>7</strong></td><td><strong>School website</strong> maintained on our own domain</td><td>Club, supervised</td><td>3&ndash;4 weeks</td><td class="free">FREE</td></tr>
      <tr><td><strong> - </strong></td><td><em>Optional later:</em> a <span class="mono">.edu.in</span> address from ERNET India, or an Atal Tinkering Lab grant</td><td>School management</td><td>Later</td><td class="paid">&asymp; &#8377;1,180 / yr<br><small>only if chosen</small></td></tr>
    </tbody></table></div>
  <div class="note good" style="margin-top:22px">
    <h4>Total compulsory cost to the school</h4>
    <p><strong>&#8377;0. Nothing, in the first year or any year after.</strong> The domain is already the
    school's, and every programme above is free to verified schools. An optional consumables budget of
    &#8377;3,000&ndash;&#8377;6,000 a year is proposed for the electronics squad, and the club will function
    without it if the school prefers. There is no compulsory expenditure anywhere in this plan.</p>
  </div>
  <div class="btns">
    <a class="btn btn-p" href="{PDF}" download>{I_DOWN} Download the proposal</a>
    <a class="btn btn-s" href="proposal.html">What we are asking &rarr;</a>
  </div>
</div></section>
"""

# ══════════════════════════════════════════════════════════════════ 5. JOIN
join = f"""
<section class="hero" style="padding-bottom:26px"><div class="wrap">
  <span class="eyebrow">{I_USERS} Membership</span>
  <h1>Joining the <span class="grad">Maples Tech Club</span></h1>
  <p class="lead">The club has two doors, and that is deliberate. Some selection is needed to keep project
  teams small enough to actually teach. But selection must never turn into a way of keeping students out of
  learning, so one of the two doors has no selection at all.</p>
  <div class="tocbar">
    <a href="#doors">Two tracks</a><a href="#stages">How to get in</a><a href="#founding">First intake</a>
    <a href="#principles">Fairness rules</a><a href="#renewal">Staying a member</a>
    <a href="#conduct">Code of conduct</a><a href="#roles">Roles</a>
  </div>
</div></section>

<section class="anchor rv" id="doors" style="padding-top:10px"><div class="wrap">
  <div class="grid g2">
    <div class="card gr"><div class="ic">{I_USERS}</div>
      <h3>Open Track: no selection at all</h3>
      <p>Any student of Classes VI to XII can attend the club's open workshops, awareness sessions, guest
      talks, exhibition days and competitions. <strong>No test, no form, no previous knowledge and no limit
      on numbers.</strong></p>
      <p>This is how most of the school will meet the club, and it is the club's main job.</p>
      <div class="tags"><span class="pill p-g">Always open</span><span class="pill p-g">No fee</span>
        <span class="pill p-g">Classes VI&ndash;XII</span></div></div>
    <div class="card vi"><div class="ic">{I_TROPHY}</div>
      <h3>Core Track: selected membership</h3>
      <p>A limited number of students are taken into the six squads each year. They get regular guidance,
      laboratory time for their projects, team work and the chance to represent the school outside.</p>
      <p>In return they accept rules about attendance, conduct and teaching juniors.</p>
      <div class="tags"><span class="pill p-v">Annual intake, April</span>
        <span class="pill p-v">Mid-year intake, October</span><span class="pill p-v">No fee</span></div></div>
  </div>
</div></section>

<section class="anchor rv" id="stages"><div class="wrap">
  <div class="shead">
  <h2>An online test, then <span class="grad">one project</span>.</h2>
    <p>Two steps and that is all. No form to buy, no interview panel, no probation period and no fee.
    The test paper is the same for everybody and is marked automatically, so there is no question of
    favouritism. The project can be anything you like.</p></div>
  <div class="split">
    <div>
      <div class="steps">
        <div class="step"><div class="num">0</div><h4>Give your name to your class teacher</h4>
          <p>That is all the application there is. No form, no fee, nothing to prepare. Any student of
          Classes VI to XII may sit the test.</p></div>
        <div class="step"><div class="num">1</div><h4>The online test - 25 questions, 30 minutes</h4>
          <p>A Google Form you can open on a phone or on a laboratory computer. Objective questions only.
          <strong>Basic technical skills</strong>: simple logic and patterns, elementary computer awareness,
          reading instructions correctly and ordinary arithmetic.
          <strong>No programming is required and none is assumed.</strong> Marked
          <strong>class-wise</strong>, so a junior is never compared with a senior.</p>
          <div class="tags"><span class="pill p-c">Weight: 40%</span>
            <span class="pill p-c">Judged on: clear thinking, not knowledge</span></div></div>
        <div class="step"><div class="num">2</div><h4>A project - make anything you like</h4>
          <p>Everyone who clears the test makes <strong>one thing of their own choosing</strong>. There is
          no list and no fixed subject. A poster, a web page, a game, a working circuit, a short film, a
          model, a spreadsheet that actually does something, a piece of writing about technology
       - whatever you want. One week. Hand it in with a few lines saying what it is and what went
          wrong while you were making it. <strong>Beginners' attempts are expected and welcome.</strong></p>
          <div class="tags"><span class="pill p-v">Weight: 60%</span>
            <span class="pill p-v">Judged on: effort and finishing it, not polish</span></div></div>
        <figure class="fig" style="margin:30px 0 34px">
    <img loading="lazy" src="assets/project-bench.jpg" width="1376" height="768"
         alt="A student's hands wiring a small breadboard circuit with a lit LED, next to a
         notebook of handwritten diagrams.">
    <figcaption>A first attempt is a pass. The project is marked on effort and on finishing it.</figcaption>
  </figure>
  <div class="step"><div class="num">3</div><h4>Results on the notice board</h4>
          <p>If you are not selected you remain a full Open Track member, can attend every workshop the
          club holds, and may try again at the next intake.</p></div>
      </div>
      <div class="note vi" style="margin-top:20px">
        <h4>Who runs this first test</h4>
        <p>Before the club exists there is nobody in it to run an intake. So this first selection is
        conducted by <strong>Harsh, on behalf of the School Coordinator</strong>, under whatever
        supervision the Principal directs, and every paper stays open to the school. Once the club is
        working, selection passes to its elected President and Core Committee.</p>
      </div>
    </div>
    <div class="hpanel">
      <div class="kicker">Selection at a glance</div>
      <div class="row"><span>Step 1 - test</span><span>25 questions &middot; 30 min</span></div>
      <div class="row"><span>Format</span><span>Online - Google Form</span></div>
      <div class="row"><span>Coding needed</span><span class="free">None</span></div>
      <div class="row"><span>Step 2 - project</span><span>Anything you like</span></div>
      <div class="row"><span>Time for the project</span><span>One week</span></div>
      <div class="row"><span>Weights</span><span>40% test &middot; 60% project</span></div>
      <div class="row"><span>Open to</span><span>Classes VI &ndash; XII</span></div>
      <div class="row"><span>Fee</span><span class="free">&#8377;0</span></div>
    </div>
  </div>
</div></section>

<section class="anchor rv" id="founding"><div class="wrap">
  <div class="shead"><h2>The club starts with <span class="grad">four to six students</span></h2></div>
  <div class="grid g2">
    <div class="card vi"><div class="ic">{I_USERS}</div><h3>Who sets it up</h3>
      <p>A club cannot be built by a crowd on the first day. It begins with <strong>Harsh</strong>,
      his friend <strong>Vidhan</strong> - both Class XII - and two to four other students
      taken from the top of the selection. Four to six in all.</p>
      <p>They set up the accounts, write the first sessions and get the weekly routine working.</p>
      <p><strong>Both founders leave at the end of this session</strong>, which is exactly why the
      remaining founding places are asked for students of <strong>Classes VIII to X</strong>. They are
      the ones who will actually run it.</p></div>
    <div class="card gr"><div class="ic">{I_TROPHY}</div><h3>Then it opens to everyone</h3>
      <p>Once the routine is running, the club opens to the whole school and fills up in the ordinary
      way, with the <strong>40% junior reservation</strong> applying from that point onwards.</p>
      <p>From then on the club is run by its elected <strong>President</strong> and Core Committee, not
      by its founder.</p></div>
  </div>
</div></section>

<section class="anchor rv" id="principles"><div class="wrap">
  <div class="shead"><h2>Rules that bind the selection</h2></div>
  <div class="grid g2">
    <div class="card gr"><div class="ic">{I_SHIELD}</div><h3>Access</h3>
      <ul class="ck" style="margin-bottom:0">
        <li><strong>No fee of any kind</strong> to apply or to be a member.</li>
        <li><strong>Previous experience is not a condition.</strong> A complete beginner who finishes a
          simple task will be placed above an experienced student who submits nothing.</li>
        <li><strong>Marks are not a condition either.</strong> What matters is whether a student can keep up
          with the club without their studies suffering.</li>
        <li><strong>Not being selected does not mean being shut out.</strong> A student who is not taken into
          the Core Track stays a full Open Track member and can attend every workshop the club holds.</li>
      </ul></div>
    <div class="card vi"><div class="ic">{I_USERS}</div><h3>Balance and transparency</h3>
      <ul class="ck" style="margin-bottom:0">
        <li><strong>At least 40% of the places go to Classes VI&ndash;IX</strong>, so the club keeps
          renewing itself.</li>
        <li>The club will <strong>make a point of encouraging girl students to apply</strong>, and will aim
          for a balanced group.</li>
        <li><strong>Everything is put up in advance.</strong> Any student who is not selected will be told,
          if they ask, what would make their next application stronger.</li>
        <li><strong>The Faculty Advisor can overrule</strong> any selection or removal decision, and the
          Principal's decision is final.</li>
      </ul></div>
  </div>
</div></section>

<section class="anchor rv" id="renewal"><div class="wrap">
  <div class="shead"><h2>Staying a member</h2></div>
  <div class="grid g3">
    <div class="card"><div class="ic">{I_USERS}</div><h4>Attendance</h4>
      <p>Not less than <strong>70%</strong> of sessions in the term.</p></div>
    <div class="card"><div class="ic">{I_CODE}</div><h4>Term project</h4>
      <p>One finished, written-up project each term, however small.</p></div>
    <div class="card"><div class="ic">{I_SHIELD}</div><h4>Conduct</h4>
      <p>Satisfactory conduct under the code of conduct below.</p></div>
  </div>
  <div class="note warn">
    <p><strong>Removal.</strong> The Faculty Advisor may remove a member for indiscipline, for misusing
    school equipment or the internet, for copying, or for breaking the code of conduct. In every such case
    the student is heard first, and the matter is reported to the Principal.</p>
  </div>
</div></section>

<section class="anchor rv" id="conduct"><div class="wrap">
  <div class="shead"><h2>Code of Conduct</h2>
    <p>Every member signs this when they join. The Faculty Advisor keeps the
    signed copy.</p></div>
  <div class="tw"><table>
    <thead><tr><th>I, a member of the Maples Tech Club, undertake that - </th></tr></thead>
    <tbody>
      <tr><td><strong>1. My studies come first.</strong> I will not allow club work to affect my attendance,
        homework or examinations, and I accept that the Faculty Advisor may keep me out of the club at any
        time if my marks start falling.</td></tr>
      <tr><td><strong>2. I will respect school property.</strong> I will use the computer laboratory, its
        machines, the internet connection and all equipment carefully, only for club purposes, only during
        permitted hours, and never without a teacher present.</td></tr>
      <tr><td><strong>3. I will be honest in my work.</strong> I will not copy another person's work and
        present it as mine. Where I use code, images, designs or text made by somebody else, including
        anything produced by an artificial intelligence tool, I will say so clearly. I understand that
        handing in AI output as my own work counts as copying.</td></tr>
      <tr><td><strong>4. I will keep the school safe online.</strong> I will not share my school account
        password, will not attempt to access any account or system that is not mine, will not install
        unapproved software, and will not visit or share inappropriate, pirated or unlawful material.</td></tr>
      <tr><td><strong>5. I will publish nothing in the school's name without approval.</strong> No website
        change, notice, poster, photograph, video or social media post representing Maples Academy will be
        go out from me without the Faculty Advisor approving it in writing first.</td></tr>
      <tr><td><strong>6. I will protect others' privacy.</strong> I will not photograph, record or publish any
        student or teacher without their knowledge and consent, and I will not share anyone's personal
        data.</td></tr>
      <tr><td><strong>7. I will teach what I learn.</strong> I will help juniors and new members willingly,
        and I will not mock or discourage a beginner. Every member of this club started by knowing
        nothing.</td></tr>
      <tr><td><strong>8. I will conduct myself with courtesy</strong> towards teachers, staff, visitors and
        fellow students, in the club and when representing the school outside it.</td></tr>
      <tr><td><strong>9. I accept the authority of the Faculty Advisor and the Principal</strong> in all
        matters concerning the club. I understand that breaking this undertaking can mean removal from the
        club, and action under the school's normal disciplinary rules.</td></tr>
    </tbody></table></div>
</div></section>

<section class="anchor rv" id="roles"><div class="wrap">
  <div class="shead"><h2>Core Committee roles, elected each year in Term IV</h2></div>
  <div class="grid g3">
    <div class="card"><h4>President</h4><p><small>Class XI&ndash;XII. Chairs meetings, owns the annual plan,
      reports monthly to the Faculty Advisor.</small></p></div>
    <div class="card"><h4>Vice-President</h4><p><small>Deputises for the President, owns the weekly session
      schedule and the induction of new members.</small></p></div>
    <div class="card"><h4>Secretary</h4><p><small>Keeps the attendance register, minutes and all club
      records; drafts correspondence for the Advisor's signature.</small></p></div>
    <div class="card"><h4>Technical Lead</h4><p><small>Owns the school website, the club's repositories and
      the technical quality of all projects.</small></p></div>
    <div class="card"><h4>Design &amp; Media Lead</h4><p><small>Owns posters, the club's visual identity,
      photography and video for school events.</small></p></div>
    <div class="card"><h4>Outreach Lead</h4><p><small>Handles competitions, external entries, guest speakers
      and communication with feeder schools.</small></p></div>
  </div>
  <div class="note good">
    <h4>Not yet sanctioned</h4>
    <p>The Maples Tech Club is a <strong>proposal</strong> awaiting the Principal's approval. There is no
    intake open at present. Once sanction is granted, the Open Call notice will go up on the school board and
    the first intake will begin in Term I.</p>
  </div>
  <div class="btns">
    <a class="btn btn-p" href="{PDF}" download>{I_DOWN} Download the proposal</a>
    <a class="btn btn-s" href="about.html">Read the club charter &rarr;</a>
  </div>
</div></section>
"""

# ══════════════════════════════════════════════════════════════════ 6. PROPOSAL
proposal = f"""
<section class="hero" style="padding-bottom:22px"><div class="wrap">
  <div class="split mid">
    <div>
      <span class="eyebrow">{I_DOC} For the Principal</span>
      <h1>The application, <span class="grad">in summary</span></h1>
      <p class="lead">Respected Sir, this page is a short summary of a formal application submitted
      by Harsh, Class XII, Roll No. 13, asking for permission to start the Maples Tech Club and to begin the
      school's technology registrations. The full {NP}-page document, with all five annexures, can be
      downloaded below. Nothing in it is fixed - it is written out in full so that there is something
      definite to correct.</p>
      <div class="btns">
        <a class="btn btn-p" href="{PDF}" download>{I_DOWN} Download the proposal</a>
        <a class="btn btn-s" href="registration.html">How registration works &rarr;</a>
      </div>
    </div>
    <div class="hpanel">
      <div class="kicker">What is being asked for</div>
      <div class="row"><span>Permission to form the club</span><span class="free">Nil cost</span></div>
      <div class="row"><span>One Faculty Advisor</span><span class="free">Nil cost</span></div>
      <div class="row"><span>One Coordinator <small>(may be the same teacher)</small></span><span class="free">Nil cost</span></div>
      <div class="row"><span>Computer lab, 2 hrs / week</span><span class="free">Nil cost</span></div>
      <div class="row"><span>Signatures on the sign-up forms</span><span class="free">Nil cost</span></div>
      <div class="row"><span>Domain to buy</span><span class="free">None - already owned</span></div>
      <div class="row"><span>Consumables (optional)</span><span class="paid">&#8377;3,000&ndash;6,000 / yr</span></div>
      <div class="row"><span>Notice board space</span><span class="free">Nil cost</span></div>
    </div>
  </div>
</div></section>

<section class="anchor rv" style="padding-top:8px"><div class="wrap">
  <div class="note vi">
    <h4>The essence of the request</h4>
    <p>The school is not being asked to spend money. Not one rupee. Maples Academy already owns
    <span class="mono">mapleskhatauli.com</span>, so there is no domain to buy, and every programme in
    this proposal is free to verified schools. What is being asked for is <strong>permission</strong>,
    <strong>one teacher as Faculty Advisor</strong> to supervise the sessions, <strong>one teacher as
    Coordinator</strong> to hold the Google Admin Console, and the computer laboratory for
    <strong>two hours a week</strong>.</p>
  </div>
</div></section>

<section class="rv"><div class="wrap">
  <div class="shead"><h2>What the school's IT administration has to do</h2>
    <p>Two steps, and the club will do the legwork for both under the Coordinator's supervision.</p></div>
  <div class="grid g2">
    <div class="card gr"><div class="ic">{I_SHIELD}</div><h3>1. Verify our educational eligibility with Google</h3>
      <p>Using the school's official domain, <span class="mono">mapleskhatauli.com</span>. Google needs
      two things: proof that the school controls the domain, which is a short record added to the DNS
      settings, and proof that Maples Academy is a recognised educational institution, which is the CBSE
      affiliation certificate. Once that is accepted, the school is on record with Google as a school and
      the free education editions become available.</p></div>
    <div class="card"><div class="ic">{I_CLOUD}</div><h3>2. Set up the Google Admin Console</h3>
      <p>This is the school's permanent control panel. From it the Coordinator creates and closes student
      and teacher accounts, organises users by class, sets the data privacy and content-filtering rules,
      and decides which apps each class is allowed to use. The Principal and the Coordinator hold the
      passwords. No student is ever given administrator rights.</p></div>
  </div>
  <div class="note warn">
    <h4>Two things the school office should confirm first</h4>
    <p>Who holds the account that <span class="mono">mapleskhatauli.com</span> was registered through, and
    whether any email is already running on that domain. If email already exists there, it is declared
    during the sign-up and carries on working. If it does not, Google simply becomes the school's mail
    provider. Either way the plan is the same. The office only has to tell the Coordinator which case
    applies.</p>
  </div>
</div></section>

<section class="rv"><div class="wrap">
  <div class="shead"><h2>Every reasonable objection, answered</h2>
    <p>These are the questions any principal would ask. They are answered here rather than dodged.</p></div>
  <div class="tw"><table>
    <thead><tr><th style="width:27%">Concern</th><th>Safeguard offered</th></tr></thead>
    <tbody>
      <tr><td><strong>Will studies suffer?</strong></td>
        <td>One session a week, after school hours. <strong>Nothing at all in the four weeks before any
        examination</strong>, or during the board examinations. If a member's marks fall, the Faculty Advisor
        keeps them out until they recover.</td></tr>
      <tr><td><strong>Who controls the accounts and the data?</strong></td>
        <td><strong>The school does.</strong> The school owns the domain and every account made under it. The
        administrator passwords stay with the Coordinator and the Principal. No student gets administrator
        rights. Accounts are switched off when a student leaves. Google Workspace for Education and Microsoft 365
        Education are built for exactly this kind of control, through a single admin console.</td></tr>
      <tr><td><strong>Will students misuse internet access?</strong></td>
        <td>The laboratory is never used without a teacher present. Every member signs the code of conduct, and
        Content filtering is switched on at administrator level for all school
        accounts. Anything that goes wrong is reported to the Principal the same day.</td></tr>
      <tr><td><strong>Is the school's reputation at risk online?</strong></td>
        <td>Nothing goes out in the school's name without the Faculty Advisor approving it in writing first.
        That covers the website, notices, posters, photographs and social media. Photographs of students are only
        put up with their consent.</td></tr>
      <tr><td><strong>What happens when the founder leaves after Class XII?</strong></td>
        <td>The structure is built against exactly that. Every squad has a junior deputy. The Core Committee is
        elected fresh every year. All records, passwords and files are handed to the Faculty Advisor before the
        outgoing batch leaves, and 40% of every intake is kept for Classes VI&ndash;IX.</td></tr>
      <tr><td><strong>What if the Faculty Advisor or the Coordinator leaves the school?</strong></td>
        <td>This is the more serious risk of the two, because the accounts are in a teacher's name. Three
        things protect against it. The <strong>Principal holds the administrator passwords jointly with the
        Coordinator</strong>, so access is never lost with one person. The accounts belong to the school's
        domain, not to any individual, so a new teacher is simply made administrator in the same console.
        And a written handover of passwords, records and files is required before either teacher is
        relieved, exactly as it is for the outgoing students.</td></tr>
      <tr><td><strong>Will this cost the school money later?</strong></td>
        <td>The free plans named here are these companies' standing education offers. There is no obligation to
        upgrade to a paid plan, and the school can stop using any of them whenever it wants. <strong>No contract
        ties the school to paying anything later.</strong></td></tr>
      <tr><td><strong>Is AI use appropriate for school students?</strong></td>
        <td>The club teaches students to <em>understand</em> AI: what these systems are, where they get things
        wrong, how to check them, and why handing in their output as your own work is dishonest. All of it is
        supervised, on approved free plans, and submitting AI work without saying so is treated as copying.</td></tr>
    </tbody></table></div>
</div></section>

<section class="rv"><div class="wrap">
  <div class="shead"><h2>Judge us against this, after one year</h2>
    <p>I am asking for the club to be checked against these after twelve months, and closed without any
    argument from me if it has clearly not met them.</p></div>
  <div class="tw"><table>
    <thead><tr><th>By the end of Year One</th><th style="width:130px">Target</th></tr></thead>
    <tbody>
      <tr><td><span class="mono">mapleskhatauli.com</span> verified with Google and school accounts live</td><td class="free">Yes</td></tr>
      <tr><td>Official school email accounts issued to teachers and to Classes IX&ndash;XII</td><td class="free">100%</td></tr>
      <tr><td>Google Workspace for Education and Microsoft 365 Education active</td><td class="free">Both</td></tr>
      <tr><td>Official school website live, built and maintained by students</td><td class="free">Yes</td></tr>
      <tr><td>Students attending at least one club session</td><td class="free">150 +</td></tr>
      <tr><td>Core members with a completed, documented project</td><td class="free">40 +</td></tr>
      <tr><td>Workshops and awareness sessions conducted</td><td class="free">20 +</td></tr>
      <tr><td>External competitions or olympiads entered</td><td class="free">3 +</td></tr>
      <tr><td>Teachers trained in Google Classroom or Microsoft Teams</td><td class="free">10 +</td></tr>
      <tr><td>Public technology exhibition for parents and the community</td><td class="free">1</td></tr>
      <tr><td>Licence cost to the school for all software obtained</td><td class="free">&#8377;0</td></tr>
    </tbody></table></div>
</div></section>

<section class="rv"><div class="wrap">
  <div class="shead"><h2>What is inside the PDF</h2></div>
  <div class="grid g3">
    <div class="card"><div class="ic">{I_DOC}</div><h4>The application letter</h4>
      <p><small>A formal letter to the Principal setting out the two-part request and the reasoning behind
      it, with space for the proposer's and faculty advisor's signatures.</small></p></div>
    <div class="card vi"><div class="ic">{I_USERS}</div><h4>Annexure A - Club Charter</h4>
      <p><small>Identity, definition, vision and mission, the nine objectives, the seven-tier structure,
      the six squads, the annual calendar and the examination-discipline rule.</small></p></div>
    <div class="card gr"><div class="ic">{I_SPARK}</div><h4>Annexure B - Schedule of Benefits</h4>
      <p><small>Every institutional and student benefit, with eligibility, cost and the provider's official
      web address for independent verification - including a frank note on what is <em>not</em>
      available in India.</small></p></div>
    <div class="card am"><div class="ic">{I_GLOBE}</div><h4>Annexure C - Registration Roadmap</h4>
      <p><small>Eight phases starting from the domain the school already owns, with the documents needed,
      the owner of each step, realistic timings and the total cost.</small></p></div>
    <div class="card"><div class="ic">{I_TROPHY}</div><h4>Annexure D - Selection &amp; Conduct</h4>
      <p><small>The two membership tracks, the online test and the project, the founding group, the fairness
      principles, renewal and removal rules, and the nine-point code of conduct for signature.</small></p></div>
    <div class="card gr"><div class="ic">{I_SHIELD}</div><h4>Annexure E - Safeguards &amp; Targets</h4>
      <p><small>Answers to every foreseeable concern, including what happens if a teacher leaves, the
      precise list of what is requested from the school, and the one-year target sheet the club asks to be
      judged against.</small></p></div>
  </div>
</div></section>

<section class="rv" style="padding-top:12px"><div class="wrap">
  <div class="band">
    <h2>{NP} pages. Print it, read it, mark it up.</h2>
    <p class="lead" style="margin:0 auto">A4, laid out for printing. Nothing in it is fixed: the name, the
    timings, the number of members, the way they are selected, the posts and the rules may all be changed
    or struck out as the Principal thinks proper.</p>
    <div class="btns">
      <a class="btn btn-p" href="{PDF}" download>{I_DOWN} Maples_Tech_Club_Proposal_Principal.pdf</a>
      <a class="btn btn-s" href="benefits.html">Verify every claim &rarr;</a>
    </div>
    <p style="margin-top:20px;font-size:14.5px;color:var(--tx3)">
      &ldquo;Every school in the country is being told to go digital. Most are waiting for someone to give
      them the means to do it. Maples Academy does not have to wait. It already qualifies for all of this,
      and it has students who are willing to do the work. I am asking for permission, one teacher, and two
      hours a week.&rdquo;<br>
      <strong style="color:var(--tx2)">Harsh, Class XII, Roll No. 13</strong></p>
  </div>
</div></section>
"""

# ══════════════════════════════════════════════════════════════════ write
built = [
    page("index.html", "Home",
         "The Maples Tech Club - a proposed student technology society at Maples Academy, Khatauli, "
         "and a plan to get free Google, Microsoft and GitHub education programmes for the school.", home),
    page("about.html", "The Club",
         "Full charter of the Maples Tech Club: definition, purpose, vision and mission, structure, the six "
         "domain squads and the annual calendar.", about),
    page("benefits.html", "Benefits",
         "Every free education benefit Maples Academy and its students are eligible for - Google Workspace "
         "for Education, Microsoft 365 A1, GitHub Education, Canva, Figma and more, with official links.", benefits),
    page("registration.html", "Registration",
         "Step-by-step roadmap to register Maples Academy using the domain it already owns: Google "
         "Workspace for Education and the Admin Console, Microsoft 365 Education, GitHub Education - "
         "with documents, timings and costs.", registration),
    page("join.html", "Join Us",
         "How to join the Maples Tech Club: the open track, the 25-question online test and project, fairness "
         "rules and the member code of conduct.", join),
    page("proposal.html", "For the Principal",
         "Summary of the formal application to the Principal of Maples Academy, Khatauli, with safeguards, "
         f"costs, one-year targets and a downloadable {NP}-page PDF.", proposal),
]

# Netlify (and GitHub Pages) serve this for any address that does not exist.
# It is not in PAGES, so it never appears in the navigation.
notfound = """
<section class="hero"><div class="wrap" style="text-align:center;padding:90px 0 70px">
  <div class="kicker" style="justify-content:center">Error 404</div>
  <h1 style="margin:14px 0 18px">That page is not here.</h1>
  <p class="lead" style="max-width:620px;margin:0 auto 34px">
    The link may be mistyped, or it may point at something that has since been renamed.
    Everything about the club is reachable from the pages below.</p>
  <div class="btns" style="justify-content:center">
    <a class="btn b1" href="/index.html">Home page</a>
    <a class="btn b2" href="/join.html">How to join</a>
    <a class="btn b2" href="/proposal.html">For the Principal</a>
  </div>
</div></section>"""

page("404.html", "Page not found",
     "That page does not exist on the Maples Tech Club site.", notfound)

# A 404 can be served at any depth, so relative links in it would break.
_p404 = os.path.join(OUT, "404.html")
with open(_p404, encoding="utf-8") as f:
    _h = f.read()
if "<base " not in _h:
    _h = _h.replace("<head>", '<head>\n<base href="/">', 1)
    with open(_p404, "w", encoding="utf-8") as f:
        f.write(_h)

# Netlify reads _headers and _redirects from inside the published folder. They
# are written here rather than in netlify.toml because netlify.toml only
# applies to Git-connected and CLI deploys - a folder dropped on
# app.netlify.com/drop would silently lose every rule. These files travel with
# the folder, so all three routes behave the same. GitHub Pages ignores them.
HEADERS = """# Generated by build_site.py - do not edit by hand.

/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: SAMEORIGIN
  Referrer-Policy: strict-origin-when-cross-origin

# The Principal should get the proposal in his browser's PDF viewer, not as a
# mystery file in his downloads folder.
/Maples_Tech_Club_Proposal_Principal.pdf
  Content-Type: application/pdf
  Content-Disposition: inline; filename="Maples Tech Club - Proposal.pdf"
  Cache-Control: public, max-age=0, must-revalidate

# Rebuilt every deploy, so never serve a stale copy.
/*.html
  Cache-Control: public, max-age=0, must-revalidate
"""

REDIRECTS = """# Generated by build_site.py - do not edit by hand.

# Extensionless URLs, so a link written either way reaches the same page.
/about          /about.html          200
/benefits       /benefits.html       200
/registration   /registration.html   200
/join           /join.html           200
/proposal       /proposal.html       200

# Short links that are easy to write on a notice board or read out in assembly.
/pdf            /Maples_Tech_Club_Proposal_Principal.pdf   302
/apply          /join.html                                 302
"""

for _name, _text in (("_headers", HEADERS), ("_redirects", REDIRECTS)):
    with open(os.path.join(OUT, _name), "w", encoding="utf-8") as f:
        f.write(_text)

src = os.path.join(BASE, PDF)
if os.path.exists(src):
    shutil.copy(src, os.path.join(OUT, PDF))

for (f, _), n in zip(PAGES, built):
    print(f"  {f:22s} {n/1024:6.1f} KB")
print("\nsite ->", OUT)
