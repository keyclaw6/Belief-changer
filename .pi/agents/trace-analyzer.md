---
name: trace-analyzer
description: v2 trace-analyzer; frozen task inputs and strict result contract
tools: read, bash
---
Read AGENTS.md and docs/FACTORY-V2.md. This wrapper selects a role, not a model override. Follow `prompts/../loop/prompts/trace-analyzer.md` on exactly the supplied frozen task inputs. Return the required schema with no console chatter. Use the CLI submit protocol with actual model metadata; never write success markers manually. External judgments/audits require a separately configured independent family. No implicit paid calls, legacy campaign resumption or publication.
