# Ways to do each step

`SKILL.md` says what to do. This file lists ways to do it with tools you may have. Use whatever is connected. Run Python with `python3`, or `py` on Windows. On Windows, save multi-line snippets to a `.py` file, because the `<<'EOF'` heredoc is bash-only.

## 1. Find the PDF

### Zotero MCP server (`zotero_*` tools)

- `zotero_list_libraries` lists the personal library and every group. `zotero_switch_library(library_id="<group id>", library_type="group")` points later calls at one of them. Switching lasts for the whole session, so switch back when you're done with `zotero_switch_library(library_id="0", library_type="default")`.
- `zotero_search_items("Owen 2017")` matches title, creator and year. Keep queries short: an author, or author and year. Extra words make the search stricter, not broader.
- `zotero_get_item_children(item_key)` gives the child attachments. The one with `application/pdf` is the PDF, and its **key** is the attachment key.
- The file is at `<Zotero data dir>/storage/<attachment key>/<filename>.pdf`. The data dir is `~/Zotero` on macOS and Linux, and `C:\Users\<you>\Zotero` on Windows, unless the user moved it (Zotero → Settings → Advanced → Files and Folders). Group files arrive only if the user's Zotero syncs them.
- `zotero_get_item_fulltext` returns text without figures. It's useful for quotes when no local file exists, but it can't ground a figure.

### Zotero database, read-only (no MCP needed)

Desktop Zotero keeps everything in `<data dir>/zotero.sqlite`. The query below searches every library at once. Opening the file with `?immutable=1` keeps it read-only and works while Zotero is running. Never write to this file.

```bash
sqlite3 'file:/Users/<you>/Zotero/zotero.sqlite?immutable=1' "
SELECT i.key AS item, a.key AS attachment, att.path, i.libraryID,
  (SELECT v2.value FROM itemData d2
     JOIN fields f2 ON f2.fieldID = d2.fieldID AND f2.fieldName = 'citationKey'
     JOIN itemDataValues v2 ON v2.valueID = d2.valueID
   WHERE d2.itemID = i.itemID) AS citekey
FROM items i
JOIN itemData d ON d.itemID = i.itemID
JOIN fields f ON f.fieldID = d.fieldID AND f.fieldName = 'title'
JOIN itemDataValues v ON v.valueID = d.valueID
LEFT JOIN itemAttachments att ON att.parentItemID = i.itemID AND att.contentType = 'application/pdf'
LEFT JOIN items a ON a.itemID = att.itemID
WHERE v.value LIKE '%cytoskeletal clutch%';"
```

- **`path`** is `storage:<filename>.pdf`, and the file lives under `<data dir>/storage/<attachment>/`.
- **An empty `attachment`** means that copy of the paper has no PDF.
- **`libraryID`** is 1 for the personal library. Anything else is a group.

### Project folder: identify each PDF by its own text

```bash
python3 - "/path/to/project-pdfs" <<'EOF'
import fitz, glob, re, sys  # PyMuPDF: pip install pymupdf
for path in sorted(glob.glob(sys.argv[1] + "/*.pdf")):
    doc = fitz.open(path)
    text = " ".join(doc[i].get_text() for i in range(min(2, len(doc))))
    doi = re.search(r'10\.\d{4,9}/[^\s"<>]+', text)
    print(path, "|", doc.metadata.get("title"), "|", doi.group(0) if doi else None)
EOF
```

Without PyMuPDF, `pdfinfo file.pdf` (from poppler) prints the metadata, and `pdftotext -l 2 file.pdf -` prints the first two pages.

### Open-access copy, only when the person agrees

Use the `paper-acquisition` skill if it's installed. Otherwise look up the DOI on Unpaywall or Europe PMC. Check that the download starts with `%PDF` and isn't an HTML error page.

## 2. Find the caption page (PyMuPDF)

A caption begins a line, and the character after the number isn't a letter. That rules out "Figure 3a" and mid-sentence references. This filter comes from the living-synthesis pipeline (`figure_pipeline.py`).

```python
import fitz
doc = fitz.open(pdf_path)

def caption_pages(fig):
    pats = [f"Figure {fig}", f"Fig. {fig}", f"FIGURE {fig}", f"FIG. {fig}", f"Fig {fig}"]
    for i, page in enumerate(doc):
        text = page.get_text()
        for pat in pats:
            j = text.find(pat)
            while j != -1:
                after = text[j + len(pat): j + len(pat) + 1]
                if (j == 0 or text[j - 1] == "\n") and not after.isalnum():
                    yield i, pat
                    break
                j = text.find(pat, j + 1)
```

With poppler only, `pdftotext -layout file.pdf out.txt` gives the text. Find the caption, then count the form feeds (`\f`) before it to get the page.

When the legend sits on the page after its figure, the figure page often carries a note such as "(caption on next page)". Searching for that string finds those figure pages directly. The automatic first guess under Capture looks only on the caption's page, so it misses this layout.

## 3. Capture

