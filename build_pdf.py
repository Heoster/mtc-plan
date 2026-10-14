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
                                PageBreak, Flowable)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from datetime import datetime, timezone, timedelta

import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "Maples_Tech_Club_Proposal_Principal.pdf")

# ---- Date on the letter ---------------------------------------------------
# By default this is TODAY's date in India, worked out fresh every time the
# script runs, so the application is never dated in the past.
# Only set APP_DATE_OVERRIDE if you deliberately want a different date,
# e.g. APP_DATE_OVERRIDE = "5 November 2026"
APP_DATE_OVERRIDE = "15 October 2026"

# IST is permanently UTC+05:30 (India has no daylight saving), so a fixed
# offset is exact and needs no timezone database installed.
_IST = timezone(timedelta(hours=5, minutes=30))


def _today_in_india() -> str:
    """'27 September 2026' - no leading zero on the day, the way it is written here."""
    d = datetime.now(_IST)
    return f"{d.day} {d:%B %Y}"


APP_DATE = APP_DATE_OVERRIDE or _today_in_india()

# --- Unicode fallback fonts: the PDF core fonts have no rupee sign or ballot box ---
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
st_small    = S("small", fontSize=8.7, leading=11.8, textColor=MUTED)
st_tiny     = S("tiny", fontSize=7.6, leading=10, textColor=MUTED)

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


def table(data, widths, header=True, zebra=True, pad=4.5):
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
    canv.setFillColor(ACCENT)
    canv.rect(0, PAGE_H - 6.5 * mm, PAGE_W, 6.5 * mm, stroke=0, fill=1)
    canv.setFillColor(ACCENT2)
    canv.rect(0, PAGE_H - 8.1 * mm, PAGE_W, 1.6 * mm, stroke=0, fill=1)

    canv.setStrokeColor(RULE)
    canv.setLineWidth(0.5)
    canv.line(LM, 12.5 * mm, PAGE_W - RM, 12.5 * mm)
    canv.setFont("Times-Italic", 7.8)
    canv.setFillColor(MUTED)
    canv.drawString(LM, 9 * mm,
                    "Proposal for the Maples Tech Club  \u00b7  "
                    "Maples Academy, Khatauli, Uttar Pradesh")
    canv.setFont("Times-Bold", 8.2)
    canv.setFillColor(ACCENT)
    canv.drawRightString(PAGE_W - RM, 9 * mm, f"Page {doc.page}")
    canv.restoreState()


doc = BaseDocTemplate(
    OUT, pagesize=A4,
    leftMargin=LM, rightMargin=RM, topMargin=TM, bottomMargin=BM,
    title="Proposal for the Maples Tech Club \u2014 Maples Academy, Khatauli",
    author="Harsh, Class XII, Maples Academy, Khatauli",
    subject="Application to the Principal: a school technology club and "
            "registration for free education technology programmes",
    keywords="Maples Tech Club, Maples Academy Khatauli, Google Workspace for Education, "
             "Microsoft 365 Education A1, GitHub Education, mapleskhatauli.com",
)
frame = Frame(LM, BM, PAGE_W - LM - RM, PAGE_H - TM - BM, id="main",
              leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=on_page)])

F = []
W = PAGE_W - LM - RM

# ================================================================ LETTERHEAD
F.append(Spacer(1, 3))
F.append(Paragraph("MAPLES ACADEMY, KHATAULI", st_school))
F.append(Paragraph("Khatauli, District Muzaffarnagar, Uttar Pradesh \u2014 251201", st_schoolsub))
F.append(Rule(thick=1.1, color=ACCENT, pad=3))
F.append(Spacer(1, 6))
F.append(Paragraph("APPLICATION FOR PERMISSION TO ESTABLISH<br/>"
                   "THE <b>MAPLES TECH CLUB</b>", st_doctitle))
F.append(Paragraph("and to register the school for the free technology programmes "
                   "it already qualifies for", st_sub))
F.append(Rule(thick=0.7, color=RULE, pad=2))
F.append(Spacer(1, 8))

