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
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#070b16; --bg2:#0b1224; --panel:#111a30; --panel2:#0e1628;
  --line:rgba(148,178,255,.15); --line2:rgba(148,178,255,.28);
  --tx:#e8eeff; --tx2:#a9b8dc; --tx3:#7488b3;
  --cy:#22d3ee; --vi:#a78bfa; --gr:#34d399; --am:#fbbf24; --rd:#fb7185;
  --grad:linear-gradient(135deg,#22d3ee 0%,#818cf8 50%,#a78bfa 100%);
  --r:16px; --rs:10px;
}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{
  background:var(--bg); color:var(--tx); line-height:1.68;
  font-family:'Segoe UI',-apple-system,BlinkMacSystemFont,Roboto,'Helvetica Neue',Arial,sans-serif;
  font-size:16px; overflow-x:hidden;
}
body::before{
  content:""; position:fixed; inset:0; z-index:-2; pointer-events:none;
  background:
    radial-gradient(900px 520px at 12% -8%, rgba(34,211,238,.16), transparent 62%),
    radial-gradient(820px 480px at 92% 4%, rgba(167,139,250,.15), transparent 60%),
    radial-gradient(700px 600px at 50% 108%, rgba(52,211,153,.08), transparent 60%);
}
body::after{
  content:""; position:fixed; inset:0; z-index:-1; pointer-events:none; opacity:.4;
  background-image:linear-gradient(rgba(148,178,255,.045) 1px,transparent 1px),
                   linear-gradient(90deg,rgba(148,178,255,.045) 1px,transparent 1px);
  background-size:56px 56px;
  mask-image:radial-gradient(ellipse 100% 70% at 50% 0%,#000 40%,transparent 100%);
  -webkit-mask-image:radial-gradient(ellipse 100% 70% at 50% 0%,#000 40%,transparent 100%);
}
a{color:var(--cy);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:1160px;margin:0 auto;padding:0 22px}

/* ── nav ── */
header.nav{position:sticky;top:0;z-index:60;backdrop-filter:blur(16px);
  -webkit-backdrop-filter:blur(16px);background:rgba(7,11,22,.82);
  border-bottom:1px solid var(--line)}
.navin{max-width:1160px;margin:0 auto;padding:11px 22px;display:flex;align-items:center;gap:14px}
.brand{display:flex;align-items:center;gap:11px;text-decoration:none;flex-shrink:0}
.brand:hover{text-decoration:none}
.logo{width:38px;height:38px;flex-shrink:0}
.bname{font-weight:800;font-size:16.5px;letter-spacing:-.3px;color:var(--tx);line-height:1.15}
.bsub{font-size:10.5px;color:var(--tx3);letter-spacing:1.3px;text-transform:uppercase;font-weight:600}
nav.links{margin-left:auto;display:flex;gap:3px;align-items:center;flex-wrap:wrap}
nav.links a{padding:8px 13px;border-radius:9px;font-size:14px;font-weight:600;
  color:var(--tx2);transition:.16s;white-space:nowrap}
nav.links a:hover{background:rgba(148,178,255,.09);color:var(--tx);text-decoration:none}
nav.links a.on{color:var(--tx);background:rgba(34,211,238,.13);
  box-shadow:inset 0 0 0 1px rgba(34,211,238,.3)}
nav.links a.cta{background:var(--grad);color:#050810;font-weight:800;margin-left:6px}
nav.links a.cta:hover{filter:brightness(1.1);text-decoration:none}
.burger{display:none;margin-left:auto;background:rgba(148,178,255,.1);border:1px solid var(--line2);
  color:var(--tx);width:40px;height:38px;border-radius:9px;font-size:18px;cursor:pointer;line-height:1}

/* ── sections ── */
section{padding:62px 0}
.hero{padding:76px 0 56px}
h1{font-size:clamp(31px,5.4vw,55px);line-height:1.08;font-weight:850;letter-spacing:-1.6px;
   margin-bottom:18px}
h2{font-size:clamp(23px,3.3vw,33px);line-height:1.2;font-weight:800;letter-spacing:-.8px;
   margin-bottom:12px}
h3{font-size:19px;font-weight:750;letter-spacing:-.3px;margin-bottom:8px}
h4{font-size:15.5px;font-weight:750;margin-bottom:6px}
p{color:var(--tx2);margin-bottom:13px}
.lead{font-size:18.5px;color:var(--tx2);max-width:74ch}
.grad{background:var(--grad);-webkit-background-clip:text;background-clip:text;
  -webkit-text-fill-color:transparent;color:transparent}
.eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:11.5px;font-weight:800;
  letter-spacing:1.9px;text-transform:uppercase;color:var(--cy);
  background:rgba(34,211,238,.1);border:1px solid rgba(34,211,238,.28);
  padding:6px 14px;border-radius:99px;margin-bottom:20px;line-height:1.5}
.shead{margin-bottom:30px;max-width:80ch}
.shead p{font-size:16.5px}
.kicker{font-size:11.5px;font-weight:800;letter-spacing:1.9px;text-transform:uppercase;
  color:var(--vi);margin-bottom:9px}

/* ── buttons ── */
.btns{display:flex;gap:12px;flex-wrap:wrap;margin-top:26px}
.btn{display:inline-flex;align-items:center;gap:9px;padding:13px 24px;border-radius:12px;
  font-weight:750;font-size:15px;transition:.18s;border:1px solid transparent;cursor:pointer}
.btn:hover{text-decoration:none;transform:translateY(-2px)}
.btn-p{background:var(--grad);color:#050810;box-shadow:0 10px 28px -10px rgba(34,211,238,.6)}
.btn-p:hover{box-shadow:0 16px 36px -10px rgba(34,211,238,.75)}
.btn-s{background:rgba(148,178,255,.07);color:var(--tx);border-color:var(--line2)}
.btn-s:hover{background:rgba(148,178,255,.13);border-color:var(--cy)}

/* ── cards / grid ── */
.grid{display:grid;gap:17px}
.g2{grid-template-columns:repeat(2,1fr)}
.g3{grid-template-columns:repeat(3,1fr)}
.g4{grid-template-columns:repeat(4,1fr)}
.card{background:linear-gradient(160deg,rgba(255,255,255,.045),rgba(255,255,255,.015));
  border:1px solid var(--line);border-radius:var(--r);padding:22px;transition:.2s}
.card:hover{border-color:var(--line2);transform:translateY(-3px);
  box-shadow:0 18px 44px -22px rgba(0,0,0,.85)}
.card p:last-child{margin-bottom:0}
.card .ic{width:42px;height:42px;border-radius:11px;display:grid;place-items:center;
  margin-bottom:13px;background:rgba(34,211,238,.12);border:1px solid rgba(34,211,238,.25)}
svg.i{width:18px;height:18px;flex:0 0 auto;display:inline-block;vertical-align:-3px;
  fill:none;stroke:currentColor;stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round}
.card .ic svg.i{width:21px;height:21px;stroke:var(--cy)}
.eyebrow svg.i{width:14px;height:14px;stroke:var(--cy)}
.btn svg.i{width:17px;height:17px}
.lnk svg.i{width:18px;height:18px;stroke:var(--cy)}
.card.vi .ic{background:rgba(167,139,250,.12);border-color:rgba(167,139,250,.25)}
.card.vi .ic svg.i{stroke:var(--vi)}
.card.gr .ic{background:rgba(52,211,153,.12);border-color:rgba(52,211,153,.25)}
.card.gr .ic svg.i{stroke:var(--gr)}
.card.am .ic{background:rgba(251,191,36,.12);border-color:rgba(251,191,36,.25)}
.card.am .ic svg.i{stroke:var(--am)}
.card small{color:var(--tx3);font-size:13.5px}

/* ── stats ── */
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:38px}
.stat{background:rgba(148,178,255,.05);border:1px solid var(--line);border-radius:var(--r);
  padding:19px;text-align:center}
.stat b{display:block;font-size:clamp(23px,3.4vw,31px);font-weight:850;letter-spacing:-1px;
  line-height:1.1;margin-bottom:3px}
.stat span{font-size:12.5px;color:var(--tx3);font-weight:600;line-height:1.35;display:block}

/* ── tables ── */
.tw{overflow-x:auto;border:1px solid var(--line);border-radius:var(--r);
  background:rgba(148,178,255,.028);-webkit-overflow-scrolling:touch}
table{width:100%;border-collapse:collapse;font-size:14.3px;min-width:640px}
thead th{background:rgba(34,211,238,.1);color:var(--tx);text-align:left;padding:13px 15px;
  font-weight:750;font-size:12.5px;letter-spacing:.7px;text-transform:uppercase;
  border-bottom:1px solid var(--line2);white-space:nowrap}
tbody td{padding:13px 15px;border-bottom:1px solid var(--line);color:var(--tx2);
  vertical-align:top}
tbody tr:last-child td{border-bottom:none}
tbody tr:hover td{background:rgba(148,178,255,.045)}
td strong,td b{color:var(--tx);font-weight:700}
.free{color:var(--gr);font-weight:800;white-space:nowrap}
.paid{color:var(--am);font-weight:800;white-space:nowrap}

/* ── pills / tags ── */
.pill{display:inline-block;padding:3px 10px;border-radius:99px;font-size:11.5px;font-weight:750;
  letter-spacing:.3px;white-space:nowrap}
.p-g{background:rgba(52,211,153,.14);color:var(--gr);border:1px solid rgba(52,211,153,.3)}
.p-c{background:rgba(34,211,238,.13);color:var(--cy);border:1px solid rgba(34,211,238,.3)}
.p-v{background:rgba(167,139,250,.14);color:var(--vi);border:1px solid rgba(167,139,250,.3)}
.p-a{background:rgba(251,191,36,.13);color:var(--am);border:1px solid rgba(251,191,36,.3)}
.p-r{background:rgba(251,113,133,.13);color:var(--rd);border:1px solid rgba(251,113,133,.3)}
.tags{display:flex;gap:7px;flex-wrap:wrap;margin-top:11px}

/* ── notes ── */
.note{border-left:3px solid var(--cy);background:rgba(34,211,238,.06);padding:16px 19px;
  border-radius:0 var(--rs) var(--rs) 0;margin:20px 0}
.note.warn{border-color:var(--am);background:rgba(251,191,36,.06)}
.note.good{border-color:var(--gr);background:rgba(52,211,153,.06)}
.note.vi{border-color:var(--vi);background:rgba(167,139,250,.06)}
.note h4{color:var(--tx)}
.note p:last-child{margin-bottom:0}
.note strong{color:var(--tx)}

/* ── steps / timeline ── */
.steps{position:relative;padding-left:40px;margin-top:8px}
.steps::before{content:"";position:absolute;left:14px;top:10px;bottom:10px;width:2px;
  background:linear-gradient(180deg,var(--cy),var(--vi),transparent)}
.step{position:relative;margin-bottom:26px}
.step:last-child{margin-bottom:0}
.step .num{position:absolute;left:-40px;top:0;width:30px;height:30px;border-radius:50%;
  background:var(--bg2);border:2px solid var(--cy);display:grid;place-items:center;
  font-weight:800;font-size:13px;color:var(--cy)}
.step h4{font-size:17px;margin-bottom:5px}
.step p{margin-bottom:7px;font-size:15px}

/* ── lists ── */
ul.ck{list-style:none;margin:10px 0}
ul.ck li{position:relative;padding-left:27px;margin-bottom:9px;color:var(--tx2)}
ul.ck li::before{content:"";position:absolute;left:0;top:9px;width:14px;height:8px;
  border-left:2.2px solid var(--gr);border-bottom:2.2px solid var(--gr);
  transform:rotate(-45deg)}
ul.ar{list-style:none;margin:10px 0}
ul.ar li{position:relative;padding-left:23px;margin-bottom:9px;color:var(--tx2)}
ul.ar li::before{content:"\203A";position:absolute;left:4px;top:-2px;color:var(--cy);
  font-size:20px;font-weight:800}
ul.ck li strong,ul.ar li strong{color:var(--tx)}
ol.no{counter-reset:n;list-style:none;margin:10px 0}
ol.no li{counter-increment:n;position:relative;padding-left:34px;margin-bottom:11px;color:var(--tx2)}
ol.no li::before{content:counter(n);position:absolute;left:0;top:2px;width:23px;height:23px;
  border-radius:7px;background:rgba(34,211,238,.13);border:1px solid rgba(34,211,238,.3);
  color:var(--cy);font-size:12.5px;font-weight:800;display:grid;place-items:center}
ol.no li strong{color:var(--tx)}

/* ── link rows ── */
.lnk{display:flex;align-items:center;gap:11px;padding:12px 15px;border-radius:var(--rs);
  background:rgba(148,178,255,.045);border:1px solid var(--line);transition:.16s;
  color:var(--tx2);font-size:14.5px;font-weight:600}
.lnk:hover{background:rgba(34,211,238,.09);border-color:rgba(34,211,238,.35);
  color:var(--tx);text-decoration:none;transform:translateX(3px)}
.lnk span.u{margin-left:auto;font-size:12px;color:var(--tx3);font-weight:500;
  font-family:ui-monospace,Menlo,Consolas,monospace}
.lnkgrid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-top:14px}

/* ── hero panel ── */
.hpanel{background:linear-gradient(160deg,rgba(34,211,238,.08),rgba(167,139,250,.05));
  border:1px solid var(--line2);border-radius:20px;padding:26px}
.hpanel .row{display:flex;justify-content:space-between;align-items:center;gap:12px;
  padding:11px 0;border-bottom:1px dashed var(--line)}
.hpanel .row:last-child{border-bottom:none}
.hpanel .row span:first-child{color:var(--tx2);font-size:14.5px}
.hpanel .row span:last-child{font-weight:800;font-size:14.5px;text-align:right}
.split{display:grid;grid-template-columns:1.15fr .85fr;gap:34px;align-items:start}
.split.mid{align-items:center}

/* ── cta band ── */
.band{background:linear-gradient(135deg,rgba(34,211,238,.1),rgba(167,139,250,.09));
  border:1px solid var(--line2);border-radius:20px;padding:36px;text-align:center;margin-top:8px}
.band h2{margin-bottom:10px}
.band .btns{justify-content:center}

/* ── footer ── */
footer{border-top:1px solid var(--line);margin-top:34px;padding:38px 0 30px;
  background:rgba(7,11,22,.6)}
.fgrid{display:grid;grid-template-columns:1.6fr 1fr 1fr 1fr;gap:26px;margin-bottom:26px}
footer h5{font-size:12px;letter-spacing:1.5px;text-transform:uppercase;color:var(--tx3);
  margin-bottom:11px;font-weight:800}
footer ul{list-style:none}
footer ul li{margin-bottom:7px}
footer ul li a{color:var(--tx2);font-size:14px}
footer ul li a:hover{color:var(--cy)}
.fbot{border-top:1px solid var(--line);padding-top:18px;display:flex;
  justify-content:space-between;gap:14px;flex-wrap:wrap;font-size:13px;color:var(--tx3)}
.disc{font-size:12.5px;color:var(--tx3);line-height:1.6;margin-top:14px;
  padding:13px 16px;background:rgba(148,178,255,.035);border:1px solid var(--line);
  border-radius:var(--rs)}

/* ── misc ── */
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13.5px;
  background:rgba(34,211,238,.09);padding:2px 5px;border-radius:5px;color:var(--cy)}
