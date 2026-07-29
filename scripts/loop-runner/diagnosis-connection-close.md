# Diagnosis — instant connection-close on OpenRouter research calls (2026-07-28)

Symptom: POST https://openrouter.ai/api/v1/responses fails with
"[transport error] Remote end closed connection without response",
latency ~0.0s, on all retries; affected all 12 research subagent calls
(both at 12-parallel and 4-parallel), while GET /models and the earlier
single lead call succeeded.

Evidence:
- Direct probes at 21:47 CEST (no creds): GET /models 200; POST /responses
  with small, 50KB, and 50KB+tools bodies → all reach OpenRouter (401
  missing-auth). Transport fine when the egress proxy is healthy.
- Failure windows interleave with "Domain ... blocked by network policy"
  403 pages in the same minutes (queue logs, runs8 + round-1 retries).
- Concurrency ruled out: 4-parallel failed identically to 12-parallel.
  Body size ruled out by probes. Endpoint shape ruled out (lead call
  succeeded with identical shape).

Root cause: the sandbox egress firewall flaps; while degraded it either
serves a 403 block page or silently closes new upstream connections
(the http=0 face of the same outage). Not an OpenRouter/API issue.

Fix (applied to all three runners): treat code==0 with latency < 5s as a
firewall window — patient 60s waits, up to 120 windows, not consuming
PROGRAM retry attempts. Batched dispatch (RESEARCH_MAX_PARALLEL=4, 15s
stagger) retained as a courtesy to the proxy.

Residual risk: a call that dies MID-flight (latency high) after the
proxy drops a long-lived connection still consumes a normal retry; for
multi-hour research calls this is the remaining failure mode to watch.