meta = [
    [Paragraph("<b>To</b>", st_tdb),
     Paragraph("The Principal<br/>Maples Academy, Khatauli<br/>District Muzaffarnagar, Uttar Pradesh", st_td),
     Paragraph("<b>Date</b>", st_tdb),
     Paragraph(APP_DATE, st_td)],
    [Paragraph("<b>From</b>", st_tdb),
     Paragraph("<b>Harsh</b>, Class XII, Roll No. 13<br/>Maples Academy, Khatauli", st_td),
     Paragraph("<b>Subject</b>", st_tdb),
     Paragraph("Permission to start a technology club, and to register the school "
               "for free software it is already eligible for", st_td)],
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
    "I am <b>Harsh</b> of Class XII, Roll No. 13. I want to start a small technology club "
    "in our school \u2014 the <b>Maples Tech Club</b> \u2014 and, with it, switch on software "
    "that Google, Microsoft, GitHub and others already give recognised schools for free. "
    "We qualify. We have never applied.", st_body))

F.append(numbered([
    "<b>Start the club.</b> One session a week, after school, under a teacher you name. "
    "Open to Classes VI to XII, any stream. We learn by making things \u2014 a page, a "
    "program, a robot, a poster \u2014 not by repeating the syllabus.",

    "<b>Register the school.</b> The companies above give official email, Classroom, "
    "Teams, cloud storage and design tools only to schools that ask. They identify a "
    "school by its domain name. <b>We already own <i>mapleskhatauli.com</i>.</b> That is "
    "the hard part. A teacher verifies it once with Google; after that, Workspace, "
    "Microsoft 365, GitHub Education and Canva are free for every teacher and student. "
    "Annexure B is the list, with the official link against each item. Annexure C is "
    "the steps. The club does the paperwork under the teacher you appoint.",

    "<b>Let four to six of us set it up.</b> Myself, my friend <b>Vidhan of Class XII</b>, "
    "and two to four juniors from the test in Annexure D. Vidhan and I leave this year, "
    "so those extra places should go to Classes VIII to X \u2014 they will actually run "
    "the club. After the first term it opens to the rest of the school.",
]))

F.append(callout(
    "What I need from you",
    "No money. Permission; <b>one teacher</b> as Faculty Advisor (and, if you wish, as "
    "Coordinator for the Google Admin Console \u2014 it can be the same person); the "
    "computer laboratory for <b>two hours a week</b>; and a word to the management so "
    "that teacher can add Google's verification record to <i>mapleskhatauli.com</i>. "
    "Without that last piece, registration cannot start.",
    fill=colors.HexColor("#ecfdf5"), bar=GREEN))

F.append(Paragraph(
    "I leave in a few months, so this is not for me. It is for the juniors, and because "
    "CBSE already treats AI and IT as skill subjects while colleges keep asking what a "
    "student has actually built. I found these programmes, dropped the ones that do not "
    "apply here, and wrote this application myself. If someone can carry the club better, "
    "I will hand it over.", st_body))

F.append(Paragraph(
    "Nothing here is fixed. Change the name, the timing, the numbers, the rules \u2014 or "
    "strike any of it out. Your decision on every point is final. Annexure E is how you "
    "should judge us after a year.", st_body))

sig = [
    [Paragraph("Yours obediently,", st_td), Paragraph("", st_td)],
    [Spacer(1, 12), Spacer(1, 12)],
    [Paragraph("<b>Harsh</b><br/>Class XII &nbsp;\u00b7&nbsp; Roll No. 13<br/>"
               "Maples Academy, Khatauli<br/>"
               "Mobile: ____________________", st_td),
     Paragraph("<b>Countersigned \u2014 Proposed Faculty Advisor</b><br/><br/>"
               "Name: ______________________________<br/><br/>"
               "Designation: _________________________<br/><br/>"
               "Signature: ___________________________", st_td)],
]
sigt = Table(sig, colWidths=[W*0.48, W*0.52])
sigt.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                          ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
F.append(KeepTogether([
    Paragraph(
        "I would be grateful for a few minutes to explain this in person. "
        "The club will work inside the school's timings, rules and discipline. Thanking you.",
        st_body),
    Spacer(1, 4),
    sigt,
]))

F.append(Spacer(1, 14))
F.append(Paragraph(
    "Annexures. &nbsp; A \u2014 what the club is &nbsp;\u00b7&nbsp; "
    "B \u2014 what registration gives the school &nbsp;\u00b7&nbsp; "
    "C \u2014 the steps &nbsp;\u00b7&nbsp; "
    "D \u2014 who joins, and the rules they sign &nbsp;\u00b7&nbsp; "
    "E \u2014 safeguards and one-year targets.", st_small))


