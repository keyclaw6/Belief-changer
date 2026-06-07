# books/ — DEPRECATED

This folder held the **reference / source PDFs**. The project structure changed:

- **Reference source texts** (the books we extracted style from) now live in [`/analysis/reference-books/`](../analysis/reference-books/), grouped with their analyses.
- **Books the pipeline produces** go in [`/production-books/`](../production-books/).

### Action needed (manual, ~30 sec in the GitHub UI)
Move the three PDFs from this folder into `analysis/reference-books/`, then delete this `books/` folder:
- `The Easy Way to Quit Caffeine.pdf`
- `The Freedom Model for Addictions Abridged.pdf`
- `Burgeon-Book.pdf`

> Why manual: the agent has no `git` push credentials in its sandbox, and the commit API it uses corrupts binary files — so it can't relocate the PDFs itself without risking damage. Text/structure was set up automatically; only the binary move is left to you.
