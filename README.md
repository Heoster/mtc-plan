# Maples Tech Club — proposal pack
**Harsh · Class XII · Roll No. 13 · Maples Academy, Khatauli, Muzaffarnagar, Uttar Pradesh**

The pack is finished and ready to print and submit. Your name, class and roll number are
already on it, and **the date fills itself in** — the PDF is stamped with whatever today's
date is in India each time you build it. Only three things are left, and they are listed
below.

## What's here

| File | What it is |
|---|---|
| `Maples_Tech_Club_Proposal_Principal.pdf` | **The main deliverable.** A 13-page formal A4 application to the Principal, with 6 annexures and a tear-off order sheet for the Principal's signature. Print and submit. |
| `maples-tech-club/` | The 6-page website. Open `index.html` in any browser. |
| `build_pdf.py` | Regenerates the PDF (`pip install reportlab` then `python3 build_pdf.py`). |
| `build_site.py` | Regenerates the website (`python3 build_site.py`). |
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

**The simple way — GitHub Pages.**

1. Create a GitHub account → new **public** repository named `maples-tech-club`
2. Upload every file from the `maples-tech-club/` folder
3. Repo **Settings → Pages → Source: main branch / root → Save**
4. Live in ~2 minutes at `https://<your-username>.github.io/maples-tech-club/`

The school already owns **`mapleskhatauli.com`**, so the finished site can be pointed at
that domain whenever the school wishes.

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
