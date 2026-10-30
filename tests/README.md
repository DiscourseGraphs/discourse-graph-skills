# Tests

## Script regression

```bash
python3 tests/test_check_quote.py
```

This builds a small PDF with the layouts that broke earlier versions of `check_quote.py`: a hyphenated line break, a legend inside a sentence, and a full-page figure between two text pages. It checks 9 cases: true quotes pass, near-misses fail (a flipped `<`, a lost minus sign, a changed word), and a dropped phrase is never reported as plain verbatim. Run it after any change to the script.

## Agent scenarios

Run these with a fresh agent after changing a skill. Point the agent at the two `SKILL.md` files, tell it to draft only (no writes to the graph or Zotero, no downloads), and ask for `draft.md`, the image files and a `log.md` ending in "Skill feedback". Compare the output against the checklist below.

| Scenario | Paper | Connected | Exercises |
|---|---|---|---|
| A. Zotero | Owen et al. 2017, MBoC, "A cytoskeletal clutch mediates cellular force transmission in a soft, three-dimensional extracellular matrix", DOI 10.1091/mbc.E17-02-0102. Question: "How do cells transmit force to a soft 3D extracellular matrix?" | Zotero, Roam (`matsulab`) | Zotero lookup; two duplicate items with keys `owen2017cytoskeletal` / `owen2017cytoskeletala`; a quote interrupted by a figure legend; no `@source` page in the graph |
| B. Folder only | Takahashi et al. 2025, Exp Cell Res, "A genome-wide CRISPR-Cas9 knockout screen … identifies Nf2 and Traf3 …", DOI 10.1016/j.yexcr.2025.114470, saved as `1-s2.0-S0014482725000667-main.pdf` in a folder with two unrelated PDFs. Question: "Which genes mediate dynamin-independent endocytosis?" | Nothing: no Zotero, no Roam | Identifying a PDF by its text; figure on p. 5 with its legend on p. 6; vector bar chart (Fig. 2E); unconfirmed citekey; unchecked conventions and target |

Checklist:
- **PDF:** found in the right place, in the right order, with one copy used throughout.
- **Statement:** past tense, one observation, names the system, observable, number and panel.
- **Quote:** passes `check_quote.py` and carries a page number.
- **Grounding:** a panel-level crop with the panel letter, axes and legend intact. The line names the page, the source file, the method and the verdict.
- **Observable:** says what was measured, how, and in what.
- **Citekey:** read from the graph or Zotero, or written as `CITEKEY-TO-CONFIRM`.
- **Hand-off:** lists unchecked items, pages that staging would create, and anything pending.

## Results, October 27, 2026

- **Baselines (no skill, default model).** Both runs wrote precise statements and clean crops. Neither included a verbatim quote or recorded where a crop came from. One cropped from the folder copy but cited the Zotero copy, and guessed a citekey (`takahashi2025genomewide`) that differs from Zotero's (`takahashiGenomewideCRISPRCas9Knockout2025`). Both spent many calls working out the graph's staging format. Tool calls: 59 (A) and 51 (B).
- **With the skills, round 1 (default model).** Every candidate had a verbatim quote and a full Grounding line. B used the placeholder instead of guessing a key. Tool calls: 72 (A) and 24 (B). The feedback led to the fixes in round 2.
- **With the skills, round 2 (A on the default model, B on Sonnet).** Both passed the checklist. Both found that `check_quote.py` ignored signs and `<`/`>`. That was fixed, and the regression test above was added. Not yet re-run after the final round of text edits.

## Standalone HTML proposal

Run `python3 tests/test_bundle_html.py` for the offline bundler contracts (7 tests), and `node --check plugins/discourse-graph/skills/create-standalone-html/assets/ui.js` for JavaScript syntax. The [rainwater example checklist](../plugins/discourse-graph/skills/create-standalone-html/examples/rainwater/README.md) covers manual browser behavior. Browser checks are pending because local-file rendering was blocked during preparation.
