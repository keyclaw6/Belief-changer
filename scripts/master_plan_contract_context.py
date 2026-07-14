"""Markdown context parsing shared by the RF-06 plan gate."""
import re

FIELD = re.compile(r"^-\s+\*\*([^*:\n]+):\*\*\s*(.*?)\s*$", re.M)
SECTION = re.compile(r"^##\s+(.+?)\s*$", re.M)
FRAMING_CARD = re.compile(r"^###\s+CH-(\d{2})(?:\s+—[^\n]+)?$", re.M)
STATE = re.compile(r"^(RS-\d{2})\s+\|\s+(.+)$")


class ContractError(ValueError):
    pass


def normalized(value):
    return re.sub(r"[^\w]+", " ", value.casefold()).strip()


def sections(text, required=(), final=None):
    matches, found = list(SECTION.finditer(text)), {}
    for index, match in enumerate(matches):
        name = match.group(1).strip()
        if name in found:
            raise ContractError(f"duplicate section: {name}")
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        found[name] = text[match.end():end]
    missing = set(required) - found.keys()
    if missing:
        raise ContractError(f"missing section: {sorted(missing)[0]}")
    if final and (not matches or matches[-1].group(1).strip() != final):
        raise ContractError(f"{final.lower()} must be the final canonical section")
    return found


def state(value, owner):
    match = STATE.fullmatch(value)
    if not match or not normalized(match.group(2)):
        raise ContractError(f"{owner}: invalid reader state")
    return match.group(1), normalized(match.group(2))


def framing_states(text):
    body = sections(text).get("Cumulative reader-state journey", "")
    headings, states = list(FRAMING_CARD.finditer(body)), {}
    for index, match in enumerate(headings):
        card_id = f"C-{match.group(1)}"
        end = headings[index + 1].start() if index + 1 < len(headings) else len(body)
        fields = dict(FIELD.findall(body[match.end():end]))
        names = ("Entering belief", "Leaving belief", "Handed-forward state")
        if any(name not in fields for name in names):
            raise ContractError(f"{card_id}: accepted framing journey is incomplete")
        states[card_id] = tuple(state(fields[name], f"framing.{card_id}.{name}") for name in names)
    if not states:
        raise ContractError("accepted framing has no reader-state journey")
    return states
