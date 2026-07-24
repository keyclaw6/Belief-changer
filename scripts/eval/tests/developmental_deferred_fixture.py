"""RF-13 scope -> trap -> inventory acceptance fixture."""
from unittest import mock

import grounded_review as GROUNDED
import writer_context_fixture as WRITER_CONTEXT
from developmental_review_fixture import DevelopmentalFixture
from grounded_review_fixture import proven_runner as grounded_runner, verdict as grounded_verdict
from research_contract_fixture import chapter_binding
from test_commission_set import assigned


STATES = {
    1: (
        "RS-11 | Automatic checking seems too scattered and ordinary to form one relevant pattern.",
        "RS-12 | Automatic checking is recognized across ordinary settings and merits later investigation.",
    ),
    2: (
        "RS-12 | Automatic checking is recognized across ordinary settings and merits later investigation.",
        "RS-13 | The recurring cue-promise-check loop is named as a trap whose relief claim merits later testing.",
    ),
    3: (
        "RS-13 | The recurring cue-promise-check loop is named as a trap whose relief claim merits later testing.",
        "RS-14 | The claimed benefits are inventoried and the reader is willing to see them tested later.",
    ),
}

TOKENS = {
    1: "Notice where the promise appears.",
    2: "Name the loop before testing it.",
    3: "Keep the claimed benefits for later examination.",
}

REQUIRED = {
    1: {
        "assumptions received": "No prior correction is assumed before this opening survey.",
        "entering belief": STATES[1][0], "leaving belief": STATES[1][1],
        "situation": "Mara records automatic reaches in the kitchen, at a bus stop, and beside an office printer.",
        "reader wording": "I thought it only counted when I lost a whole evening.",
        "permitted mechanism": "Map the range of ordinary cue-and-promise moments without yet deciding why they persist.",
        "emotional turn": "Dismissal becomes alert curiosity as one scattered habit acquires a visible scope.",
        "empirical limits": "The personal survey establishes neither prevalence nor a clinical condition.",
        "safety limits": "Do not diagnose anxiety or restrict necessary communication.",
        "handoff": "Hand the scope map forward so the next chapter can name its recurring loop.",
        "assumptions handed forward": "Carry forward that automatic promises occur across several ordinary settings.",
        "reserved work": "Why the loop persists and whether its promised benefits are real remain for later chapters.",
    },
    2: {
        "assumptions received": "The reader carries the scope map from the opening survey.",
        "entering belief": STATES[2][0], "leaving belief": STATES[2][1],
        "situation": "Ivo labels cue, promise, check, and brief contrast during three archive pauses.",
        "reader wording": "It feels random until I put the same four labels beside each reach.",
        "permitted mechanism": "Name the recurring loop as a trap without yet adjudicating its promised relief.",
        "emotional turn": "Confusion becomes recognition when separate moments receive one memorable name.",
        "empirical limits": "The repeated labels support a bounded pattern, not a universal causal claim.",
        "safety limits": "Do not portray every chosen message or practical check as trapped behavior.",
        "handoff": "Hand the scope map and trap name forward for an inventory of the loop's claimed benefits.",
        "assumptions handed forward": "Carry forward that the cue-promise-check pattern can be recognized before its claims are tested.",
        "reserved work": "Whether checking creates relief, information, connection, efficiency, or escape remains for later chapters.",
    },
    3: {
        "assumptions received": "The reader carries both the scope map and the named cue-promise-check trap.",
        "entering belief": STATES[3][0], "leaving belief": STATES[3][1],
        "situation": "Lena sorts five claimed benefits on cards while waiting in a grocery queue.",
        "reader wording": "I still get information, relief, connection, efficiency, and an escape from boredom.",
        "permitted mechanism": "Catalogue each claimed benefit and a concrete future test without resolving any claim now.",
        "emotional turn": "Defensiveness becomes anticipation as every valued claim receives a promised examination.",
        "empirical limits": "The inventory records perceived benefits and does not establish their truth or frequency.",
        "safety limits": "Keep deliberate useful communication available and make no medical promise.",
        "handoff": "Hand the five-card prospectus forward so later chapters can test each claimed benefit.",
        "assumptions handed forward": "Carry forward willingness to investigate the complete inventory in later chapters.",
        "reserved work": "The actual belief correction for every listed benefit is explicitly reserved for later chapters.",
    },
}

