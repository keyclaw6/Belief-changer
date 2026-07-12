# Calibration state — STOPPED

This is the current recovery checkpoint, not an experiment diary; history lives in run records.

## Founder stop

- **State: STOPPED by founder direction.** Do not infer or execute a next artifact.
- Do not launch models, audit, write prose, revise prompts, or resume calibration until
  the founder explicitly selects a resume fork.
- There is no external access or funding blocker recorded. The stop is a direction and
  contract decision boundary.

## Accepted base

- Branch: `calibration-lab`.
- Accepted base HEAD: `e9aeca03ecc72707a0de382db70aebfb36477b31`.
- Last accepted prose: quit-sugar Chapter 1 from run-002 and Chapter 2 from run-004.
  No run-014 prose is accepted or exists.
- Corrected lived synthesis: `e21506f804920898b3f314cd44bb20954d1524dd0eb70395ae4d95425e7afc5b`.
- Corrected framing: `d1fe0a1b2ea1c56dab8f56a10aa2a4ed3a8f86f3552c83db9f5f46ecb62bfece`.
- The two-file source correction was accepted at
  `f862fd27eff3aa97822b6561e8e1f1c5db0f6b6e`.
- Accepted production master plan: `b1726d736cb543f0b16c24f225136b86ebda336f4a1981f0c1f323cb311530b4`.
- Accepted production plan review: `346c172c5b00c6460f6c229fd7d1119364ac5504c7372e4e55ff43e9be8267ed`.
- Promotion `d9279d4c4960b0b1daca5e4fdd2cbcc04835a0e1`; acceptance record `e9aeca03ecc72707a0de382db70aebfb36477b31`.

## Stopped commission handoff

The following exact candidate bytes were generated from accepted base `e9aeca0` and
are preserved in the stop/handoff commit as evidence. They are **not accepted
commissions or product inputs**. Each was produced by one native Sol-ultra call, is readable,
has the required title, and has no mechanical `COMMISSION BLOCKED` marker:

- CH-01: `f2cd40ab8919cdf7a9a7f1816baeea406d96d00c516085c78e3d98ae0432fce9`.
- CH-02: `2a5bcca99181be17aaafd2fd7884cd3ed725d8068d00d3e31f5e231e5027678b`.
- CH-03: `744a64e541eb70b4a000648f2eb0eb7f2dd89a2f23b58a51b0ed9850e40f7e39`.

**All three remain semantically UNAUDITED and UNACCEPTED.** Mechanical validity,
handoff commitment, or absence of a blocked marker is not source-fidelity approval.
Do not promote, repair, regenerate, or feed them to a writer while stopped.

`git log` anchors the accepted product base at `e9aeca0`; current HEAD will be the later
stop/handoff commit, which does not advance that accepted product base.

## Active hypothesis

- H-050 remains **TESTING**. Run-013 was inconclusive; run-014 has produced no causal
  or product inference.
- Plan acceptance and commission transport do not support or refute H-050.

## Required recovery and resume forks

Before any resume, read `calibration/FAILURE-ANALYSIS.md`. If it is absent, remain
stopped and ask the founder for the intended failure-analysis handoff. Then verify:

- `calibration/runs/run-014/manifest.json`
- `calibration/runs/run-014/report.md`
- the final run-014 row in `calibration/runs/LEDGER.md`
- H-050 in `calibration/hypotheses.md`
- `git log -5` and the working tree

The founder must choose between the resume forks documented in FAILURE-ANALYSIS:

1. preserve the frozen run contract and continue from the unaudited commission set; or
2. fix the writer-input contract as a generic change and start the required new run.

Do not blend the forks or silently send both a master plan and a commission to a writer.
There is **no active next artifact while STOPPED**.

## Route law

- OpenRouter is permitted only for Claude Opus 4.6 chapter writing with reasoning
  disabled and DeepSeek research at its top supported mode.
- Never route GPT/OpenAI, Sol, Luna, Gemini, Grok, planning, reviewing, auditing,
  framing, summarization, or judging through OpenRouter.
- Non-writer roles require their authorized native or direct route at top reasoning.
- Credentials remain environment-only and never enter repository artifacts.

## Update rule

On an explicit founder resume, replace this checkpoint with current facts. Keep history
in the run records; do not grow this file back into a diary.