# ================================================================ ANNEXURE A
# No forced page break: the letter's last lines sit with the signature,
# and Annexure A starts on whatever space is left.
F.append(Spacer(1, 10))
F.append(Paragraph("ANNEXURE A", S("anx", fontName="Times-Bold", fontSize=8.8,
                                   textColor=ACCENT2, spaceAfter=1)))
F.append(Paragraph("The Club \u2014 What It Is, Who Runs It, What We Do", st_doctitle))
F.append(Rule(thick=0.8, color=ACCENT, pad=2))
F.append(Spacer(1, 7))

idt = [
    [Paragraph("Name", st_tdb), Paragraph("Maples Tech Club (MTC)", st_td)],
    [Paragraph("School", st_tdb), Paragraph("Maples Academy, Khatauli, District Muzaffarnagar, Uttar Pradesh", st_td)],
    [Paragraph("Motto", st_tdb), Paragraph("<i>Learn it. Build it. Ship it.</i>", st_td)],
    [Paragraph("Nature", st_tdb), Paragraph("A student club. Not commercial, not political. A teacher nominated by the Principal is present at every session.", st_td)],
    [Paragraph("Open to", st_tdb), Paragraph("Classes VI to XII, every stream. Open sessions turn nobody away for marks, gender or background.", st_td)],
    [Paragraph("Proposed by", st_tdb), Paragraph("Harsh, Class XII, Roll No. 13", st_td)],
    [Paragraph("When", st_tdb), Paragraph("Two hours, once a week \u2014 Saturday after the last period, if that suits the school. No meetings in the four weeks before any examination, and none during the boards.", st_td)],
]
t = Table(idt, colWidths=[32*mm, W-32*mm])
t.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"),
                       ("BOX", (0,0), (-1,-1), 0.6, colors.HexColor("#9ca3af")),
                       ("INNERGRID", (0,0), (-1,-1), 0.35, RULE),
                       ("BACKGROUND", (0,0), (0,-1), BAND),
                       ("TOPPADDING", (0,0), (-1,-1), 5),
                       ("BOTTOMPADDING", (0,0), (-1,-1), 5)]))
F.append(t)

F.append(Paragraph("A.1 &nbsp; The idea", st_h1))
F.append(Paragraph(
    "A workshop, not another class. At the end of every term each member should have "
    "made one thing themselves. Theory is taught when the thing being made needs it. "
    "In return for the two hours, members also help with the school website, notices, "
    "photographs and the email accounts \u2014 always under the Faculty Advisor. "
    "Seniors teach juniors, so the club does not die when Class XII leaves.", st_body))

F.append(Paragraph("A.2 &nbsp; Who is in charge", st_h1))
F.append(Paragraph(
    "Authority runs Principal \u2192 Faculty Advisor \u2192 students. No student handles money or discipline.", st_sub))
org = [
    [Paragraph("Office", st_th), Paragraph("Held by", st_th), Paragraph("Does", st_th)],
    [Paragraph("Patron", st_tdb), Paragraph("The Principal", st_td),
     Paragraph("Gives permission. Final word on everything.", st_td)],
    [Paragraph("Faculty Advisor", st_tdb), Paragraph("One teacher you name", st_td),
     Paragraph("Present at every session. Signs every letter. Attendance, discipline, safety.", st_td)],
    [Paragraph("Coordinator", st_tdb), Paragraph("One teacher \u2014 may be the same person", st_td),
     Paragraph("Holds the Google Admin Console and all admin passwords, jointly with you. Creates and closes accounts. School contact for Google, Microsoft, GitHub and Canva.", st_td)],
    [Paragraph("Core Committee", st_tdb), Paragraph("Six students, Classes XI\u2013XII", st_td),
     Paragraph("President, Vice-President, Secretary, Technical Lead, Design Lead, Outreach Lead. Plan sessions, keep the register, report monthly.", st_td)],
    [Paragraph("Members", st_tdb), Paragraph("Core (selected) and Open (anyone)", st_td),
     Paragraph("Core members finish a term project and teach juniors. Open members come to workshops \u2014 no test, no limit.", st_td)],
]
F.append(table(org, [32*mm, 48*mm, W-80*mm]))