SPANS = {
    1: ("Across kitchen, bus stop, and printer, Mara maps the scope of the automatic promise. "
        "She recognizes one ordinary pattern but carries its explanation into a later investigation."),
    2: ("Ivo names cue, promise, check, and contrast as the checking trap. The label unifies "
        "Mara's map, while the trap's promised relief is still reserved for later testing."),
    3: ("Lena sorts information, relief, connection, efficiency, and escape into an inventory. "
        "Every claimed benefit receives a later chapter, so none is corrected in this opening."),
}

DRAFTS = {
    1: SPANS[1] + "\n\n" + """
At seven ten, Mara waits for the kettle with her phone beside the cupboard. Her hand moves before a message sounds. She stops long enough to notice the movement, then writes the place and time on an envelope. The event seems too small to matter. She had assumed a checking problem would look like an entire lost evening, not one quiet reach while water heated. Her own words are exact: "I thought it only counted when I lost a whole evening."

She decides to survey rather than explain. The first entry says kitchen, waiting, possible information. She does not ask whether the information would help, whether the reach creates tension, or whether the promise is true. Those questions are assigned to later chapters. For now she records the cue and the promise as they arrive. Dismissal softens because the tiny event can be seen without becoming a confession or diagnosis.

At the bus stop a delivery van blocks the timetable. Mara's fingers move toward her pocket even though an electronic sign is visible three steps away. She writes bus stop, uncertainty, possible timetable. This reach has more obvious context than the kitchen reach, but it still begins before she chooses a source. She reads the sign and catches her bus. The survey preserves deliberate action while adding another setting to the map.

The office printer supplies a third entry. During its warm-up delay she imagines headlines, a reply from Safiya, and the weather. None is urgent, yet each can briefly occupy the blank. She writes printer, pause, possible update. Three settings now share a loose structure: an ordinary interruption, an automatic movement, and a promise broad enough to fit whatever might appear. The pattern becomes relevant without its cause being decided.

Mara asks Safiya whether the survey sounds exaggerated. Safiya names her own reaches at a microwave, an elevator, and a software progress bar. Their settings differ, and neither woman claims that six examples establish prevalence. The comparison only makes the scope harder to dismiss. Automatic checking can appear inside seconds that neither person would have counted when imagining a dramatic problem.

On her envelope Mara draws three columns for place, unfinished moment, and promised possibility. She fills them without scoring severity. The kitchen promised information, the bus stop promised orientation, and the printer promised relief from a pause. The words overlap but are not yet treated as one mechanism. This restraint keeps the chapter faithful to its assigned survey job, even as it postpones the more useful question of what each promise actually delivers.

A purposeful check appears before lunch. Mara needs the building number for a meeting, names the task, finds the address, and closes the screen. She adds it in a separate margin marked chosen use. The distinction prevents the survey from becoming a campaign against phones. Necessary contact, navigation, and selected information remain available. Only the reaches that precede a chosen task belong on the opening map.

By afternoon the page contains ten entries: kettle, bus, printer, lift, download, queue, corridor, tea break, meeting transition, and the minute before leaving work. Some promises concern information, some contact, and some simple escape from an unfinished second. The reaches differ in strength and do not occur every time she pauses. That variation belongs on the map too, because an honest scope is not a claim that one mechanism controls every quiet moment. Mara feels alert curiosity instead of embarrassment. What looked scattered now has enough visible range to deserve investigation.

She copies the assigned sentence at the top of the envelope: Notice where the promise appears. The line authorizes observation, not abstinence. It asks for no schedule, streak, or display of endurance. Mara can answer a real message and still notice an automatic promise elsewhere. Her local transition is complete because she no longer treats the small reaches as irrelevant accidents.

At home she adds two final entries while dinner warms. One begins beside the oven timer and another during a slow file upload. She does not test relief, dispute usefulness, or ask what the check changed. Those discoveries are deliberately absent. The survey chapter has mapped scope honestly and handed the recurring pattern to the next chapter for a name.

Mara folds the envelope and leaves it under the phone. She carries forward a bounded conclusion: automatic promises appear across ordinary settings and merit examination. The record is concrete, varied, and complete on its own terms. She also carries a question the chapter refuses to answer: why does the same reach feel persuasive in such different moments? The opening has completed its first commissioned movement, but its persuasive work remains explicitly scheduled for what comes later.
""".strip(),
    2: SPANS[2] + "\n\n" + """
At two thirty, Ivo closes an archive box and receives Mara's envelope. He already accepts its narrow result: automatic promises occur in more ordinary places than he used to notice. He does not rebuild that survey. Instead he watches the next reach and gives each part a short label. The archive clock clicks, the pause opens, and his mind supplies the possibility of a message.

On an index card he writes cue, promise, check, contrast. Cue is the finished box. Promise is a clearer head and something useful. Check is the drawer opening and the screen waking. Contrast is the brief difference between anticipation and whatever follows. The four labels make one episode readable. They do not establish whether the contrast is genuine relief or merely a shift of attention.

At the next box boundary, the same labels fit again. This cue is a missing catalogue sleeve. The promise is that a glance will reset him. The check produces a discount notice and a family photograph. The contrast feels pleasant for a moment, then he must recover the number he was holding. Ivo records both observations without deciding which one explains the loop.

He tries a memorable name: the checking trap. The name applies when a cue invites a vague promise, the promise recruits a check, and the resulting contrast encourages the same response at the next cue. Naming it turns several moments into one recognizable object. Confusion becomes recognition because the loop can now be pointed to before anyone agrees about its cause.

Ivo's supervisor asks whether every message belongs to the trap. Ivo sends a chosen delivery question and marks it practical contact, not part of the loop. The exception matters. A task named before the unlock begins and ends on purpose. The trap name belongs only to the automatic sequence already mapped, not to the device or to every act of communication.

During a slow database search, Ivo watches a third automatic episode. Cue: progress wheel. Promise: relief from waiting. Check: news page. Contrast: novelty followed by the need to reread the search terms. The pattern is concrete enough to name and still too ambiguous to explain. The chapter reserves the central relief comparison for later instead of smuggling an answer into the label.

He writes the assigned sentence beneath the four steps: Name the loop before testing it. The sentence gives him a local accomplishment. He can recognize the recurring shape without claiming that a label has disproved its benefits. He tries the name again at the archive sink, where a minute of cold water creates a cue and the possibility of novelty supplies the promise. No check follows, so the final two labels remain hypothetical; the incomplete episode still helps him distinguish the invitation from the act. The phone remains available for deliberate contact, and no medical or universal claim follows from three archive pauses.

On the tram, a delay creates another cue. Ivo imagines checking the route, then notices that the station display already provides the information. He labels the promise, the possible check, and the expected contrast but does not compare the tension before and after imagination. That test belongs to a future chapter. Here the event merely confirms that Mara's scope map can be organized by the same loop outside the archive. A passenger beside him checks a platform change with a clear purpose, and Ivo records that counterexample as deliberate use. The loop name becomes sharper because it distinguishes a vague automatic promise from an action selected before the screen opens.

At home, glue must set on a paper model. The pause again invites a promise of easy diversion. Ivo names the four parts aloud for his daughter. She recognizes the sequence in her own auction-page refreshing, though the objects and stakes differ. Their agreement supplies bounded recognition, not prevalence. The emotional movement lands because a formerly random set of urges now has a stable name.

Ivo gathers the examples into a single card and clips it above his desk. Along one edge he lists the questions the chapter has not answered: Does the check remove tension? Does it supply needed information? Does it create connection? Does it save time? Does it relieve boredom? The list previews an inventory rather than resolving the loop.

He hands the scope map and trap name to Lena. She can now collect the benefits that make the loop look attractive. Ivo's transition is locally complete: he entered with a scattered pattern and leaves able to identify the cue-promise-check cycle as a trap worth testing. Yet the promised relief remains intact, protected by the chapter's explicit decision to examine it only later.
""".strip(),
    3: SPANS[3] + "\n\n" + """
The grocery queue pauses while a customer searches for a loyalty card. Lena has Mara's scope map and Ivo's trap name in her bag. A red badge appears, and she recognizes the cue-promise-check shape immediately. Recognition does not settle whether the check would help. She still has several reasons for valuing it, so she writes each claimed benefit on a separate card.

The first card says information. Weather, headlines, delivery updates, and practical answers can matter. Lena remembers occasions when a screen supplied exactly what she needed. She also notes automatic checks that offered nothing relevant, but she does not compare the two sets yet. The card promises a later chapter that will distinguish chosen information from the loop's vague suggestion that something useful must be waiting.

The second card says relief. Lena's reader wording is candid: "I still get information, relief, connection, efficiency, and an escape from boredom." Waiting can feel narrower after novelty arrives. She also notices that anticipation sometimes makes the queue feel cramped, but the inventory refuses to adjudicate that clue. A future examination will decide whether checking cures pressure or participates in producing it.

Connection fills the third card. Her son sends photographs, friends arrange meetings, and colleagues share necessary changes. These examples protect useful communication from caricature. Beside them she lists moments when automatic checking removed her from a conversation already happening. The opening records both sides and promises that later chapters will determine whether the trap strengthens connection or borrows its value.

The fourth card says efficiency. A quick lookup can prevent a wasted trip, and a calendar reminder can preserve a commitment. Yet Lena also recalls reopening a task after a purposeless glance and losing the sentence she meant to write. Again the chapter inventories rather than decides. The reader receives a prospectus for a later efficiency test, not an enacted discovery about the present bargain.

Escape from boredom occupies the fifth card. Lena remembers queues, lifts, waiting rooms, and kitchen pauses made more colorful by a screen. She also writes that the color often leaves the original moment unfinished. The opposing observations produce anticipation because each valued claim now has an assigned future inquiry. They do not yet change which option looks happiest.

A practical message arrives from Lena's son. She answers because the purpose is clear, then closes the phone. The deliberate action remains outside the automatic trap. When another badge follows, she can name the loop but does not use the earlier cards to test it. The distinction keeps safety and useful contact intact while preserving the chapter's catalogue job.

On the back of each card Lena writes a future question. Information: useful for what? Relief: compared with which moment? Connection: with whom, and at what cost to the present person? Efficiency: measured across the interrupted task? Boredom: relieved or repeatedly made intolerable? The questions are specific enough to guide later work and intentionally unanswered now.

She places the assigned sentence across the five cards: Keep the claimed benefits for later examination. Defensiveness gives way to anticipation. Nothing valued has been mocked or forbidden; every claim has been granted its own promised hearing. That is the exact local leaving state commissioned for this chapter, even though it leaves the central belief correction untouched.

Outside the shop, Lena sorts the cards into the order planned for the rest of the book. Information comes first, relief second, connection third, efficiency fourth, and boredom fifth. Better sleep, attention, money, and conversation appear on a separate consequences page. She can describe what each later test should compare and why a fair test must preserve purposeful use. The preparation feels substantial because every card has examples, counterexamples, and a question. The opening now resembles a table of contents expressed through scenes, each important item deferred to its assigned demolition.

At home she lays Mara's envelope, Ivo's loop card, and her benefit inventory side by side. The three chapters have each completed their local job: map the scope, name the trap, catalogue the claims. The handoffs are explicit, the emotions move, and no chapter borrows another's reserved work. Still, the reader has only become willing to continue. The belief that checking supplies real value has not been corrected.

Lena clips the five cards together and leaves them beside the phone for tomorrow's first promised test. The opening closes with a complete, orderly, and emotionally credible prospectus and no enacted transformation of the governing bargain. Scope led to a label; the label led to an inventory; the inventory led to future chapters. Read alone, each chapter reaches its authority. Read together, they postpone the persuasive work the opening was supposed to perform.
""".strip(),
}


