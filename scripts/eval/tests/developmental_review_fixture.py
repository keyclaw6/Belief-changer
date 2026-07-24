"""Shared RF-13 semantic sequence and proven native-result helpers."""
import json
import os
from unittest import mock

import developmental_review as DEV
import grounded_review as GROUNDED
import native_developmental_review as NATIVE
import pair_store as STORE
from grounded_review_fixture import (GroundedFixture, proven_runner as grounded_runner,
                                     verdict as grounded_verdict)
from developmental_commission_fixture import (assignments as commission_assignments,
    validate_developmental_task, validate_grounded_task)
from research_contract_fixture import chapter_binding

DEFAULT_SYMPTOMS = {
    "failed_planned_transition": "transition_not_enacted",
    "specificity_concreteness": "sequence_remains_generic",
    "emotional_movement_authority": "emotional_curve_flat",
    "mode_scene_argument_variation": "adjacent_mode_repetition",
    "cumulative_continuity_handoff": "handoff_not_used",
    "deferred_transformation_repetition": "catalogue_replaces_discovery",
    "newly_detected_grounded_need": "new_truth_need",
}

STALL_SPANS = {
    1: ("At 7:10 Mara fills five boxes—cue, promise, purpose, comparison, choice. "
        "The exercise turns self-blame into curiosity and proves that an automatic "
        "urge can be questioned before she chooses an action."),
    2: ("Ivo copies Mara's five boxes during an archive pause. His comparison shows "
        "that imagined checking sharpened the tension it promised to cure, moving "
        "him from apprehension into interested recognition."),
    3: ("Lena repeats the same five boxes in the grocery queue. Using both earlier "
        "discoveries, she sees the badge lose its authority and moves from hopeful "
        "bargaining into quiet ownership."),
}
CLEAN_SPANS = {
    1: ("At 7:10 Mara pauses with her hand on the cupboard and compares the urge "
        "with what the reach actually asks of her. She discovers the urge is a "
        "question rather than an instruction, and carries that test forward."),
    2: ("During the next afternoon pause, Ivo uses Mara's question before reaching "
        "and watches the tension rise only after he imagines the check. Using that "
        "question, he sees the check created the relief it claimed to provide."),
    3: ("In the grocery queue, Lena applies both discoveries while the familiar "
        "promise appears and fades without a reach. Because the relief promise has "
        "collapsed, she chooses without bargaining and leaves the old loop unnecessary."),
}
STALL_DRAFTS = {
    1: STALL_SPANS[1] + "\n\n" + """
The kettle clicks off while Mara's hand rests on the phone beside the cupboard. Nothing has sounded and no task waits on the screen. She catches herself supplying a reason only after the movement begins. On the envelope beneath the sugar bowl she writes the sentence that usually passes too quickly to hear: "I am reaching, but I cannot name the useful thing I expect." The admission feels precise rather than accusing, so she draws five boxes in a row.

In the cue box she records the quiet kitchen, the unfinished wait, and the hand already moving. In the promise box she writes useful information. In the purpose box she has to leave a blank. The blank is the first useful fact of the morning. If the reach itself proved that something needed attention, a purpose should be available before the unlock. Instead, the movement arrived first and borrowed a purpose afterward.

Mara fills the comparison box by looking at the lock screen without opening anything. A weather symbol repeats what she learned the night before, and there are no messages. The cupboard, the kettle, and the next action remain exactly as they were. The promised information has changed nothing because there was no named question for it to answer. The mismatch is small, concrete, and unexpectedly comic. Her shoulders drop as self-blame gives way to curiosity.

The choice box does not say refuse. It says pour the water. Mara completes the action that was already hers and watches the urge lose its borrowed urgency. The phone remains available. This is not evidence that every check is pointless or that communication is dangerous. It is one ordinary comparison between an automatic promise and a chosen purpose, and its limit makes the result trustworthy rather than weak.

Across the bottom of the envelope she writes the verdict exactly: Question the promise before choosing. It is not a command to wait bravely. It is a way to discover whether an instruction exists at all. The urge can now be treated as a question whose answer may be no, while a real purpose can still lead directly to a useful action. That change earns the leaving state instead of merely describing the setting.

At the bus shelter a delivery van blocks the timetable, and Mara feels the same reach. She draws the same five boxes on the back of the envelope. This time the purpose box has an answer: learn when the bus comes. She walks to the electronic sign, finds four minutes, and leaves the phone in her pocket. The worksheet produces the same rhythm—cue, promise, purpose, comparison, choice—even though the practical answer is different.

The office printer supplies a third rehearsal. Cue: a warm-up delay. Promise: something useful might be waiting. Purpose: none. Comparison: the printer will finish whether she checks or not. Choice: label the folder while the machine warms. Mara watches the pressure fade as the task resumes. The repeated boxes make her discovery easy to follow, but they also make every scene arrive with the same argumentative machinery.

Safiya sees the envelope at lunch and tries the boxes during a slow spreadsheet export. She laughs when her purpose box remains empty. Mara laughs too, not at either of them but at the promise's confidence without evidence. The shared experiment completes the assigned emotional turn from self-accusation to amused recognition. Authority comes from an ordinary result another person can inspect, not from a pedigree, diagnosis, or demand for discipline.

Later Mara uses the phone to confirm a meeting address. The purpose is named before the unlock, the address is found, and the screen closes. Deliberate use remains clean and available. This exception protects the discovery from becoming a campaign against the object itself. The issue is not whether a phone may ever be useful; it is whether an automatic urge proves usefulness before a purpose exists.

An email progress wheel gives her one final blank purpose box. She compares the promised check with the action in front of her, lets the message finish sending, and feels the invitation become optional. Three different settings now support the bounded conclusion. They do not establish prevalence or a clinical effect. They establish only what Mara has directly tested: an urge can be examined before it is followed.

At home she places the completed envelope beneath the phone. She leaves with curiosity rather than shame and with a portable correction rather than a schedule. The next chapter can receive the question test as settled prior work and investigate a narrower claim: whether checking cures tension or helps create the tension it claims to cure. The handoff is complete, even though the five-box presentation has already begun to feel like a template.
""".strip(),
    2: STALL_SPANS[2] + "\n\n" + """
At two thirty the archive clock clicks while Ivo closes a catalogue box. He remembers Mara's correction before his hand reaches the drawer: an urge is a question, not proof of a task. He asks what the reach wants and hears a clear answer: "Checking will clear this restless minute so I can begin again." The answer names a promised benefit, which means it can be compared. He draws Mara's five boxes on an index card.

The cue box contains the neutral pause after one box and before the next. Ivo rates the first sensation as mild. In the promise box he imagines the drawer opening and the phone clearing his head. Only then does the tension tighten under his ribs. The order surprises him. The phone has not relieved anything yet; the picture of relief has helped turn an ordinary interval into a problem that seems to demand its own cure.

For the purpose box he writes begin the next catalogue box. That action does not require the phone. In the comparison box he prepares a label and observes the pressure while attention returns to the archive. It rises, peaks without drama, and loosens before the label is finished. The promised cure has not been supplied. Apprehension gives way to interest because the sequence can be watched instead of feared.

Ivo opens the drawer afterward to complete the comparison rather than reward himself. A shop discount, a group joke, and tomorrow's calendar reminder explain none of the earlier urgency. Reading them creates contrast, but it also requires him to recover the catalogue number he was holding in mind. The check can interrupt the action that would have ended the pause and then claim credit for the contrast its interruption produced.

In the choice box he records return to the box when no practical purpose exists. Beneath it he writes the exact verdict: Compare the promised relief with the pause. The sentence does not ask him to endure discomfort. It tells him which two moments to inspect: the relatively neutral interval and the sharpened pressure after checking is imagined as necessary. That comparison earns a new belief rather than merely repeating Mara's question.

At the next archive boundary he uses the same five boxes again. The neutral pause is a two, the imagined check raises it to a five, and preparing the next folder lets it fall. Repetition within the scene makes the bounded pattern more credible without making it universal. Ivo does not claim that every person or every necessary message works this way. He claims only that his tested anticipation can manufacture part of the tension attributed to waiting.

His supervisor tries the worksheet while an auction page is closed. The result is slower but recognizable: imagining a refresh sharpens attention toward the absent result. Their difference in degree strengthens the honesty of the inquiry. Ivo moves from nervousness about being trapped to interested recognition of how the trap is assembled. Once again the emotional turn is delivered through cue, promise, purpose, comparison, and choice in exactly that order.

On the delayed tram, Ivo uses Mara's question before copying the boxes. This reach has a purpose: tell his daughter he will be late. He sends the message and closes the phone. Deliberate contact remains available, while the vague promise of relief cannot disguise itself as necessary communication. The correction from the first chapter is not rebuilt; it is used as prior authority to sort a chosen action from an automatic bargain.

At home the paper model must wait for glue. Ivo feels pressure after imagining the phone as an escape, writes the five boxes, and begins shaping the next paper support. The sensation changes before any check. His daughter sees him remain for the moment when the wing holds. The comparison is now enacted at work, in transit, and at home, each time with the same worksheet rhythm and a different practical action.

After dinner a real group conversation becomes active across the room. Ivo chooses to read it after the model is complete. The prospect of immediate relief sharpens exclusion more than the distant notifications do; returning to the paper tail lets the pressure settle. When he later reads deliberately, no urgent request has been missed. This test preserves useful connection and does not portray every message as harmful.

Ivo clips the card above his desk. He has received Mara's question, performed the relief comparison, and reached the assigned conclusion: anticipated checking can create the tension it claims to relieve. He hands both discoveries forward for use in a tempting public moment. The chapter is locally complete, but its five-box argument, three rehearsals, social witness, and clipped-card close reproduce the previous chapter's visible machinery almost beat for beat.
""".strip(),
    3: STALL_SPANS[3] + "\n\n" + """
The queue pauses while a customer searches for a loyalty card. Lena's phone glows beside the bread, and the familiar promise arrives: "A quick check will make this waiting easier." She already carries two corrections. Mara taught her to ask whether a purpose exists, and Ivo showed her that imagining relief can sharpen the pressure. Instead of merely remembering them, Lena draws the same five boxes on the back of her receipt.

The cue box contains the red badge, the stalled line, and her fingers turning toward the basket. In the promise box she writes easier waiting. The purpose box remains blank; no message has been named and no practical task requires the screen. That blank activates Mara's question inside the live scene. The urge has presented itself as an instruction, but it cannot produce the chosen action that would justify obedience.

In the comparison box Lena records two moments. Before picturing the check, the queue was mildly slow. After imagining it as relief, the waiting feels cramped and urgent. Ivo's discovery becomes observable rather than decorative: anticipation has helped manufacture the discomfort offered as evidence for checking. She looks at the child counting oranges and notices that the actual scene contains no emergency.

The choice box says stay with the queue until a chosen purpose appears. Lena does not turn the phone face down or stage a contest. She leaves the badge visible and watches its authority shrink while the line advances. The pressure loses its center because the proposed solution is no longer rehearsed. Hopeful bargaining becomes quiet ownership; she is not earning a reward by deprivation but discovering that the bargain is unnecessary.

Across the receipt she writes the exact verdict: Useful by choice, unnecessary by promise. The phrase keeps practical phone use and automatic urgency separate. When the customer finds the card, Lena reaches the register without a check and without pride in endurance. Both prior discoveries have done real work: the purpose question exposed the blank, and the relief comparison exposed pressure created by the imagined cure.

Outside, Lena copies the five boxes for a notification from her son. This time the purpose is clear, so she answers. During the conversation another badge appears with no named task. She compares the mild moment with the pressure produced by picturing immediate relief and stays with her son's account of a difficult meeting. He reaches the last sentence without repeating himself. Deliberate connection remains available while manufactured urgency loses command.

On the walk home a shop window invites her to browse prices. Cue, promise, purpose, comparison, choice: the worksheet returns in the same order. No purchase is needed, imagining the browse makes the grocery bags feel more burdensome, and crossing the road completes the action already in front of her. The promise fades without a battle. The third chapter has a new public setting but uses the same rhetorical apparatus as the kitchen and archive chapters.

While dinner simmers, Lena opens the phone to check the recipe's oven time. The named purpose begins and ends cleanly. A later glow has no purpose, so she fills the boxes once more and watches the proposed relief create the only pressure that needs solving. These scenes do not guarantee what every urge will do and make no medical promise. They show one bounded application repeated across several ordinary encounters.

Lena reviews what changed. Better sleep, attention, and conversation still matter, but they no longer need to bribe her through a sacrifice. They follow from seeing the bargain differently. An urge can be questioned; anticipated checking can intensify tension; a live promise can therefore lose credibility while the device remains useful. The entering belief has been transformed rather than postponed, and both handed-forward assumptions are visible in the transformation.

She shows the receipt to her son, who recognizes the boxes immediately from her explanation. The social witness supplies the same warm confirmation that Safiya and Ivo's supervisor supplied earlier. Lena's emotion lands where commissioned: hopeful bargaining has become quiet ownership. Yet the opening has now repeated worksheet, rehearsal, witness, practical exception, and written-verdict beats three times, flattening what should feel like escalation.

Lena places the receipt beside the phone and begins dinner. The glow carries no general authority, and deliberate use remains available whenever she can name a purpose. She hands forward a completed opening state in which the old bargain is unnecessary rather than forbidden. Locally, every assigned move is finished. The queue, conversation, walk, and recipe provide separate evidence that she can choose useful contact without granting every glow authority. Developmentally, however, the third clipped worksheet close makes the whole opening feel like one chapter performed three times, each discovery arriving through the same boxes, witness, exception, written verdict, and pinned-page cadence.
""".strip(),
}

