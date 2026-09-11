# Harness bindings — v2

The runtime is agent-driven, through explicit `scripts/factory.py` tasks. Default factory HTTP routes preserve the owner's Muse Spark contributor Go → Zen → Vercel choices, now public configuration in factory/config.json. Their live availability has NOT been retested with paid calls by the upgrade.

The external profile is intentionally null. Select and configure an independent model family explicitly. There is no silent fall-through to the generator when external capacity fails. Research search/fetch can use the existing web_tools.py primitives or the host's browser, with exact provenance; access failure is not evidence scarcity.

A command adapter receives {task,prompt} as JSON on stdin, uses a fresh temporary working directory, and returns exactly {output,model,family,route,usage} on stdout. argv is an array, never shell text; environment forwarding is allowlisted. This is process isolation, NOT an operating-system sandbox. Use a trusted adapter and appropriate external sandbox for tools. Do not let an evaluator read repository scores/history or load an ambient author-identity prompt.

An existing agent harness may instead read a frozen task, call the requested isolated role and submit the strict JSON response plus actual execution metadata. Imported metadata is the operator's assertion, not cryptographic provider attestation. Paid execution requires --allow-paid; supplying that flag is an explicit operation, not part of tests or CI.
