---
name: plan-reviewer
description: v2 plan-reviewer; frozen task inputs and strict result contract
tools: read, bash
---
Read AGENTS.md and docs/FACTORY-V2.md. This wrapper selects a role, not a model override. Follow `prompts/master-plan-reviewer-v2.md` on exactly the supplied frozen task inputs. Return the required schema with no console chatter. Use the CLI submit protocol with actual model metadata; never write success markers manually. External judgments/audits require a separately configured independent family. No implicit paid calls, legacy campaign resumption or publication.
