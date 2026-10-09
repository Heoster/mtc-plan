#!/usr/bin/env python3
"""
Builds the Maples Tech Club recruitment poster.

Outputs (A3 portrait, 297 x 420 mm):
    Maples_Tech_Club_Poster.pdf        dark  - print / digital
    Maples_Tech_Club_Poster.png        dark  - WhatsApp / Instagram
    Maples_Tech_Club_Poster_Print.pdf  light - cheap on school printers
    Maples_Tech_Club_Poster_Print.png  light

Change the four constants below if the dates move, then re-run.
"""
import os

# ─────────────────────────────── the only things you may need to edit
TEST_DATE   = "Saturday, 17 October 2026"
TEST_TIME   = "11:00 am"
NAMES_BY    = "Wednesday, 14 October 2026"
PRICE_NOTE  = ("Retail prices checked September 2026: Canva Pro \u20b94,500/yr, "
               "Microsoft 365 Personal \u20b96,899/yr.")
OUTDIR      = os.path.dirname(os.path.abspath(__file__))
# ───────────────────────────────────────────────────────────────────

THEMES = {
    "dark": dict(
        suffix="", bg="#070b16", bg2="#0b1120", ink="#f1f5f9", ink2="#cbd5e1",
        ink3="#94a3b8", card="rgba(255,255,255,.045)", cardln="rgba(255,255,255,.10)",
        cy="#22d3ee", vi="#a78bfa", gr="#34d399", am="#fbbf24", rd="#fb7185",
        glow=".55", hair="rgba(255,255,255,.12)", stripe="rgba(255,255,255,.05)",
    ),
    "light": dict(
        suffix="_Print", bg="#ffffff", bg2="#f1f5f9", ink="#0b1220", ink2="#1e293b",
        ink3="#64748b", card="#f8fafc", cardln="#dbe3ee",
        cy="#0e7490", vi="#6d28d9", gr="#047857", am="#b45309", rd="#be123c",
        glow="0", hair="#e2e8f0", stripe="#f8fafc",
    ),
}

LOGO = """<svg viewBox="0 0 48 48" class="lg">
<defs><linearGradient id="g1" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="var(--cy)"/><stop offset=".55" stop-color="#818cf8"/>
<stop offset="1" stop-color="var(--vi)"/></linearGradient></defs>
<rect x="2" y="2" width="44" height="44" rx="12" fill="url(#g1)" opacity=".18"/>
<rect x="2" y="2" width="44" height="44" rx="12" fill="none" stroke="url(#g1)" stroke-width="2"/>
<path d="M14 30V18l6 7 6-7v12" fill="none" stroke="url(#g1)" stroke-width="3"
 stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="33.5" cy="28.5" r="3.2" fill="none" stroke="url(#g1)" stroke-width="2.6"/>
</svg>"""