sq = [
    [Paragraph("Squad", st_th), Paragraph("They learn", st_th), Paragraph("A typical term project", st_th)],
    [Paragraph("Web &amp; Apps", st_tdb),
     Paragraph("HTML, CSS, JavaScript, Git, hosting", st_td),
     Paragraph("School website and an online notice board", st_td)],
    [Paragraph("AI &amp; Data", st_tdb),
     Paragraph("Python, charts, a first look at machine learning, AI ethics", st_td),
     Paragraph("A small data study, or an image classifier on a tiny set", st_td)],
    [Paragraph("Robotics &amp; Electronics", st_tdb),
     Paragraph("Circuits, Arduino, sensors, 3D design", st_td),
     Paragraph("A line-following robot or a water-level alarm for the exhibition", st_td)],
    [Paragraph("Design &amp; Media", st_tdb),
     Paragraph("Posters, photography, video, magazine layout", st_td),
     Paragraph("Visual identity and coverage of Annual Day", st_td)],
    [Paragraph("Cyber Safety", st_tdb),
     Paragraph("Passwords, phishing, privacy, honest use of AI", st_td),
     Paragraph("A school-wide safety drive and a parents' handout", st_td)],
    [Paragraph("Programming &amp; Logic", st_tdb),
     Paragraph("Problem solving, algorithms, olympiad practice", st_td),
     Paragraph("A school coding contest; entries to national olympiads", st_td)],
]
F.append(KeepTogether([
    Paragraph("A.3 &nbsp; Six squads", st_h1),
    table(sq, [42*mm, 62*mm, W-104*mm]),
]))

cal = [
    [Paragraph("Term", st_th), Paragraph("When", st_th), Paragraph("Focus", st_th), Paragraph("Done when", st_th)],
    [Paragraph("I", st_tdb), Paragraph("Apr \u2013 Jun", st_td),
     Paragraph("Recruitment, basics", st_td),
     Paragraph("Each new member publishes one small thing", st_td)],
    [Paragraph("II", st_tdb), Paragraph("Jul \u2013 Sep", st_td),
     Paragraph("Squad work; website", st_td),
     Paragraph("School website live; inter-house coding contest", st_td)],
    [Paragraph("III", st_tdb), Paragraph("Oct \u2013 Dec", st_td),
     Paragraph("Competitions, exhibition", st_td),
     Paragraph("TechFest Maples \u2014 open to parents and feeder schools", st_td)],
    [Paragraph("IV", st_tdb), Paragraph("Jan \u2013 Mar", st_td),
     Paragraph("Light term: write-up, teaching, handover", st_td),
     Paragraph("Report to you; next Core Committee elected", st_td)],
]
F.append(KeepTogether([
    Paragraph("A.4 &nbsp; The year", st_h1),
    table(cal, [16*mm, 26*mm, 52*mm, W-94*mm]),
]))


# ================================================================ ANNEXURE B
F.append(PageBreak())
F.append(Paragraph("ANNEXURE B", S("anx2", fontName="Times-Bold", fontSize=8.8,
                                   textColor=ACCENT2, spaceAfter=1)))
F.append(Paragraph("What Registration Actually Gives the School", st_doctitle))
F.append(Rule(thick=0.8, color=ACCENT, pad=2))
F.append(Spacer(1, 7))

F.append(Paragraph(
    "I have not guessed any of this. Each row is a real programme. The official address "
    "is there so you can check it before agreeing to anything. None of it is a paid contract.", st_body))

