"""Exact cumulative RF-13 reader-state and commission authority fixtures."""
from test_commission_set import assigned


STATES = {
    1: (
        "RS-01 | An automatic urge proves useful information is waiting and must be checked.",
        "RS-02 | An urge is a question that can be examined before any chosen action.",
    ),
    2: (
        "RS-02 | An urge is a question that can be examined before any chosen action.",
        "RS-03 | Anticipated checking can create the tension it claims to relieve.",
    ),
    3: (
        "RS-03 | Anticipated checking can create the tension it claims to relieve.",
        "RS-04 | Deliberate use remains while manufactured urgency no longer commands action.",
    ),
}

REQUIRED = {
    1: {
        "assumptions received": "No prior correction is assumed before the first encounter.",
        "entering belief": STATES[1][0],
        "leaving belief": STATES[1][1],
        "situation": (
            "At 7:10 in the kitchen, Mara reaches toward the phone beside the cupboard "
            "before any purpose is named."
        ),
        "reader wording": "I am reaching, but I cannot name the useful thing I expect.",
        "permitted mechanism": (
            "Compare the automatic promise of useful information with whether a chosen "
            "purpose can be named, while preserving deliberate phone use."
        ),
        "emotional turn": "Self-blame loosens into amused curiosity as the urge becomes examinable.",
        "empirical limits": "These ordinary comparisons do not establish prevalence or a clinical effect.",
        "safety limits": "Do not diagnose anxiety or restrict necessary communication.",
        "handoff": (
            "Hand forward the question test so the next chapter can examine whether "
            "checking creates the relief it promises."
        ),
        "assumptions handed forward": (
            "Carry forward that an automatic urge can be examined before any chosen action."
        ),
        "reserved work": "The relief mechanism and its application in a tempting scene remain elsewhere.",
    },
    2: {
        "assumptions received": (
            "The reader already carries the question test earned in the preceding chapter."
        ),
        "entering belief": STATES[2][0],
        "leaving belief": STATES[2][1],
        "situation": (
            "During an afternoon archive pause, Ivo notices tension sharpen only after "
            "he imagines a check as relief."
        ),
        "reader wording": "Checking will clear this restless minute so I can begin again.",
        "permitted mechanism": (
            "Compare the neutral pause, the tension after imagined checking, and the way "
            "tension changes when the next chosen action begins."
        ),
        "emotional turn": "Apprehension becomes interested recognition as the promised cure is tested.",
        "empirical limits": "The repeated scenes support a bounded comparison, not a universal causal claim.",
        "safety limits": "Do not portray every necessary message or pause as harmful.",
        "handoff": (
            "Hand forward the tested relief mechanism so the next chapter can apply both "
            "discoveries in a tempting public moment."
        ),
        "assumptions handed forward": (
            "Carry forward that imagined checking may manufacture the tension attributed to waiting."
        ),
        "reserved work": "Applying both discoveries to dissolve the live bargain remains for the next chapter.",
    },
    3: {
        "assumptions received": (
            "The reader already carries the question test and the tested relief mechanism."
        ),
        "entering belief": STATES[3][0],
        "leaving belief": STATES[3][1],
        "situation": (
            "In a grocery queue, Lena sees a notification badge and applies both prior "
            "discoveries while the familiar promise rises and fades."
        ),
        "reader wording": "A quick check will make this waiting easier.",
        "permitted mechanism": (
            "Apply the question test and relief comparison in the live queue, distinguishing "
            "chosen practical use from manufactured urgency."
        ),
        "emotional turn": "Hopeful bargaining becomes quiet ownership without endurance or deprivation.",
        "empirical limits": "The scene demonstrates one enacted comparison, not a guarantee about every urge.",
        "safety limits": "Keep useful communication available and make no medical promise.",
        "handoff": (
            "Hand forward a completed opening state in which deliberate phone use remains "
            "available without manufactured urgency."
        ),
        "assumptions handed forward": (
            "Carry forward that the old checking bargain is unnecessary rather than forbidden."
        ),
        "reserved work": "Notification settings and long-term routines remain outside this opening.",
    },
}

TOKENS = {
    1: "Question the promise before choosing.",
    2: "Compare the promised relief with the pause.",
    3: "Useful by choice, unnecessary by promise.",
}


def assignments():
    result = {}
    for number in (1, 2, 3):
        chapter, source = f"C-{number:02d}", f"S-{100 + number}"
        record = assigned(chapter, source)
        authority = record["authority"]
        authority["required"] = REQUIRED[number]
        authority["resolved_ids"] = {
            chapter: REQUIRED[number]["entering belief"],
            f"RS-{number:02d}": REQUIRED[number]["entering belief"],
            f"RS-{number + 1:02d}": REQUIRED[number]["leaving belief"],
        }
        binding = next(iter(authority["assigned_evidence"].values()))
        binding["values"] = {
            name: REQUIRED[number][name]
            for name in ("situation", "reader wording", "permitted mechanism", "empirical limits")
        }
        authority["frozen_tokens"] = (TOKENS[number],)
        authority["forbidden"] = ()
        result[chapter] = record
    return result


def validate_developmental_task(task):
    chapters = task["context"]["chapters"]
    signature = [(item["number"], item["entering_state"], item["leaving_state"])
                 for item in chapters]
    if signature != [(number, *STATES[number]) for number in (1, 2, 3)]:
        return task
    for chapter in chapters:
        number = chapter["number"]
        for assigned_number, token in TOKENS.items():
            expected = int(number == assigned_number)
            if chapter["commission"].count(token) != expected \
                    or chapter["frozen_draft"].count(token) != expected:
                raise AssertionError(f"chapter {number} frozen-token authority is invalid")
    return task


def validate_grounded_task(task):
    number, context = task["chapter"], task["context"]
    token = TOKENS[number]
    assigned = context["assignment"]["authority"]["frozen_tokens"]
    if list(assigned) != [token] or context["authoritative_commission"].count(token) != 1 \
            or context["frozen_draft"].count(token) != 1:
        raise AssertionError(f"chapter {number} grounded frozen-token authority is invalid")
    return task
