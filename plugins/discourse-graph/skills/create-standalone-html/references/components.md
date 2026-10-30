# Offline starter 1.0.0

Use this optional Primer-based starter for reusable page chrome. Author only the page fragments and any small page-specific CSS; the helper copies stable assets without loading them into the prompt. Keep content structure driven by the task. Search and tabs are optional, not requirements for every page.

## Bundle a page

Python 3 standard library only; the recipient needs only a browser. Put `page.json` beside authored `overview.html` and `content.html` fragments:

```json
{
  "title": "Queue retries, explained",
  "subtitle": "Check completion, then retry or send a job for review.",
  "overview": "overview.html",
  "content": "content.html",
  "nav": [{"label": "Execution", "target": "#execution"}],
  "search": true
}
```

```powershell
python <skill-directory>/scripts/bundle_html.py --config page.json --output queue.html
```

Paths are relative to the config file. `title`, `overview`, and `content` are required; the latter two are fragment paths. Optional fields: `subtitle`, `nav` (existing local IDs), `search` (default false), `theme` and `disclosure_controls` (default true), and `extra_css` (stylesheet path). `--force` replaces the selected existing output. The output directory must already exist.

The bundler embeds styles, scripts, pinned tokens, license and version metadata. It rejects script/import tags, event-handler attributes, CSS imports, remote runtime assets, duplicate/reserved IDs, and missing navigation targets. Reference links remain clickable. Embed images as `data:` URLs or use inline SVG. A restrictive CSP also blocks network dependencies and form submission. This is an authored-fragment workflow, not a general HTML sanitizer; specialized scripts can be added through a deliberate asset/output revision with renewed offline verification.

## Components and hooks

| Need | Markup / classes |
| --- | --- |
| Structure | Shell includes header, visible overview, optional underline navigation, main and skip link. Keep supporting content in the content fragment. |
| Text and emphasis | Semantic headings, `strong`, `mark`, `.muted`, `.callout`; `.badge-fact`, `.badge-unknown`, `.badge-recommendation` alongside `.badge`. Keep qualifications and source links in authored content. |
| Controls | Native `button`, `.button` for links, `.button-primary`; labeled `input`, `select`, `textarea`. Inputs are styled, not automatically given calculations or persistence. |
| Detail | `details[data-level="group"]` containing `details[data-level="card"]`. Omit `open` for closed defaults; use meaningful summaries. Other native details remain independent. |
| Local controls | Buttons use `data-disclose="group"` or `"card"`, `data-open="true"` or `"false"`, optional `data-root="execution"` naming a containing element ID. Wrap in `.toolbar[data-disclosure-controls]` with `hidden`; put `hidden` on buttons. |
| Search | With `search:true`, mark non-overlapping units `data-search-item`, typically cards. No search marker on the overview. Matches open needed disclosures; clearing restores the previous disclosure/hidden state. In tabs, search covers the active panel. |
| Visuals/code | `.flow` on an ordered process list; `figure` with labels/caption; `pre > code` with a visible Pseudocode label for conceptual logic. `.table-wrap` around a table when horizontal overflow is needed. |

```html
<details id="execution" data-level="group">
  <summary>Execution: check, attempt, then retry or review</summary>
  <div class="toolbar" data-disclosure-controls hidden>
    <button type="button" data-disclose="card" data-open="true" data-root="execution" hidden>Expand execution cards</button>
    <button type="button" data-disclose="card" data-open="false" data-root="execution" hidden>Collapse execution cards</button>
  </div>
  <details id="retry" data-level="card" data-search-item>
    <summary>Temporary failures wait before retrying</summary>
    <p>Preserve the meaningful limits and <a href="https://example.test/notes">source</a>.</p>
  </details>
</details>
```

Group controls change only group state; card controls change only card state. Scopes exclude items hidden by search or inactive tabs, while cards inside closed groups can still be toggled. Fragment navigation clears an active search, activates the required tab, opens ancestor disclosures, and focuses the target. The overview/navigation stay visible. Native details work without JavaScript; enhanced controls stay hidden.

## Optional tabs

Use ordinary navigation anchors when all sections should remain on one page. For actual alternative panels, supply explicit tab markup. Panels start visible in authored HTML so all content remains readable without JavaScript; the controller hides inactive panels. Use unique IDs and matching controls/labels:

```html
<section data-tabs>
  <div class="tabs" role="tablist" aria-label="Examples" hidden>
    <button type="button" role="tab" id="tab-a" aria-controls="panel-a" aria-selected="true">Example A</button>
    <button type="button" role="tab" id="tab-b" aria-controls="panel-b" aria-selected="false">Example B</button>
  </div>
  <section id="panel-a" data-tab-panel role="tabpanel" aria-labelledby="tab-a" tabindex="0"><p>Example A</p></section>
  <section id="panel-b" data-tab-panel role="tabpanel" aria-labelledby="tab-b" tabindex="0"><p>Example B</p></section>
</section>
```

Tabs support click, ArrowLeft/Right, Home and End with automatic activation and one tab stop. The Dark mode toggle exposes `aria-pressed`, follows system preference until chosen, and tries to save only a theme preference. Blocked storage leaves the page usable with a short status message after a user change. Reduced motion disables CSS animation/transitions and smooth navigation; add pause controls for any custom continuing animation.

## Assets and updates

The starter embeds Primer Primitives 11.10.0 tokens and retains their MIT license. `assets/provenance.json` records the shared starter and token versions. No external repository or service is needed at runtime.

Keep the third-party license with the assets. Each generated HTML contains its own embedded assets; editing the starter does not update existing pages. Use `extra_css` for page-specific style adjustments.