F.append(Paragraph("B.1 &nbsp; For the school", st_h1))
inst = [
    [Paragraph("Programme", st_th), Paragraph("What we get", st_th),
     Paragraph("Who it is for", st_th), Paragraph("Cost", st_th)],

    [Paragraph("Google Workspace for Education<br/>"
               "<font size=7 color='#6b7280'>edu.google.com/workspace-for-education</font>", st_tdb),
     Paragraph("School Gmail on our own domain for every student and teacher; "
               "Classroom, Meet, Drive, Docs, Sheets, Slides, Forms; a central Admin Console.", st_td),
     Paragraph("Accredited K\u201312 schools. Google verifies.", st_td),
     Paragraph("FREE", st_tdg)],

    [Paragraph("Microsoft 365 Education (A1)<br/>"
               "<font size=7 color='#6b7280'>microsoft.com/education/products/office</font>", st_tdb),
     Paragraph("Word, Excel, PowerPoint, Outlook, Teams; 1 TB OneDrive each; unlimited staff and student licences.", st_td),
     Paragraph("Accredited schools, after Microsoft's academic check.", st_td),
     Paragraph("FREE", st_tdg)],

    [Paragraph("GitHub Education<br/>"
               "<font size=7 color='#6b7280'>github.com/education</font>", st_tdb),
     Paragraph("GitHub Classroom, free private repositories for verified teachers, free hosting for the school website.", st_td),
     Paragraph("A teacher at an accredited school, verified with school email.", st_td),
     Paragraph("FREE", st_tdg)],

    [Paragraph("Canva for Education<br/>"
               "<font size=7 color='#6b7280'>canva.com/education</font>", st_tdb),
     Paragraph("Canva Pro for verified K\u201312 teachers and their students \u2014 notices, magazines, event design.", st_td),
     Paragraph("Verified K\u201312 teachers. Students join through a class.", st_td),
     Paragraph("FREE", st_tdg)],

    [Paragraph("Atal Tinkering Laboratory<br/>NITI Aayog &nbsp;\u00b7&nbsp; "
               "<font size=7 color='#6b7280'>aim.gov.in</font>", st_tdb),
     Paragraph("A government grant of up to <b>&#8377;20 lakh</b> \u2014 kits, a 3D printer, sensors \u2014 if we apply in an open window and can spare the space. Optional, and later.", st_td),
     Paragraph("Schools with Classes VI\u2013XII.", st_td),
     Paragraph("GRANT", st_tdg)],
]
F.append(table(inst, [44*mm, 68*mm, 38*mm, W-150*mm]))

F.append(Spacer(1, 4))
F.append(Paragraph(
    "Also free once we have school email, and not listed at length: Cisco Networking Academy, "
    "Autodesk / Tinkercad, Figma, JetBrains, Notion, Code.org, Scratch, SWAYAM, NPTEL. "
    "A <b>.edu.in</b> domain from ERNET (~&#8377;1,180 a year) is optional standing only \u2014 "
    "nothing above needs it. We already have <i>mapleskhatauli.com</i>.", st_small))

F.append(Paragraph("B.2 &nbsp; For each student", st_h1))
F.append(Paragraph(
    "These open once a student has a school email address.", st_sub))
stu = [
    [Paragraph("Programme", st_th), Paragraph("What a student gets", st_th)],

    [Paragraph("GitHub Student Developer Pack<br/>"
               "<font size=7 color='#6b7280'>education.github.com/pack</font>", st_tdb),
     Paragraph("Professional developer tools, cloud credits and learning subscriptions, free while enrolled. "
               "Open to school students aged 13+, verified by school email or a photo of the identity card.", st_td)],

    [Paragraph("Design and coding tools", st_tdb),
     Paragraph("Figma, JetBrains and Notion Plus, free for verified high-school students and teachers, renewed yearly.", st_td)],

    [Paragraph("Open courses", st_tdb),
     Paragraph("Code.org, MIT Scratch, freeCodeCamp, Harvard CS50, SWAYAM, IBM SkillsBuild \u2014 many with certificates, none paid.", st_td)],
]
F.append(table(stu, [50*mm, W-50*mm]))

F.append(Spacer(1, 4))
F.append(callout(
    "Two things that do <i>not</i> apply to us",
    "OpenAI's free ChatGPT-for-teachers plan is U.S. K\u201312 only. Some of Google's "
    "headline student-AI offers need the user to be 18. I have left both out. Everything "
    "else in this annexure, as far as I can check, is available to an Indian CBSE school "
    "today. Please still open the official link before the school commits.",
    fill=colors.HexColor("#fff7ed"), bar=colors.HexColor("#c2410c")))


# ================================================================ ANNEXURE C
F.append(PageBreak())
F.append(Paragraph("ANNEXURE C", S("anx3", fontName="Times-Bold", fontSize=8.8,
                                   textColor=ACCENT2, spaceAfter=1)))
F.append(Paragraph("The Steps \u2014 Sequence, Papers, Time, Cost", st_doctitle))
F.append(Rule(thick=0.8, color=ACCENT, pad=2))
F.append(Spacer(1, 6))

F.append(Paragraph(
    "Six steps, in this order. The school may stop after any of them.", st_body))