.hr{height:1px;background:var(--line);margin:44px 0}
.anchor{scroll-margin-top:86px}
.tocbar{display:flex;gap:8px;flex-wrap:wrap;margin:22px 0 4px}
.tocbar a{font-size:13.5px;font-weight:650;padding:7px 14px;border-radius:99px;
  background:rgba(148,178,255,.06);border:1px solid var(--line);color:var(--tx2)}
.tocbar a:hover{border-color:var(--cy);color:var(--tx);text-decoration:none}
.cent{text-align:center}

@media(max-width:940px){
  .g4{grid-template-columns:repeat(2,1fr)}
  .g3{grid-template-columns:repeat(2,1fr)}
  .split{grid-template-columns:1fr;gap:26px}
  .fgrid{grid-template-columns:1fr 1fr}
  .stats{grid-template-columns:repeat(2,1fr)}
}
@media(max-width:760px){
  .burger{display:block}
  nav.links{display:none;position:absolute;top:100%;left:0;right:0;flex-direction:column;
    align-items:stretch;gap:4px;padding:12px 18px 18px;background:rgba(9,14,28,.99);
    border-bottom:1px solid var(--line2)}
  nav.links.open{display:flex}
  nav.links a{padding:11px 14px}
  nav.links a.cta{margin-left:0;text-align:center}
  .g2,.g3,.g4{grid-template-columns:1fr}
  .lnkgrid{grid-template-columns:1fr}
  section{padding:46px 0}
  .hero{padding:48px 0 38px}
  .band{padding:26px 20px}
  .steps{padding-left:34px}
  .step .num{left:-34px;width:26px;height:26px;font-size:12px}
}
@media(max-width:480px){
  .stats{grid-template-columns:1fr 1fr}
  .fgrid{grid-template-columns:1fr}
  .btn{width:100%;justify-content:center}
  .pill{white-space:normal}
}
"""

LOGO = """<svg class="logo" viewBox="0 0 48 48" aria-hidden="true">
<defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#22d3ee"/><stop offset=".55" stop-color="#818cf8"/>
<stop offset="1" stop-color="#a78bfa"/></linearGradient></defs>
<rect x="2" y="2" width="44" height="44" rx="12" fill="url(#lg)" opacity=".16"/>
<rect x="2.9" y="2.9" width="42.2" height="42.2" rx="11.2" fill="none" stroke="url(#lg)" stroke-width="1.7"/>
<path d="M24 9c3.4 3.6 5.2 7.3 5.2 11 0 2.6-1 4.6-2.2 6.3l3.1 1.1-4 1.7 1 3.4-3.4-2-0.4 4.2h-1.6l-.4-4.2-3.4 2 1-3.4-4-1.7 3.1-1.1c-1.2-1.7-2.2-3.7-2.2-6.3 0-3.7 1.8-7.4 5.2-11z"
 fill="url(#lg)" opacity=".92"/>