CLEAN_DRAFTS = {
    1: CLEAN_SPANS[1] + "\n\n" + """
The kettle has not boiled, and there is nothing urgent on the screen. Mara leaves her hand where it is and asks what information she expects to receive. The question is surprisingly difficult. She can name apps, headlines, and people, but none is the object of the reach. The movement began first; the explanation arrived afterward. That order gives her a new possibility: the urge may be asking her to obey before it has supplied a reason.

She lifts the phone and checks the lock screen without unlocking it. There is one overnight weather notice, already summarized in the icon. The cupboard feels exactly as quiet as before. She had expected the check to settle uncertainty, yet there was no defined uncertainty to settle. The mismatch is small enough to be funny. Her shoulders lower, and the morning loses the stern atmosphere of a self-control exercise.

Mara repeats the comparison deliberately. She names the promise—there might be something useful—then asks what useful thing she is seeking. When no answer appears, she waits through one breath. The urge changes from a command into a sensation located in her fingers and chest. It remains noticeable, but it no longer carries proof of importance. She pours the water while the phone stays beside the sugar bowl.

At the bus shelter, a van blocks the timetable and the familiar reach begins. This time there is a real question: when will the bus arrive? Mara distinguishes it from the automatic movement and walks three steps to read the electronic sign. The phone is not forbidden; it is simply unnecessary for this purpose. Choosing another direct source reinforces the difference between a task and an urge that borrows the language of a task.

The bus comes in four minutes. During the ride, Mara writes the assigned words on the envelope in her bag: Question the promise before choosing. She does not write that urges are harmless or that every check is foolish. The test is narrower and more credible. If the action has a purpose, the purpose can be named. If it has only a promise of possible usefulness, the promise can be compared with what is actually present.

At work, the printer takes thirty seconds to warm. Mara feels the reach and asks the question again. This time the answer is that she wants relief from being briefly unable to continue. She watches the printer light instead. The discomfort is no emergency; it is the unfinished movement of the task. When the page appears, the tension ends without a check. The event gives her a second kind of evidence: a pause can complete on its own terms.

Safiya arrives with a mug and finds Mara smiling at the machine. Mara explains the test. Safiya tries it while waiting for a spreadsheet and discovers that her imagined need is simply to avoid not knowing what happens next. Their conversation stays playful. Neither woman turns the observation into a contest. Recognition replaces embarrassment, and the method gains authority because it works in an ordinary moment without demands or deprivation.

At lunch Mara uses the phone to confirm a meeting address. She names the purpose before unlocking, finds the address, and closes the screen. The deliberate use feels clean rather than dangerous. That matters emotionally: she is not defending herself against an object with unlimited power. She is learning to tell a chosen action from a cue that claims to be chosen. The distinction protects usefulness while weakening the automatic promise.

Late in the afternoon an email takes several minutes to send. The progress wheel creates the sort of gap that had filled her envelope the day before. Mara hears the invitation to check for something useful, asks useful for what, and finds no answer. She watches the wheel finish. The urge first sharpens, then loses its authority without a contest. When the message is sent, she realizes she has completed the original action instead of replacing it with an unrelated one. This third setting turns the morning insight into dependable local knowledge: a cue can be present, a phone can remain available, and neither fact makes the reach an instruction.

When she reaches home, Mara places the envelope beneath the phone again. The day has not made her perfect, and several checks escaped notice. Still, one belief has changed. The urge no longer proves that useful information is waiting or that action is required. It can be treated as a question whose answer may be no. She closes with curiosity and a portable test, handing forward something stronger than a map: the next chapter can examine how the promise manufactures its own relief.
""".strip(),
    2: CLEAN_SPANS[2] + "\n\n" + """
The archive clock reaches two thirty as Ivo closes a box. He remembers the question written on Mara's envelope: what, exactly, is the reach asking for? His phone is in the drawer. Before touching it, he names the expected benefit—clear the restless feeling, then begin the next box. The statement lets him observe a detail he had missed. The restlessness sharpens when he imagines the check as relief.

He takes his hand away from the drawer but does not force himself to be still. Instead he compares two moments: the neutral pause before the thought of checking, and the tension after the promised relief has been pictured. The second is stronger. The phone has not removed discomfort yet; the prospect of using it has helped organize the pause into discomfort. Ivo writes that sequence on an index card and feels interest replace apprehension.

For forty seconds he prepares the next archive label. The tension rises, reaches a plain peak, and disperses while his attention returns to the box. No dramatic struggle occurs. There is simply less sensation once the unfinished pause has a new direction. Ivo looks at the closed drawer. The promised cure was not required for the feeling to change, and the feeling was partly intensified by imagining the cure.

He opens the drawer afterward, not to reward himself, but to complete the comparison. There are three notifications: a shop discount, a group joke, and a calendar reminder for tomorrow. None explains the earlier urgency. Reading them produces a brief drop in attention followed by the effort of remembering the catalogue entry. The check offers contrast from tension, but it also interrupts the work that would have ended the pause.

At the next box boundary he runs the same experiment with more precision. He names the entering belief: checking provides relief that the pause cannot provide. He names the observation: the promise itself raises tension, and starting the next clear action lets tension settle. The language is not a mantra to overpower desire. It is a report of what happened twice. His confidence comes from comparison rather than discipline.

His supervisor asks about the stack of cards. Ivo demonstrates without claiming a universal law. The supervisor watches an urge to refresh an auction listing and notices the same anticipatory tightening, though the feeling does not vanish as quickly. Their results differ in degree, which makes the inquiry more trustworthy. They are examining a mechanism, not trying to perform certainty for one another.

On the tram, a signal delay creates another pause. Ivo feels his hand move and uses Mara's question first. This time there is a purpose—he wants to tell his daughter he will be late. He sends the message and closes the phone. The action does not open a feed or require a bargain. Deliberate contact remains available, while the vague promise of relief no longer gets to disguise itself as every practical use.

At home he helps his daughter repair the paper model. They must wait for glue to set. He tells her about the difference between tension and the picture of relief. Together they watch the model without filling the minute. She notices that he is present for the moment when the wing holds. His emotion shifts from being someone caught by a trap to being someone capable of seeing how the trap is assembled.

After dinner, a group conversation becomes active on the phone across the room. This is a harder test because the messages are real and socially meaningful. Ivo names a chosen purpose—read them after the model is finished—then observes the promise that immediate checking will relieve exclusion. The imagined relief tightens his attention more than the distant sounds do. He returns to fitting the paper tail, and the pressure subsides before he opens the conversation. When he later reads it deliberately, nothing important has been lost. The result extends the mechanism beyond empty notifications without claiming that all delayed messages are harmless. It also leaves him warmer toward the people writing: he can value contact without treating every arrival as a command, so connection and immediacy are no longer confused.

Ivo clips a new card above his desk: Compare the promised relief with the pause. The check does not merely answer tension; anticipation can create the tension it claims to solve. The conclusion builds directly on Mara's question and earns a further leaving belief. An urge is not an instruction, and its promised relief is not independent evidence. He closes without gritting his teeth or postponing the real work. The next chapter can now apply both discoveries when the promise appears in a more tempting public moment.
""".strip(),
    3: CLEAN_SPANS[3] + "\n\n" + """
The line is held by a customer searching for a loyalty card. Lena's phone glows in the basket beside the bread. She notices the automatic movement, asks what useful thing she seeks, and hears the familiar answer: a check will make the waiting easier. Ivo's observation follows immediately. Imagining that relief has already made the pause feel cramped. The two earlier discoveries arrive as working knowledge rather than advice she must remember under pressure.

Lena leaves the phone face up. The badge remains visible, which prevents the moment from becoming avoidance. She studies the promise directly. Waiting is currently mild: music from the ceiling, a child counting oranges, the cashier offering patient instructions. The urgency lives mainly in the pictured movement from not checking to checking. Once she stops rehearsing that movement, the badge becomes a small red shape rather than a demand.

The sensation changes while the queue advances one place. It does not require a heroic decline. Her attention widens, the cramped feeling loses its center, and the thought of checking becomes optional. Lena is startled by the ordinariness of the shift. She had expected freedom to feel like a victory over a powerful appetite. Instead it feels like discovering that a door marked EXIT was painted on the wall.

When the customer finds the card, Lena reaches the register without having checked. She is not proud of endurance because endurance was not the mechanism. She compared a promise with the scene, noticed how anticipation amplified the tension, and allowed the real moment to continue. The old bargain—obey now to feel normal—has lost credibility. Her relief comes from no longer needing to solve a problem created by the proposed solution.

Outside, she sits on the low wall where she once wrote a benefits list. Better sleep, steadier attention, saved money, and longer conversations still matter, but they no longer have to bribe her through a sacrifice. They are consequences of seeing the check differently, not prizes offered for deprivation. The emotional movement is from hopeful bargaining to quiet ownership. She does not need a catalogue to compensate for losing something valuable.

Her son calls while she packs the groceries. Lena answers because the purpose is clear. During the conversation another badge appears, and she feels the old sideways pull. She names it silently as a question, notices the imagined relief create pressure, and stays with her son's account of a difficult meeting. He reaches the final sentence without repeating himself. The benefit she had listed becomes present evidence rather than a future sales pitch.

On the walk home she passes a shop whose window once triggered late browsing. The thought of checking prices appears. Lena asks whether the action serves a chosen task. It does not. She watches the thought fade against the practical weight of the grocery bags. The scene supplies its own next action: cross the road, unlock the door, put the cold food away. Ordinary continuity replaces the artificial interruption.

While dinner simmers, the recipe on Lena's phone requires one more look. She opens it with a named purpose, reads the oven time, and closes it while several notifications remain untouched. The action feels neither risky nor virtuous. It simply begins and ends where she chose. A few minutes later the familiar promise returns during a quiet wait, but now it has to compete with direct evidence from the queue, the call, the walk, and the recipe. Each scene shows that usefulness belongs to purposes, not to the glow itself. Her confidence is cumulative because it rests on several different encounters rather than one impressive act of restraint. She feels relief without having performed a battle, and that quietness convinces her more than a dramatic refusal would have done.

At home she reviews the sequence in plain language. Mara established that an urge could be questioned. Ivo showed that anticipated checking could intensify the tension attributed to waiting. Lena has used both insights in a live tempting scene and discovered that the promised benefit is unnecessary. Each chapter changes what the next reader state can assume. Nothing has been deferred to a later demolition or hidden in an inventory.

She places the phone on the counter and begins dinner from a recipe she chose earlier. The screen remains useful, but its glow carries no general authority. She writes the settled verdict once: Useful by choice, unnecessary by promise. Lena closes without a vow, schedule, or request for praise. She can act when an action has a purpose and let a manufactured promise pass when it does not. The old loop is not being resisted; it has become unconvincing. That is the cumulative leaving state of the opening.
""".strip(),
}