road = [
    [Paragraph("#", st_th), Paragraph("Action", st_th), Paragraph("Papers", st_th),
     Paragraph("Who", st_th), Paragraph("Time", st_th), Paragraph("Cost", st_th)],

    [Paragraph("0", st_tdc),
     Paragraph("<b>Permission.</b> You approve the club and name the Advisor and the Coordinator.", st_td),
     Paragraph("This application, and a line naming the two teachers.", st_td),
     Paragraph("Principal", st_td), Paragraph("1 week", st_tdc), Paragraph("Nil", st_tdg)],

    [Paragraph("1", st_tdc),
     Paragraph("<b>Prove we own the domain.</b> Add the short record Google gives us. The existing website does not change.", st_td),
     Paragraph("Login for wherever <i>mapleskhatauli.com</i> was bought. The office, or whoever built the site, will have it.", st_td),
     Paragraph("Coordinator", st_td), Paragraph("1\u20132 days", st_tdc), Paragraph("Nil", st_tdg)],

    [Paragraph("2", st_tdc),
     Paragraph("<b>Verify with Google</b> as a recognised school, on that domain.", st_td),
     Paragraph("Name, address, strength, phone; affiliation certificate; a contact email not on the school domain.", st_td),
     Paragraph("Coordinator", st_td), Paragraph("2 weeks", st_tdc), Paragraph("FREE", st_tdg)],

    [Paragraph("3", st_tdc),
     Paragraph("<b>Google Admin Console.</b> Teacher and student accounts, class groups, privacy and which apps each class may use.", st_td),
     Paragraph("A list of staff and students by class. You and the Coordinator hold the passwords.", st_td),
     Paragraph("Coordinator", st_td), Paragraph("1 week", st_tdc), Paragraph("FREE", st_tdg)],

    [Paragraph("4", st_tdc),
     Paragraph("<b>Microsoft 365, GitHub, Canva</b> \u2014 same pattern, using the school domain and a teacher's identity.", st_td),
     Paragraph("School email; teacher ID or a letter of employment; for students, the school identity card.", st_td),
     Paragraph("Coordinator", st_td), Paragraph("2\u20133 weeks", st_tdc), Paragraph("FREE", st_tdg)],

    [Paragraph("5", st_tdc),
     Paragraph("<b>School website</b> rebuilt on the same domain, looked after by the Web squad.", st_td),
     Paragraph("Text and photographs you have already approved. Hosting is free on GitHub Pages.", st_td),
     Paragraph("Club, supervised", st_td), Paragraph("3\u20134 weeks", st_tdc), Paragraph("FREE", st_tdg)],
]
F.append(table(road, [10*mm, 48*mm, 52*mm, 24*mm, 18*mm, W-152*mm], pad=3.2))

F.append(Spacer(1, 6))
F.append(Paragraph(
    "Compulsory cost of all six steps: <b>nothing.</b> The Atal Lab grant and a .edu.in address "
    "are optional and later. The school can drop any programme whenever it wants \u2014 there is no upgrade trap.", st_body))


# ================================================================ ANNEXURE D
F.append(PageBreak())
F.append(Paragraph("ANNEXURE D", S("anx4", fontName="Times-Bold", fontSize=8.8,
                                   textColor=ACCENT2, spaceAfter=1)))
F.append(Paragraph("Who Joins, and the Rules They Sign", st_doctitle))
F.append(Rule(thick=0.8, color=ACCENT, pad=2))
F.append(Spacer(1, 7))

F.append(Paragraph(
    "Two doors, on purpose. Project teams have to stay small enough to teach. "
    "That must never become a way of keeping students out of learning. "
    "No fee to apply or to belong. Beginners are expected.", st_body))

