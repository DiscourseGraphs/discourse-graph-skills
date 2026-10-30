# Discourse Graph skills

Agent skills for working with [discourse graphs](https://discoursegraphs.com), packaged as a Claude Code plugin marketplace. Each skill is a standard [Agent Skill](https://agentskills.io) folder, so other agents can use them too. These are research prototypes, so anticipate that they will change frequently.

## What's in it

One plugin, `discourse-graph` (version in `plugins/discourse-graph/.claude-plugin/plugin.json`):

| Skill | Use it to |
|---|---|
| `evidence-candidates` | Stage findings from papers as Evidence candidates, each with a verbatim quote, a figure panel and its methods context |
| `create-standalone-html` | Draft standalone HTML explanations with an optional offline starter; requires the separately installed `discourse-engineering-writing-style` skill |
| `figure-extraction` | Find a paper's PDF (Zotero → project folder → ask) and crop the figure panel a statement reports, recording which file and method it came from |

The research skills are tool-agnostic. `SKILL.md` describes each step, and the `references/` files list ways to do each step with Zotero, PyMuPDF, poppler, PubMed Central, Roam and Obsidian.

The proposed HTML skill includes a [fictional rainwater example](plugins/discourse-graph/skills/create-standalone-html/examples/rainwater/README.md). Download `example.html` and open it locally; GitHub displays its source. The HTML bundler needs Python 3 and no third-party Python packages. Its writing-style dependency is not bundled here.

## Install

In Claude Code:

```
/plugin marketplace add DiscourseGraphs/discourse-graph-skills
/plugin install discourse-graph@discourse-graph-skills
```

The skills then show up as `discourse-graph:evidence-candidates` and `discourse-graph:figure-extraction`. If you have no GitHub SSH key, set `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` before adding the marketplace.

To get updates, run `/plugin marketplace update discourse-graph-skills`, or turn on auto-update for this marketplace under **Marketplaces** in `/plugin`.

The quote checker needs Python 3 with PyMuPDF (`pip install pymupdf`).

For other agents (Codex, Cursor, Gemini CLI and others), copy a folder from `plugins/discourse-graph/skills/` into that agent's skills directory.

## Editing

- **Edit here, never in an installed copy.**
- **Bump `version` in `plugin.json` for each release.** People who installed the plugin get changes only when the version changes.
- **Remove personal copies.** If you also have a personal skill with the same name in `~/.claude/skills/`, both can trigger. Remove the personal copy once you use the plugin.
- **Test changes first.** Run the scenarios in `tests/` with a fresh agent and compare against the recorded results. After changing `check_quote.py`, run `python3 tests/test_check_quote.py`.
- **Validate:** `claude plugin validate .`

## Credits

- `evidence-candidates` is generalized from the Akamatsu lab's `evidence-candidates` skill.
- The verbatim-quote rule, the evidence bundle, and the figure-capture methods and PubMed Central route in `figure-extraction` are adapted from the living-synthesis pipeline (Joel Chan's team, with work by Karola Kirsanow, building on Jay Patel's living-synthesis vault).

## License

- The skills, references and documentation are licensed under [CC BY 4.0](LICENSE).
- The code (`*.py` files and the code snippets in the references) is licensed under the [MIT License](LICENSE-CODE).

Copyright (c) 2026 Discourse Graphs Project contributors.
