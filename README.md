# Maples Tech Club — proposal pack
**Harsh · Class XII · Roll No. 13 · Maples Academy, Khatauli, Muzaffarnagar, Uttar Pradesh**

The pack is finished and ready to print and submit. Your name, class and roll number are
already on it, and **the date fills itself in** — the PDF is stamped with whatever today's
date is in India each time you build it. Only three things are left, and they are listed
below.

## What's here

| File | What it is |
|---|---|
| `Maples_Tech_Club_Proposal_Principal.pdf` | **The main deliverable.** A 12-page formal A4 application to the Principal, with 5 annexures (A–E). Dated **12 October 2026**. Print and submit. |
| `maples-tech-club/` | The website as published — 6 pages, a 404, the PDF, plus `_headers` and `_redirects`. Open `index.html` in any browser. Committed on purpose: Netlify uploads this folder without rebuilding it. |
| `build_pdf.py` | Regenerates the PDF (`pip install reportlab` then `python3 build_pdf.py`). |
| `build_site.py` | Regenerates the website (`python3 build_site.py`). Also calls `build_pdf.py`, so this one command rebuilds everything. |
| `fonts/` | DejaVu Serif and Sans. Embedded in the PDF for `₹` and `☐`. Needed for the build to work anywhere without root. |
| `netlify.toml`, `runtime.txt`, `requirements.txt` | Netlify build configuration. |
| `deploy-netlify.sh` | Build, verify, then publish to Netlify in one command. |
| `push.sh` | Push this repository to GitHub in one command. |
| `NETLIFY.md`, `PUSH_TO_GITHUB.md` | Step-by-step for each, including the traps. |
| `Maples_Tech_Club_Poster.pdf` / `.png` | **Recruitment poster, A3.** Dark version — looks best on a screen, share the PNG on the class WhatsApp groups. |
| `Maples_Tech_Club_Poster_Print.pdf` / `.png` | Same poster, light background. **Use this one for the notice board** — it costs a fraction of the toner to print. |
| `build_poster.py` | Regenerates all four poster files. |
| `serve.py` | Runs the website locally **and rebuilds the PDF on every download**, so it is always dated today. |
| `.github/workflows/publish.yml` | Rebuilds and republishes the site to GitHub Pages every morning. |

## Before you submit the PDF

Only three things are left, and two of them are done with a pen after printing.

1. **Write your mobile number** on the `Mobile: ______` line on page 2. That is the only blank
   left for you in the whole document.
2. **Get the proposed faculty advisor to countersign page 2.** There is a signature block for
   it on the right. A teacher's signature makes a student proposal much harder to refuse, so
   do this before you hand it in, not after.
3. **Check the PIN code** on the page 1 letterhead. It currently says 251201. If Khatauli's PIN
   is different for your school, change it in `build_pdf.py` and re-run the script.

Two optional things:

- **The date looks after itself.** Re-run `python3 build_pdf.py` on the morning you submit and
  the letter and the order sheet will both carry that day's date. It uses India time, so a
  late-night or early-morning build still gives the right day.
- Print it on school letterhead if your school prefers applications that way.

If you ever need a date that is *not* today — say you are handing it in on Monday but building
it on Saturday — set the override near the top of `build_pdf.py` and re-run:

```python
APP_DATE_OVERRIDE = "5 November 2026"   # None = use today's date
```

## Running it locally

```
python3 serve.py          # then open http://localhost:8080
```

This is not a plain file server. When someone clicks the download link it checks
today's date in India, and if the PDF was not built today it **runs `build_pdf.py`
again before sending the file**. So the application anyone downloads is always
dated the day they downloaded it. Repeat downloads on the same day are served
from memory, so it stays fast.

## Putting the website online (free)

Two targets are set up. They do not conflict; run either or both.

**Netlify — the shorter URL, and the one to give the Principal.**

The project `mtc-plan` (owner CODEEX) is already configured. One command:

```bash
NETLIFY_AUTH_TOKEN=xxxxx ./deploy-netlify.sh --prod
```

No token to hand? Drag `mtc-plan-netlify-drop.zip` onto <https://app.netlify.com/drop>.
Full detail, including the Git-connected route: **`NETLIFY.md`**.

**GitHub Pages — rebuilds itself on a schedule.**

1. Create a **public** repository named `maples-tech-club`
2. Push this project to it — see **`PUSH_TO_GITHUB.md`**, or run `./push.sh`
3. Repo **Settings → Pages → Source: GitHub Actions**
4. Live in two or three minutes at `https://<your-username>.github.io/maples-tech-club/`

The school already owns **`mapleskhatauli.com`**, so the finished site can be pointed at
that domain whenever the school wishes.

### Fonts are committed, and that matters

The PDF prints `₹` and `☐`, neither of which exists in the PDF core fonts, so DejaVu is
embedded. Both faces live in `fonts/` and `build_pdf.py` looks there before any system
path. That is what lets the build run on Netlify, where there is no `sudo apt-get`. Do
not delete that folder.

### One thing to understand about the date

GitHub Pages only hands out files that already exist. **It cannot run Python when
a visitor clicks download**, so on Pages the PDF carries whatever date it had when
you last published.

Two ways round it, depending on how much you care:

- **Publish daily, automatically.** Upload the *whole project* (scripts included,
  not just the `maples-tech-club/` folder) and the included workflow at
  `.github/workflows/publish.yml` will rebuild and republish every morning at
  06:00 India time. The live PDF is then never more than a day old. Set
  **Settings → Pages → Source: GitHub Actions** and it runs by itself, free.
