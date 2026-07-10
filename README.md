# Belief-Changer

An open-source, nonprofit effort to generate high-quality, **Allen Carr "Easyway"-style belief-change books** for the many behaviors no such book exists for yet — gaming, doom-scrolling, pornography, and more.

## The core idea

People already choose what they believe is their happiest option in the moment. The problem is that those beliefs are often misaligned with reality — we price in the immediate payoff and silently zero out the real costs. **Correct the belief model and the behavior changes on its own**, without willpower or a sense of sacrifice. That is the mechanism Easyway and *The Freedom Model* exploit, and the one this project aims to generalize and scale with AI.

## The map

- **`AGENTS.md`** — the constitution for agents working in this repo (mission, priorities, truth hierarchy, YAGNI, workflow, the canonical gate). **Agents start here.**
- **`docs/VISION.md`** — the living vision & working tracker (philosophy, pipeline, orchestration, north star). The product intent.
- **`openspec/specs/`** — behavior and method truth; read the relevant spec before changing pipeline or content behavior.
- **`prompts/style-guide.md`** — the writing bible fed to every chapter-writer.
- **`production-books/<slug>/`** — the per-book workshop. **`analysis/`** — the reverse-engineered reference-book analyses.

The canonical repo gate is **`bash scripts/check.sh`**. This repository is early; the current focus is the MVP (the quit-porn book).

## License

Software is `AGPL-3.0-or-later`; project-owned books, prompts, documentation,
research metadata, and synthesis are `CC-BY-SA-4.0`. Third-party material is
excluded from those grants. See **`LICENSE`** for the exact scope.
