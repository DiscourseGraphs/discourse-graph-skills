# How to write an evidence statement

Adapted from the Akamatsu lab's journal-club rubric, with the evidence bundle from the living-synthesis pipeline.

An evidence statement is in the **past tense** and names:

- **what was measured**: the observable
- **what the result was**: the outcome, with the number, n and statistic when the source gives them
- **what the model system was**: the cell type, organism, simulation or preparation

Example:

> `[[EVD]] - Knockdown of DNM2 reduced the transferrin internalization in neuronal differentiated CAD cells - [[@mcfarland2008rna]]`

## The four rules

1. **One observation per statement.** Two findings joined by "and" are two statements. A statement should be promotable to a node title almost verbatim.
2. **Evidence is not a claim.** Evidence is what was seen, and a claim is what it's taken to mean.
   - Claim: "Curvature makes tissue more fluid."
   - Evidence: "In a vertex model of epithelium on a spherical surface (N = 36–360 cells), increasing curvature lowered the T1-rearrangement energy barrier and raised cell self-diffusivity."

   If a sentence names no system and no measured quantity, it's a claim. Sharpen it, or label it as the authors' claim.
3. **Read it, don't recall it.** Every number, threshold, organism and direction comes from the source in front of you: the full text, a figure legend or the panel itself. If a number can be read only off a chart, write it as approximate (≈) and say so.
4. **Name the panel.** Each statement carries the figure panel or table it rests on (`Fig. 4D`, `Table 2`), so a reader can check it against the data and not against your paraphrase.

## The evidence bundle

A complete piece of evidence has three parts:
- the **observation**: the statement
- the **data artifact**: the figure panel or table, attached as the Grounding image
- the **methods context**: what was measured, how, and in what system or sample, with n

When the paper doesn't supply one of the three, keep the finding and add a caveat that names the gap. Don't drop the finding.

## Useful distinctions when reading

- **Quantitative beats qualitative.** "84% ± 5% of coated pits (92 pits, 4 cells)" is worth more than "most pits".
- **A control is evidence too**, and often the load-bearing kind. A perturbation that does nothing where the mechanism is absent is what separates a mechanism from a correlation.
- **Watch the gap between abstract and figure.** An abstract may say "exclusively" where the panel shows a distribution. Report what the panel shows.
- **When the legend, the text and a table disagree,** follow the one that carries the numbers, usually the table or the Results text. Add a caveat that names the conflict.
- **Separate what was measured from what the metric can support.** A periodicity score dropping is not the same as holes enlarging, even when the authors say it is.
- **Screens measure their readout.** A genetic screen scored by cell survival identifies genes whose loss changes survival. That those genes act in the pathway is the authors' hypothesis until a later experiment tests it.