- **Host somewhere that runs Python** — Render, Railway or PythonAnywhere all have
  free tiers. Point them at `serve.py` and you get a genuinely per-download build.

Honestly, for handing a printed application to your Principal none of this matters
— you run `python3 build_pdf.py` on the morning you submit and the date is right.
The daily rebuild only matters for the copy sitting on the public website.

## The order things must happen in

The school **already owns `mapleskhatauli.com`**, which is the part that normally costs
money and takes weeks. Everything below is free.

1. Principal grants permission and names two teachers: a **Faculty Advisor** (runs the
   sessions) and a **Coordinator** (holds the Google Admin Console). May be one person.
2. **Prove we control the domain** — add Google's verification record. 1–2 days, ₹0.
3. **Verify educational eligibility with Google** using `mapleskhatauli.com` and the CBSE
   affiliation certificate.
4. **Set up the Google Admin Console** — accounts, class groups, data privacy, app access.
5. Microsoft 365 A1 → GitHub Education → Canva, Figma, JetBrains, Notion
6. Students individually claim GitHub Student Pack, Figma, JetBrains, Notion

**Total compulsory cost: ₹0.** An ERNET `.edu.in` address (~₹1,180/yr) is listed as an
*optional later credibility upgrade only* — nothing in the plan depends on it.

### Two things the school office must confirm first
- **Who controls the domain account** `mapleskhatauli.com` was registered through, and
  whether the renewal is paid up.
- **Whether email already runs on that domain.** If it does, say so during the Google
  sign-up and existing mail keeps working. If it does not, Google becomes the mail
  provider. Either way the plan is unchanged — the documents are written to cover both.

## Two things stated honestly in both documents
- OpenAI's free **ChatGPT for Teachers** plan is **U.S. K–12 only** — not available in India.
  Use OpenAI Academy (free, global) + free tiers of ChatGPT / Gemini / Copilot instead.
- Most headline "free AI for students" offers require the user to be **18+** and target
  college students.

Confirm every fee and eligibility rule on the official links before acting — they change.

## The poster

A3, ready to print. Two versions of the same design: dark for sharing on phones, light for
pinning on the notice board.

Three dates are hard-coded at the top of `build_poster.py`. Change them there and re-run
`python3 build_poster.py`:

```
TEST_DATE = "Saturday, 17 October 2026"
TEST_TIME = "11:00 am"
NAMES_BY  = "Wednesday, 14 October 2026"
```

Two things to know before you put it up:

- **Don't print it until the Principal has signed.** The poster says the club is awaiting
  approval, but advertising an intake before you have permission will annoy exactly the person
  you need on your side.
- **The ₹11,000+ figure is real and checked.** It is Canva Pro (₹4,500/yr) plus Microsoft 365
  Personal (₹6,899/yr) at India retail, September 2026. It is deliberately conservative — it
  counts only two of the eight tools listed. If a teacher challenges the number, that is the
  answer, and the small print on the poster already says it.

## A note on the writing

Every line of the PDF and the website was written in plain language on purpose. It reads like a
Class XII student wrote it, because that is who is signing it. Don't let anyone "polish" it into
officialese before you submit it. The honest bits are the persuasive bits, especially the
paragraph on page 2 about you leaving in a few months.

If you rebuild anything:

```
pip install reportlab
python3 build_pdf.py      # writes the PDF
python3 build_site.py     # writes the website and copies the PDF into it
```

Run them in that order. `build_site.py` reads the page count straight out of the PDF, so the
website can never quote a stale number.


## Final plan — what changed in the last revision

- **Dated 12 October 2026.** Pinned in `build_pdf.py` via `APP_DATE_OVERRIDE`. Set it back to
  `None` to go back to auto-dating. The GitHub Actions date check follows the override.
- **Annexure F (the order sheet) was removed**, along with the "Enclosed with this application"
  list and the "working on it for most of this year" line.
- **Parent/guardian involvement removed everywhere** — members sign the code of conduct themselves.
- **Selection has two steps.**
  **Step 1 — the online test (40%)**: 25 objective questions, 30 minutes, Google Form, basic
  technical skills, no coding, open to Classes VI–XII, marked class-wise.
  **Step 2 — a project (60%)**: everyone who clears the test makes *one thing of their own
  choosing*. There is no list and no fixed subject — a poster, a web page, a game, a circuit, a
  short film, a model, a spreadsheet, a piece of writing. One week, handed in with a few lines on
  what it is and what went wrong. Judged on effort and on finishing, not on polish.
  The interview panel and the 30-day probation stay removed.
- **Founding group**: Harsh, Vidhan and two to four others from the top of the selection — four to
  six in all. **Both Harsh and Vidhan are in Class XII** and leave at the end of this session, so
  the proposal asks that the remaining founding places go to students of **Classes VIII to X**.
  Harsh runs the first intake on behalf of the School Coordinator; afterwards the elected
  President and Core Committee take over.
- **Added to the letter**: a "Why me, and not somebody else" note, a request that the Principal
  speak to the management about domain/website access, and an explicit statement that nothing in
  the proposal is fixed.
- **Added**: an objective for running the school's Facebook/Instagram presence and designing
  function posters, and a safeguard answering what happens if a *teacher* leaves, not just the founder.

### One detail still blank
**Vidhan's class is now stated — Class XII** — in the letter (ask 3), in Annexure D.1.1 and on the
join page of the website. His **roll number** is still not stated anywhere, because it was never
supplied and inventing it would be wrong on a document going to the Principal. Give it and it will
be filled in everywhere in one pass.