doors = [
    [Paragraph("Open Track \u2014 no selection", st_th),
     Paragraph("Core Track \u2014 selected", st_th)],
    [Paragraph("Any student of Classes VI to XII can come to workshops, talks, exhibition days "
               "and competitions. No test, no form, no previous knowledge, no cap on numbers. "
               "This is how most of the school will meet the club.", st_td),
     Paragraph("A limited number join the squads each year. They get regular guidance and "
               "laboratory time, and they may represent the school. In return: attendance, "
               "a term project, and teaching juniors.", st_td)],
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

F.append(Paragraph("D.1 &nbsp; How Core members are chosen", st_h1))
F.append(Paragraph(
    "Two steps. No form to buy, no interview, no probation. I will run the first intake "
    "myself, under the Coordinator, because the club does not yet exist to run it. After "
    "that the elected committee takes over. At least 40% of Core places go to Classes VI to IX. "
    "Girl students will be actively asked to apply. Marks are not a condition; the Advisor "
    "decides only whether a student can keep up without studies suffering.", st_body))

sel = [
    [Paragraph("Step", st_th), Paragraph("What happens", st_th),
     Paragraph("Judged on", st_th), Paragraph("Weight", st_th)],

    [Paragraph("<b>1</b><br/><font size=7>Online test</font>", st_tdc),
     Paragraph("<b>25 questions, 30 minutes</b>, a Google Form, sat on a phone or a lab computer. "
               "Simple logic, elementary computer awareness, reading instructions, ordinary arithmetic. "
               "<b>No programming.</b> Marked class-wise, so a Class VI student is never scored against Class XII.", st_td),
     Paragraph("Clear thinking. Not knowledge, not speed.", st_td),
     Paragraph("40%", st_tdc)],

    [Paragraph("<b>2</b><br/><font size=7>One thing</font>", st_tdc),
     Paragraph("Everyone who clears the test makes <b>one thing of their own choosing</b> in a week: "
               "a poster, a page, a game, a circuit, a short film, a model, a spreadsheet, a piece of writing. "
               "Handed in with a few lines on what it is and what went wrong. Beginners' attempts are welcome.", st_td),
     Paragraph("Effort, and finishing. Polish counts for very little.", st_td),
     Paragraph("60%", st_tdc)],
]
F.append(table(sel, [18*mm, 78*mm, 42*mm, W-138*mm]))

F.append(Paragraph(
    "Results go on the notice board. A student who is not selected stays a full Open member "
    "and may try again next intake. The Advisor can overrule any selection; your decision is final.", st_body))

F.append(Paragraph(
    "Core membership is renewed each term: 70% attendance, the project finished, conduct in order. "
    "The Advisor may remove a member for indiscipline, misuse of equipment or the internet, or copying "
    "\u2014 after hearing the student, and after reporting it to you.", st_body))

coc_head = [
    Paragraph("D.2 &nbsp; Code of Conduct \u2014 signed by every Core member", st_h1),
    Paragraph("The Faculty Advisor keeps the signed copy.", st_sub),
]

coc = [
    [Paragraph("I, a member of the Maples Tech Club, undertake that \u2014", st_th)],
    [Paragraph("<b>1. Studies first.</b> Club work will not touch my attendance, homework or exams. "
               "I accept being kept out if my marks fall.", st_td)],
    [Paragraph("<b>2. School property.</b> Laboratory, machines, internet \u2014 carefully, for club work, "
               "in permitted hours, never without a teacher present.", st_td)],
    [Paragraph("<b>3. Honest work.</b> I will not copy. If I use someone else's code, image or text, "
               "including anything an AI tool produced, I will say so. Handing in AI output as mine is copying.", st_td)],
    [Paragraph("<b>4. Safe accounts.</b> I will not share my password, touch anyone else's account, "
               "install unapproved software, or visit or share anything inappropriate or unlawful.", st_td)],
    [Paragraph("<b>5. Nothing in the school's name without approval.</b> No website change, notice, "
               "poster, photograph, video or social post as Maples Academy without the Advisor's written yes. "
               "I will not photograph or publish anyone without their consent.", st_td)],
    [Paragraph("<b>6. Courtesy, and teaching juniors.</b> I will not mock a beginner. I accept the "
               "Advisor's and the Principal's authority. Breach may mean removal, and ordinary school discipline.", st_td)],
]
t = Table(coc, colWidths=[W])
t.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("BACKGROUND", (0, 0), (0, 0), ACCENT),
    ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#9ca3af")),
    ("INNERGRID", (0, 0), (-1, -1), 0.35, RULE),
    ("TOPPADDING", (0, 0), (-1, -1), 4.2),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4.2),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
]))

sgn = [[Paragraph("<br/><br/>______________________________<br/>"
                  "<b>Signature of Member</b><br/>Name &amp; Class", st_td),
        Paragraph("<br/><br/>______________________________<br/>"
                  "<b>Faculty Advisor</b><br/>Signature &amp; Date", st_td)]]
sgnt = Table(sgn, colWidths=[W/2]*2)
sgnt.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                          ("LEFTPADDING", (0, 0), (-1, -1), 0),
                          ("RIGHTPADDING", (0, 0), (-1, -1), 10)]))
F.append(KeepTogether(coc_head + [t, Spacer(1, 8), sgnt]))