- **Native resolution.** `pdfimages -list -f 5 -l 5 file.pdf` prints the `x-ppi` of each embedded image. In PyMuPDF, `page.get_image_rects(xref)` gives an image's box in PDF points.
- **Preview a page** to find the panel: `doc[p].get_pixmap(dpi=100).save("page.png")`, then look at it.
- **Converting pixels to PDF points:** for any render at D dpi whose clip starts at (x₀, y₀) points, point = x₀ + pixel ÷ (D/72). The same holds for y. A whole-page render starts at (0, 0).
- **Render the region:** `doc[p].get_pixmap(dpi=400, clip=fitz.Rect(x0, y0, x1, y1)).save("crop.png")`. Coordinates are in PDF points. Re-render the clip; don't crop and enlarge a preview.
- **With poppler only:** `pdftoppm -r 300 -f 5 -l 5 -png file.pdf page` renders the page. Crop the panel with Pillow at that resolution.
- **Automatic first guess** (the living-synthesis pipeline's three methods, in order of precision):
  1. the embedded image nearest the caption (`page.get_images` / `get_image_bbox`)
  2. the union of vector drawings (`page.get_drawings()`) on the figure side of the caption, within the caption's text column
  3. a half page in that column, which is low confidence

  Treat the result as a starting point and crop to the panel by eye.
- **Edge check.** After cropping, every border should be blank. A dark pixel on an edge means something is cut off:

  ```python
  from PIL import Image
  im = Image.open("crop.png").convert("L"); w, h = im.size
  edges = [im.crop(b) for b in [(0,0,w,3), (0,h-3,w,h), (0,0,3,h), (w-3,0,w,h)]]
  print([min(e.getdata()) for e in edges])  # each above ~230; JPEG artifacts alone give ~240
  ```

- **Finding the gap between two panels.** The edge check can't see a neighbor's ink inside the crop. To place an edge in a tight gutter, count dark pixels per column (or per row) of a page render across the gap. The gutter is the run of zeros:

  ```python
  from PIL import Image
  im = Image.open("page.png").convert("L")
  band = im.crop((x0, y0, x1, y1))           # a strip spanning both panels, in render pixels
  w, h = band.size; px = band.load()
  print([sum(px[x, y] < 200 for y in range(h)) for x in range(w)])  # zeros = gutter
  ```

## 3b. Publisher figure files (PubMed Central)

Use this when the PDF can't give a clean image. The route comes from the living-synthesis pipeline's `xml-figure-extraction-protocol.md`, as used in May 2026. Check the URLs still respond before relying on them.

1. Find the PMC ID: `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:"<doi>"&format=json&resultType=core`. Use `pmcid`, and check that `isOpenAccess` is `Y`.
2. Get the full-text XML: `https://www.ebi.ac.uk/europepmc/webservices/rest/<PMCID>/fullTextXML`. Each `<fig>` has a `<label>` and a `<graphic xlink:href="…">`.
3. Download the image: `https://www.ncbi.nlm.nih.gov/pmc/articles/instance/<numeric PMC id>/bin/<href>`. Add `.jpg` if the href has no extension.
4. Check that the file starts with bytes `FF D8` (JPEG). An HTML error page means it failed.

These are whole figures, never single panels. bioRxiv's servers block scripted downloads, so use the PDF for preprints.

## 5. Read values off a chart

If the statement needs a number the text doesn't give, and the chart is drawn as vector graphics, read it from the drawing itself instead of by eye. The bars share a bottom edge, which is the axis baseline. Figure lettering often shows up as small filled shapes too, and grouping by that shared edge separates the bars from it.

```python
import fitz
from collections import Counter
doc = fitz.open(pdf_path)
page = doc[4]                                    # 0-based: the 5th page
clip = fitz.Rect(x0, y0, x1, y1)                 # the panel, in PDF points
rects = [d["rect"] for d in page.get_drawings()
         if d["rect"].intersects(clip) and d.get("fill") is not None and d["rect"].height > 10]
base = Counter(round(r.y1, 1) for r in rects).most_common(1)[0][0]
bars = sorted((r for r in rects if round(r.y1, 1) == base), key=lambda r: r.x0)
for r in bars:
    print(f"x={r.x0:.1f}  height={r.height:.1f} pt")
```

- Each bar can appear twice, once for its fill and once for its outline. They differ by a fraction of a point, so use either one.
- To turn a height into a value, divide by the height of a bar whose value you know, such as a control normalized to 100. You can also use the distance between two axis ticks.
- Values read this way are still approximate (≈), because they come from a chart and not from the text.
- For a raster chart, calibrate pixel positions against two axis tick labels on the crop.

## 6. Attach

- **Roam** (local Roam MCP server): `file_upload(filePath, graph)` returns a URL. Embed it as `![](url)`. Some Roam servers need the graph's guidelines read once in the session before any other call. If one Roam server's call fails, try another connected Roam server.
- **Obsidian vault:** copy the image into the vault's attachments folder and embed it as `![[filename.png]]`.
- **No graph tool:** save the image beside the draft and embed it as `![](filename.png)`.
