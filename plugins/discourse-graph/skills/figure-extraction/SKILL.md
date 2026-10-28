---
name: figure-extraction
description: Use when a statement drawn from a paper needs the figure panel or table it reports as an image, such as grounding an evidence, claim or caveat candidate, "screenshot / crop / grab the figure", or "find the PDF for this paper". Also use when the paper's PDF may be in Zotero, in a project folder, or not on hand yet. Works in any discourse graph (Roam, Obsidian, plain markdown) and with whatever PDF and reference-manager tools are connected.
---

# Figure extraction

A grounding image lets a reviewer judge a statement against the data instead of against your paraphrase. That works only if the image shows exactly what the statement reports, and anyone can tell which file and page it came from.

This protocol says what to do at each step. `references/tools.md` lists known ways to do each step with specific tools: Zotero, PyMuPDF, poppler, PubMed Central, Roam and Obsidian. Use whatever is connected.

## 1. Find the PDF

Look in this order, and stop at the first place that has it:

1. **Zotero.** Search every library you can see: the personal library and each group library.
   - Many Zotero tools search only the default library until you switch, so a miss there is not a miss.
   - One search that covers all libraries at once, such as the database query in `references/tools.md`, also counts.
   - Search by first author and year, then by a distinctive title word.
   - If Zotero isn't connected, say so in the hand-off and go on to the folder.
   - If Zotero holds the paper twice, use the PDF of the item whose citekey you cite.
2. **The project's PDF folder.** Identify each file by its own text, using the DOI on its first pages or the title in its metadata. Filenames are often meaningless.
3. **Ask the person.** Name the paper and its DOI, and say where you looked. Offer to fetch an open-access copy if they want one.

Use that one copy for everything: reading, quotes and crops. If a second copy turns up later, keep using the first. Note where it came from, because the Grounding line in step 6 needs it.

## 2. Find the figure's page

Search the PDF text for the caption, meaning "Figure 4." or "Fig. 4" at the start of a line. A mid-sentence mention such as "as in Figure 4B" is a reference, not the caption.

The figure is usually on the caption's page. If that page has no figure, check the page before it, because some journals print the legend on the following page.

If text search finds nothing, as with scanned pages or captions drawn as graphics, render the pages and look.

## 3. Capture the figure

Render the region from the PDF.
- **An embedded image:** render at its native resolution, usually 300–400 dpi; check the embedded image's resolution.
- **A chart drawn as vector graphics:** it has no native resolution, so render it at 300–400 dpi.

Re-render the region. Never enlarge a small screenshot.

Sometimes the PDF can't give a clean image: a scanned page, a blurry low-resolution raster, or a figure you can't separate from the text around it. Then get the publisher's figure file instead. For open-access papers, PubMed Central serves each figure as an image. Publisher files are whole figures, so you still crop the panel.

Record which method you used: `pdf render`, `publisher file`, or `half page (low confidence)`.

## 4. Crop to the panel

Crop the one panel the statement reads off. Crop more than one only if the statement rests on more than one. Keep:
- the panel letter
- both axis labels and their tick values
- the legend or color bar
- any significance marks

Leave out neighboring panels. If an axis has no title, say so in the candidate's methods context, along with what it appears to show.

Look at the crop. Adjust the edges and look again, until nothing is cut off and nothing from a neighbor shows.

## 5. Check the panel against the statement

Check that the panel shows what the statement says: the direction, the comparison and the number. If the statement gives a number the text doesn't state, read it off the chart and mark it approximate (≈). Give one verdict:

| Verdict | Meaning |
|---|---|
| confirmed | The panel shows this. If the numbers come from the text or a table rather than the panel, write `confirmed (numbers from text)`. If the panel plots data processed differently from the reported numbers (uncorrected against corrected, say), also add a caveat. |
| rewritten | You corrected the statement from the panel. Say what changed. |
| falsified | The panel contradicts the statement. Don't stage it. Tell the person. |
| pending | No image yet, for example the PDF wasn't found or the panel is in a supplement the PDF lacks. Say what's missing. |

If the panel lives in supplementary material that isn't in the PDF, the verdict is pending. Say where the supplement is, usually the article's DOI page. Don't ground the statement with a different panel.

## 6. Name, record and attach

Name the file `{citekey}_fig{N}{panel}.png`, for example `smith2021tension_fig3B.png`. Until the citekey is confirmed, use the first author and year instead, for example `smith2021_fig3B.png`.

The Grounding line goes under the statement, with the image beneath it:

```
**Grounding:** Fig. 3B (p. 6) · Zotero PDF ABCD1234 · pdf render · confirmed
  ![](smith2021tension_fig3B.png)
```

Fill its five parts in this order:
1. The figure and panel.
2. The page: the PDF page the figure is printed on, even when its legend is on another page.
3. The source: `Zotero PDF {attachment key}`, or `folder: {filename}` for a file in the project folder. The attachment key is the PDF's own key, not the paper's item key.
4. The method from step 3.
5. The verdict from step 5.

Attach the image the way the graph does. In Roam, use the file upload and paste the returned URL. In an Obsidian vault, use its attachments folder. With no graph tool connected, save the image beside the draft and use the filename. When two statements read off the same panel, attach the image once and reuse it.

When several statements come from one paper, open the PDF once and crop all their panels in one pass.

## Common mistakes

- **Cropping from one copy and citing another.** The Grounding source must be the file you cropped.
- **Searching only the default Zotero library** and deciding the paper isn't there.
- **Matching folder PDFs by filename** instead of by DOI or title.
- **A Grounding line with no source or method**, so nobody can retrace the crop.
- **Enlarging a low-resolution crop** instead of re-rendering the region.