<path d="M15.5 38.5h17" stroke="url(#lg)" stroke-width="2.1" stroke-linecap="round"/>
<circle cx="13.2" cy="21.5" r="1.7" fill="#22d3ee"/><circle cx="34.8" cy="21.5" r="1.7" fill="#a78bfa"/>
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
        Maples Academy, Khatauli, Uttar Pradesh &mdash; teaching computing, AI, robotics and design
        by building real things.</p>
        <p style="font-size:13.5px;color:var(--tx3);margin-top:8px">
        Motto &mdash; <em>Learn it. Build it. Ship it.</em></p>
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
<meta name="theme-color" content="#070b16">
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
      <span class="eyebrow">{I_SPARK} Proposed &middot; Session 2026&ndash;27</span>
      <h1>The <span class="grad">Maples Tech&nbsp;Club</span><br>at Maples Academy, Khatauli</h1>
      <p class="lead">A student-run technology club where members don't only study computers, they build
      things with them. Along with a plan to get hold of the free technology our school already
      qualifies for, at no cost at all: official school email on the domain we already own,
      Google Workspace for Education, Microsoft 365, GitHub and more.</p>
      <div class="btns">
        <a class="btn btn-p" href="{PDF}" download>{I_DOWN} Download the proposal (PDF)</a>
        <a class="btn btn-s" href="benefits.html">See every benefit &rarr;</a>
      </div>
    </div>
    <div class="hpanel">
      <div class="kicker">The proposal in numbers</div>
      <div class="row"><span>Cost to the school, per year</span><span class="free">&#8377;0</span></div>
      <div class="row"><span>Licence cost of all software</span><span class="free">&#8377;0</span></div>
      <div class="row"><span>Domain to buy</span><span class="free">None &mdash; already owned</span></div>
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

<section style="padding-top:8px"><div class="wrap">
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

<section class="anchor"><div class="wrap">
  <div class="shead">
    <div class="kicker">What the club does</div>
    <h2>Six squads. One rule: <span class="grad">finish something</span>.</h2>
    <p>Every member ends every term holding something they actually made &mdash; a working website, a
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
  <div class="btns"><a class="btn btn-s" href="about.html">Full club charter &rarr;</a></div>
</div></section>