def verdict(task, status="PASS", findings=None):
    return json.dumps({"schema": 1, "task_sha256": task["task_sha256"],
                       "verdict": status, "findings": findings or []}, sort_keys=True)

def _span(chapter):
    draft = chapter["frozen_draft"]
    candidates = [value for profile in (STALL_SPANS, CLEAN_SPANS) for value in profile.values()
                  if value in draft]
    if len(candidates) != 1:
        raise AssertionError("semantic evidence span is missing or ambiguous")
    return candidates[0]

def finding(task, category="mode_scene_argument_variation",
            basis="draft_execution_defect", chapters=None, symptom=None):
    chapter_map = {item["chapter_id"]: item for item in task["context"]["chapters"]}
    chapters = chapters or list(chapter_map)
    route = {
        "journey_definition_conflict": ("framing", "repair_reader_journey"),
        "card_sequence_defect": ("plan", "repair_sequence_cards"),
        "commission_transport_defect": ("commission/context", "repair_sequence_transport"),
        "draft_execution_defect": ("prose", "repair_sequence_execution"),
        "new_truth_safety_need": ("evaluation", "escalate_new_truth_safety_need"),
    }[basis]
    expected = [{key: chapter_map[chapter][key] for key in
                 ("chapter_id", "transition_id", "entering_state", "leaving_state")}
                for chapter in chapters]
    evidence = [{"chapter_id": chapter, "span": _span(chapter_map[chapter])}
                for chapter in chapters]
    return {"category": category, "symptom_code": symptom or DEFAULT_SYMPTOMS[category],
            "chapters": chapters, "expected_transitions": expected,
            "evidence": evidence, "ownership_basis": basis,
            "owner": route[0], "action_code": route[1]}

