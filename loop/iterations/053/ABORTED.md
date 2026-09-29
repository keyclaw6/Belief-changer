# Iteration 053 — ABORTED BEFORE MODEL EXECUTION

## Status

Iteration 053 did **not** complete and does not count as an autoresearch iteration.

The preregistration in `hypothesis.md` is retained unchanged as historical evidence of what was intended. No later iteration was authorized by a completed 053 decision.

## What happened

The campaign was armed with an hourly heartbeat before the actual worker path had proven that it could return even one successful model response and advance a durable factory marker.

The intended architecture is one persistent top-level Pi Coding Agent. During startup/supervision, stale alternate runtime paths were incorrectly considered, including ChatGPT/OpenCodex/OpenCode-host/Vercel-style provider paths. Those are not part of the intended live factory architecture.

No valid `COMPLETE_UNRELEASED` book, outer judgment, learning packet, or iteration decision was produced.

## Why it was stopped

The owner stopped the campaign after repeated no-progress wake-ups. The supervisor treated persistence as repeated recovery instead of recognizing a startup blocker.

This is now a permanent process lesson:

- the Pi worker must prove a successful OpenCode Go model response and durable state advancement **before** a recurring heartbeat is armed;
- OpenCode Go is the only live model provider;
- the heartbeat is a watchdog, not a retry engine;
- the same error twice, two no-progress wake-ups, no successful first model response, auth/quota/credential/provider misconfiguration, required human action, or a wrong-provider invariant violation stops and disables the schedule;
- a general infrastructure defect may be fixed once with regression coverage, then the same Pi session is resumed once;
- a blocker is never counted as an iteration.

The controlling procedure is now `skills/running-auto-research-loop/SKILL.md`.

## Historical note

The earlier 053 hypothesis named ChatGPT as an evaluator route. That preregistration is not rewritten because it is immutable historical evidence, but the campaign was aborted before that design was executed. Current active contracts prohibit ChatGPT/Vercel/Zen/alternate-provider model execution and require OpenCode Go only.
