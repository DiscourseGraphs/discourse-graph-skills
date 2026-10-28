"""Regression test for evidence-candidates/scripts/check_quote.py.

Builds a small PDF with the layouts that broke earlier versions: a word hyphenated
across a line break, a figure legend inside a sentence, a full-page figure between
two text pages, and minus signs and inequalities. Then it checks that true quotes
pass, near-misses fail, and a dropped phrase is never reported as plain verbatim.

    python3 tests/test_check_quote.py
"""
import pathlib
import sys
import tempfile

import fitz

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "plugins/discourse-graph/skills/evidence-candidates/scripts"))
from check_quote import CHECK_SKIPS, NOT_VERBATIM, VERBATIM, check  # noqa: E402


def build_pdf(path):
    # The built-in font can't encode U+2212, so minus signs are plain hyphens here, as in
    # many real PDFs. The quotes below use the typeset −/⁻, which also tests that they match.
    doc = fitz.open()
    p1 = doc.new_page()
    y = 72
    for line in [
        "Knockout of Nf2 reduced uptake (p < 10-4, log fold change = -5.27, n = 3) and the ef-",
        "fect was robust across independent clones. A volcano plot also showed that Nf2 (p =",
        "Fig. 1. Screening overview. (A) Schematic of the screen. (B) Ranked genes.",
    ]:
        p1.insert_text((72, y), line, fontsize=9)
        y += 14
    doc.new_page().insert_text((72, 72), "(caption on next page)", fontsize=9)
    doc.new_page().insert_text(
        (72, 72), "2.21 × 10-7) was located away from the distribution (Fig. 1D).", fontsize=9)
    doc.save(path)


FIRST = ("Knockout of Nf2 reduced uptake (p < 10⁻⁴, log fold change = −5.27, n = 3) "
         "and the effect was robust across independent clones.")
VOLCANO = ("A volcano plot also showed that Nf2 (p = 2.21 × 10⁻⁷) was located away "
           "from the distribution (Fig. 1D).")

CASES = [
    (VERBATIM, FIRST, "hyphenated line break, typeset minus signs"),
    (VERBATIM, FIRST.replace("⁻", "-").replace("−", "-"), "plain hyphens as minus signs"),
    (CHECK_SKIPS, VOLCANO, "legend and a figure page inside the sentence"),
    (NOT_VERBATIM, FIRST.replace("p <", "p >"), "flipped inequality"),
    (NOT_VERBATIM, FIRST.replace("= −5.27", "= 5.27"), "lost sign"),
    (NOT_VERBATIM, FIRST.replace("reduced", "increased"), "changed word"),
    (NOT_VERBATIM, VOLCANO.replace("10⁻⁷", "10⁷"), "lost exponent sign"),
    (CHECK_SKIPS, FIRST.replace(" independent", ""), "dropped word: must not pass as plain verbatim"),
    (CHECK_SKIPS, FIRST.replace(" log fold change = −5.27,", ""), "dropped phrase: must not pass as plain verbatim"),
]


def main():
    with tempfile.TemporaryDirectory() as tmp:
        pdf = pathlib.Path(tmp) / "fixture.pdf"
        build_pdf(pdf)
        doc = fitz.open(pdf)
        failures = 0
        for expected, quote, what in CASES:
            status, pages, notes = check(doc, quote)
            # A dropped word may also be caught outright; either is acceptable as long as
            # it isn't reported as plain verbatim.
            good = status == expected or (expected == CHECK_SKIPS and status == NOT_VERBATIM
                                          and "dropped" in what)
            failures += not good
            print(f"{'ok' if good else 'WRONG':5s} {what}: {status} ({pages})")
            if not good:
                for n in notes:
                    print(f"        {n}")
    print(f"\n{len(CASES) - failures}/{len(CASES)} cases as expected")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
