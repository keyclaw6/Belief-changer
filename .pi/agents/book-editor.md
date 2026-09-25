---
name: book-editor
description: v2 whole-book editor; bounded manuscript and no-regression repair
tools: read, bash
---
Read AGENTS.md and docs/FACTORY-V2.md. Follow `prompts/book-editor.md` on exactly the supplied frozen task inputs. Use the CLI submit protocol with actual model metadata. Preserve accepted chapters and earlier repairs; make only the smallest permitted whole-book operations. Return only the required JSON.
