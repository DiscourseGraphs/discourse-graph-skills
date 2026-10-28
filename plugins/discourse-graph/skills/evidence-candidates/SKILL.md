---
name: evidence-candidates
description: Use when capturing findings from papers as Evidence (EVD) candidates in a discourse graph (Roam, Obsidian, or another tool). Triggers include "make / stage evd candidates", "add this paper's finding as evidence", collecting literature evidence for a question, hypothesis, claim or model, mining a paper or literature search into the graph, or sharpening vague evidence statements into specific observations. Also use when staged evidence reads like a claim, lacks a verbatim quote or figure, or loses its source on promotion.
---

# Evidence candidates

An evidence candidate is one observation from a paper, staged so a person can review it and choose whether to promote it. Stage it; never promote it yourself. A reviewer should be able to judge a good candidate from the graph alone, using three things: the statement, the paper's own words, and the figure panel it was read from.

## 1. Orient

- **Read the graph's conventions** before writing anything:
  - the node format, e.g. `[[EVD]] - {statement} - [[@source]]`
  - the candidate tag, often `#evd-candidate`
  - the relation names and the citekey style
  - where staging goes

  In Roam they're in the graph guidelines. In an Obsidian vault they're in its `CLAUDE.md` or conventions notes. If the conventions leave something out, copy how existing staged candidates in the graph look.
- **Know the target.** This is the question, hypothesis or claim the evidence feeds. Link the existing node by its exact title, in the graph's typed form, e.g. `[[QUE]] - {question}`. If none exists, say that staging would create it.
- **Check what already exists** from this paper: evidence nodes and staged candidates. Don't restage an observation that's already there. If a new candidate overlaps an existing node, note the overlap for the reviewer.
- **Where to stage:** wherever the person says. If they haven't said, propose a place and confirm it before writing. Good choices are the graph's staging page if it has one, the person's own page, or today's entry.
- **If you can't check something here** (the conventions, the target or existing nodes): use the format in step 4 and the target as the person phrased it. List each unchecked item in the hand-off.

## 2. Find and read the paper

Find the PDF with the **figure-extraction** skill, step 1: Zotero, then the project folder, then ask. Read the paper itself before writing: the results, the figure legends and the methods. Take every number, organism and direction from the paper, never from memory.

## 3. Write each statement

Follow `references/evidence-rubric.md`. In short:
- One observation, in the past tense.
- Name the model system, what was measured, and the result, with the number, n and statistic when the paper gives them.
- Name the panel, e.g. `(Fig. 2E)`.
- Evidence is what was seen. What it means is a claim, so it doesn't belong in the statement.
- Keep it short enough to become a node title. If it runs long, move n and the statistic to the Observable and keep the result's number.

Two statements may read off the same panel and share its quote and image.

## 4. Fill every slot

The source block holds its candidates, and every candidate has a Quote, a Grounding and an Observable:

```
- **Source:** [[@{citekey}]] — {Authors Year}, {Journal} — {DOI} — {Zotero item KEY, or folder: filename}
  - {statement} #evd-candidate
    - **Quote:** "{the paper's own sentence stating this result}" (p. {N})
    - **Grounding:** Fig. {N}{panel} (p. {N}) · {source} · {method} · {verdict}
      - ![]({image})
    - **Observable:** {what was measured} · {how: method, design, statistics} · {in what: system, sample, n}
    - **Caveat:** {one limitation; repeat the line for each; optional}
    - **Why it matters:** {what this pins down for the target; optional}
    - **Informs:** [[{target node's exact title}]]
```

In Roam a target's title includes its type, so the link doubles the brackets, e.g. `[[[[QUE]] - Which genes …?]]`.

**When the graph has its own house style.** The graph's existing staged candidates may use other labels, or wrap each staged set in a header block, for example a dated block. Follow the graph's labels and wrapper, but keep every slot above.

- **Quote:**
  - Copy it from the PDF, usually from the Results or the figure legend. If the result appears only in the figure, quote the legend.
  - Write it as typeset, restoring symbols the text layer mangles, such as superscripts: `10⁻⁴`, not `10−4`.
  - Check it with `python3 {this skill's folder}/scripts/check_quote.py {pdf} "{quote}"`. A plain text search fails on correct quotes because of line breaks, hyphenation, superscripts and legends that interrupt the text. The script checks words, numbers, signs and `<` `>` `=` `±`, and gives one of three results:
    - `verbatim`: done.
    - `verbatim if the skipped text is an interruption`: it lists the PDF text it skipped. A legend, a header or a page break is fine. Words from the sentence mean the quote left something out.
    - `NOT VERBATIM`: copy the sentence again.

    The script can't see whether a digit is superscript, so check exponents against the page by eye.
  - The page is the PDF page where the quoted words are, or `(pp. 4–5)` when they span pages.
- **Grounding:** comes from the **figure-extraction** skill: the panel, the page the figure is printed on, the source file and the capture method, with the image beneath.
- **Observable:** the methods context, meaning what was measured, how, and in what.
- **Missing pieces:** each statement needs a figure or table to read it from and the methods context. If the paper doesn't supply one of them, stage the finding anyway. Add a Caveat that names what's missing, e.g. "n not stated" or "no figure; reported in text only".
- **The source stays the parent.** In Roam, the Discourse Graph plugin attaches the citation on promotion only when `[[@citekey]]` is in an ancestor block. In an Obsidian vault, the paper's source page plays this role. Follow the vault's own nesting under it.

**Citekey.** Find it in this order:
1. If the graph already has a source page for this paper, use that page's key.
2. Otherwise use the key from the reference manager. In Zotero that's the `citationKey` field, the BetterBibTeX key, or a `Citation Key:` line in Extra.
3. If Zotero holds the paper twice, use the key without a disambiguation suffix (`smith2021tension`, not `smith2021tensiona`). Mention the duplicate.
4. If the graph and Zotero disagree, use the graph's key and flag the mismatch.
5. If you can't confirm a key, write `CITEKEY-TO-CONFIRM` in its place. Don't write to the graph until it's replaced. Never make one up. The image can keep its first-author-and-year name.

**Missing source page.** In Roam, linking `[[@citekey]]` before its source page exists creates an empty page without the paper's metadata. If the page doesn't exist, say so in the hand-off. The person can import it from Zotero first.

## 5. Check before hand-off

- Each quote passes `check_quote.py`: `verbatim`, or its skipped text is only legends, headers or page breaks.
- Each image has a verdict from **figure-extraction** step 5. A falsified candidate is withdrawn, not presented.
- Each citekey and each target title was read from Zotero or the graph, or it's listed as unconfirmed.
- No candidate repeats an existing node.
- After writing to a graph, read the result back and confirm the nesting, the tag, the image and the links.

## 6. Hand off

Give the person a short list containing:
- each candidate's statement, citekey and verdict
- what you left out and why
- the pages that staging would create, such as a missing source page or target question
- anything unchecked or pending: a supplement, a citekey you couldn't confirm, or a step you couldn't check

Let them choose what to promote. Don't promote, merge or edit existing nodes unless asked.

## Common mistakes

- **A paraphrase with no Quote.** The quote is what lets a reviewer check the statement without opening the paper.
- **A claim dressed as evidence:** no system, no measured quantity. Sharpen it, or label it as the authors' claim.
- **Two findings in one statement.** Split them.
- **A citekey in a child block in Roam.** The citation won't follow the node on promotion.
- **An invented citekey or target title.**
- **Restaging an observation** the graph already holds.
