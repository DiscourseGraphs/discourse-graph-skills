# Standalone HTML skill

Create portable HTML explanations with an optional offline page generator.

## Requirements and use

Use an assistant that can load a `SKILL.md` folder and read/write files. The DG writing-style skill, named `discourse-engineering-writing-style`, must already be installed. It is referenced by name and is not included in this package.

Copy the whole `create-standalone-html` folder into your assistant's supported skills directory, preserving its subfolders. Invoke `$create-standalone-html` where supported, or ask the assistant to read `SKILL.md` and follow it.

The optional generator needs Python 3 (standard library only). Recipients of generated HTML need only a modern browser. No npm packages, API keys, or network downloads are needed to build a page.

## Minimal generator example

In a working directory, create `overview.html` containing `<p>A concise overview.</p>` and `content.html` containing `<details><summary>More detail</summary><p>Supporting explanation.</p></details>`.

Create `page.json`:

```json
{"title":"Example","overview":"overview.html","content":"content.html"}
```

Run from that directory, adjusting the skill path:

```sh
python /path/to/create-standalone-html/scripts/bundle_html.py --config page.json --output example.html
```

On systems where Python is named `python3`, use that command instead. The output directory must exist. Existing output is preserved unless `--force` is supplied. Open `example.html` in a browser.

## Included files

- `SKILL.md`: instructions for the assistant.
- `references/components.md`: generator options and component markup.
- `scripts/bundle_html.py`: embeds page fragments and assets into one HTML file.
- `assets/shell.html`, `ui.css`, `ui.js`: page structure, styling, and interactions.
- `assets/primer-tokens.css`: pinned Primer design tokens.
- `assets/primer-LICENSE.txt`: required upstream MIT notice.
- `assets/provenance.json`: versions and Primer upstream attribution.

Keep the license when redistributing the token stylesheet or generated pages.
