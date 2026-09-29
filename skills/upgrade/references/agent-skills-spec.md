# Agent Skills open-spec constraints

Re-check the live Agent Skills specification when compatibility may have changed. This local reference records the stable constraints used by this repository.

## Directory layout

```
<skill-name>/
├── SKILL.md
├── scripts/        # optional
├── references/     # optional
└── assets/         # optional
```

## Frontmatter

- `name` is required, 1–64 characters, lowercase alphanumerics and hyphens only, and must match the parent directory.
- `description` is required, non-empty, and should say both what the skill does and when to use it.
- Optional fields may be used only when they add real compatibility/license/tool information.

## Progressive disclosure

1. Metadata: skill name + description should be enough for discovery.
2. SKILL.md: core workflow only; keep it focused.
3. References/scripts/assets: load only when the workflow says they are needed.

References from SKILL.md should be one level deep and should say when to read them.

## Validation

For every material skill change:
- verify directory name equals frontmatter `name`;
- verify the description states what + when;
- verify every referenced file exists;
- avoid duplicated content between SKILL.md and references;
- run `bash scripts/check.sh`;
- if `skills-ref validate` or another compatible Agent Skills validator is available in the current harness, run it too.