def css(t):
    root = ";".join(f"--{k}:{v}" for k, v in t.items() if k != "suffix")
    return "@page{size:A3 portrait;margin:0}\n:root{" + root + "}\n" + r"""
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body{width:297mm;height:420mm}
body{background:var(--bg);color:var(--ink);
  font-family:"Inter","Inter Display","DejaVu Sans",sans-serif;
  -webkit-font-smoothing:antialiased;overflow:hidden;position:relative}
.bgfx{position:absolute;inset:0;pointer-events:none;opacity:var(--glow)}
.bgfx i{position:absolute;display:block;border-radius:50%;filter:blur(90px)}
.b1{width:520px;height:520px;top:-170px;right:-130px;background:rgba(34,211,238,.30)}
.b2{width:560px;height:560px;bottom:-220px;left:-170px;background:rgba(167,139,250,.26)}
.b3{width:380px;height:380px;top:44%;right:-160px;background:rgba(52,211,153,.16)}
.sheet{position:relative;height:420mm;padding:13mm 13mm 9mm;display:flex;flex-direction:column}
.sheet>*{flex:0 0 auto}

/* ── header ── */
.hd{display:flex;align-items:center;gap:9px;padding-bottom:7mm;
  border-bottom:1.5px solid var(--hair)}
.lg{width:40px;height:40px;flex:none}
.hd .nm{font-size:19px;font-weight:900;letter-spacing:-.4px;line-height:1.05}
.hd .sc{font-size:10.5px;font-weight:700;color:var(--ink3);letter-spacing:2.1px;
  text-transform:uppercase;margin-top:2px}
.hd .rt{margin-left:auto;text-align:right}
.tag{display:inline-block;padding:6px 14px;border-radius:99px;font-size:11px;font-weight:800;
  letter-spacing:1.3px;text-transform:uppercase;background:rgba(52,211,153,.14);
  color:var(--gr);border:1.5px solid var(--gr)}

/* ── headline ── */
.hero{padding:6mm 0 0}
.eyeb{font-size:12px;font-weight:800;letter-spacing:3.4px;text-transform:uppercase;
  color:var(--cy);margin-bottom:4mm}
h1{font-family:"Inter Display","Inter",sans-serif;font-size:58px;line-height:.95;
  font-weight:900;letter-spacing:-2.5px}
h1 .c{color:var(--cy)}  h1 .v{color:var(--vi)}  h1 .g{color:var(--gr)}
.sub{margin-top:4.5mm;font-size:17px;line-height:1.38;color:var(--ink2);font-weight:500;
  max-width:225mm}
.sub b{color:var(--ink);font-weight:800}

/* ── money strip ── */
.money{margin-top:5mm;display:flex;align-items:stretch;gap:0;border-radius:16px;overflow:hidden;
  border:1.5px solid var(--cardln);background:var(--card)}
.money div{padding:4.2mm 5.4mm;flex:1}
.money div + div{border-left:1.5px solid var(--cardln)}
.money .k{font-size:9.6px;font-weight:800;letter-spacing:1.7px;text-transform:uppercase;
  color:var(--ink3);margin-bottom:5px}
.money .v{font-size:29px;font-weight:900;letter-spacing:-1.3px;line-height:1}
.money .n{font-size:10.8px;line-height:1.35;color:var(--ink3);margin-top:4px;font-weight:500}

/* ── tools ── */
.sh{margin:6mm 0 3.4mm;display:flex;align-items:baseline;gap:10px}
.sh h2{font-size:22px;font-weight:900;letter-spacing:-.8px}
.sh span{font-size:11.5px;color:var(--ink3);font-weight:600}
.tools{display:grid;grid-template-columns:repeat(4,1fr);gap:2.7mm}
.t{background:var(--card);border:1.5px solid var(--cardln);border-radius:12px;padding:3.6mm 3.6mm}
.t .n{font-size:13.4px;font-weight:900;letter-spacing:-.4px;line-height:1.14}
.t .d{font-size:10.3px;line-height:1.38;color:var(--ink3);margin-top:4px;font-weight:500}
.t .p{font-size:9.8px;font-weight:900;margin-top:5px;letter-spacing:.2px}
.t.a{border-color:var(--cy)}      .t.a .n{color:var(--cy)}   .t.a .p{color:var(--cy)}
.t.b{border-color:var(--vi)}      .t.b .n{color:var(--vi)}   .t.b .p{color:var(--vi)}
.t .p.free{color:var(--gr)}

/* ── the unlock line ── */
.key{margin-top:3.8mm;border-radius:13px;padding:4mm 5mm;background:var(--stripe);
  border:1.5px dashed var(--cardln);font-size:12.6px;line-height:1.45;color:var(--ink2);
  font-weight:500}
.key b{color:var(--ink);font-weight:800}
.key code{font-family:"DejaVu Sans Mono",monospace;font-size:11.8px;color:var(--cy);
  font-weight:700}

/* ── selection ── */
.grid2{display:grid;grid-template-columns:1fr 88mm;gap:5mm;margin-top:5mm;align-items:start}
.steps{display:flex;flex-direction:column;gap:2.5mm}
.st{display:flex;gap:11px;align-items:flex-start}
.st .num{width:22px;height:22px;flex:none;border-radius:50%;border:1.8px solid var(--cy);
  color:var(--cy);font-size:12.5px;font-weight:900;display:flex;align-items:center;
  justify-content:center;margin-top:1px}
.st .tt{font-size:13.4px;font-weight:800;letter-spacing:-.25px;line-height:1.2}
.st .dd{font-size:10.6px;line-height:1.42;color:var(--ink3);margin-top:3px;font-weight:500}

/* ── the test box ── */
.test{border-radius:15px;padding:4.6mm;background:var(--card);
  border:2.2px solid var(--am);position:relative}
.test .lab{font-size:9.6px;font-weight:900;letter-spacing:2.2px;text-transform:uppercase;
  color:var(--am);margin-bottom:9px}
.test .big{font-size:23px;font-weight:900;line-height:1.06;letter-spacing:-.95px}
.test .tm{font-size:13.2px;font-weight:800;color:var(--am);margin-top:6px}
.test ul{list-style:none;margin-top:10px;border-top:1.5px solid var(--hair);padding-top:9px}
.test li{font-size:10.9px;line-height:1.44;color:var(--ink2);font-weight:600;
  padding-left:15px;position:relative;margin-bottom:5px}
.test li::before{content:"";position:absolute;left:0;top:7px;width:6px;height:6px;
  border-radius:50%;background:var(--am)}
.test li b{color:var(--ink)}

/* ── apply ── */
.apply{margin-top:4.4mm;border-radius:15px;padding:4.2mm 5.4mm;
  border:2.2px solid var(--gr);background:var(--card);display:flex;align-items:center;gap:7mm}
.apply .l{flex:none}
.apply .k{font-size:9.6px;font-weight:900;letter-spacing:2.2px;text-transform:uppercase;
  color:var(--gr);margin-bottom:6px}
.apply .t2{font-size:19.5px;font-weight:900;letter-spacing:-.8px;line-height:1.16}
.apply .r{margin-left:auto;text-align:right;font-size:11px;line-height:1.48;
  color:var(--ink3);font-weight:600;border-left:1.5px solid var(--hair);padding-left:7mm}
.apply .r b{color:var(--ink);display:block;font-size:12.6px;font-weight:900;margin-bottom:3px}

/* ── pills + foot ── */
.pills{display:flex;flex-wrap:wrap;gap:2mm;margin-top:4.4mm}
.pl{padding:4px 11px;border-radius:99px;font-size:10.4px;font-weight:800;letter-spacing:.2px;
  border:1.5px solid var(--cardln);background:var(--card);color:var(--ink2)}
.pl.g{border-color:var(--gr);color:var(--gr)} .pl.c{border-color:var(--cy);color:var(--cy)}
.pl.v{border-color:var(--vi);color:var(--vi)}
.foot{margin-top:auto;padding-top:4mm;border-top:1.5px solid var(--hair);
  font-size:8.8px;line-height:1.48;color:var(--ink3);font-weight:500;display:flex;gap:8mm}
.foot .fl{flex:1}
.foot b{color:var(--ink2);font-weight:800}
.foot .fr{text-align:right;flex:none;max-width:68mm}
"""