<section><div class="wrap">
  <div class="shead">
    <div class="kicker">Why it matters</div>
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
      <p>A published project, a GitHub profile, a competition certificate &mdash; evidence a student
      can show to a college, a scholarship committee or an employer. Marks alone no longer
      distinguish anyone.</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="shead">
    <div class="kicker">Honesty first</div>
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
    CBSE school right now &mdash; and every claim links to the provider's own page so the school can
    verify it independently.</p>
  </div>
</div></section>

<section style="padding-top:12px"><div class="wrap">
  <div class="band">
    <span class="eyebrow">{I_DOC} For the Principal</span>
    <h2>A {NP}-page formal application, ready to print and sign</h2>
    <p class="lead" style="margin:0 auto">Complete with the club charter, a verified schedule of every
    benefit, the registration roadmap with documents and costs, the member selection process, the code
    of conduct, safeguards, a one-year target sheet, and an order sheet for the Principal's signature.</p>
    <div class="btns">
      <a class="btn btn-p" href="{PDF}" download>{I_DOWN} Download the PDF application</a>
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

<section class="anchor" id="definition" style="padding-top:20px"><div class="wrap">
  <div class="shead"><div class="kicker">01 &mdash; Definition</div>
    <h2>A workshop, not a lecture hall</h2></div>
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

<section class="anchor" id="purpose" style="padding-top:0"><div class="wrap">
  <div class="shead"><div class="kicker">02 &mdash; Purpose</div>
    <h2>The eight objectives</h2>
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
        licence cost &mdash; but only to registered institutions. The club does the registration and the upkeep.</td></tr>
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
      <tr><td><strong>7</strong></td><td><strong>Teach digital safety and AI ethics</strong></td>
        <td>Students already use AI and social media. Structured guidance on privacy, safe conduct online,
        misinformation and honesty in their work protects the school as much as it protects them.</td></tr>
      <tr><td><strong>8</strong></td><td><strong>Widen career horizons</strong></td>
        <td>Exposure to software, data, design and hardware careers &mdash; and to the free national learning
        platforms that teach them, aimed at students who would otherwise never hear of any of it.</td></tr>
    </tbody></table></div>
</div></section>

<section class="anchor" id="vision"><div class="wrap">
  <div class="shead"><div class="kicker">03 &mdash; Vision &amp; mission</div><h2>What we are aiming at</h2></div>
  <div class="note vi">
    <h4>Vision</h4>
    <p style="font-size:18px;color:var(--tx)">No student should leave Maples Academy having only
    <em>read</em> about technology. They should leave having <em>made</em> something with it.</p>
  </div>
  <h3 style="margin-top:26px;margin-bottom:6px">Mission &mdash; the club commits to:</h3>
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

<section class="anchor" id="structure" style="padding-top:0"><div class="wrap">
  <div class="shead"><div class="kicker">04 &mdash; Structure</div>
    <h2>Who answers to whom</h2>
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

<section class="anchor" id="squads"><div class="wrap">
  <div class="shead"><div class="kicker">05 &mdash; Squads</div>
    <h2>The six domain squads</h2>
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

<section class="anchor" id="calendar"><div class="wrap">
  <div class="shead"><div class="kicker">06 &mdash; Calendar</div><h2>How a year runs</h2></div>
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
        <td><strong>TechFest Maples</strong> &mdash; an open exhibition for parents and feeder schools</td></tr>
      <tr><td><strong>Term IV</strong></td><td>January &ndash; March</td>
        <td>Board-exam-light term: documentation, peer teaching, handover</td>
        <td>Annual report to the Principal; election of the next Core Committee</td></tr>
    </tbody></table></div>
</div></section>

<section class="anchor" id="discipline" style="padding-top:12px"><div class="wrap">
  <div class="note warn">
    <h4>Academic discipline &mdash; a binding rule of the club</h4>
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
  <h1>Everything our school and its students <span class="grad">can get free</span></h1>
  <p class="lead">Every entry below is a published programme of the named organisation, with its
  official link so the school can verify the claim independently. Nothing here requires Maples Academy
  to enter into a paid contract.</p>
  <div class="tocbar">
    <a href="#school">For the school</a><a href="#students">For students</a>
    <a href="#learn">Free learning</a><a href="#ai">AI tools</a><a href="#govt">Government schemes</a>
    <a href="#worth">What it is worth</a>
  </div>
</div></section>

<section class="anchor" id="school" style="padding-top:14px"><div class="wrap">
  <div class="shead"><div class="kicker">Institutional</div>
    <h2>What <span class="grad">Maples Academy</span> receives</h2>
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
    {row("GitHub Education &mdash; Teachers &amp; Schools",
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
         "students: premium templates, brand kit, background remover and classroom assignment tools &mdash; "
         "for school notices, the magazine and event design.",
         "Verified K&ndash;12 teachers and their schools. Students receive access through a "
         "teacher-created class; they cannot enrol independently.",
         "FREE")}
    {row("Optional later: a .edu.in address &mdash; ERNET India, MeitY, Govt. of India",
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
         "<a href='https://www.tinkercad.com/' target='_blank' rel='noopener'>Tinkercad</a> &mdash; free "
         "browser-based 3D design, circuit simulation and block coding, built for school classrooms.",
         "Students and educators at accredited institutions; Tinkercad classrooms are open to schools.",
         "FREE")}
    </tbody></table></div>
</div></section>

