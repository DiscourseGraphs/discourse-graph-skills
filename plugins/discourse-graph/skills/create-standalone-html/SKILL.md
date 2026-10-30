---
name: create-standalone-html
description: Create or revise standalone HTML explanation and reference pages that make complex topics, processes, or technical material easy to understand. Use for an explanatory HTML file rather than a general website or application.
---

# Create Standalone HTML

Create a complete HTML document with a useful overview and supporting detail on demand. Match the audience and question instead of imposing a fixed template. Save it in the requested location, or the current workspace when none is specified.

## Content

- Read and apply the installed `$discourse-engineering-writing-style` skill to page copy. This external dependency is not bundled; resolve it through the assistant's skill catalog. Follow the user's requested tone when it differs.
- Lead with the main takeaway. Use concise, plain language and preserve necessary qualifications and technical meaning. Follow the requested tone.
- Keep source links near the claims they support. Distinguish facts, inference, uncertainty, and recommendations.
- When revising a page, preserve useful content, attribution, and working interactions.

## Layout and interaction

- Use a responsive layout, sans-serif fonts, readable contrast, and clear visual hierarchy. Keep the overview, essential takeaways, and navigation visible.
- Put supporting detail in native `<details>` sections, closed by default, with meaningful `<summary>` labels. Do not hide the entire page inside a disclosure.
- Add expand/collapse controls when useful. For nested groups and cards, provide separate controls with explicit scope. Toggling one level must not silently toggle another. Navigation into hidden content must reveal the necessary ancestors or target a visible summary.
- Use tables, callouts, and editable inputs only when they help explain or compare information. Label inputs and make their behavior clear.
- Use semantic headings, keyboard-operable controls, visible focus, and appropriate state announcements. Native disclosures should work without JavaScript.

## Visual explanation

Use diagrams, images, pseudocode, or animation when they clarify a relationship or mechanism. Keep them near the explanation and provide labels and accessible text equivalents. Prefer inline SVG or HTML/CSS for simple diagrams. Label pseudocode clearly as conceptual rather than executable.

Animate only when change over time helps explain the subject. Respect `prefers-reduced-motion`, provide a static equivalent, and add pause/stop controls for continuing motion.

## Standalone output

- For the optional bundled starter, read [references/components.md](references/components.md), then use `scripts/bundle_html.py` with authored page fragments. The helper embeds the supplied assets; there is no need to load the large token stylesheet into the prompt.
- Otherwise, write a complete document with inline CSS and small inline JavaScript as needed. Avoid introducing a framework build, recipient build step, or CDN dependency by default.
- Embed required styles, scripts, fonts, images, and diagrams for single-file delivery. For offline use, avoid remote imports, fetches, fonts, images, and libraries. Reference hyperlinks may remain without being required to operate the page.

## Verify and deliver

Inspect the actual output at desktop and narrow widths. Check initial disclosure states, overview visibility, keyboard navigation, and group/card controls after mixed individual toggles. Test calculations, editable inputs, and reduced motion when present. For offline output, check opening through `file://`, missing assets, browser errors, and network attempts with networking disabled when supported.

Return a link or path to the HTML file and any material unverified behavior. Publish or deploy only when requested.
