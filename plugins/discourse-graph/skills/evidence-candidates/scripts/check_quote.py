#!/usr/bin/env python3
"""Check that a quote appears word for word in a PDF, and on which page.

The PDF's text layer breaks lines, hyphenates words, flattens superscripts, and
interleaves figure legends, headers and footers with the body text, so a plain
text search fails on correct quotes. This check compares letters, digits, signs
and the symbols < > = ± × %, ignoring spaces and other punctuation. It matches
the quote in order against the PDF text and reports any PDF text it had to skip:

- No skips: the quote is verbatim.
- Long skips (a figure legend, a running header, a full-page figure): the quote is
  verbatim if each skipped passage really is an interruption. Look at them.
- A short skip (under 12 characters) is almost always a word, number or sign the
  quote left out, so the quote fails. A bare page number is the exception.
- Quote text missing from the PDF (a changed or added word) fails.

It can't tell whether a digit was superscript (10⁴ and 104 look the same), so
check exponents against the page by eye.

    python3 check_quote.py paper.pdf "The quoted sentence (Fig. 2E)."
    python3 check_quote.py paper.pdf --file quotes.txt     # one quote per line

Exits 0 if every quote is verbatim, 2 if some need their skipped text looked at,
and 1 if any quote fails. Needs PyMuPDF (pip install pymupdf).
"""
import argparse
import re
import string
import sys
import unicodedata

import fitz

KEEP = set(string.ascii_lowercase + string.digits + "<>=±×%≤≥~")
MIN_RUN = 8      # shortest piece of quote matched on its own
SHORT_SKIP = 12  # skipped PDF text shorter than this counts as left out of the quote


def norm(s):
    s = unicodedata.normalize("NFKC", s).lower()      # also turns ⁻⁴ into −4
    s = re.sub(r"-\s*\n\s*(?=[a-z])", "", s)         # rejoin words hyphenated at a line break
    s = re.sub(r"[-‐‑‒–—−](?=\s*\d)", "~", s)        # a dash or minus before a digit is a sign: keep it
    return "".join(ch for ch in s if ch in KEEP)      # drop spaces, other punctuation, Greek


def page_text(doc):
    """Normalized text of the whole document, plus the offset where each page starts."""
    texts = [norm(p.get_text()) for p in doc]
    starts, pos = [], 0
    for t in texts:
        starts.append(pos)
        pos += len(t)
    return "".join(texts), starts


def page_of(offset, starts):
    return max(i for i, s in enumerate(starts) if s <= offset) + 1


def align(q, t):
    """Match q in order against t as a series of runs, each as long as possible.

    Returns (runs, failed_at): runs are (q_start, q_end, t_start, t_end); failed_at is
    the position in q where matching stopped, or None if the whole quote matched.
    """
    runs, qpos, tpos = [], 0, 0
    while qpos < len(q):
        need = min(MIN_RUN, len(q) - qpos)
        if t.find(q[qpos:qpos + need], tpos) == -1:
            return runs, qpos
        lo, hi = need, len(q) - qpos
        while lo < hi:                                 # longest prefix still present
            mid = (lo + hi + 1) // 2
            if t.find(q[qpos:qpos + mid], tpos) != -1:
                lo = mid
            else:
                hi = mid - 1
        i = t.find(q[qpos:qpos + lo], tpos)
        runs.append((qpos, qpos + lo, i, i + lo))
        qpos, tpos = qpos + lo, i + lo
    return runs, None


VERBATIM, CHECK_SKIPS, NOT_VERBATIM = "verbatim", "verbatim if the skipped text is an interruption", "NOT VERBATIM"


def check(doc, quote):
    """Return (status, pages, notes). Status is VERBATIM, CHECK_SKIPS or NOT_VERBATIM."""
    t, starts = page_text(doc)
    q = norm(quote)
    runs, failed_at = align(q, t)
    notes, failed, skips = [], failed_at is not None, False
    if failed:
        notes.append(f'quote text not in the PDF from here: "{q[failed_at:failed_at + 30]}"')
    for (_, _, _, prev_end), (q_start, _, next_start, _) in zip(runs, runs[1:]):
        skipped = t[prev_end:next_start]
        before = q[max(0, q_start - 15):q_start]
        if len(skipped) < SHORT_SKIP:
            failed = True
            notes.append(f'the PDF has "{skipped}" after "...{before}" that the quote leaves out')
        else:
            skips = True
            notes.append(f'skipped {len(skipped)} chars after "...{before}": "{skipped[:50]}..." '
                         f'(fine if this is a legend, header or page break; not if it is part of the sentence)')
    status = NOT_VERBATIM if failed else CHECK_SKIPS if skips else VERBATIM
    if runs:
        first, last = page_of(runs[0][2], starts), page_of(runs[-1][3] - 1, starts)
        pages = f"p. {first}" if first == last else f"pp. {first}–{last}"
    else:
        pages = "?"
    return status, pages, notes


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("pdf")
    ap.add_argument("quote", nargs="?")
    ap.add_argument("--file", help="text file with one quote per line")
    args = ap.parse_args()
    if args.file:
        quotes = [l.strip() for l in open(args.file, encoding="utf-8") if l.strip()]
    elif args.quote:
        quotes = [args.quote]
    else:
        ap.error("give a quote or --file")

    doc = fitz.open(args.pdf)
    worst = 0
    for quote in quotes:
        status, pages, notes = check(doc, quote)
        worst = max(worst, {VERBATIM: 0, CHECK_SKIPS: 2, NOT_VERBATIM: 3}[status])
        head = quote if len(quote) <= 70 else quote[:67] + "..."
        print(f"{status}, {pages}  {head}")
        for n in notes:
            print(f"  {n}")
    sys.exit({0: 0, 2: 2, 3: 1}[worst])


if __name__ == "__main__":
    main()