TOOLS = [
    ("a", "Canva Pro", "Every premium template, font and stock photo. Magic Studio AI. "
                       "Videos, posters, presentations.", "\u20b94,500 / yr \u2192 FREE", ""),
    ("b", "Microsoft 365", "Word, Excel, PowerPoint and Outlook, Teams, and 1 TB of "
                           "OneDrive storage.", "\u20b96,899 / yr \u2192 FREE", ""),
    ("", "GitHub Student Pack", "Copilot, unlimited private repositories and 100+ paid "
                                "developer tools.", "FREE", "free"),
    ("", "Google Workspace", "Your own school email, Classroom, Drive, Docs, Sheets, "
                             "Meet.", "FREE", "free"),
    ("", "Figma", "The design tool real product teams use. School students get the "
                  "top plan.", "FREE", "free"),
    ("", "Autodesk &amp; Tinkercad", "3D design and printing, circuit simulation, CAD for "
                                     "school students.", "FREE", "free"),
    ("", "JetBrains IDEs", "The editors professional programmers pay thousands of rupees "
                           "for.", "FREE", "free"),
    ("", "Notion", "Notes, planners, project boards and databases on the Plus plan.",
     "FREE", "free"),
]

STEPS = [
    ("Give your name to your class teacher",
     f"By {NAMES_BY}. No form to buy, no fee, nothing to prepare."),
    ("Step 1 \u2014 the online test, 25 questions in 30 minutes",
     "On your own phone or a school computer. Marked class-wise, so nobody competes against "
     "a senior. Worth 40%."),
    ("Step 2 \u2014 make one thing. Anything you like.",
     "A poster, a web page, a game, a circuit, a short film, a model, a spreadsheet. No list, "
     "no fixed subject, one week. Worth 60%, and judged on effort, not polish."),
    ("Names go up on the notice board",
     "Two steps and that is all. No interview panel, no probation. If you are not picked you "
     "can still come to every open workshop."),
]


