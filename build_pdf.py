#!/usr/bin/env python3
"""
Generates: Maples_Tech_Club_Proposal_Principal.pdf
A formal application + annexures addressed to the Principal, Maples Academy, Khatauli.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_RIGHT
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph as _RLPara,
                                Spacer, Table, TableStyle, KeepTogether, ListFlowable, ListItem,
                                HRFlowable, PageBreak, Flowable)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from datetime import datetime, timezone, timedelta

import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "Maples_Tech_Club_Proposal_Principal.pdf")

# ---- Date on the letter and on the order sheet ----------------------------
# By default this is TODAY's date in India, worked out fresh every time the
# script runs, so the application is never dated in the past.
# Only set APP_DATE_OVERRIDE if you deliberately want a different date,
# e.g. APP_DATE_OVERRIDE = "5 November 2026"
APP_DATE_OVERRIDE = "12 October 2026"

# IST is permanently UTC+05:30 (India has no daylight saving), so a fixed
# offset is exact and needs no timezone database installed.
_IST = timezone(timedelta(hours=5, minutes=30))


def _today_in_india() -> str:
    """'27 September 2026' - no leading zero on the day, the way it is written here."""
    d = datetime.now(_IST)
    return f"{d.day} {d:%B %Y}"


APP_DATE = APP_DATE_OVERRIDE or _today_in_india()

# --- Unicode fallback fonts: the PDF core fonts have no rupee sign or ballot box ---
# DejaVu lives in different places on different systems; find it rather than
# assume one path, so the script also runs on CI runners and on a laptop.
# The copies shipped in fonts/ come first, so the PDF is byte-for-byte the same
# whoever builds it. It also means the build needs no apt-get, which matters on
# Netlify and anywhere else without root.
_FONT_DIRS = [
    os.path.join(BASE, "fonts"),
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/dejavu",
    "/usr/share/fonts/TTF",
    "/usr/local/share/fonts/dejavu",
    "/Library/Fonts", os.path.expanduser("~/.fonts"),
]


def _find_font(fname):
    for d in _FONT_DIRS:
        p = os.path.join(d, fname)
        if os.path.exists(p):
            return p
    raise SystemExit(
        f"Could not find {fname}. Install the DejaVu fonts \n"
        f"  Debian/Ubuntu : sudo apt-get install fonts-dejavu-core\n"
        f"  or drop the .ttf files into {os.path.join(BASE, 'fonts')}/")


pdfmetrics.registerFont(TTFont("DjvSerif", _find_font("DejaVuSerif.ttf")))
pdfmetrics.registerFont(TTFont("DjvSans",  _find_font("DejaVuSans.ttf")))

RUPEE = "\u20b9"
BALLOT = "\u2610"


def Paragraph(text, style=None, **kw):
    """Drop-in Paragraph that swaps glyphs missing from Times/Helvetica
    for the same glyph from a registered DejaVu face."""
    serif = True
    try:
        serif = "Times" in (style.fontName or "")
    except Exception:
        pass
    rf = "DjvSerif" if serif else "DjvSans"
    t = text.replace("&#8377;", f'<font name="{rf}">{RUPEE}</font>')
    t = t.replace("&#9744;", f'<font name="DjvSans">{BALLOT}</font>')
    return _RLPara(t, style, **kw)

# ---------------------------------------------------------------- palette
INK      = colors.HexColor("#111827")
BODY     = colors.HexColor("#1f2937")
MUTED    = colors.HexColor("#6b7280")
ACCENT   = colors.HexColor("#0f4c81")   # deep institutional blue
ACCENT2  = colors.HexColor("#0e7490")   # teal
RULE     = colors.HexColor("#d1d5db")
BAND     = colors.HexColor("#eef2f7")
BAND2    = colors.HexColor("#f8fafc")
GREEN    = colors.HexColor("#0f766e")

PAGE_W, PAGE_H = A4
LM = RM = 19 * mm
TM = 18 * mm
BM = 18 * mm

# ---------------------------------------------------------------- styles
ss = getSampleStyleSheet()

def S(name, **kw):
    base = dict(fontName="Times-Roman", fontSize=10.3, leading=15.2, textColor=BODY,
                spaceAfter=0, spaceBefore=0)
    base.update(kw)
    return ParagraphStyle(name, **base)

st_body     = S("body", alignment=TA_JUSTIFY, spaceAfter=7)
st_body_c   = S("bodyc", alignment=TA_CENTER)
st_small    = S("small", fontSize=8.7, leading=11.8, textColor=MUTED)
st_smallb    = S("smallb", fontSize=8.7, leading=11.8, textColor=BODY)
st_tiny     = S("tiny", fontSize=7.6, leading=10, textColor=MUTED)
st_right    = S("right", alignment=TA_RIGHT, fontSize=10.3)

st_school   = S("school", fontName="Times-Bold", fontSize=19, leading=22,
                textColor=ACCENT, alignment=TA_CENTER, spaceAfter=1)
st_schoolsub= S("schoolsub", fontSize=9.4, leading=12, textColor=MUTED,
                alignment=TA_CENTER, spaceAfter=2)
st_doctitle = S("doctitle", fontName="Times-Bold", fontSize=13.4, leading=17,
                textColor=INK, alignment=TA_CENTER, spaceBefore=4, spaceAfter=2)

st_h1       = S("h1", fontName="Times-Bold", fontSize=12.6, leading=16, textColor=ACCENT,
                spaceBefore=13, spaceAfter=5)
st_h2       = S("h2", fontName="Times-Bold", fontSize=10.9, leading=14, textColor=INK,
                spaceBefore=9, spaceAfter=4)
st_sub      = S("sub", fontName="Times-Italic", fontSize=9.6, leading=13, textColor=MUTED,
                spaceAfter=5)

st_li       = S("li", alignment=TA_JUSTIFY, spaceAfter=3.2)
st_th       = S("th", fontName="Helvetica-Bold", fontSize=8.3, leading=10.8,
                textColor=colors.white)
st_td       = S("td", fontName="Helvetica", fontSize=8.3, leading=11.2, textColor=BODY)
st_tdb      = S("tdb", fontName="Helvetica-Bold", fontSize=8.3, leading=11.2, textColor=INK)
st_tdc      = S("tdc", fontName="Helvetica", fontSize=8.3, leading=11.2, textColor=BODY,
                alignment=TA_CENTER)
st_tdg      = S("tdg", fontName="Helvetica-Bold", fontSize=8.3, leading=11.2, textColor=GREEN,
                alignment=TA_CENTER)

st_quote    = S("quote", fontName="Times-Italic", fontSize=10.2, leading=14.6,
                textColor=ACCENT, alignment=TA_JUSTIFY)


class Rule(Flowable):
    def __init__(self, w=None, thick=0.7, color=RULE, pad=0):
        super().__init__()
        self.w, self.thick, self.color, self.pad = w, thick, color, pad
    def wrap(self, aw, ah):
        self._w = self.w or aw
        return (self._w, self.thick + self.pad)
    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thick)
        self.canv.line(0, self.pad, self._w, self.pad)


def bullets(items, style=st_li, bullet="\u2022", left=12):
    return ListFlowable(
        [ListItem(Paragraph(t, style), leftIndent=left, value=bullet) for t in items],
        bulletType="bullet", start=bullet, leftIndent=left, bulletFontSize=8.5,
        bulletOffsetY=0.6, spaceBefore=1, spaceAfter=5)


def numbered(items, style=st_li, left=16):
    return ListFlowable(
        [ListItem(Paragraph(t, style), leftIndent=left) for t in items],
        bulletType="1", bulletFormat="%s.", leftIndent=left,
        bulletFontName="Times-Bold", bulletFontSize=10,
        spaceBefore=1, spaceAfter=5)


def table(data, widths, header=True, align=None, zebra=True, fs=8.3, pad=4.5):
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    cmds = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), pad),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -2), 0.35, RULE),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#9ca3af")),
    ]
    if header:
        cmds += [("BACKGROUND", (0, 0), (-1, 0), ACCENT),
                 ("LINEBELOW", (0, 0), (-1, 0), 0.6, ACCENT)]
        if zebra:
            for r in range(2, len(data), 2):
                cmds.append(("BACKGROUND", (0, r), (-1, r), BAND2))
    t.setStyle(TableStyle(cmds))
    return t


def callout(title, body_html, fill=BAND, bar=ACCENT):
    inner = []
    if title:
        inner.append(Paragraph(f"<b>{title}</b>", S("cot", fontName="Times-Bold",
                                                    fontSize=10.2, leading=13.4,
                                                    textColor=bar, spaceAfter=3)))
    inner.append(Paragraph(body_html, S("cob", fontSize=9.7, leading=13.6,
                                        alignment=TA_JUSTIFY, textColor=BODY)))
    t = Table([[inner]], colWidths=[PAGE_W - LM - RM])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), fill),
        ("LINEBEFORE", (0, 0), (0, -1), 2.6, bar),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return KeepTogether([Spacer(1, 3), t, Spacer(1, 8)])


# ---------------------------------------------------------------- page furniture
def on_page(canv, doc):
    canv.saveState()
    # top accent bar
    canv.setFillColor(ACCENT)
    canv.rect(0, PAGE_H - 6.5 * mm, PAGE_W, 6.5 * mm, stroke=0, fill=1)
    canv.setFillColor(ACCENT2)
    canv.rect(0, PAGE_H - 8.1 * mm, PAGE_W, 1.6 * mm, stroke=0, fill=1)

    # footer
    canv.setStrokeColor(RULE)
    canv.setLineWidth(0.5)
    canv.line(LM, 12.5 * mm, PAGE_W - RM, 12.5 * mm)
    canv.setFont("Times-Italic", 7.8)
    canv.setFillColor(MUTED)
    canv.drawString(LM, 9 * mm,
                    "Proposal for the establishment of the Maples Tech Club  \u00b7  "
                    "Maples Academy, Khatauli, Uttar Pradesh")
    canv.setFont("Times-Bold", 8.2)
    canv.setFillColor(ACCENT)
    canv.drawRightString(PAGE_W - RM, 9 * mm, f"Page {doc.page}")
    canv.restoreState()


doc = BaseDocTemplate(
    OUT, pagesize=A4,
    leftMargin=LM, rightMargin=RM, topMargin=TM, bottomMargin=BM,
    title="Proposal for the Establishment of the Maples Tech Club \u2014 Maples Academy, Khatauli",
    author="Harsh, Class XII, Maples Academy, Khatauli",
    subject="Application to the Principal: formation of a school technology club and "
            "institutional registration for free education technology programmes",
    keywords="Maples Tech Club, Maples Academy Khatauli, Google Workspace for Education, "
             "Microsoft 365 Education A1, GitHub Education, Google Admin Console, "
             "mapleskhatauli.com, Atal Tinkering Lab",
)
frame = Frame(LM, BM, PAGE_W - LM - RM, PAGE_H - TM - BM, id="main",
              leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=on_page)])

F = []          # story
W = PAGE_W - LM - RM

# ================================================================ LETTERHEAD
F.append(Spacer(1, 3))
F.append(Paragraph("MAPLES ACADEMY, KHATAULI", st_school))
F.append(Paragraph("Khatauli, District Muzaffarnagar, Uttar Pradesh \u2014 251201", st_schoolsub))
F.append(Rule(thick=1.1, color=ACCENT, pad=3))
F.append(Spacer(1, 6))
F.append(Paragraph("APPLICATION FOR PERMISSION TO ESTABLISH<br/>"
                   "THE <b>MAPLES TECH CLUB</b>", st_doctitle))
F.append(Paragraph("and to register the school for free institutional technology "
                   "programmes offered by Google, Microsoft, GitHub and the "
                   "Government of India", st_sub))
F.append(Rule(thick=0.7, color=RULE, pad=2))
F.append(Spacer(1, 8))

# ---- meta block
meta = [
    [Paragraph("<b>To</b>", st_tdb),
     Paragraph("The Principal<br/>Maples Academy, Khatauli<br/>District Muzaffarnagar, Uttar Pradesh", st_td),
     Paragraph("<b>Date</b>", st_tdb),
     Paragraph(APP_DATE, st_td)],
    [Paragraph("<b>From</b>", st_tdb),
     Paragraph("<b>Harsh</b>, Class XII, Roll No. 13<br/>Maples Academy, Khatauli<br/>"
               "Proposer of the club", st_td),
     Paragraph("<b>Subject</b>", st_tdb),
     Paragraph("Permission to start a technology club in the school, and to "
               "register the school for the free technology programmes it is "
               "eligible for", st_td)],
]
t = Table(meta, colWidths=[16*mm, 74*mm, 20*mm, W-110*mm])
t.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("BACKGROUND", (0, 0), (-1, -1), BAND2),
    ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#9ca3af")),
    ("INNERGRID", (0, 0), (-1, -1), 0.35, RULE),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
]))
F.append(t)
F.append(Spacer(1, 11))

# ================================================================ LETTER
F.append(Paragraph("Respected Sir,", S("sal", fontSize=10.5, spaceAfter=7)))

F.append(Paragraph(
    "With due respect, I beg to state that I am <b>Harsh</b> of <b>Class XII, Roll No. 13</b>, "
    "a student of this school. I am writing to ask your permission for something I have "
    "prepared carefully, and which I believe the school will benefit from.", st_body))

F.append(Paragraph(
    "I want to start a technology club in our school. In this application I have called it the "
    "<b>Maples Tech Club</b>. There are three parts to my request, and I would ask you to "
    "read them together, because it is the second part that makes the first one worth "
    "anything to the school.", st_body))

F.append(numbered([
    "<b>Permission to start the Maples Tech Club.</b> It would meet once a week, under a "
    "teacher appointed by you, and teach students of Classes VI to XII computer science, "
    "artificial intelligence, robotics and electronics, design, cyber safety and digital "
    "media. The teaching would be done by building things. Explaining would come second.",

    "<b>Permission to register the school with the education programmes run by Google, "
    "Microsoft and GitHub.</b> These companies give schools software, cloud storage and "
    "official email addresses <b>free of cost</b>. So does Canva, and so does the Government "
    "of India in its own way. But they give it only to schools that apply for it. Our school "
    "qualifies today, already owns the domain name these companies ask for, and has simply "
    "never applied. The club would do the paperwork and then look after the accounts "
    "afterwards, under the teacher you appoint.",

    "<b>Permission for a small founding group to set the club up.</b> To begin with I am "
    "asking only for myself and my friend <b>Vidhan of Class XII</b>, together with two to "
    "four other "
    "students chosen by the test described in Annexure&nbsp;D. Four to six of us in all. "
    "I will run the setting-up myself. Once the club is standing on its feet, it passes to "
    "its elected President and members, and the rest of the school is admitted in the "
    "ordinary way.",
]))

F.append(Paragraph(
    "Almost every free offer in this application depends on one thing: the school having a "
    "<b>domain name of its own</b>, so that teachers and students can be given addresses like "
    "<b><i>name@mapleskhatauli.com</i></b>. <b>Our school already owns "
    "<i>mapleskhatauli.com</i>.</b> That is the difficult and expensive part already done. "
    "What has not been done is using it. Once that domain is verified with Google as belonging "
    "to a recognised school, Google Workspace for Education, Microsoft 365 Education, GitHub "
    "Education and a long list of paid software become free for our teachers and students, "
    "lawfully, and for as long as we remain a school.", st_body))

F.append(Paragraph(
    "To switch these benefits on, somebody at the school has to do two things. "
    "<b>First</b>, verify our educational eligibility with Google using our official domain, "
    "<i>mapleskhatauli.com</i>. <b>Second</b>, set up the <b>Google Admin Console</b>, which is "
    "the control panel from which student and teacher accounts are created, data privacy is "
    "managed, and it is decided which apps each class may use. Neither step costs anything. "
    "Both are described step by step in Annexure&nbsp;C. I am asking that a teacher be named as "
    "<b>Coordinator</b> to hold this responsibility, and the club will do the work under him.", st_body))

F.append(callout(
    "What I am actually asking for",
    "<b>I am not asking the school to spend any money at all.</b> Because we already own "
    "<i>mapleskhatauli.com</i>, there is no domain to buy. Everything listed in "
    "Annexure&nbsp;B is free to verified schools. What I need from you is <b>permission</b>, "
    "<b>one teacher as Faculty Advisor</b> to supervise our sessions, <b>one teacher as "
    "Coordinator</b> to hold the Google Admin Console (it may be the same person), and the "
    "computer laboratory for <b>two hours a week</b>.", fill=colors.HexColor("#ecfdf5"),
    bar=GREEN))

F.append(Paragraph(
    "I am not asking for this only because I am interested in computers. CBSE has already made "
    "Artificial Intelligence and Information Technology skill subjects, and the National "
    "Education Policy 2020 asks schools to teach coding and computational thinking. Outside "
    "school, colleges and employers have started asking students what they have actually "
    "built. A student who has built something can answer that question. Marks alone cannot.", st_body))

F.append(Paragraph(
    "I should be honest. I am in Class XII and I will be leaving the school in "
    "a few months, so I will get very little out of this myself. I am asking for it because our "
    "juniors will get years out of it, and because the school is presently missing something it "
    "can have for almost nothing.", st_body))

F.append(Paragraph(
    "I have tried to keep this application practical rather than impressive. The annexures "
    "give the club's rules, an honest list of every benefit with the official website address "
    "against it so that you can check each claim yourself, the registration steps with the "
    "documents and costs involved, how members will be chosen, the code of conduct they will "
    "sign, and the targets the club should be judged against after one year. If it has not met "
    "them by then, I have written down that it should be closed.", st_body))

F.append(callout(
    "Why me, and not somebody else",
    "I am not claiming to be the best student in the school. What I can say is that nobody "
    "else has done this particular work. I found these programmes, read the eligibility rules "
    "for each one, checked which of them a K\u201312 school in India can use, and listed the ones "
    "that do not apply to us instead of hiding them. The website for this club, the posters "
    "and this application were all made by me. I am asking for the job because the work is "
    "already done and I am the one who did it. If somebody can carry it better, I will hand it "
    "over and stay on as a member.",
    fill=colors.HexColor("#eef2ff"), bar=ACCENT2))

F.append(Paragraph(
    "One thing is beyond me. The domain <i>mapleskhatauli.com</i> and the present school "
    "website are handled by the management, or by whoever built the site. <b>I would request "
    "you to kindly speak to the management</b>, so that the Coordinator can be given access to "
    "the domain settings. Without that, nothing in Annexure&nbsp;C can begin. It costs "
    "nothing.", st_body))

F.append(Paragraph(
    "Nothing here is fixed. The name, the timings, the number of members, the way they are "
    "selected, the posts, the rules, any of it may be changed or struck out as you think "
    "proper. I have written it out in full only so that you have something definite to "
    "correct rather than a vague idea. Your decision on any point will be final.", st_body))

F.append(Paragraph(
    "I therefore request you to kindly grant permission for the Maples Tech Club, and to allow "
    "the registrations described here to be started. I would be grateful for a few minutes of "
    "your time to explain it in person whenever it suits you. I give my word that the club will "
    "work within the timings, rules and discipline of the school.", st_body))

F.append(Paragraph("Thanking you, and hoping for a favourable reply.", st_body))
F.append(Spacer(1, 8))

sig = [
    [Paragraph("Yours obediently,", st_td), Paragraph("", st_td)],
    [Spacer(1, 15), Spacer(1, 15)],
    [Paragraph("<b>Harsh</b><br/>Class XII &nbsp;\u00b7&nbsp; Roll No. 13<br/>"
               "Maples Academy, Khatauli<br/>"
               "Mobile: ____________________", st_td),
     Paragraph("<b>Countersigned \u2014 Proposed Faculty Advisor</b><br/><br/>"
               "Name: ______________________________<br/><br/>"
               "Designation: _________________________<br/><br/>"
               "Signature: ___________________________", st_td)],
]
t = Table(sig, colWidths=[W*0.48, W*0.52])
t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                       ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
F.append(t)


# ================================================================ ANNEXURE A
F.append(PageBreak())
F.append(Paragraph("ANNEXURE A", S("anx", fontName="Times-Bold", fontSize=8.8,
                                   textColor=ACCENT2, spaceAfter=1)))
F.append(Paragraph("Club Charter \u2014 Definition, Purpose, Structure and Activities", st_doctitle))
F.append(Rule(thick=0.8, color=ACCENT, pad=2))
F.append(Spacer(1, 7))

F.append(Paragraph("A.1 &nbsp; Identity", st_h1))
idt = [
    [Paragraph("Name of the club", st_tdb), Paragraph("Maples Tech Club (MTC)", st_td)],
    [Paragraph("Institution", st_tdb), Paragraph("Maples Academy, Khatauli, District Muzaffarnagar, Uttar Pradesh", st_td)],
    [Paragraph("Motto", st_tdb), Paragraph("<i>Learn it. Build it. Ship it.</i>", st_td)],
    [Paragraph("Nature", st_tdb), Paragraph("A student club of the school. It is not commercial and not political, and it "
                                            "works under a teacher nominated by the Principal.", st_td)],
    [Paragraph("Open to", st_tdb), Paragraph("All students of Classes VI to XII, from every stream, whether or not they know "
                                             "anything about computers. No student will be turned away from an open "
                                             "session because of stream, marks, gender or background.", st_td)],
    [Paragraph("Proposed by", st_tdb), Paragraph("Harsh, Class XII, Roll No. 13", st_td)],
    [Paragraph("Meeting pattern", st_tdb), Paragraph("One session of two hours a week. I would suggest Saturday, after the last "
                                                     "period. Members may also use the computer laboratory for project "
                                                     "work during hours the school permits.", st_td)],
]
t = Table(idt, colWidths=[38*mm, W-38*mm])
t.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"),
                       ("BOX", (0,0), (-1,-1), 0.6, colors.HexColor("#9ca3af")),
                       ("INNERGRID", (0,0), (-1,-1), 0.35, RULE),
                       ("BACKGROUND", (0,0), (0,-1), BAND),
                       ("TOPPADDING", (0,0), (-1,-1), 5),
                       ("BOTTOMPADDING", (0,0), (-1,-1), 5)]))
F.append(t)

F.append(Paragraph("A.2 &nbsp; What the club <i>is</i> \u2014 a definition", st_h1))
F.append(Paragraph(
    "The club is a <b>workshop, not another class</b>. The rule I want to build it on is that "
    "at the end of every term, each member should have something they made themselves. A "
    "working web page. A small program. A robot that moves. A poster, a short film, a chart "
    "drawn from real data. Theory gets taught when it is needed for the thing being made. The "
    "club will not repeat the syllabus. It will use it.", st_body))
F.append(Paragraph(
    "The club would also <b>look after the school's digital work</b>. Once the registrations "
    "in Annexure C are done, members would help maintain the school website, the official "
    "email accounts, the Google Classroom sections, and the photographs and videos from school "
    "functions. Always under the faculty advisor. That way the school gets something back every "
    "week for the two hours it gives us.", st_body))

F.append(Paragraph("A.3 &nbsp; Vision and Mission", st_h1))
F.append(callout("Vision",
                 "No student should leave Maples Academy having only <i>read</i> about "
                 "technology. They should leave having <i>made</i> something with it.",
                 fill=BAND, bar=ACCENT))
F.append(Paragraph("<b>What the club promises to do:</b>", st_h2))
F.append(bullets([
    "Teach computing, AI and electronics by doing, free of cost, to any student of this school who wants to learn.",
    "Get hold of the free technology our school is entitled to, and look after it properly, so that the benefit reaches every student and teacher, not just club members.",
    "Train juniors so that the club keeps running after its seniors have left, including after I have left.",
    "Enter the school's name in competitions, olympiads, hackathons and national innovation challenges.",
    "Do real work for the school: the website, notices, results, event photography, posters and records.",
    "Teach students to use computers and AI safely and honestly, and take a firm line against copying.",
]))

F.append(Paragraph("A.4 &nbsp; Purpose \u2014 the eight objectives", st_h1))
pur = [
    [Paragraph("#", st_th), Paragraph("Objective", st_th), Paragraph("Why it matters to Maples Academy", st_th)],
    [Paragraph("1", st_tdc), Paragraph("Close the gap between syllabus and practice", st_tdb),
     Paragraph("CBSE now examines Artificial Intelligence and Information Technology as skill subjects. A student who "
               "has written code and run it understands the paper much better than one who has only learnt it by heart.", st_td)],
    [Paragraph("2", st_tdc), Paragraph("Get the school the free digital infrastructure it qualifies for", st_tdb),
     Paragraph("Official school email, cloud storage, Google Classroom and Microsoft Teams cost the school nothing, but "
               "only if it registers. The club does the registering and then the upkeep.", st_td)],
    [Paragraph("3", st_tdc), Paragraph("Give every member a verifiable portfolio", st_tdb),
     Paragraph("Work put up publicly is something a student can show to a college, a scholarship committee or an "
               "employer. Marks by themselves no longer make anyone stand out.", st_td)],
    [Paragraph("4", st_tdc), Paragraph("Build a self-sustaining peer-teaching chain", st_tdb),
     Paragraph("Members of Classes XI and XII teach Classes VI to X. So the club does not fall apart when its seniors "
               "pass out, and no extra teaching load falls on the staff.", st_td)],
    [Paragraph("5", st_tdc), Paragraph("Represent the school externally", st_tdb),
     Paragraph("Taking part, and winning, in olympiads, science fairs, hackathons and innovation challenges brings a "
               "name to the school and to Khatauli.", st_td)],
    [Paragraph("6", st_tdc), Paragraph("Digitise and support school operations", st_tdb),
     Paragraph("A website that is kept up to date, an online notice board, digital forms, event photographs and a "
               "results page. Done by students, checked by staff, without paying an agency.", st_td)],
    [Paragraph("7", st_tdc), Paragraph("Run the school's presence online", st_tdb),
     Paragraph("With your permission the club will set up and look after the school's official pages on "
               "Facebook, Instagram and the other platforms you approve, and will design the posters and "
               "notices for Annual Day, Sports Day, Science Exhibition, admissions and every other school "
               "function. Nothing is posted and nothing is printed without the Faculty Advisor approving it "
               "in writing first. This work is presently either not done at all or paid for outside; the "
               "club will do it free.", st_td)],
    [Paragraph("8", st_tdc), Paragraph("Teach digital safety and AI ethics", st_tdb),
     Paragraph("Students are already using AI and social media anyway. Teaching them properly about privacy, safe "
               "behaviour online, false information and honest work protects the school as much as the student.", st_td)],
    [Paragraph("9", st_tdc), Paragraph("Widen career horizons", st_tdb),
     Paragraph("Many students here will never hear about careers in software, data, design or hardware unless someone "
               "shows them, along with the free national platforms that teach these subjects.", st_td)],
]
F.append(table(pur, [8*mm, 47*mm, W-55*mm]))

F.append(Paragraph("A.5 &nbsp; Organisational structure", st_h1))
F.append(Paragraph(
    "Authority comes from the Principal to the Faculty Advisor, and only then to students. No "
    "student office-bearer handles money or discipline.", st_sub))
org = [
    [Paragraph("#", st_th), Paragraph("Office", st_th), Paragraph("Held by", st_th),
     Paragraph("Responsibility", st_th)],
    [Paragraph("1", st_tdc), Paragraph("Patron", st_tdb), Paragraph("The Principal", st_td),
     Paragraph("Gives permission, approves the year's plan and any outside participation, and has the final word on everything.", st_td)],
    [Paragraph("2", st_tdc), Paragraph("Faculty Advisor", st_tdb), Paragraph("One teacher nominated by the Principal", st_td),
     Paragraph("Present at every session. Signs every letter that leaves the club. Responsible for discipline, "
               "attendance and the safety of the members.", st_td)],
    [Paragraph("3", st_tdc), Paragraph("Coordinator", st_tdb), Paragraph("One teacher nominated by the Principal. May be the same person as the Faculty Advisor.", st_td),
     Paragraph("Holds the <b>Google Admin Console</b> and all administrator passwords, jointly with the Principal. "
               "Is the school's verified contact for Google, Microsoft, GitHub and Canva. Creates and closes "
               "accounts, and is answerable for data privacy and for which apps each class may use.", st_td)],
    [Paragraph("4", st_tdc), Paragraph("Core Committee", st_tdb), Paragraph("6 students of Classes XI\u2013XII", st_td),
     Paragraph("President, Vice-President, Secretary, Technical Lead, Design and Media Lead, Outreach Lead. They plan "
               "the sessions, keep the attendance register and report to the advisor every month.", st_td)],
    [Paragraph("5", st_tdc), Paragraph("Squad Leads", st_tdb), Paragraph("6 students, one per domain", st_td),
     Paragraph("Decide the week's work for their own squad and guide its members.", st_td)],
    [Paragraph("6", st_tdc), Paragraph("Core Members", st_tdb), Paragraph("Selected students, Classes VIII\u2013XII", st_td),
     Paragraph("Attend regularly, finish their term project, teach juniors and represent the school outside.", st_td)],
    [Paragraph("7", st_tdc), Paragraph("Open Members", st_tdb), Paragraph("Any student, Classes VI\u2013XII", st_td),
     Paragraph("Come to the open workshops and awareness sessions. There is no selection for this.", st_td)],
]
F.append(table(org, [8*mm, 26*mm, 40*mm, W-74*mm]))

F.append(Paragraph("A.6 &nbsp; The six domain squads", st_h1))
sq = [
    [Paragraph("Squad", st_th), Paragraph("What members learn", st_th), Paragraph("A typical term project", st_th)],
    [Paragraph("Web &amp; App Development", st_tdb),
     Paragraph("HTML, CSS, JavaScript, Git and GitHub, hosting, responsive design, basic databases", st_td),
     Paragraph("The official Maples Academy website and an online notice board", st_td)],
    [Paragraph("Artificial Intelligence &amp; Data", st_tdb),
     Paragraph("Python, data handling, charts and statistics, introductory machine learning, prompt literacy, AI ethics", st_td),
     Paragraph("A data study of school attendance or an image classifier trained on a small dataset", st_td)],
    [Paragraph("Robotics, IoT &amp; Electronics", st_tdb),
     Paragraph("Circuits, sensors, Arduino, micro:bit, 3D design and printing, automation", st_td),
     Paragraph("An automatic water-level alarm or a line-following robot for the science exhibition", st_td)],
    [Paragraph("Design &amp; Digital Media", st_tdb),
     Paragraph("Graphic design, typography, poster and magazine layout, photography, video editing", st_td),
     Paragraph("The complete visual identity and coverage of the Annual Day", st_td)],
    [Paragraph("Cyber Safety &amp; Digital Citizenship", st_tdb),
     Paragraph("Passwords and two-factor authentication, phishing and fraud, privacy, safe social media, fact-checking", st_td),
     Paragraph("A school-wide digital safety awareness drive and a parents' handout", st_td)],
    [Paragraph("Competitive Programming &amp; Logic", st_tdb),
     Paragraph("Problem solving, algorithms, data structures, olympiad and aptitude preparation", st_td),
     Paragraph("A school coding contest and entry to national olympiads", st_td)],
]
F.append(table(sq, [40*mm, 62*mm, W-102*mm]))

F.append(Paragraph("A.7 &nbsp; Annual calendar", st_h1))
cal = [
    [Paragraph("Term", st_th), Paragraph("Period", st_th), Paragraph("Focus", st_th), Paragraph("Deliverable", st_th)],
    [Paragraph("Term I", st_tdb), Paragraph("April \u2013 June", st_td),
     Paragraph("Recruitment, induction, fundamentals, digital hygiene", st_td),
     Paragraph("Every new member publishes a first small project", st_td)],
    [Paragraph("Term II", st_tdb), Paragraph("July \u2013 September", st_td),
     Paragraph("Squad specialisation; the school website goes live", st_td),
     Paragraph("Live school website; inter-house coding contest", st_td)],
    [Paragraph("Term III", st_tdb), Paragraph("October \u2013 December", st_td),
     Paragraph("Competitions, science exhibition, hackathon participation", st_td),
     Paragraph("<b>TechFest Maples</b> \u2014 an open exhibition for parents and feeder schools", st_td)],
    [Paragraph("Term IV", st_tdb), Paragraph("January \u2013 March", st_td),
     Paragraph("Board-exam-light term: documentation, peer teaching, handover", st_td),
     Paragraph("Annual report to the Principal; election of the next Core Committee", st_td)],
]
F.append(table(cal, [18*mm, 28*mm, 60*mm, W-106*mm]))
F.append(Spacer(1, 4))
F.append(Paragraph(
    "<b>Examinations.</b> The club will not meet during the four weeks before any school "
    "examination, and not at all during the board examination period. Attending the club will "
    "never be accepted in place of schoolwork. If a member's marks fall, the Faculty Advisor "
    "will keep that member out of the club until they come up again.", st_small))

# ================================================================ ANNEXURE B
F.append(PageBreak())
F.append(Paragraph("ANNEXURE B", S("anx2", fontName="Times-Bold", fontSize=8.8,
                                   textColor=ACCENT2, spaceAfter=1)))
F.append(Paragraph("Schedule of Benefits \u2014 What Registration Actually Gives the School", st_doctitle))
F.append(Rule(thick=0.8, color=ACCENT, pad=2))
F.append(Spacer(1, 7))

F.append(Paragraph(
    "Everything listed here is a programme run by the organisation named against it. I have not "
    "estimated or guessed any of it, and none of it asks the school to sign a paid contract. "
    "The official web address is given in every row so that the school can check it before "
    "agreeing to anything.", st_body))

F.append(Paragraph("B.1 &nbsp; What the school itself gets", st_h1))
inst = [
    [Paragraph("Programme", st_th), Paragraph("What Maples Academy receives", st_th),
     Paragraph("Eligibility", st_th), Paragraph("Cost", st_th)],

    [Paragraph("Google Workspace for Education Fundamentals<br/>"
               "<font size=7 color='#6b7280'>edu.google.com/workspace-for-education</font>", st_tdb),
     Paragraph("Official school Gmail on our own domain for every student and teacher; "
               "Google Classroom; Meet; Drive; Docs, Sheets, Slides, Forms and Sites; "
               "Calendar and Chat; a central Admin Console giving the school full control "
               "over every account; pooled cloud storage for the institution.", st_td),
     Paragraph("Accredited K\u201312 schools recognised by CBSE, ICSE or a State Board. "
               "Verification by Google.", st_td),
     Paragraph("FREE", st_tdg)],

    [Paragraph("Microsoft 365 Education (Office 365 A1)<br/>"
               "<font size=7 color='#6b7280'>microsoft.com/education/products/office</font>", st_tdb),
     Paragraph("Web and mobile Word, Excel, PowerPoint, Outlook and OneNote; Microsoft Teams "
               "for classes; 1 TB of OneDrive storage per user; SharePoint; School Data Sync; "
               "unlimited staff and student licences.", st_td),
     Paragraph("Accredited academic institutions, after academic verification by Microsoft.", st_td),
     Paragraph("FREE<br/>(A1 tier)", st_tdg)],

    [Paragraph("GitHub Education \u2014 Teachers &amp; Schools<br/>"
               "<font size=7 color='#6b7280'>github.com/education</font>", st_tdb),
     Paragraph("GitHub Classroom for distributing and auto-grading assignments; the GitHub "
               "Teacher Toolbox of professional developer tools; free GitHub Team with "
               "unlimited private repositories for verified teachers; free hosting for the "
               "school website via GitHub Pages.", st_td),
     Paragraph("A currently employed teacher at an accredited institution, verified with a "
               "school email address and faculty identification.", st_td),
     Paragraph("FREE", st_tdg)],

    [Paragraph("Canva for Education<br/>"
               "<font size=7 color='#6b7280'>canva.com/education</font>", st_tdb),
     Paragraph("The complete Canva Pro feature set for verified K\u201312 teachers and, through "
               "them, their students: premium templates, brand kit, background remover and "
               "classroom assignment tools \u2014 for school notices, magazines and event design.", st_td),
     Paragraph("Verified K\u201312 teachers and their schools. Students receive access "
               "through a teacher-created class.", st_td),
     Paragraph("FREE", st_tdg)],

    [Paragraph("Optional: .edu.in domain<br/>ERNET India, MeitY, Govt. of India<br/>"
               "<font size=7 color='#6b7280'>registry.ernet.in</font>", st_tdb),
     Paragraph("<b>Not needed for anything above.</b> We already own <i>mapleskhatauli.com</i> "
               "and every programme here accepts it. A <b>.edu.in</b> address only adds standing, "
               "marking the school as a recognised academic body. ERNET India, under MeitY, is "
               "the exclusive Government registrar. Worth considering later, never first.", st_td),
     Paragraph("Primary and secondary schools affiliated to CBSE, ICSE or a recognised "
               "State Board.", st_td),
     Paragraph("\u2248 &#8377;1,180<br/>per year<br/><font size=7>(incl. GST;<br/>cheaper in<br/>multi-year<br/>blocks)</font>", st_tdc)],

    [Paragraph("Atal Tinkering Laboratory<br/>Atal Innovation Mission, NITI Aayog<br/>"
               "<font size=7 color='#6b7280'>aim.gov.in</font>", st_tdb),
     Paragraph("A Government grant-in-aid of up to <b>&#8377;20 lakh</b> per school \u2014 &#8377;10 lakh "
               "for establishing the laboratory (3D printer, robotics and electronics kits, "
               "sensors, microcontrollers, tools) and &#8377;10 lakh towards operating expenses "
               "over five years.", st_td),
     Paragraph("Schools with Classes VI\u2013XII that can spare the built-up "
               "space. Applications open in announced windows.", st_td),
     Paragraph("GRANT<br/>to the school", st_tdg)],

    [Paragraph("Cisco Networking Academy<br/>"
               "<font size=7 color='#6b7280'>netacad.com</font>", st_tdb),
     Paragraph("Free, industry-recognised curricula in networking, cybersecurity, Python and "
               "IoT, with instructor training and student certificates of completion.", st_td),
     Paragraph("Schools and teachers enrolling as an academy.", st_td),
     Paragraph("FREE", st_tdg)],

    [Paragraph("Autodesk Education / Tinkercad<br/>"
               "<font size=7 color='#6b7280'>autodesk.com/education</font>", st_tdb),
     Paragraph("Free educational licences for professional design and engineering software, "
               "and Tinkercad \u2014 free browser-based 3D design, circuits and block coding "
               "designed for school classrooms.", st_td),
     Paragraph("Students and educators at accredited institutions; Tinkercad classrooms "
               "are open to schools.", st_td),
     Paragraph("FREE", st_tdg)],
]
F.append(table(inst, [40*mm, 66*mm, 34*mm, W-140*mm]))

F.append(Spacer(1, 6))
F.append(Paragraph("B.2 &nbsp; What each student and teacher gets", st_h1))
F.append(Paragraph(
    "These become available to our students once the school has its own email domain, because "
    "nearly all of them check eligibility through an institutional email address.", st_sub))
stu = [
    [Paragraph("Programme", st_th), Paragraph("What a Maples student receives", st_th),
     Paragraph("Eligibility", st_th)],

    [Paragraph("GitHub Student Developer Pack<br/>"
               "<font size=7 color='#6b7280'>education.github.com/pack</font>", st_tdb),
     Paragraph("A large bundle of professional developer software, cloud credits, domain names "
               "and learning subscriptions contributed by dozens of technology companies, free "
               "for the duration of the student's verified enrolment.", st_td),
     Paragraph("Aged 13 or above, currently enrolled in a degree- or diploma-granting "
               "programme \u2014 <b>which expressly includes school students</b>. Verified by "
               "school email or by a photograph of the school identity card.", st_td)],

    [Paragraph("Figma for Education<br/>"
               "<font size=7 color='#6b7280'>figma.com/education</font>", st_tdb),
     Paragraph("Free access to Figma's paid design and prototyping platform, including FigJam "
               "whiteboards \u2014 the industry standard for interface design.", st_td),
     Paragraph("Verified high-school students and educators, using a school-issued email "
               "address. Renewed annually.", st_td)],

    [Paragraph("JetBrains Educational Licence<br/>"
               "<font size=7 color='#6b7280'>jetbrains.com/…/education</font>", st_tdb),
     Paragraph("The full suite of JetBrains professional programming environments, free for "
               "the duration of study and renewable each year.", st_td),
     Paragraph("Students and teachers at accredited institutions, verified by academic "
               "email address or ISIC card.", st_td)],

    [Paragraph("Notion for Education<br/>"
               "<font size=7 color='#6b7280'>notion.com/…/notion-for-education</font>", st_tdb),
     Paragraph("The Notion Plus plan free for individual students and teachers \u2014 notes, "
               "project planning, club documentation and knowledge management.", st_td),
     Paragraph("Students and educators verifying with an education email address.", st_td)],

    [Paragraph("Microsoft Learn &amp; MakeCode<br/>"
               "<font size=7 color='#6b7280'>learn.microsoft.com/training</font>", st_tdb),
     Paragraph("Free structured learning paths in programming, cloud computing, data and AI; "
               "MakeCode provides block-based coding for micro:bit and Minecraft.", st_td),
     Paragraph("Open to all; progress and achievements are tracked against the account.", st_td)],

    [Paragraph("Google for Education learning tools<br/>"
               "<font size=7 color='#6b7280'>csfirst.withgoogle.com \u00b7 grasshopper.app</font>", st_tdb),
     Paragraph("CS First provides free, ready-made computer-science lesson plans for school "
               "clubs; Google's Applied Digital Skills and Be Internet Awesome cover digital "
               "literacy and online safety.", st_td),
     Paragraph("Free and open to schools and clubs worldwide.", st_td)],

    [Paragraph("Free open learning platforms<br/>"
               "<font size=7 color='#6b7280'>code.org \u00b7 scratch.mit.edu \u00b7 freecodecamp.org \u00b7 "
               "kaggle.com/learn \u00b7 cs50.harvard.edu \u00b7 swayam.gov.in \u00b7 skillsbuild.org</font>", st_tdb),
     Paragraph("Complete, free curricula from Code.org, MIT Scratch, freeCodeCamp, Kaggle "
               "Learn, Harvard CS50, the Government of India's SWAYAM and NPTEL, and IBM "
               "SkillsBuild \u2014 many with certificates.", st_td),
     Paragraph("Free and open; certificates typically require only free registration.", st_td)],

    [Paragraph("Artificial intelligence tools<br/>"
               "<font size=7 color='#6b7280'>academy.openai.com \u00b7 gemini.google \u00b7 "
               "copilot.microsoft.com</font>", st_tdb),
     Paragraph("<b>OpenAI Academy</b> offers free AI-literacy courses worldwide, including a "
               "K\u201312 educator track. The free tiers of ChatGPT, Google Gemini and Microsoft "
               "Copilot are available for supervised classroom demonstration. Google "
               "periodically offers Indian students extended AI plans at no cost.", st_td),
     Paragraph("Free tiers are open to all. <b>Note:</b> OpenAI's dedicated free "
               "<i>ChatGPT for Teachers</i> plan is presently restricted to verified "
               "<b>U.S.</b> K\u201312 educators and is not yet offered in India; Google's "
               "student AI offers generally require the user to be 18 or above. The club "
               "will use only what is lawfully and freely available here.", st_td)],
]
F.append(table(stu, [43*mm, 62*mm, W-105*mm]))

F.append(Spacer(1, 5))
F.append(callout(
    "One thing I want to be honest about",
    "I have marked the two limitations above instead of leaving them out. Two offers that are "
    "talked about a great deal, OpenAI's free teacher plan and some of Google's AI plans for "
    "students, are restricted by country or by age and would not apply to us at present. As "
    "far as I have been able to check, everything else in this annexure is available to an "
    "Indian CBSE school right now. Even so, please have each one verified on the official link "
    "before the school commits to it. I would rather be corrected now than have the school "
    "rely on something I have got wrong.",
    fill=colors.HexColor("#fff7ed"), bar=colors.HexColor("#c2410c")))

# ================================================================ ANNEXURE C
F.append(PageBreak())
F.append(Paragraph("ANNEXURE C", S("anx3", fontName="Times-Bold", fontSize=8.8,
                                   textColor=ACCENT2, spaceAfter=1)))
F.append(Paragraph("Registration Roadmap \u2014 Sequence, Documents, Costs and Owners", st_doctitle))
F.append(Rule(thick=0.8, color=ACCENT, pad=2))

F.append(Paragraph(
    "Google, Microsoft and GitHub identify a school by its <b>domain name</b>, and we already "
    "own <b><i>mapleskhatauli.com</i></b>. What follows is mostly form-filling, and the school "
    "may stop after any phase.", st_body))

road = [
    [Paragraph("#", st_th), Paragraph("Action", st_th), Paragraph("Documents required", st_th),
     Paragraph("Owner", st_th), Paragraph("Time", st_th), Paragraph("Cost", st_th)],

    [Paragraph("0", st_tdc), Paragraph("<b>Permission</b><br/>The Principal approves the club and names the "
                                       "Faculty Advisor and the Coordinator.", st_td),
     Paragraph("This application, and a line in writing from the Principal naming the two teachers.", st_td),
     Paragraph("Principal", st_td), Paragraph("1 week", st_tdc), Paragraph("Nil", st_tdg)],

    [Paragraph("1", st_tdc), Paragraph("<b>Prove we own the domain</b><br/>Add the short verification "
                                       "record Google gives us. Nothing about the existing "
                                       "website or its email changes.", st_td),
     Paragraph("The login for wherever <i>mapleskhatauli.com</i> was bought. The office, or "
               "whoever built the present website, will have it. <b>The one thing to confirm "
               "before starting.</b>", st_td),
     Paragraph("Coordinator, with the club", st_td),
     Paragraph("1\u20132 days", st_tdc), Paragraph("Nil", st_tdg)],

    [Paragraph("2", st_tdc), Paragraph("<b>Verify our eligibility with Google</b><br/>Fill the Education "
                                       "Fundamentals sign-up on <i>mapleskhatauli.com</i> so "
                                       "Google records us as a recognised school.", st_td),
     Paragraph("School name, type, website, strength, address and telephone &#183; the verified "
               "domain &#183; a scan of the affiliation certificate &#183; a contact email not "
               "on the school domain.", st_td),
     Paragraph("Coordinator", st_td), Paragraph("2 weeks", st_tdc), Paragraph("FREE", st_tdg)],

    [Paragraph("3", st_tdc), Paragraph("<b>Set up the Google Admin Console</b><br/>Create teacher and "
                                       "student accounts, group them by class, switch on the "
                                       "privacy and filtering settings, and decide which apps "
                                       "each class may use.", st_td),
     Paragraph("A list of staff and students by class. Nothing else. The Console is the school's "
               "permanent control panel; the Principal and Coordinator hold the passwords.", st_td),
     Paragraph("Coordinator, with the club", st_td), Paragraph("1 week", st_tdc),
     Paragraph("FREE", st_tdg)],

    [Paragraph("4", st_tdc), Paragraph("<b>Microsoft 365 Education</b><br/>Start the education sign-up, get through "
                                       "Microsoft's academic check, then hand out the free A1 "
                                       "licences.", st_td),
     Paragraph("The school domain &#183; administrator details &#183; proof that we are a school, "
               "if the automatic check does not clear it.", st_td),
     Paragraph("Coordinator", st_td), Paragraph("1\u20132 weeks", st_tdc), Paragraph("FREE", st_tdg)],

    [Paragraph("5", st_tdc), Paragraph("<b>GitHub Education</b><br/>A teacher applies and opens GitHub "
                                       "Classroom. Students then apply for the Student Pack.", st_td),
     Paragraph("School email address &#183; a photograph of the teacher's identity card, or a "
               "letter confirming employment &#183; for students, the school identity card.", st_td),
     Paragraph("Coordinator, then members", st_td), Paragraph("1 week", st_tdc), Paragraph("FREE", st_tdg)],

    [Paragraph("6", st_tdc), Paragraph("<b>Canva for Education</b> and the other programmes that need a teacher to "
                                       "verify. Then give out accounts to staff and students.", st_td),
     Paragraph("School email address and teacher verification.", st_td),
     Paragraph("Coordinator", st_td), Paragraph("1 week", st_tdc), Paragraph("FREE", st_tdg)],

    [Paragraph("7", st_tdc), Paragraph("<b>Refresh the school website</b> on our existing domain, built and "
                                       "looked after by the club's Web squad.", st_td),
     Paragraph("All text and photographs approved by the school first. Hosting is free on GitHub Pages.", st_td),
     Paragraph("Club, supervised", st_td), Paragraph("3\u20134 weeks", st_tdc), Paragraph("FREE", st_tdg)],

]
F.append(table(road, [10*mm, 42*mm, 59*mm, 21*mm, 14*mm, W-146*mm], pad=1.85, fs=7.9))

F.append(Spacer(1, 1))
F.append(callout(
    "What the school actually pays",
    "<b>Nothing. Not one rupee.</b> All eight phases are free, because the domain is already "
    "ours and every programme in Annexure&nbsp;B is free to verified schools. The two paid "
    "items in Annexure&nbsp;B are optional and the school need never take either.",
    fill=colors.HexColor("#ecfdf5"), bar=GREEN))

# ================================================================ ANNEXURE D
F.append(PageBreak())
F.append(Paragraph("ANNEXURE D", S("anx4", fontName="Times-Bold", fontSize=8.8,
                                   textColor=ACCENT2, spaceAfter=1)))
F.append(Paragraph("Member Selection Process", st_doctitle))
F.append(Rule(thick=0.8, color=ACCENT, pad=2))
F.append(Spacer(1, 7))

F.append(Paragraph(
    "The club will have <b>two doors</b>, and that is deliberate. Some selection is needed to "
    "keep project teams small enough to actually teach. But selection must never turn into a "
    "way of keeping students out of learning.", st_body))

doors = [
    [Paragraph("Open Track \u2014 no selection at all", st_th),
     Paragraph("Core Track \u2014 selected membership", st_th)],
    [Paragraph("Any student of Classes VI to XII can attend the club's open workshops, awareness "
               "sessions, guest talks, exhibition days and competitions. No test, no form, no "
               "previous knowledge and no limit on numbers. This is how most of the school will "
               "meet the club, and it is the club's main job.", st_td),
     Paragraph("A limited number of students are taken into the squads each year. They get "
               "regular guidance, laboratory time for their projects, team work and the chance "
               "to represent the school outside. In return they accept rules about attendance, "
               "conduct and teaching juniors.", st_td)],
]
t = Table(doors, colWidths=[W/2, W/2])
t.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("BACKGROUND", (0,0), (-1,0), ACCENT),
    ("BOX", (0,0), (-1,-1), 0.6, colors.HexColor("#9ca3af")),
    ("INNERGRID", (0,0), (-1,-1), 0.35, RULE),
    ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7),
]))
F.append(t)

F.append(Paragraph("D.1 &nbsp; How the first members are chosen", st_h1))
F.append(Paragraph("Two steps. An online test to shortlist, then one project to decide. No form to "
                   "buy, no interview panel, no probation period and no fee.", st_sub))

F.append(Paragraph(
    "Before the club exists there is nobody in it to run an intake, so I will conduct this "
    "first selection myself, <b>on behalf of the School Coordinator</b> and under whatever "
    "supervision you direct. Afterwards the President and Core Committee take it over.", st_body))

sel = [
    [Paragraph("Step", st_th), Paragraph("What happens", st_th),
     Paragraph("What is being judged", st_th), Paragraph("Weight", st_th)],

    [Paragraph("<b>1</b><br/><font size=7>Online test</font>", st_tdc),
     Paragraph("<b>25 questions in 30 minutes</b>, set as a Google Form, so it can be sat on a "
               "phone or a laboratory computer and marked automatically. Objective questions on "
               "<b>basic technical skills</b>: simple logic and patterns, elementary computer "
               "awareness, reading instructions correctly, ordinary arithmetic. <b>No "
               "programming is required and none is assumed.</b> Open to Classes VI to XII and "
               "marked class-wise, so a junior is never compared with a senior.", st_td),
     Paragraph("Clear thinking and care in reading. Not technical knowledge, and not speed.", st_td),
     Paragraph("40%", st_tdc)],

    [Paragraph("<b>2</b><br/><font size=7>A project</font>", st_tdc),
     Paragraph("Everyone who clears the test makes <b>one thing, of their own choosing</b>. No "
               "list, no fixed subject: a poster, a web page, a game, a working circuit, a short "
               "film, a model, a useful spreadsheet, a piece of writing about technology. One "
               "week, handed in with a few lines on what it is and what went wrong while making "
               "it. Beginners' attempts are expected and welcome.", st_td),
     Paragraph("Effort, and whether the student finished what they started. How polished it looks "
               "counts for very little.", st_td),
     Paragraph("60%", st_tdc)],

    [Paragraph("", st_tdc),
     Paragraph("<b>Results</b> go up on the school notice board. A student who is not selected "
               "stays a full Open Track member and may try again at the next intake.", st_td),
     Paragraph("\u2014", st_td), Paragraph("\u2014", st_tdc)],
]
F.append(table(sel, [17*mm, 72*mm, 46*mm, W-135*mm]))

F.append(Paragraph("D.1.1 &nbsp; The founding group", st_h1))
F.append(Paragraph(
    "A club cannot be built by a crowd on the first day. I am asking that it start with "
    "<b>four to six students</b>: myself, my friend <b>Vidhan</b>, and two to four others from "
    "the top of the selection above. We will set up the accounts, write the first sessions and "
    "get the routine working, after which the club opens to the whole school. Vidhan is in "
    "Class XII with me, so we both leave at the end of this session. That is exactly why I ask "
    "that <b>the remaining founding places go to students of Classes VIII to X</b>. They will "
    "have the club for years after we have gone, and they, not us, are the ones who will "
    "really run it.", st_body))

F.append(Paragraph("D.2 &nbsp; Principles binding the selection", st_h1))
F.append(bullets([
    "<b>No fee of any kind</b> for applying, or for being a member.",
    "<b>Previous experience is not a condition.</b> A complete beginner who finishes a simple task will be placed above an experienced student who submits nothing.",
    "<b>Places kept aside.</b> At least <b>40% of the places in every intake go to Classes VI to IX</b>, so the club keeps renewing itself. Girl students will be actively encouraged to apply.",
    "<b>Marks are not a condition either.</b> What matters is whether a student can keep up with the club without their studies suffering, and the Faculty Advisor decides that.",
    "<b>Everything is put up in advance.</b> The criteria and their weights go up before the intake starts, and any student who is not selected will be told, if they ask, what would make their next attempt stronger.",
    "<b>The Faculty Advisor can overrule</b> any selection or removal decision, and the Principal's decision is final in every case.",
    "<b>Not being selected does not mean being shut out.</b> Such a student stays a full Open Track member and can attend every workshop the club holds.",
]))

F.append(Paragraph("D.3 &nbsp; Continuing membership and removal", st_h1))
F.append(Paragraph(
    "Core membership is renewed every term on three conditions: at least 70% attendance, the "
    "term project finished, and conduct found satisfactory. The Faculty "
    "Advisor may remove a member for indiscipline, for misusing school equipment or the "
    "internet, for copying, or for breaking the code of conduct. In every such case the student "
    "will be heard first, and the matter will be reported to the Principal.", st_body))

F.append(Paragraph("D.4 &nbsp; Code of Conduct \u2014 to be signed by every member", st_h1))
F.append(Paragraph(
    "Every selected member signs this when they join. The Faculty Advisor keeps the signed "
    "copy.", st_sub))

coc = [
    [Paragraph("I, a member of the Maples Tech Club, undertake that \u2014", st_th)],
    [Paragraph("<b>1. My studies come first.</b> I will not allow club work to affect my "
               "attendance, homework or examinations, and I accept that the Faculty Advisor "
               "may keep me out of the club at any time if my marks start falling.", st_td)],
    [Paragraph("<b>2. I will respect school property.</b> I will use the computer laboratory, "
               "its machines, the internet connection and all equipment carefully, only for "
               "club purposes, only during permitted hours, and never without a teacher present.", st_td)],
    [Paragraph("<b>3. I will be honest in my work.</b> I will not copy another person's work "
               "and present it as mine. Where I use code, images, designs or text made by somebody "
               "else, including anything produced by an artificial intelligence tool, I will say "
               "so clearly. I understand that handing in AI output as my own work counts as "
               "copying.", st_td)],
    [Paragraph("<b>4. I will keep the school safe online.</b> I will not share my school "
               "account password, will not attempt to access any account or system that is not "
               "mine, will not install unapproved software, and will not visit or share "
               "inappropriate, pirated or unlawful material.", st_td)],
    [Paragraph("<b>5. I will publish nothing in the school's name without approval.</b> No "
               "website change, notice, poster, photograph, video or social media post "
               "representing Maples Academy will be issued by me without the prior written "
               "approval of the Faculty Advisor.", st_td)],
    [Paragraph("<b>6. I will protect others' privacy.</b> I will not photograph, record or "
               "publish any student or teacher without their knowledge and consent, and I will "
               "not share anyone's personal data.", st_td)],
    [Paragraph("<b>7. I will teach what I learn.</b> I will help juniors and new members "
               "willingly, and I will not mock or discourage a beginner. Every member of this "
               "club started by knowing nothing.", st_td)],
    [Paragraph("<b>8. I will conduct myself with courtesy</b> towards teachers, staff, "
               "visitors and fellow students, in the club and when representing the school "
               "outside it.", st_td)],
    [Paragraph("<b>9. I accept the authority of the Faculty Advisor and the Principal</b> in "
               "all matters concerning the club, and I understand that breach of this "
               "undertaking may result in my removal from the club and in action under the "
               "school's ordinary disciplinary rules.", st_td)],
]
t = Table(coc, colWidths=[W])
t.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("BACKGROUND", (0, 0), (0, 0), ACCENT),
    ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#9ca3af")),
    ("INNERGRID", (0, 0), (-1, -1), 0.35, RULE),
    ("TOPPADDING", (0, 0), (-1, -1), 3.7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3.7),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
]))
F.append(t)
F.append(Spacer(1, 7))

sgn = [[Paragraph("<br/><br/>______________________________<br/>"
                  "<b>Signature of Member</b><br/>Name &amp; Class", st_td),
        Paragraph("<br/><br/>______________________________<br/>"
                  "<b>Faculty Advisor</b><br/>Signature &amp; Date", st_td)]]
t = Table(sgn, colWidths=[W/2]*2)
t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                       ("LEFTPADDING", (0, 0), (-1, -1), 0),
                       ("RIGHTPADDING", (0, 0), (-1, -1), 10)]))
F.append(t)

# ================================================================ ANNEXURE E
F.append(PageBreak())
F.append(Paragraph("ANNEXURE E", S("anx5", fontName="Times-Bold", fontSize=8.8,
                                   textColor=ACCENT2, spaceAfter=1)))
F.append(Paragraph("Governance, Safeguards, Budget and Measurable Outcomes", st_doctitle))
F.append(Rule(thick=0.8, color=ACCENT, pad=2))
F.append(Spacer(1, 7))

F.append(Paragraph("E.1 &nbsp; Safeguards \u2014 addressing the school's legitimate concerns", st_h1))
saf = [
    [Paragraph("Concern", st_th), Paragraph("Safeguard offered", st_th)],
    [Paragraph("Will studies suffer?", st_tdb),
     Paragraph("One session a week, after school hours. Nothing at all in the four weeks before any "
               "examination, or during the board examinations. If a member's marks fall, the Faculty Advisor "
               "keeps them out until they recover.", st_td)],
    [Paragraph("Who controls the accounts and data?", st_tdb),
     Paragraph("The <b>school</b> does. The school owns the domain and every account made under it. The "
               "administrator passwords stay with the Faculty Advisor and the Principal. No student gets "
               "administrator rights. Accounts are switched off when a student leaves. Google Workspace for "
               "Education and Microsoft 365 Education are built for exactly this kind of control, through a "
               "single admin console.", st_td)],
    [Paragraph("Will students misuse internet access?", st_tdb),
     Paragraph("The laboratory is never used without a teacher present. Every member signs the code of "
               "conduct. Content filtering is switched on at administrator level for all school accounts. "
               "Anything that goes wrong is reported to the Principal the same day.", st_td)],
    [Paragraph("Is the school's reputation at risk online?", st_tdb),
     Paragraph("Nothing goes out in the school's name without the Faculty Advisor approving it in writing "
               "first. That covers the website, notices, posters, photographs and social media. Photographs of "
               "students are only put up with their consent.", st_td)],
    [Paragraph("What if the founder leaves after Class XII?", st_tdb),
     Paragraph("The structure is built against exactly that. Every squad has a junior deputy. The Core "
               "Committee is elected fresh every year in Term IV. All records, passwords and project files are "
               "handed to the Faculty Advisor before the outgoing batch leaves.", st_td)],
    [Paragraph("What if the Faculty Advisor or the Coordinator leaves the school?", st_tdb),
     Paragraph("This is the more serious risk of the two, because the accounts are in the teacher's name. "
               "Three things protect against it. The <b>Principal holds the administrator passwords jointly "
               "with the Coordinator</b>, so access is never lost with one person. The accounts belong to the "
               "school's domain and not to any individual, so a new teacher is simply made administrator in "
               "the same console. And a written handover of passwords, records and files is required before "
               "either teacher is relieved, exactly as it is for the outgoing students.", st_td)],
    [Paragraph("Will this cost the school money later?", st_tdb),
     Paragraph("The free plans named in Annexure B are these companies' standing education offers. There is "
               "no obligation to upgrade to a paid plan, and the school can stop using any of them whenever it "
               "wants. No contract ties the school to paying anything later.", st_td)],
    [Paragraph("Is AI use appropriate for school students?", st_tdb),
     Paragraph("The club teaches students to <i>understand</i> AI: what these systems are, where they get "
               "things wrong, how to check them, and why handing in their output as your own work is "
               "dishonest. All of it is supervised, on approved free plans. Under the club's rules, submitting "
               "AI work without saying so is treated as copying.", st_td)],
]
F.append(table(saf, [48*mm, W-48*mm]))

F.append(Paragraph("E.2 &nbsp; What the club requests from the school", st_h1))
ask = [
    [Paragraph("#", st_th), Paragraph("Request", st_th), Paragraph("Detail", st_th), Paragraph("Cost", st_th)],
    [Paragraph("1", st_tdc), Paragraph("Formal sanction", st_tdb),
     Paragraph("Permission to start the Maples Tech Club as a recognised club of the school.", st_td),
     Paragraph("Nil", st_tdg)],
    [Paragraph("2", st_tdc), Paragraph("One Faculty Advisor", st_tdb),
     Paragraph("A teacher named by the Principal, preferably from Computer Science, Mathematics or Physics, to "
               "supervise one session a week.", st_td),
     Paragraph("Nil", st_tdg)],
    [Paragraph("3", st_tdc), Paragraph("One Coordinator", st_tdb),
     Paragraph("A teacher named by the Principal, who may be the same person, to verify the school with Google "
               "using <i>mapleskhatauli.com</i>, to hold the Google Admin Console, and to be the school's contact "
               "for Google, Microsoft, GitHub and Canva.", st_td),
     Paragraph("Nil", st_tdg)],
    [Paragraph("4", st_tdc), Paragraph("Computer laboratory access", st_tdb),
     Paragraph("Two hours a week outside teaching hours, and occasional extra time when we are preparing for a competition.", st_td),
     Paragraph("Nil", st_tdg)],
    [Paragraph("5", st_tdc), Paragraph("Signatures and documents", st_tdb),
     Paragraph("The Principal's signature and stamp on the sign-up forms, and copies of the affiliation and "
               "registration certificates, which Google, Microsoft and GitHub ask for.", st_td),
     Paragraph("Nil", st_tdg)],
    [Paragraph("6", st_tdc), Paragraph("Access to the domain account", st_tdb),
     Paragraph("The login for wherever <i>mapleskhatauli.com</i> was bought, so that Google's verification record "
               "can be added. The school office or whoever built the present website will have it.", st_td),
     Paragraph("Nil", st_tdg)],
    [Paragraph("7", st_tdc), Paragraph("Optional consumables budget", st_tdb),
     Paragraph("Entirely optional. Basic electronics parts, jumper wires, sensors, printing and materials for "
               "the exhibition. The club will also look for sponsorship, and will run without this if the "
               "school would rather not spend it.", st_td),
     Paragraph("&#8377;3,000 \u2013 &#8377;6,000 / yr<br/><font size=7>(optional)</font>", st_tdc)],
    [Paragraph("8", st_tdc), Paragraph("Notice board space", st_tdb),
     Paragraph("A small permanent corner of a notice board for our announcements and results.", st_td),
     Paragraph("Nil", st_tdg)],
]
F.append(table(ask, [8*mm, 40*mm, 82*mm, W-130*mm]))

F.append(Paragraph("E.3 &nbsp; Measurable outcomes for the first year", st_h1))
F.append(Paragraph("I request that the club be checked against these after twelve months, and "
                   "closed without any argument from me if it has clearly not met them.", st_sub))
kpi = [
    [Paragraph("By the end of Year One", st_th), Paragraph("Target", st_th)],
    [Paragraph("mapleskhatauli.com verified with Google and school accounts live", st_td), Paragraph("Yes", st_tdg)],
    [Paragraph("Official school email accounts issued to teachers and to Classes IX\u2013XII", st_td), Paragraph("100%", st_tdg)],
    [Paragraph("Google Workspace for Education and Microsoft 365 Education active", st_td), Paragraph("Both", st_tdg)],
    [Paragraph("Official school website live, built and maintained by students", st_td), Paragraph("Yes", st_tdg)],
    [Paragraph("Students attending at least one club session", st_td), Paragraph("150 +", st_tdg)],
    [Paragraph("Core members with a completed, documented project", st_td), Paragraph("40 +", st_tdg)],
    [Paragraph("Workshops and awareness sessions conducted", st_td), Paragraph("20 +", st_tdg)],
    [Paragraph("External competitions or olympiads entered", st_td), Paragraph("3 +", st_tdg)],
    [Paragraph("Teachers trained in Google Classroom or Microsoft Teams", st_td), Paragraph("10 +", st_tdg)],
    [Paragraph("Public technology exhibition for parents and the community", st_td), Paragraph("1", st_tdg)],
    [Paragraph("Licence cost to the school for all software obtained", st_td), Paragraph("&#8377;0", st_tdg)],
]
F.append(table(kpi, [W-30*mm, 30*mm]))

F.append(Spacer(1, 8))
F.append(callout(
    "In closing",
    "Every school in the country is being told to go digital. Most are waiting for someone to "
    "give them the means to do it. Maples Academy does not have to wait. It already qualifies "
    "for all of this, and it has students who are willing to do the work. I am asking for "
    "permission, one teacher, and two hours a week.<br/><br/>"
    "<b>Harsh, Class XII, Roll No. 13</b>"))

# ================================================================ CLOSING NOTE
F.append(Spacer(1, 10))
F.append(Rule(thick=0.5))
F.append(Spacer(1, 5))

F.append(Paragraph(
    "<b>Official websites, if you wish to check anything yourself.</b> &nbsp; "
    "Google Workspace for Education \u2014 edu.google.com/workspace-for-education &nbsp;\u00b7&nbsp; "
    "Microsoft 365 Education \u2014 microsoft.com/education/products/office &nbsp;\u00b7&nbsp; "
    "GitHub Education \u2014 github.com/education &nbsp;\u00b7&nbsp; "
    "GitHub Student Developer Pack \u2014 education.github.com/pack &nbsp;\u00b7&nbsp; "
    "ERNET India domain registry \u2014 registry.ernet.in &nbsp;\u00b7&nbsp; "
    "Atal Innovation Mission \u2014 aim.gov.in &nbsp;\u00b7&nbsp; "
    "Canva for Education \u2014 canva.com/education &nbsp;\u00b7&nbsp; "
    "Figma for Education \u2014 figma.com/education &nbsp;\u00b7&nbsp; "
    "Cisco Networking Academy \u2014 netacad.com &nbsp;\u00b7&nbsp; "
    "CS First \u2014 csfirst.withgoogle.com &nbsp;\u00b7&nbsp; "
    "OpenAI Academy \u2014 academy.openai.com", st_tiny))
F.append(Spacer(1, 4))
F.append(Paragraph(
    "Prepared by Harsh, Class XII, Roll No. 13, Maples Academy, Khatauli. The details, "
    "eligibility conditions and fees given here are the ones published by these organisations "
    "at the time of writing, and they do change from time to time. The school is requested to "
    "confirm them on the official links above before acting.", st_tiny))

doc.build(F)
print("written:", OUT)
