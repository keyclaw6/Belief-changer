"""Canonical RF-14 owner routing and causal invalidation scopes."""
import hashlib
import json


SCHEMA = 1
OWNERS = (
    "brief",
    "research/synthesis",
    "framing",
    "plan",
    "commission/context",
    "prose",
    "revision",
    "evaluation",
)
ARTIFACTS = {
    "brief": ("00-brief.md",),
    "research/synthesis": ("research/**",),
    "framing": ("framing.md", "framing-review.md"),
    "plan": ("master-plan.md", "master-plan-review.md"),
    "commission/context": ("commissions/**",),
    "prose": ("chapters/**",),
    "revision": ("revisions/**",),
    "evaluation": ("evaluation/**",),
}


class RoutingError(RuntimeError):
    pass


def _hash(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"),
                     ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _route(row, source, index, default_action):
    if not isinstance(row, dict) or row.get("owner") not in OWNERS:
        raise RoutingError("defect owner is outside the canonical vocabulary")
    action = row.get("action_code", default_action)
    if not isinstance(action, str) or not action.strip():
        raise RoutingError("defect action code is missing")
    return {"finding_sha256": _hash(row), "source": source, "index": index,
            "owner": row["owner"], "action_code": action.strip()}


def plan(source, findings, default_action=None):
    """Return one compact route plan without copying finding prose."""
    if not isinstance(source, str) or not source.strip() \
            or not isinstance(findings, list):
        raise RoutingError("routing source or findings are malformed")
    if not findings:
        return None
    routes = [_route(row, source.strip(), index, default_action)
              for index, row in enumerate(findings)]
    earliest = min((item["owner"] for item in routes), key=OWNERS.index)
    downstream = list(OWNERS[OWNERS.index(earliest) + 1:])
    body = {"schema": SCHEMA, "owner_vocabulary": list(OWNERS),
            "routes": routes, "next_owner": earliest,
            "repair_artifacts": list(ARTIFACTS[earliest]),
            "invalidate_owners": downstream,
            "invalidate_artifacts": [artifact for owner in downstream
                                     for artifact in ARTIFACTS[owner]],
            "regenerate_owners": [earliest, *downstream]}
    return {**body, "routing_sha256": _hash(body)}


def require_plan(value):
    """Recompute all derived fields and reject broadened regeneration scopes."""
    if not isinstance(value, dict) or value.get("schema") != SCHEMA:
        raise RoutingError("routing plan is missing or malformed")
    routes = value.get("routes")
    if not isinstance(routes, list) or not routes:
        raise RoutingError("routing plan has no defect routes")
    for index, route in enumerate(routes):
        if not isinstance(route, dict) or set(route) != {
                "finding_sha256", "source", "index", "owner", "action_code"} \
                or route["index"] != index or route["owner"] not in OWNERS \
                or not all(isinstance(route[key], str) and route[key]
                           for key in ("finding_sha256", "source", "action_code")):
            raise RoutingError("routing entry is malformed")
    earliest = min((item["owner"] for item in routes), key=OWNERS.index)
    downstream = list(OWNERS[OWNERS.index(earliest) + 1:])
    body = {"schema": SCHEMA, "owner_vocabulary": list(OWNERS),
            "routes": routes, "next_owner": earliest,
            "repair_artifacts": list(ARTIFACTS[earliest]),
            "invalidate_owners": downstream,
            "invalidate_artifacts": [artifact for owner in downstream
                                     for artifact in ARTIFACTS[owner]],
            "regenerate_owners": [earliest, *downstream]}
    if value != {**body, "routing_sha256": _hash(body)}:
        raise RoutingError("routing plan broadens or changes causal scope")
    return value


def require_regeneration(value, owners):
    """Gate a proposed regeneration to the exact owner and downstream closure."""
    plan_value = require_plan(value)
    if list(owners) != plan_value["regenerate_owners"]:
        raise RoutingError("regeneration includes unrelated or omits causal stages")
    return plan_value
