---
name: running-auto-research-loop
description: Run and supervise Belief-Changer autoresearch campaigns with one persistent Pi Coding Agent, OpenCode Go models only, bounded heartbeats, durable progress checks, proactive root-cause repair, and circuit breakers.
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

If the first successful model response does not arrive, **do not immediately give up**. Diagnose the startup path while still under direct supervision: inspect the Pi session, OpenCode Go route/configuration, credentials wiring, provider response, process state, and relevant logs; repair the smallest safe root cause; verify the repair; and retry the same Pi session. Only classify the campaign as `STARTUP_BLOCKED` when the same blocker survives a real repair attempt or no safe autonomous repair path exists. Do not arm a recurring heartbeat until startup is actually proven.

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
Be proactive. A scheduled agent is the only actor available between owner messages, so its job is to **attempt to restore forward progress**, not merely report a problem.

1. classify the failure from evidence rather than guessing;
2. inspect the directly connected runtime/config/log/state paths;
3. try the smallest safe autonomous repair that preserves the architecture;
4. add or update a regression test when the defect is general/deterministic;
5. run the relevant verification gate;
6. resume the **same** Pi session;
7. verify that the repair created a successful model response or new durable factory progress.

Examples of appropriate autonomous repair:
- repair a stale path, broken config, missing wiring, parser bug, dead local process, expired non-human session, or recoverable tool state;
- restart/reconnect a required local component when safe;
- correct credential **routing** when an already-authorized credential exists but is wired incorrectly;
- repair the Pi session/runtime state without changing its identity/model/provider;
- fix repository code/config and tests when the failure is a reproducible system defect.

Do **not** fabricate credentials, bypass authorization, silently change model/provider, create a replacement worker, or synthesize factory output.

A blocker is not grounds to stop until the supervisor has either attempted the relevant safe repair path or established from evidence that no autonomous repair is possible.

## Repair budget and circuit breakers

The heartbeat must be proactive **and** bounded. It should try to fix what is broken, but never devolve into an unattended retry storm.

### Repair before stop

Before tripping a circuit breaker, the supervisor must record one of:
- **repair attempted:** the concrete root-cause repair it performed and how it verified the result; or
- **no autonomous repair exists:** the evidence showing why the next step requires unavailable credentials, owner action, provider-side recovery, or another external dependency it cannot safely perform.

For a recoverable blocker, allow up to **two distinct evidence-driven repair actions in one wake-up** when the first repair reveals a different underlying blocker. Do not repeat the same repair twice. A transient network/provider error may receive one bounded retry after checking current state.

Examples:
- invalid credential *wiring* → locate the already-authorized credential source/config and repair the wiring;
- dead tool/process → restart or reconnect it safely and verify health;
- provider misconfiguration → correct the OpenCode Go route/config and verify with a real response;
- parser/session/runtime defect → fix the defect, add regression coverage if general, and resume the same Pi session;
- human login/2FA/CAPTCHA → navigate/recover as far as safely possible, then stop only at the actual human checkpoint;
- account/provider quota exhaustion → confirm it is genuinely provider-side and not a routing/config mistake; if no OpenCode-Go-compatible repair exists, stop.

### Stop conditions

Stop and disable the heartbeat when any of these is true:
- the **same failure fingerprint recurs after a real repair**;
- two consecutive heartbeat checks produce no durable progress **and** the current wake-up cannot identify and execute a new evidence-backed repair;
- startup still has no successful model response after the startup repair path has been exercised;
- the remaining blocker requires owner/human action that the agent cannot perform;
- the remaining blocker is confirmed account/provider quota exhaustion with no permitted OpenCode Go repair;
- an independent evaluator family required by the experiment is unavailable through OpenCode Go after checking the available permitted configuration;
- preserving the runtime invariant would require switching provider/worker/model without authorization.

A merely running process is not progress. A repeated `continue` is not a repair.

When a circuit breaker trips:
- mark the campaign/run `BLOCKED` or `STARTUP_BLOCKED` in durable state;
- preserve the existing Pi session and artifacts;
- disable the recurring schedule;
- report what failed, what autonomous repair was attempted, what evidence remained, and the smallest next action;
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
> If there is no durable progress, do not blindly send another `continue`. Classify the blocker from logs/state and proactively attempt the smallest safe root-cause repair while preserving the same Pi session and OpenCode Go-only architecture. Repair broken wiring/config/process/session/parser/tool state when possible, add regression coverage for general deterministic defects, verify the repair, and resume the same Pi session. You may perform up to two distinct evidence-driven repairs in one wake-up when fixing one issue reveals another; never repeat the same repair blindly.
>
> Stop only after the same failure recurs after repair, two consecutive no-progress wake-ups leave no new evidence-backed repair, startup still has no successful model response after its repair path, or the remaining blocker genuinely requires unavailable human action/provider-side quota/credentials that cannot be safely repaired. Before stopping, record what you tried or why no autonomous repair exists. Then mark the run blocked, disable this schedule, preserve the session, and report the exact blocker.
>
> When the factory reaches verified `COMPLETE_UNRELEASED`, perform the outer judgment/decision/learning boundary and freeze it before starting the next iteration. Stop the schedule when the requested campaign count is complete or any circuit breaker fires.

## Campaign completion

The schedule must disable itself when:
- the requested number of iterations is complete;
- a circuit breaker fires;
- the owner says stop.

Persistence is useful only while the system is making real progress. A scheduler must never turn a blocked provider or broken worker into an unattended retry storm.