<section class="anchor" id="students"><div class="wrap">
  <div class="shead"><div class="kicker">Individual</div>
    <h2>What <span class="grad">Maples students</span> receive</h2>
    <p>These become available once the school email domain exists, because almost all of them verify
    eligibility through an institutional email address &mdash; though several also accept a photograph
    of a school identity card.</p></div>
  <div class="tw"><table>
    <thead><tr><th style="width:21%">Programme</th><th style="width:37%">What a student receives</th>
      <th style="width:26%">Eligibility</th><th style="width:16%">Cost</th></tr></thead>
    <tbody>
    {row("GitHub Student Developer Pack",
         "https://education.github.com/pack",
         "A large bundle of professional developer software, cloud credits, domain names and learning "
         "subscriptions contributed by dozens of technology companies &mdash; free for as long as the "
         "student's enrolment is verified.",
         "Aged <strong>13 or above</strong>, currently enrolled in a degree- or diploma-granting programme "
         "&mdash; <strong>which expressly includes school students</strong>. Verified by school email <em>or</em> "
         "a photograph of the school identity card.",
         "FREE")}
    {row("Figma for Education",
         "https://www.figma.com/education/",
         "Free access to Figma's paid design and prototyping platform, including FigJam whiteboards &mdash; "
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
         "The Notion Plus plan free for individual students and teachers &mdash; notes, project planning, "
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

<section class="anchor" id="learn"><div class="wrap">
  <div class="shead"><div class="kicker">Open learning</div>
    <h2>Free curricula the club will teach from</h2>
    <p>None of these require the school to register anything. They are simply the best free material
    available, and the club's weekly sessions will be built on them.</p></div>
  <div class="lnkgrid">
    <a class="lnk" href="https://code.org/" target="_blank" rel="noopener">{I_CODE} Code.org &mdash; full K&ndash;12 CS curriculum <span class="u">code.org</span></a>
    <a class="lnk" href="https://scratch.mit.edu/" target="_blank" rel="noopener">{I_PEN} MIT Scratch &mdash; block coding for juniors <span class="u">scratch.mit.edu</span></a>
    <a class="lnk" href="https://www.freecodecamp.org/" target="_blank" rel="noopener">{I_CODE} freeCodeCamp &mdash; web development, certified <span class="u">freecodecamp.org</span></a>
    <a class="lnk" href="https://cs50.harvard.edu/x/" target="_blank" rel="noopener">{I_BOOK} Harvard CS50x &mdash; introduction to CS <span class="u">cs50.harvard.edu</span></a>
    <a class="lnk" href="https://www.kaggle.com/learn" target="_blank" rel="noopener">{I_CHART} Kaggle Learn &mdash; Python, data, ML <span class="u">kaggle.com/learn</span></a>
    <a class="lnk" href="https://swayam.gov.in/" target="_blank" rel="noopener">{I_GLOBE} SWAYAM &amp; NPTEL &mdash; Govt. of India courses <span class="u">swayam.gov.in</span></a>
    <a class="lnk" href="https://skillsbuild.org/" target="_blank" rel="noopener">{I_SPARK} IBM SkillsBuild &mdash; free courses &amp; badges <span class="u">skillsbuild.org</span></a>
    <a class="lnk" href="https://www.arduino.cc/education" target="_blank" rel="noopener">{I_CHIP} Arduino Education &mdash; electronics projects <span class="u">arduino.cc/education</span></a>
    <a class="lnk" href="https://microbit.org/" target="_blank" rel="noopener">{I_CHIP} micro:bit &mdash; classroom hardware &amp; lessons <span class="u">microbit.org</span></a>
    <a class="lnk" href="https://www.tinkercad.com/" target="_blank" rel="noopener">{I_CHIP} Tinkercad &mdash; 3D design &amp; circuits in a browser <span class="u">tinkercad.com</span></a>
    <a class="lnk" href="https://classroom.github.com/" target="_blank" rel="noopener">{I_GIT} GitHub Classroom &mdash; assignments &amp; auto-grading <span class="u">classroom.github.com</span></a>
    <a class="lnk" href="https://cbseacademic.nic.in/" target="_blank" rel="noopener">{I_BOOK} CBSE Academic &mdash; AI &amp; IT skill syllabi <span class="u">cbseacademic.nic.in</span></a>
  </div>
</div></section>

<section class="anchor" id="ai"><div class="wrap">
  <div class="shead"><div class="kicker">Artificial intelligence</div>
    <h2>AI tools &mdash; what is actually available to us in India</h2>
    <p>This is the section most often exaggerated online, so it is written carefully.</p></div>
  <div class="grid g2">
    <div class="card gr"><div class="ic">{I_BOOK}</div><h3>Available to us, free, today</h3>
      <ul class="ck" style="margin-bottom:0">
        <li><a href="https://academy.openai.com/" target="_blank" rel="noopener"><strong>OpenAI Academy</strong></a>
          &mdash; free AI-literacy courses worldwide, including a K&ndash;12 educator track.</li>
        <li><strong>Free tiers of ChatGPT, Google Gemini and Microsoft Copilot</strong> for supervised
          classroom demonstration, with a teacher present.</li>
        <li><a href="https://learn.microsoft.com/en-us/training/" target="_blank" rel="noopener"><strong>Microsoft Learn AI paths</strong></a>
          and <a href="https://www.kaggle.com/learn" target="_blank" rel="noopener"><strong>Kaggle Learn</strong></a>
          &mdash; free, structured, certificate-bearing.</li>
        <li><strong>CBSE's own AI skill-subject material</strong>, which the club will use to support
          classroom teaching.</li>
      </ul></div>
    <div class="card am"><div class="ic">{I_LOCK}</div><h3>Not available to us &mdash; stated plainly</h3>
      <ul class="ar" style="margin-bottom:0">
        <li><strong>OpenAI's free <em>ChatGPT for Teachers</em> plan is United States only.</strong> It is
          genuinely free for verified U.S. K&ndash;12 educators, but it is not offered to Indian schools
          at present.</li>
        <li><strong>Most headline &ldquo;free AI for students&rdquo; offers require the user to be 18 or above</strong>
          and are aimed at college students, not school students.
          <a href="https://gemini.google/students/" target="_blank" rel="noopener">Google's student offers</a>
          change periodically &mdash; always read the current eligibility.</li>
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

<section class="anchor" id="govt"><div class="wrap">
  <div class="shead"><div class="kicker">Government of India</div>
    <h2>Schemes the school itself can apply for</h2></div>
  <div class="grid g2">
    <div class="card vi"><div class="ic">{I_CHIP}</div><h3>Atal Tinkering Laboratory &mdash; up to &#8377;20 lakh</h3>
      <p>Under the Atal Innovation Mission, NITI Aayog, a selected school receives grant-in-aid of
      <strong>&#8377;10 lakh</strong> to establish the laboratory (3D printer, robotics and electronics kits,
      sensors, microcontrollers, tools) and a further <strong>&#8377;10 lakh</strong> towards operating
      expenses over five years.</p>
      <p><small>Open to schools with Classes VI&ndash;XII that can spare the built-up space AIM asks for.
      Applications open in announced windows &mdash; watch the portal.</small></p>
      <div class="tags"><a class="pill p-v" href="https://aim.gov.in/atl.php" target="_blank" rel="noopener">aim.gov.in/atl.php &rarr;</a></div></div>
    <div class="card"><div class="ic">{I_GLOBE}</div><h3>ERNET India &mdash; optional academic domain</h3>
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

<section class="anchor" id="worth" style="padding-top:12px"><div class="wrap">
  <div class="band">
    <span class="eyebrow">{I_RUPEE} The bottom line</span>
    <h2>All of the above, for <span class="grad">&#8377;0 a year</span></h2>
    <p class="lead" style="margin:0 auto">The school already owns
    <span class="mono">mapleskhatauli.com</span>, so there is no domain to buy and no yearly fee to find.
    Every software licence on this page is offered free to verified schools, with no obligation to
    upgrade and no contract committing the school to future payment. The only priced row in the table
    above is the optional <span class="mono">.edu.in</span> address, which nothing else depends on.</p>
    <div class="btns">
      <a class="btn btn-p" href="registration.html">See the registration roadmap &rarr;</a>
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
  <strong>domain name</strong> &mdash; and the school already owns one, so the part that normally costs
  money and takes weeks is done. Each phase is small, and the school may halt after any phase without
  loss.</p>
  <div class="tocbar">
    <a href="#domain">0&ndash;1. Our domain</a><a href="#google">2&ndash;3. Google</a>
    <a href="#microsoft">4. Microsoft</a><a href="#github">5. GitHub</a>
    <a href="#rest">6&ndash;7. The rest</a><a href="#docs">Document checklist</a>
    <a href="#optional">Optional .edu.in</a><a href="#cost">Total cost</a>
  </div>
</div></section>

<section class="anchor" style="padding-top:8px"><div class="wrap">
  <div class="note vi">
    <h4>Read this first</h4>
    <p>Almost every free education programme in the world verifies a school the same way: it looks for an
    <strong>institutional email address on a domain the school owns</strong>. Maples Academy already owns
    <span class="mono">mapleskhatauli.com</span>. Nothing has to be bought and nothing has to be renewed.
    What remains is to prove to Google that the domain belongs to a recognised school, and then to set up
    the Admin Console. After that the rest is form-filling.</p>
  </div>
</div></section>

<section class="anchor" id="domain" style="padding-top:10px"><div class="wrap">
  <div class="shead"><div class="kicker">Phases 0&ndash;1 &mdash; the keystone</div>
    <h2>Activate the domain we <span class="grad">already own</span></h2>
    <p>The school owns <span class="mono">mapleskhatauli.com</span>. Google does not care what the
    suffix is. It cares that the school controls the domain and that the school is a recognised
    educational institution. Both are true today.</p></div>
  <div class="split">
    <div>
      <div class="steps">
        <div class="step"><div class="num">0</div><h4>The Principal names two teachers</h4>
          <p>A <strong>Faculty Advisor</strong> to supervise the club's sessions, and a
          <strong>Coordinator</strong> to hold the Google Admin Console and act as the school's verified
          contact. These may be the same person. Annexure F of the proposal is a ready order sheet.</p></div>
        <div class="step"><div class="num">1</div><h4>Find out who controls the domain</h4>
          <p>Somebody bought <span class="mono">mapleskhatauli.com</span> and somebody renews it. The
          school office, or whoever built the present website, will have that login.
          <strong>This is the one thing to confirm before anything else starts.</strong></p></div>
        <div class="step"><div class="num">2</div><h4>Check whether email already runs on it</h4>
          <p>If the school already receives mail at an address ending in
          <span class="mono">@mapleskhatauli.com</span>, say so during the Google sign-up so the existing
          mail is not interrupted. If there is no email on the domain yet, Google simply becomes the
          school's mail provider. Either way it works &mdash; the office just has to tell the Coordinator
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
        href="https://support.google.com/a/answer/60216" target="_blank" rel="noopener">How Google verifies a domain &rarr;</a></p>
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

<section class="anchor" id="docs"><div class="wrap">
  <div class="shead"><div class="kicker">Checklist</div>
    <h2>Documents to keep ready</h2>
    <p>Google, Microsoft and GitHub all ask for roughly the same proof that we are a real school. Scan
    these once, as PDFs under 2&nbsp;MB each, and the same folder serves every application.</p></div>
  <div class="grid g2">
    <div class="card"><div class="ic">{I_DOC}</div><h3>From the Principal</h3>
      <ul class="ck" style="margin-bottom:0">
        <li><strong>The signed order sheet</strong> at Annexure F of the proposal, naming the Faculty
          Advisor and the Coordinator.</li>
        <li><strong>A letter on school letterhead</strong> confirming that the Coordinator is authorised
          to act for the school online. Google and Microsoft occasionally ask for this.</li>
        <li><strong>The login for the domain account</strong>, or somebody from the office available to
          add the verification record on the Coordinator's instruction.</li>
        <li><strong>Teacher identity proof</strong> &mdash; an identity card or an employment letter.
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

<section class="anchor" id="google" style="padding-top:0"><div class="wrap">
  <div class="shead"><div class="kicker">Phases 2&ndash;3</div><h2>Google Workspace for Education, and the Admin Console</h2></div>
  <div class="split">
    <div>
      <ol class="no">
        <li><strong>Open the Education Fundamentals sign-up</strong> and start an application as the school's
          administrator. Supply the school's name, type, website, student and staff numbers, address,
          telephone and a contact email that is <em>not</em> on the new domain.</li>
        <li><strong>Enter <span class="mono">mapleskhatauli.com</span></strong> and prove ownership by
          adding the verification record Google provides to the domain's DNS settings.</li>
        <li><strong>Upload the accreditation document</strong> &mdash; the CBSE or Board affiliation
          certificate &mdash; when Google asks for evidence of educational status.</li>
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

<section class="anchor" id="microsoft"><div class="wrap">
  <div class="shead"><div class="kicker">Phase 4</div><h2>Microsoft 365 Education (Office 365 A1)</h2></div>
  <div class="split">
    <div>
      <ol class="no">
        <li><strong>Begin the education sign-up</strong> on the Microsoft Education site using an address on
          the school domain.</li>
        <li><strong>Complete academic verification.</strong> If the domain is not automatically recognised,
          Microsoft asks for proof of the school's academic status &mdash; supply the affiliation
          certificate. Approval can take a few business days.</li>
        <li><strong>Assign the free A1 licences</strong> from the Microsoft 365 admin centre:
          <em>Users &rarr; Active users &rarr; Assign licences</em>. There is no cap on the number of staff
          and student licences.</li>
        <li><strong>Set up Teams</strong> for classes and staff, and enable OneDrive for each user.</li>
      </ol>
      <div class="note warn">
        <p><strong>Two practical cautions.</strong> The free A1 tier gives <em>web and mobile</em> Office
        apps &mdash; installable desktop Word and Excel require the paid A3 tier. And if Microsoft asks for
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

<section class="anchor" id="github"><div class="wrap">
  <div class="shead"><div class="kicker">Phase 5</div><h2>GitHub Education</h2>
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

<section class="anchor" id="rest"><div class="wrap">
  <div class="shead"><div class="kicker">Phases 6&ndash;7</div><h2>Finishing the job</h2></div>
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
    <div class="card gr"><div class="ic">{I_CHIP}</div><h3>Optional &mdash; Atal Tinkering Lab</h3>
      <p>When the Atal Innovation Mission next opens applications, the school management applies for the
      grant of up to <strong>&#8377;20 lakh</strong>. Watch
      <a href="https://aim.gov.in/atl.php" target="_blank" rel="noopener">aim.gov.in</a> for the window; the
      club will prepare the supporting material.</p></div>
  </div>
</div></section>

<section class="anchor" id="optional"><div class="wrap">
  <div class="shead"><div class="kicker">Optional, and only later</div>
    <h2>Would a <span class="grad">.edu.in</span> address be better?</h2>
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
      below and the earlier work is not wasted &mdash; a second domain can be added to the same Google
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
    <h4>Fees change &mdash; confirm before paying</h4>
    <p>Published ERNET tariffs have varied over the years and differ between sources. The figure quoted
    here (&asymp;&nbsp;&#8377;1,180 for one year, inclusive of GST) is indicative only.
    <strong>Please confirm the current tariff on the ERNET portal at the time of applying</strong>, and
    note that registering several years at once reduces the yearly cost. A restoration fee applies if a
    domain is allowed to lapse. None of this affects the main plan, which costs nothing.</p>
  </div>
</div></section>

<section class="anchor" id="cost"><div class="wrap">
  <div class="shead"><div class="kicker">Summary</div><h2>Sequence, owners, time and cost</h2></div>
  <div class="tw"><table>
    <thead><tr><th style="width:60px">Phase</th><th style="width:28%">Action</th><th style="width:22%">Owner</th>
      <th style="width:110px">Time</th><th>Cost</th></tr></thead>
    <tbody>
      <tr><td><strong>0</strong></td><td><strong>Permission</strong> &mdash; Principal approves the club and names the Faculty Advisor and the Coordinator</td><td>Principal</td><td>1 week</td><td class="free">Nil</td></tr>
      <tr><td><strong>1</strong></td><td><strong>Prove we own <span class="mono">mapleskhatauli.com</span></strong> by adding Google's verification record</td><td>Coordinator, with the club</td><td>1&ndash;2 days</td><td class="free">Nil</td></tr>
      <tr><td><strong>2</strong></td><td><strong>Verify our eligibility with Google</strong> &mdash; Education Fundamentals sign-up</td><td>Coordinator</td><td>2 weeks</td><td class="free">FREE</td></tr>
      <tr><td><strong>3</strong></td><td><strong>Set up the Google Admin Console</strong> &mdash; accounts, groups, privacy, app access</td><td>Coordinator, with the club</td><td>1 week</td><td class="free">FREE</td></tr>
      <tr><td><strong>4</strong></td><td><strong>Microsoft 365 Education</strong> A1 licences</td><td>Coordinator</td><td>1&ndash;2 weeks</td><td class="free">FREE</td></tr>
      <tr><td><strong>5</strong></td><td><strong>GitHub Education</strong> &mdash; teacher, then students</td><td>Coordinator, then members</td><td>1 week</td><td class="free">FREE</td></tr>
      <tr><td><strong>6</strong></td><td><strong>Canva, Figma, JetBrains, Notion</strong> and other verified programmes</td><td>Coordinator</td><td>1 week</td><td class="free">FREE</td></tr>
      <tr><td><strong>7</strong></td><td><strong>School website</strong> maintained on our own domain</td><td>Club, supervised</td><td>3&ndash;4 weeks</td><td class="free">FREE</td></tr>
      <tr><td><strong>&mdash;</strong></td><td><em>Optional later:</em> a <span class="mono">.edu.in</span> address from ERNET India, or an Atal Tinkering Lab grant</td><td>School management</td><td>Later</td><td class="paid">&asymp; &#8377;1,180 / yr<br><small>only if chosen</small></td></tr>
    </tbody></table></div>
  <div class="note good" style="margin-top:22px">
    <h4>Total compulsory cost to the school</h4>
    <p><strong>&#8377;0. Nothing, in the first year or any year after.</strong> The domain is already the
    school's, and every programme above is free to verified schools. An optional consumables budget of
    &#8377;3,000&ndash;&#8377;6,000 a year is proposed for the electronics squad, and the club will function
    without it if the school prefers. There is no compulsory expenditure anywhere in this plan.</p>
  </div>
  <div class="btns">
    <a class="btn btn-p" href="{PDF}" download>{I_DOWN} Download the full proposal</a>
    <a class="btn btn-s" href="proposal.html">What we are asking the Principal for &rarr;</a>
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
    <a href="#doors">Two tracks</a><a href="#stages">The five stages</a><a href="#principles">Fairness rules</a>
    <a href="#renewal">Staying a member</a><a href="#conduct">Code of conduct</a><a href="#roles">Roles</a>
  </div>
</div></section>

<section class="anchor" id="doors" style="padding-top:10px"><div class="wrap">
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

<section class="anchor" id="stages"><div class="wrap">
  <div class="shead"><div class="kicker">Selection</div>
    <h2>The five stages of Core Track selection</h2>
    <p>Held once a year in April, with a short second intake in October for Class VI and for students newly
    admitted. The criteria and their weights go up on the board before the intake starts.</p></div>
  <div class="steps">
    <div class="step"><div class="num">1</div>
      <h4>Open Call &mdash; <span style="color:var(--tx3);font-weight:600">nobody is rejected here</span></h4>
      <p>A notice on the school board and a simple form. The student writes their class, the squad they want,
      why they want to join, and anything they have already tried to make.
      <strong>No previous knowledge of computers is needed, and none is assumed.</strong></p>
      <div class="tags"><span class="pill p-c">Judged on: whether they want to be there</span></div></div>
    <div class="step"><div class="num">2</div><h4>Aptitude screening &mdash; 30 minutes, on paper</h4>
      <p>Patterns, simple reasoning, basic mathematics, and one short written answer about a problem in the
      school the student would like to fix. <strong>No coding of any kind.</strong></p>
      <div class="tags"><span class="pill p-c">Weight: 25%</span>
        <span class="pill p-c">Judged on: thinking and curiosity, not skill</span></div></div>
    <div class="step"><div class="num">3</div><h4>Make something &mdash; one week</h4>
      <p>Make one small thing, chosen from a list we put up: a poster, a one-page website, a Scratch
      animation, a working circuit, a short video, a chart, a small program. Whatever suits the squad they
      applied for. <strong>Beginners' attempts are welcome and are expected.</strong></p>
      <div class="tags"><span class="pill p-v">Weight: 40%</span>
        <span class="pill p-v">Judged on: effort and finishing it, not polish</span></div></div>
    <div class="step"><div class="num">4</div><h4>Conversation &mdash; five to seven minutes</h4>
      <p>Five to seven minutes with two Core Committee members, with the Faculty Advisor sitting in. The
      student explains what they made, what went wrong while making it, and what they want to learn next.</p>
      <div class="tags"><span class="pill p-c">Weight: 25%</span>
        <span class="pill p-c">Judged on: honesty and willingness to listen</span></div></div>
    <div class="step"><div class="num">5</div><h4>Induction and 30-day probation</h4>
      <p>Names go up on the notice board. The student signs the code of conduct along with a parent or
      guardian, then serves <strong>thirty days on probation</strong>, during which they have to attend
      regularly. Full membership is confirmed after that.</p>
      <div class="tags"><span class="pill p-a">Weight: 10% attendance</span></div></div>
  </div>
</div></section>

<section class="anchor" id="principles"><div class="wrap">
  <div class="shead"><div class="kicker">Fairness</div><h2>Rules that bind the selection</h2></div>
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

<section class="anchor" id="renewal"><div class="wrap">
  <div class="shead"><div class="kicker">Continuing</div><h2>Staying a member</h2></div>
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

<section class="anchor" id="conduct"><div class="wrap">
  <div class="shead"><div class="kicker">Undertaking</div>
    <h2>Code of Conduct</h2>
    <p>Every member signs this at induction, along with a parent or guardian. The Faculty Advisor keeps the
    signed copy.</p></div>
  <div class="tw"><table>
    <thead><tr><th>I, a member of the Maples Tech Club, undertake that &mdash;</th></tr></thead>
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

<section class="anchor" id="roles"><div class="wrap">
  <div class="shead"><div class="kicker">Office</div><h2>Core Committee roles, elected each year in Term IV</h2></div>
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
      school's technology registrations. The full {NP}-page document, with its annexures and an order sheet
      for your signature, can be downloaded below.</p>
      <div class="btns">
        <a class="btn btn-p" href="{PDF}" download>{I_DOWN} Download the application (PDF)</a>
        <a class="btn btn-s" href="registration.html">See the registration roadmap &rarr;</a>
      </div>
    </div>
    <div class="hpanel">
      <div class="kicker">What is being asked for</div>
      <div class="row"><span>Permission to form the club</span><span class="free">Nil cost</span></div>
      <div class="row"><span>One Faculty Advisor</span><span class="free">Nil cost</span></div>
      <div class="row"><span>One Coordinator <small>(may be the same teacher)</small></span><span class="free">Nil cost</span></div>
      <div class="row"><span>Computer lab, 2 hrs / week</span><span class="free">Nil cost</span></div>
      <div class="row"><span>Signatures on the sign-up forms</span><span class="free">Nil cost</span></div>
      <div class="row"><span>Domain to buy</span><span class="free">None &mdash; already owned</span></div>
      <div class="row"><span>Consumables (optional)</span><span class="paid">&#8377;3,000&ndash;6,000 / yr</span></div>
      <div class="row"><span>Notice board space</span><span class="free">Nil cost</span></div>
    </div>
  </div>
</div></section>

<section class="anchor" style="padding-top:8px"><div class="wrap">
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

<section><div class="wrap">
  <div class="shead"><div class="kicker">Activation</div>
    <h2>What the school's IT administration has to do</h2>
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

<section><div class="wrap">
  <div class="shead"><div class="kicker">Concerns</div>
    <h2>Every reasonable objection, answered</h2>
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
        so does a parent or guardian. Content filtering is switched on at administrator level for all school
        accounts. Anything that goes wrong is reported to the Principal the same day.</td></tr>
      <tr><td><strong>Is the school's reputation at risk online?</strong></td>
        <td>Nothing goes out in the school's name without the Faculty Advisor approving it in writing first.
        That covers the website, notices, posters, photographs and social media. Photographs of students are only
        put up with their consent.</td></tr>
      <tr><td><strong>What happens when the founder leaves after Class XII?</strong></td>
        <td>The structure is built against exactly that. Every squad has a junior deputy. The Core Committee is
        elected fresh every year. All records, passwords and files are handed to the Faculty Advisor before the
        outgoing batch leaves, and 40% of every intake is kept for Classes VI&ndash;IX.</td></tr>
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

<section><div class="wrap">
  <div class="shead"><div class="kicker">Accountability</div>
    <h2>Judge us against this, after one year</h2>
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

<section><div class="wrap">
  <div class="shead"><div class="kicker">Contents</div><h2>What is inside the PDF</h2></div>
  <div class="grid g3">
    <div class="card"><div class="ic">{I_DOC}</div><h4>The application letter</h4>
      <p><small>A formal letter to the Principal setting out the two-part request and the reasoning behind
      it, with space for the proposer's and faculty advisor's signatures.</small></p></div>
    <div class="card vi"><div class="ic">{I_USERS}</div><h4>Annexure A &mdash; Club Charter</h4>
      <p><small>Identity, definition, vision and mission, the eight objectives, the six-tier structure, the
      six squads, the annual calendar and the examination-discipline rule.</small></p></div>
    <div class="card gr"><div class="ic">{I_SPARK}</div><h4>Annexure B &mdash; Schedule of Benefits</h4>
      <p><small>Every institutional and student benefit, with eligibility, cost and the provider's official
      web address for independent verification &mdash; including a frank note on what is <em>not</em>
      available in India.</small></p></div>
    <div class="card am"><div class="ic">{I_GLOBE}</div><h4>Annexure C &mdash; Registration Roadmap</h4>
      <p><small>Eight phases starting from the domain the school already owns, with the documents needed,
      the owner of each step, realistic timings and the total cost.</small></p></div>
    <div class="card"><div class="ic">{I_TROPHY}</div><h4>Annexure D &mdash; Selection &amp; Conduct</h4>
      <p><small>The two membership tracks, the five selection stages with weights, the fairness principles,
      renewal and removal rules, and the nine-point code of conduct for signature.</small></p></div>
    <div class="card gr"><div class="ic">{I_SHIELD}</div><h4>Annexures E &amp; F</h4>
      <p><small>Safeguards against every foreseeable concern, the precise list of what is requested from the
      school, the one-year target sheet, and an <strong>order sheet</strong> ready for the Principal's
      signature and seal.</small></p></div>
  </div>
</div></section>

<section style="padding-top:12px"><div class="wrap">
  <div class="band">
    <span class="eyebrow">{I_DOWN} Download</span>
    <h2>{NP} pages. Print it, read it, sign the last one.</h2>
    <p class="lead" style="margin:0 auto">A4, laid out for printing, with a tear-off order sheet at the end
    for the Principal's decision, the teacher nominated as advisor, the laboratory timing and the amount
    sanctioned.</p>
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
         "The Maples Tech Club — a proposed student technology society at Maples Academy, Khatauli, "
         "and a plan to get free Google, Microsoft and GitHub education programmes for the school.", home),
    page("about.html", "The Club",
         "Full charter of the Maples Tech Club: definition, purpose, vision and mission, structure, the six "
         "domain squads and the annual calendar.", about),
    page("benefits.html", "Benefits",
         "Every free education benefit Maples Academy and its students are eligible for — Google Workspace "
         "for Education, Microsoft 365 A1, GitHub Education, Canva, Figma and more, with official links.", benefits),
    page("registration.html", "Registration",
         "Step-by-step roadmap to register Maples Academy using the domain it already owns: Google "
         "Workspace for Education and the Admin Console, Microsoft 365 Education, GitHub Education — "
         "with documents, timings and costs.", registration),
    page("join.html", "Join Us",
         "How to join the Maples Tech Club: the open track, the five-stage core selection process, fairness "
         "rules and the member code of conduct.", join),
    page("proposal.html", "For the Principal",
         "Summary of the formal application to the Principal of Maples Academy, Khatauli, with safeguards, "
         f"costs, one-year targets and a downloadable {NP}-page PDF.", proposal),
]

src = os.path.join(BASE, PDF)
if os.path.exists(src):
    shutil.copy(src, os.path.join(OUT, PDF))

for (f, _), n in zip(PAGES, built):
    print(f"  {f:22s} {n/1024:6.1f} KB")
print("\nsite ->", OUT)