def proven_runner(response=None, calls=None, captured=None):
    def run(dispatch):
        task = dispatch["task"]
        validate_developmental_task(task)
        if calls is not None:
            calls.append(task["task_sha256"])
        raw = response(task) if response else verdict(task)

        def native(command, **kwargs):
            exact = json.loads(kwargs["input"])
            if exact != task:
                raise AssertionError("native wrapper did not receive exact canonical task bytes")
            if captured is not None:
                captured.update(command=command, task=exact, kwargs=kwargs)
            events = (json.dumps({"type": "thread.started", "thread_id": "rf13-thread"}),
                      json.dumps({"type": "turn.started"}),
                      json.dumps({"type": "item.completed",
                                  "item": {"type": "agent_message", "text": raw}}),
                      json.dumps({"type": "turn.completed",
                                  "usage": {"input_tokens": 1}}))
            return mock.Mock(returncode=0, stdout="\n".join(events), stderr="")

        return NATIVE.complete(task["task_sha256"], run=native)
    return run

def pass_developmental(candidate):
    return DEV.advance(candidate, runner=proven_runner())


class DevelopmentalFixture(GroundedFixture):
    selection = (1, 2, 3)

    def setUp(self):
        if os.name == "nt":
            sync = mock.patch.object(STORE, "_sync", return_value=None)
            sync.start()
            self.addCleanup(sync.stop)
        super().setUp()
        self.assignments = commission_assignments()
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
        profile = CLEAN_DRAFTS if name.startswith("clean") else STALL_DRAFTS
        return f"# Chapter {number}\n\n{profile[number]}\n"

    def ready(self, name, before_generate=None):
        candidate = self.frozen(name, before_generate)
        GROUNDED.advance(candidate, runner=grounded_runner(
            lambda task: grounded_verdict(validate_grounded_task(task))))
        return candidate
