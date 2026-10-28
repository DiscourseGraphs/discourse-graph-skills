# dg-skills

Agent skills for working with discourse graphs, packaged as a Claude Code plugin marketplace. Edit the skills here, then install them anywhere from here.

## What's in it

One plugin, `discourse-graph` (version in `plugins/discourse-graph/.claude-plugin/plugin.json`):

| Skill | Use it to |
|---|---|
| `evidence-candidates` | Stage findings from papers as Evidence candidates, each with a verbatim quote, a figure panel and its methods context |
| `figure-extraction` | Find a paper's PDF (Zotero → project folder → ask) and crop the figure panel a statement reports, recording which file and method it came from |

Both skills are tool-agnostic. `SKILL.md` describes each step, and the `references/` files list ways to do each step with Zotero, PyMuPDF, poppler, PubMed Central, Roam and Obsidian.

## Install

In Claude Code:

```
/plugin marketplace add ~/Repos/dg-skills
/plugin install discourse-graph@dg-skills
```

Once the repo is on GitHub, the first line becomes `/plugin marketplace add <owner>/dg-skills`. The skills then show up as `discourse-graph:evidence-candidates` and `discourse-graph:figure-extraction`.

For other agents (Codex, Cursor, Gemini CLI and others), each folder under `plugins/discourse-graph/skills/` is a standard Agent Skill. Copy it into that agent's skills directory.

## Editing

- **Edit here, never in an installed copy.**
- **Bump `version` in `plugin.json` for each release.** People who installed the plugin get changes only when the version changes.
- **Remove personal copies.** If you also have a personal skill with the same name in `~/.claude/skills/`, both can trigger. Remove the personal copy once you use the plugin.
- **Test changes first.** Before a release, run the scenarios in `tests/` with a fresh agent and compare against the recorded results.
- **Validate:** `claude plugin validate .`

## Credits and license

- `evidence-candidates` is generalized from the Akamatsu lab's `evidence-candidates` skill.
- The verbatim-quote rule, the evidence bundle, and the figure-capture methods and PubMed Central route in `figure-extraction` are adapted from [DiscourseGraphs/living-synthesis-metaresearch](https://github.com/DiscourseGraphs/living-synthesis-metaresearch) (Joel Chan's team, with commits by Karola Kirsanow, building on Jay Patel's living-synthesis vault). That repository is private and has no license, so check with Joel before sharing these skills outside the team.

This repository has no license yet.
