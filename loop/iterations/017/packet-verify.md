# 017 Grok packet verification vs campaign 014 prompts

**Verified:** 2026-08-30  
**Packet:** `loop/iterations/017/grok-packet.md`  
**Campaign 014 targets:** `prompts/chapter-writer.md`, `prompts/style-guide.md`  
**Method:** byte-exact `in` check on each GO SEARCH string; W1 REPLACE forbidden-substring check; NO-GO presence grep. No hunks applied.

---

## GO SEARCH blocks (6 hunks)

| Hunk | File | Line (014) | SEARCH exact match | Result |
|------|------|------------|-------------------|--------|
| W1 | `prompts/chapter-writer.md` | 45–46 | `objection, pose two or three questions whose only honest answer concedes` … `land one short verdict. Perform` | **PASS** |
| S1 | `prompts/style-guide.md` | 173 | `- **Ask, don't assert.** Pose the question whose only honest answer dismantles the belief; let the reader supply the evidence and feel discovered, not lectured.` | **PASS** |
| S2 | `prompts/style-guide.md` | 300 | `- **Make the reader reach the conclusion — inside a frame of flat assertion.** Carr asserts constantly ("The fact is...") *and* runs the trap questions whose only honest answer concedes the point. Keep both: settled-fact delivery for the reframes, Socratic traps for the reader's own evidence.` | **PASS** |
| S3 | `prompts/style-guide.md` | 313 | `- **Never cushion a belief landing…** Cut cues such as "sit with this," "let that land," and "if you wish": … then ask the trap question whose only honest answer completes the credit inversion.` | **PASS** |
| S4 | `prompts/style-guide.md` | 422 | `- [ ] Did I run the **trap questions inside a frame of flat settled-fact assertion** — Carr's balance (§9): "The fact is..." delivery for reframes, Socratic traps for the reader's own evidence?` | **PASS** |
| S5 | `prompts/style-guide.md` | 525 | `3. **Concession question** — pose one question whose only honest answer concedes the point; perform it in flat Carr voice without naming, announcing, or labeling the question type.` | **PASS** |

### Quote / whitespace notes

- **S3:** Packet SEARCH uses Unicode curly double quotes (U+201C / U+201D) around `sit with this`, `let that land`, and `if you wish` — matching `style-guide.md` L313 exactly. A straight-ASCII `"` variant would **FAIL**; the packet file is correct.
- **W1:** Leading two-space continuation indent on wrapped list lines matches `chapter-writer.md` L45–46.
- **S2, S4:** Straight ASCII `"` around `The fact is...` matches the campaign file.
- No other whitespace or punctuation mismatches found across the six SEARCH blocks.

---

## W1 REPLACE forbidden strings

| Check | Result |
|-------|--------|
| REPLACE must NOT contain `land one short verdict` | **PASS** (absent) |
| REPLACE must NOT contain `stop on the verdict sentence` | **PASS** (absent) |

W1 REPLACE text: `objection, ask, perform the credit inversion. Perform`

---

## NO-GO strings still present (must not be removed by packet)

| Item | Expected location | String | Present | Result |
|------|-------------------|--------|---------|--------|
| Writer anatomy item 5 | `chapter-writer.md` L124 | `numbered ALL-CAPS spoken imperative` | yes | **PASS** |
| Historical-evidence operator | `style-guide.md` L631 | `historical-evidence operator` | yes | **PASS** |
| Pin frozen quote on cards | `style-guide.md` L487 | `pin the frozen quote on the card` | yes | **PASS** |

---

## Per-hunk summary

| Hunk | SEARCH | W1 REPLACE (W1 only) | Overall hunk |
|------|--------|----------------------|--------------|
| W1 | PASS | PASS | **PASS** |
| S1 | PASS | — | **PASS** |
| S2 | PASS | — | **PASS** |
| S3 | PASS | — | **PASS** |
| S4 | PASS | — | **PASS** |
| S5 | PASS | — | **PASS** |

---

## Overall verdict

**PASS** — All six GO SEARCH strings match campaign 014 prompts exactly; W1 REPLACE omits both forbidden verdict cues; all three NO-GO anchor strings remain untouched in the 014 files.
