---
name: running-auto-research-loop
description: Run and supervise Belief-Changer autoresearch campaigns with one persistent Pi Coding Agent, OpenCode Go models only, bounded heartbeats, durable progress checks, and circuit breakers.
---

# Running the Auto Research Loop

Use this skill whenever starting, resuming, or scheduling a Belief-Changer autoresearch campaign.

## Runtime invariant

- The book-factory worker is **one persistent top-level Pi Coding Agent** using `.pi/agents/factory-orchestrator.md`.
- Live model execution uses **OpenCode Go only**. Do not use OpenCode Zen, Vercel, ChatGPT, OpenCodex, OpenCode CLI agents, or any other provider/agent as a fallback worker.
- The outer host may inspect durable state, schedule wake-ups, perform deterministic orchestration, and decide what should happen next. It must not impersonate a factory role or substitute itself for the Pi worker.
- External evaluator/reviewer roles must also be powered through OpenCode Go. Independence means an independently configured model family, not a different provider. If an independent family is unavailable through OpenCode Go, stop rather than substitute.
- Never change the Pi controller model/provider merely to get past a failure.

## Do not arm the heartbeat until startup is proven

Start the worker once under direct supervision before creating a recurring schedule.

Require all of the following:
1. the intended Pi session exists and its identity is recorded;
2. its configured provider is OpenCode Go;
3. at least one real model request has returned a non-empty successful response;
4. the factory has advanced at least one durable state marker.

A process that exists, a session that is "running", repeated provider retries, or new log lines are **not** startup proof.

If the first successful model response never arrives, classify the campaign as `STARTUP_BLOCKED`. Do not create or keep a recurring heartbeat.

## A heartbeat is a watchdog, not a retry engine

Every wake-up starts by reading durable state and asking:

> **What durable progress marker changed since the previous wake-up?**

Durable progress means something such as:
- a new validated factory result;
- a run/status stage advancing;
- a new accepted plan/chapter/assembly/audit;
- `COMPLETE_UNRELEASED`;
- a frozen outer judgment, decision, learning packet, or next hypothesis.

These do **not** count as progress:
- the same PID/session still existing;
- the same task being retried;
- another 429/503/auth failure;
- repeated "continue" messages;
- more logs without a new validated artifact;
- another scheduler wake-up.

### If healthy progress exists
Leave the Pi worker alone. Do not send a generic nudge and do not start another worker.

### If the worker completed
Take control at the outer boundary: verify `COMPLETE_UNRELEASED`, run the intended independent judging/decision/learning work, freeze the result, and only then consider the next iteration.

### If there is an infrastructure defect
Be proactive:
1. identify the root cause rather than repeatedly nudging the worker;
2. make the smallest general repair;
3. add or update a regression test when appropriate;
4. run the relevant verification gate;
5. resume the **same** Pi session once.

If the same failure fingerprint occurs again after that repair, stop.

## Circuit breakers

The heartbeat must stop itself instead of running indefinitely.

**Stop immediately with zero automatic retries** for:
- missing/invalid credentials;
- provider/account quota exhaustion;
- provider misconfiguration;
- required tool unavailable;
- human login/2FA/CAPTCHA/action required;
- no successful model response since campaign startup;
- independent evaluator unavailable through OpenCode Go;
- an invariant violation such as the wrong provider or wrong worker type.

**Allow at most one bounded recovery attempt** for a genuinely transient provider/network error inside one wake-up. If the same error fingerprint appears again, stop.

**Stop after two consecutive heartbeat checks with no durable progress**, unless the Pi worker itself exposes a verified long-running stage with an expected durable completion boundary and no repeated error. Merely being alive is insufficient.

**Never send generic `continue` more than once without evidence that the previous continuation created durable progress.**

When a circuit breaker trips:
- mark the campaign/run `BLOCKED` or `STARTUP_BLOCKED` in durable state;
- preserve the existing Pi session and artifacts;
- disable the recurring schedule;
- report the exact blocker and the smallest next action;
- do not silently switch provider, model, harness, or worker.

## Iteration boundary

Do not start iteration N+1 until iteration N has:
1. reached verified `COMPLETE_UNRELEASED` for all required books;
2. completed the preregistered outer judgments;
3. frozen the deterministic decision;
4. frozen transferable learning/reviewer output where required;
5. frozen the next falsifiable hypothesis.

A blocker does not count as an iteration.

## Heartbeat prompt template

Use wording at least this strict when scheduling an autoresearch continuation:

> Inspect durable repository state before doing anything. This heartbeat is a watchdog, not a retry loop. First determine exactly what durable progress marker changed since the previous wake-up. If the Pi Coding Agent is healthy and progressing, leave it alone. The only worker is the existing persistent Pi Coding Agent and all model execution must use OpenCode Go; never substitute ChatGPT, OpenCodex, OpenCode CLI, OpenCode Zen, Vercel, or another provider/model path.
>
> If there is no durable progress, do not blindly send another `continue`. Classify the blocker. Fix a genuine general infrastructure bug once, add regression coverage when appropriate, and resume the same Pi session. If the same error repeats after one repair/retry, if there are two consecutive no-progress wake-ups, if no first successful model response has ever occurred, or if the blocker is auth/quota/credentials/provider configuration/required human action, mark the run blocked, disable this schedule, preserve the session, and report the blocker instead of retrying.
>
> When the factory reaches verified `COMPLETE_UNRELEASED`, perform the outer judgment/decision/learning boundary and freeze it before starting the next iteration. Stop the schedule when the requested campaign count is complete or any circuit breaker fires.

## Campaign completion

The schedule must disable itself when:
- the requested number of iterations is complete;
- a circuit breaker fires;
- the owner says stop.

Persistence is useful only while the system is making real progress. A scheduler must never turn a blocked provider or broken worker into an unattended retry storm.