# ================================================================ ANNEXURE E
F.append(PageBreak())
F.append(Paragraph("ANNEXURE E", S("anx5", fontName="Times-Bold", fontSize=8.8,
                                   textColor=ACCENT2, spaceAfter=1)))
F.append(Paragraph("Safeguards and One-Year Targets", st_doctitle))
F.append(Rule(thick=0.8, color=ACCENT, pad=2))
F.append(Spacer(1, 7))

F.append(Paragraph("E.1 &nbsp; The questions you are entitled to ask", st_h1))
saf = [
    [Paragraph("Question", st_th), Paragraph("Answer", st_th)],
    [Paragraph("Will studies suffer?", st_tdb),
     Paragraph("One session a week, after school. Nothing in the four weeks before exams, or during the boards. Falling marks \u2192 out, until they recover.", st_td)],
    [Paragraph("Who owns the accounts?", st_tdb),
     Paragraph("The school. The domain and every account under it stay with Maples Academy. Admin passwords sit with you and the Coordinator. No student gets administrator rights. Accounts close when a student leaves.", st_td)],
    [Paragraph("Internet misuse?", st_tdb),
     Paragraph("No laboratory without a teacher. Code of conduct signed. Content filtering on at admin level. Anything that goes wrong is reported to you the same day.", st_td)],
    [Paragraph("The school's name online?", st_tdb),
     Paragraph("Nothing goes out without the Advisor's written approval \u2014 website, notices, posters, photographs, social media. Photographs of students only with consent.", st_td)],
    [Paragraph("What if the founder leaves?", st_tdb),
     Paragraph("Built for that. Every squad has a junior deputy. The committee is re-elected in Term IV. Records and files go to the Advisor before Class XII leaves.", st_td)],
    [Paragraph("What if the teacher leaves?", st_tdb),
     Paragraph("You hold the admin passwords jointly, so access is never in one person's pocket. Accounts belong to the school domain; a new teacher is simply made administrator. Written handover before either teacher is relieved.", st_td)],
    [Paragraph("Hidden cost later?", st_tdb),
     Paragraph("These are the companies' standing free education plans. No obligation to upgrade. The school can stop any of them whenever it wants.", st_td)],
]
F.append(table(saf, [42*mm, W-42*mm]))

F.append(Paragraph("E.2 &nbsp; Judge us on this after twelve months", st_h1))
F.append(Paragraph(
    "If we have clearly missed these, close the club. I will not argue.", st_sub))
kpi = [
    [Paragraph("By the end of Year One", st_th), Paragraph("Target", st_th)],
    [Paragraph("mapleskhatauli.com verified; school accounts live", st_td), Paragraph("Yes", st_tdg)],
    [Paragraph("School email issued to teachers and to Classes IX\u2013XII", st_td), Paragraph("100%", st_tdg)],
    [Paragraph("Google Workspace and Microsoft 365 both active", st_td), Paragraph("Both", st_tdg)],
    [Paragraph("School website live, built and kept by students", st_td), Paragraph("Yes", st_tdg)],
    [Paragraph("Students who attended at least one session", st_td), Paragraph("150+", st_tdg)],
    [Paragraph("Core members with a finished, documented project", st_td), Paragraph("40+", st_tdg)],
    [Paragraph("Workshops held \u00b7 competitions entered \u00b7 teachers trained on Classroom/Teams", st_td),
     Paragraph("20+ \u00b7 3+ \u00b7 10+", st_tdg)],
    [Paragraph("Public exhibition for parents \u00b7 licence cost to the school", st_td),
     Paragraph("1 \u00b7 &#8377;0", st_tdg)],
]
F.append(table(kpi, [W-38*mm, 38*mm]))

F.append(Spacer(1, 10))
F.append(callout(
    "In closing",
    "Most schools are waiting to be given the means to go digital. Maples Academy does not "
    "have to wait. It already qualifies, and it has students willing to do the work.<br/><br/>"
    "<b>Harsh, Class XII, Roll No. 13</b>"))

F.append(Spacer(1, 8))
F.append(Rule(thick=0.5))
F.append(Spacer(1, 5))
F.append(Paragraph(
    "Prepared by Harsh, Class XII, Roll No. 13, Maples Academy, Khatauli. Fees and eligibility "
    "are as these organisations published them at the time of writing; they do change. Please "
    "confirm each item on the official link in Annexure B before acting.", st_tiny))

doc.build(F)
print("written:", OUT)