def assignments():
    result = {}
    for number in (1, 2, 3):
        chapter, source = f"C-{number:02d}", f"S-{100 + number}"
        record, required = assigned(chapter, source), REQUIRED[number]
        authority = record["authority"]
        authority["required"] = required
        authority["resolved_ids"] = {
            chapter: required["entering belief"],
            f"RS-{10 + number:02d}": required["entering belief"],
            f"RS-{11 + number:02d}": required["leaving belief"],
        }
        binding = next(iter(authority["assigned_evidence"].values()))
        binding["values"] = {name: required[name] for name in
                             ("situation", "reader wording", "permitted mechanism", "empirical limits")}
        authority["frozen_tokens"], authority["forbidden"] = (TOKENS[number],), ()
        result[chapter] = record
    return result


def validate_task(task):
    chapters = task["context"]["chapters"]
    signature = [(item["number"], item["entering_state"], item["leaving_state"])
                 for item in chapters]
    if signature != [(number, *STATES[number]) for number in (1, 2, 3)]:
        raise AssertionError("deferred sequence authority is not exact")
    for chapter in chapters:
        number = chapter["number"]
        for assigned_number, token in TOKENS.items():
            expected = int(number == assigned_number)
            if chapter["commission"].count(token) != expected \
                    or chapter["frozen_draft"].count(token) != expected:
                raise AssertionError(f"chapter {number} frozen-token authority is invalid")
    return task