def build(theme_name):
    t = THEMES[theme_name]
    tools = "".join(
        f'<div class="t {c}"><div class="n">{n}</div><div class="d">{d}</div>'
        f'<div class="p {pc}">{p}</div></div>'
        for c, n, d, p, pc in TOOLS)
    steps = "".join(
        f'<div class="st"><div class="num">{i}</div><div><div class="tt">{tt}</div>'
        f'<div class="dd">{dd}</div></div></div>'
        for i, (tt, dd) in enumerate(STEPS, 1))

    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Maples Tech Club \u2014 Poster</title><style>{css(t)}</style></head><body>
<div class="bgfx"><i class="b1"></i><i class="b2"></i><i class="b3"></i></div>
<div class="sheet">

  <div class="hd">{LOGO}
    <div><div class="nm">Maples Tech Club</div>
      <div class="sc">Maples Academy &middot; Khatauli</div></div>
    <div class="rt"><span class="tag">Admissions open</span></div>
  </div>

  <div class="hero">
    <div class="eyeb">Classes VI to XII &nbsp;&middot;&nbsp; No fee &nbsp;&middot;&nbsp;
      Beginners welcome</div>
    <h1><span class="c">Canva Pro.</span><br><span class="v">Microsoft 365.</span><br>
      <span class="g">GitHub.</span> Yours, free.</h1>
    <p class="sub">Join the Maples Tech Club and you get the paid versions of the software
      everybody else buys. <b>Not a trial. Not a student discount. Free, for as long as you
      are a student here.</b></p>
  </div>

  <div class="money">
    <div><div class="k">What it would cost you</div>
      <div class="v" style="color:var(--rd)">\u20b911,000+</div>
      <div class="n">a year, if you paid retail for just the first two</div></div>
    <div><div class="k">What you pay</div>
      <div class="v" style="color:var(--gr)">\u20b90</div>
      <div class="n">no membership fee, no test fee, nothing</div></div>
    <div><div class="k">What we ask for</div>
      <div class="v" style="color:var(--cy)">2 hrs</div>
      <div class="n">one session a week, after school hours</div></div>
  </div>

  <div class="sh"><h2>What every member gets</h2>
    <span>all of it legally licensed to you through the school</span></div>
  <div class="tools">{tools}</div>

  <div class="key">Every one of these unlocks the moment our school switches on its own email
    addresses \u2014 <code>yourname@mapleskhatauli.com</code>. The school already owns the
    domain. Getting it registered with Google is <b>exactly what this club is for.</b> You are
    not just joining a club. You are the reason the whole school gets this.</div>

  <div class="grid2">
    <div>
      <div class="sh" style="margin:0 0 5mm"><h2>How you get in</h2></div>
      <div class="steps">{steps}</div>
    </div>

    <div class="test">
      <div class="lab">Selection test &middot; online</div>
      <div class="big">{TEST_DATE.replace(', ', ',<br>')}</div>
      <div class="tm">{TEST_TIME} &nbsp;&middot;&nbsp; 25 questions &nbsp;&middot;&nbsp; 30 minutes</div>
      <ul>
        <li><b>25 questions in 30 minutes.</b> Objective only, marked automatically.</li>
        <li><b>Marked class-wise.</b> You are only ever compared with students of your own
          class group.</li>
        <li>Basic technical skills: simple logic and patterns, everyday computer awareness,
          reading instructions, ordinary maths.</li>
        <li><b>No coding.</b> No computer knowledge needed. Nothing to study for.</li>
        <li>Link comes to your class group the evening before.</li>
      </ul>
    </div>
  </div>

  <div class="apply">
    <div class="l"><div class="k">To enter</div>
      <div class="t2">Give your name to your<br>class teacher by {NAMES_BY}.</div></div>
    <div class="r"><b>That is the whole application.</b>
      No fee. No form to buy.<br>Ask any Class XII student<br>if you want to know more.</div>
  </div>

  <div class="pills">
    <span class="pl g">No fee, ever</span>
    <span class="pl c">Complete beginners welcome</span>
    <span class="pl v">40% of seats kept for Classes VI\u2013IX</span>
    <span class="pl">Girls strongly encouraged to apply</span>
    <span class="pl">Club stops 4 weeks before every exam</span>
    <span class="pl">Open workshops for everyone, test or no test</span>
  </div>

  <div class="foot">
    <div class="fl"><b>The honest small print.</b> The Maples Tech Club is proposed and is
      awaiting the Principal's approval, so dates may shift. Every programme named here is the
      provider's own free education offer to verified schools and their students, and each one
      needs the school to be registered first. Canva for Education reaches students through a
      class created by a teacher. GitHub requires you to be 13 or older. Microsoft 365 Education
      gives you the web and mobile apps. Nothing here is pirated, cracked or shared \u2014 all of it
      is licensed to you properly, through the school.</div>
    <div class="fr"><b>{PRICE_NOTE}</b><br><br>Proposed by Harsh, Class XII, Roll No. 13.
      Full proposal with official links is with the Principal.</div>
  </div>

</div></body></html>"""
    return html


def main():
    from playwright.sync_api import sync_playwright
    made = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=["--no-sandbox", "--force-color-profile=srgb"])
        for name, t in THEMES.items():
            html = build(name)
            tmp = os.path.join(OUTDIR, f"_poster_{name}.html")
            open(tmp, "w").write(html)
            pg = b.new_page(viewport={"width": 1123, "height": 1587},
                            device_scale_factor=2.6)
            pg.goto("file://" + tmp, wait_until="load")
            pg.wait_for_timeout(450)
            pdf = os.path.join(OUTDIR, f"Maples_Tech_Club_Poster{t['suffix']}.pdf")
            png = os.path.join(OUTDIR, f"Maples_Tech_Club_Poster{t['suffix']}.png")
            pg.pdf(path=pdf, format="A3", print_background=True,
                   margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
            pg.screenshot(path=png, full_page=False)
            pg.close()
            os.remove(tmp)
            made += [pdf, png]
        b.close()
    for f in made:
        print(f"  {os.path.basename(f):<42} {os.path.getsize(f)/1024:8.1f} KB")


if __name__ == "__main__":
    main()
