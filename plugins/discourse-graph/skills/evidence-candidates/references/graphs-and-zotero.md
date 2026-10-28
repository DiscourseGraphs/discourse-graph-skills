# Graph and Zotero recipes

`SKILL.md` is tool-agnostic. This file covers the tools teams use today. For PDF and figure tools, see the **figure-extraction** skill's `references/tools.md`.

## Roam

- **Conventions:** `get_graph_guidelines(graph)` returns the graph's node formats, candidate tags and relation names. Some Roam servers refuse other calls until it has been read once in the session. If the call errors on one connected Roam server, try another.
- **Existing evidence from this paper:**
  - `search` for the citekey and key terms
  - `get_backlinks` on the `@source` page
  - with the Discourse Graph MCP server, `search_nodes` (filter by node type without a regex if the regex filter errors)
- **Staging:** create the Source block, then its candidate children, with `create_block`. Upload each image with `file_upload` and embed the returned URL. Read the page back with `get_page` to confirm the nesting.
- **Linking a discourse node** needs doubled brackets around the typed title: `[[[[QUE]] - How do cells …?]]`. Copy titles exactly, including any double spaces.
- **Promotion** is the person's step. The Discourse Graph plugin turns a candidate into a node and carries the parent's `[[@citekey]]` with it.

## Obsidian vaults

- Read the vault's `CLAUDE.md` and any conventions or template notes before writing.
- A paper's candidates usually live on its source page (`@{citekey}.md`), nested under the question they speak to. Follow the vault's own layout.
- Images go in the vault's attachments folder and embed as `![[filename.png]]`.

## No graph tool connected

Write the blocks to a markdown file in the format from `SKILL.md`, step 4, with images beside it. Put the hand-off items (verdicts, unchecked items, pages staging would create) in a comment at the top of the file and in your reply. Say which conventions you assumed.

## Checking a quote against the PDF

A literal search fails on correct quotes. The PDF's text layer breaks lines, hyphenates words and flattens superscripts, and it interleaves figure legends and footers with the body text. The bundled script ignores all of that but still catches a changed word, number, sign or inequality:

```bash
python3 {this skill's folder}/scripts/check_quote.py paper.pdf "The quoted sentence (Fig. 2E)."
python3 {this skill's folder}/scripts/check_quote.py paper.pdf --file quotes.txt   # one quote per line
```

For each quote it prints the PDF page or pages, then one of three results:
- `verbatim` (exit 0)
- `verbatim if the skipped text is an interruption` (exit 2): look at the listed text. A legend, header or page break is fine, but words from the sentence are not.
- `NOT VERBATIM` (exit 1): it shows the words or signs that differ.

A quote that stops partway through a sentence still counts as verbatim, so make sure a cut doesn't drop a qualifier. The script needs PyMuPDF (`pip install pymupdf`). `tests/test_check_quote.py` at the repository root is its regression test.

## Zotero

- **Search every library.** `zotero_list_libraries`, then `zotero_switch_library` into each group, then `zotero_search_items("Author Year")`. Switch back afterwards.
- **Citekey:** read it with `zotero_get_item_metadata(item_key, format="markdown")`. Look for a `Citation Key:` line in Extra, or the BetterBibTeX or `citationKey` field.
  - `zotero_search_by_citation_key` searches only the Extra field on some setups, so a miss there doesn't mean the key is wrong.
  - For a read-only lookup across every library, query `zotero.sqlite` directly. The query is in figure-extraction's `references/tools.md` and returns the `citationKey` alongside the attachment.
- **Don't write to a shared group library** (adding papers, pinning keys or merging duplicates) without the person's go-ahead. It affects the whole team.
- **Duplicates:** if two items share a DOI, use the one whose key the graph already uses. If the graph uses neither, use the key without a disambiguation suffix. Mention the duplicate either way. Merging the items in Zotero can change the surviving key, so leave that to the person.