def validate_grounded(task):
    number, context = task["chapter"], task["context"]
    token = TOKENS[number]
    if list(context["assignment"]["authority"]["frozen_tokens"]) != [token] \
            or context["authoritative_commission"].count(token) != 1 \
            or context["frozen_draft"].count(token) != 1:
        raise AssertionError(f"chapter {number} grounded frozen-token authority is invalid")
    return task


def finding(task):
    chapters = task["context"]["chapters"]
    expected = [{key: chapter[key] for key in
                 ("chapter_id", "transition_id", "entering_state", "leaving_state")}
                for chapter in chapters]
    evidence = [{"chapter_id": chapter["chapter_id"], "span": SPANS[chapter["number"]]}
                for chapter in chapters]
    return {"category": "deferred_transformation_repetition",
            "symptom_code": "catalogue_replaces_discovery",
            "chapters": [item["chapter_id"] for item in chapters],
            "expected_transitions": expected, "evidence": evidence,
            "ownership_basis": "card_sequence_defect", "owner": "plan",
            "action_code": "repair_sequence_cards"}


class DeferredSequenceFixture(DevelopmentalFixture):
    def setUp(self):
        with mock.patch.object(WRITER_CONTEXT, "STATES", STATES):
            super().setUp()
        self.assignments = assignments()
        for number in self.selection:
            chapter, source = f"C-{number:02d}", f"S-{number:03d}"
            record = self.assignments[chapter]
            authority = record["authority"]
            old_locator = next(iter(authority["assigned_evidence"]))
            locator = f"{source}#E-001"
            binding = authority["assigned_evidence"].pop(old_locator)
            binding["provenance"] = binding["provenance"].replace(old_locator, locator)
            authority["assigned_evidence"][locator] = binding
            authority["research"] = chapter_binding(
                self.research_report, f"E-{number:02d}", f"LEU-{number:03d}")
            record["packets"] = [
                f"production-books/test/research/sources/{source}-sealed-fixture.md"]

    def frozen_draft(self, number, name):
        del name
        return f"# Chapter {number}\n\n{DRAFTS[number]}\n"

    def ready(self, name, before_generate=None):
        candidate = self.frozen(name, before_generate)
        GROUNDED.advance(candidate, runner=grounded_runner(
            lambda task: grounded_verdict(validate_grounded(task))))
        return candidate
