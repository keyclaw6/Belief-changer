```markdown
research/persona-retrieval-commission.md

# Persona Retrieval Commission (Scout Mode)

**Role:** Persona architecture scout
**Context:** No retrieval artifacts supplied — operating in scout mode.
**Brief:** Quit Sugar (working title). Target behavior: compulsive consumption of refined/added sugar and junk carbs. Audience: trapped adult who has failed diets, willpower, and moderation; suspects something is wrong with the whole approach. Excludes eating-disorder treatment, medical nutrition therapy, diabetes management, weight-loss mechanics.

## Overall Approach

True persona discovery must be evidence-led. This commission decomposes the work into 10 focused retrieval assignments that span the primary online communities where people discuss their struggle with sugar in their own words. Each assignment isolates one community, query cluster, or experiential dimension to enable deep, exhaustive search by retrieval subagents. Retrievers must capture exact text excerpts, source URLs, metadata, and note persona-relevant themes — but must **not** synthesize or reduce them into personas. Only after all returned artifacts are inspected will the specialist build the provisional persona set.

Assignments are designed to generate coverage across:

- Explicit justifications for wanting to quit or feeling trapped (Bank 1)
- Underlying beliefs, feared costs, identity statements (Bank 2)
- Daily costs, lowest moments, relapse triggers, private arithmetic (Bank 3)
- Seductive or cherished scenes (Bank 4)
- Escape-route rationalizations and failed moderation attempts (Bank 5)
- Organic community lexicon and native phrasing (Bank 9)
- Freedom testimonies, surprises after stopping, revelation moments (Bank 10)

All evidence below will later be filtered by persona and mapped to the bank matrix. No persona is presupposed; the commission simply ensures the raw material is deep enough that materially distinct personas will emerge.

---

## Retrieval Assignments

### A1: r/sugarfree — The “I want out” entry points
**Focus:** The moment a person decides to quit and the explicit reasons they give.
**Rationale:** r/sugarfree is the largest dedicated Reddit community for quitting sugar. Top/all-time posts, recurring “why I’m quitting” threads, and introductory posts are rich with unvarnished justification language.
**Target community:** `reddit.com/r/sugarfree` (public, primarily text).
**Search queries / strategies:**
- Browse “top” → “all time” and “month” feeds; capture posts with ≥ 50 upvotes that state reasons, struggles, or benefits.
- Reddit search: `title:"why I" OR title:"decided to" OR title:"starting" OR title:"day 1"` in r/sugarfree.
- Reddit search: `"reason I quit" OR "why I gave up" OR "I realized"` limited to r/sugarfree.
- Reddit search: `"sugar is" OR "sugar makes me" OR "my relationship with sugar"` to capture belief statements.
- Direct retriever agent may also use pushshift/Reddit API for date-range sampling if needed, but must respect rate limits and capture exact timestamps.
**Evidence to capture:** Exact post body and relevant comment threads; metadata including URL, timestamp, upvote count. Note recurring justification phrases, emotional tone, and life-situation clues.
**Expected contribution:** Bank 1 (justification inventory), Bank 2 (belief map), Bank 9 (lexicon).

---

### A2: r/sugarfree — The lived grind: costs, lowest moments, private arithmetic
**Focus:** Detailed daily hardships, rock-bottom experiences, failed previous attempts, and the personal math people do (money, calories, time).
**Rationale:** Scattered across r/sugarfree are deeply personal accounts of how the sugar loop damages daily life; these yield the “that is exactly me” moments required by Bank 3.
**Target community:** `reddit.com/r/sugarfree` (plus linked subreddits when threads cross-reference).
**Search queries / strategies:**
- Reddit search: `"rock bottom" OR "lowest point" OR "wake up call" OR "woke up" OR "can't stop"` in r/sugarfree.
- Reddit search: `"guilt" OR "shame" OR "hide" OR "sneak" OR "trigger" OR "binge"` to surface emotional costs.
- Reddit search: `"cost" OR "money" OR "spent" OR "calories"` related to sugar.
- Deep-scroll monthly top threads and capture the most emotionally detailed confessions (≥ 100 words).
**Evidence to capture:** Complete posts (and clarifying comments). Record exact phrasing of self-criticism, despair, failed attempts.
**Expected contribution:** Bank 3 (lived experience), Bank 5 (escape routes from failed attempts).

---

### A3: r/keto — Sugar as the arch-enemy
**Focus:** How low-carb/ketogenic community members frame their pre-keto sugar relationship — justifications, breakthrough moments, and post-cessation surprise.
**Rationale:** r/keto (3 M+ members) contains endless testimonies of people who eliminated sugar and junk carbs; they often describe their former compulsion in detail.
**Target community:** `reddit.com/r/keto` (plus `r/xxketo`, `r/ketobabies` if person types warrant later).
**Search queries / strategies:**
- Reddit search: `"sugar addiction" OR "sugar cravings" OR "need sugar" OR "stop sugar"` in r/keto.
- Sample recurring “I used to be a sugar addict” posts (self-text only, not link posts).
- Capture at least 20 distinct, detailed narratives that describe life before keto vs. after, focusing on the sugar-specific parts.
**Evidence to capture:** Verbatim paragraphs describing old mindset, turning point, physiological/emotional surprises. Note any mention of specific sugary foods, rituals, or contexts.
**Expected contribution:** Bank 4 (special moments), Bank 10 (freedom testimonies), Bank 3 (low moments), and lexicon that crosses over from keto to general sugar-cessation (Bank 9).

---

### A4: General weight‑loss communities (r/loseit, MyFitnessPal forums) — The “I can count calories but not kick sugar” cluster
**Focus:** Users who successfully count calories, track macros, or lose weight yet repeatedly fail to control sugar intake. They often articulate the unique grip of sugar vs. other “unhealthy” foods.
**Rationale:** This persona archetype (“everything else is fine, but sugar beats me”) is likely material to the reader; such stories are abundant in weight‑loss hubs.
**Target community:** `reddit.com/r/loseit` (primary); `community.myfitnesspal.com` → “Food and Nutrition” and “Success Stories” boards (public threads).
**Search queries / strategies:**
- Reddit search: `"can't stop sugar" OR "only thing I can't give up" OR "why is sugar so hard"` in r/loseit.
- MyFitnessPal forum search: “sugar addiction” OR “can’t stop eating sugar” within public boards.
- For each platform, capture 10–15 distinct, detailed threads where a user explicitly states that sugar uniquely defeats their willpower.
**Evidence to capture:** Exact self-descriptions of being “good with everything else” vs. sugar; failed moderation attempts; emotional reactions.
**Expected contribution:** Bank 5 (escape routes and “different for me” rationalizations), Bank 1 (justifications), Bank 2 (identity beliefs: “I have no willpower around sugar”).

---

### A5: YouTube comments — The voice of the passively searching quitter
**Focus:** Unpolished, first‑take comments on popular “quit sugar” or “sugar detox” videos. This audience often has not joined a structured community and reveals raw justifications and fears.
**Rationale:** YouTube comments capture a different demographic and linguistic tone; they are strong for Bank 9 (lexicon) and for seeing how people phrase their initial impulse to stop.
**Target community:** Comments sections of (> 100k views) videos with titles like “What Happens When You Quit Sugar?”, “I Quit Sugar for 30 Days”, “Sugar Addiction”, “How to Stop Eating Sugar”.
**Search queries / strategies:**
- Use YouTube Data API (if retriever has access) or manual scroll to capture top/“newest first” comments on at least 10 high‑view videos.
- Filter comments ≥ 2 sentences that mention personal experience, reasons, or effects.
- Avoid commenters who appear to be bots or off‑topic.
**Evidence to capture:** Exact comment text, video title, channel, comment timestamp, permalink.
**Expected contribution:** Bank 1 (justifications), Bank 3 (costs), Bank 9 (lexicon in a more casual register), Bank 10 (freedom declarations after “30‑day challenge” type videos).

---

### A6: Twitter / X — The public confessional (#sugarfree, #quitsugar, #SugarAddiction)
**Focus:** Real‑time or recent public confessions, resolutions, and declarations about sugar. Twitter’s brevity forces tight language that often reveals keystone beliefs and escape‑route rationalizations.
**Rationale:** High‑volume, multi‑demographic stream; many users tweet about sugar fails and attempts without belonging to a health forum.
**Target community:** Twitter/X public posts.
**Search queries / strategies:**
- Search Twitter (via API or nitter proxy) for `#sugarfree`, `#quitsugar`, `#sugaraddiction`, `#givingupsugar`, `#nosugar` within the past 2 years.
- Capture 50 + unique tweets that contain a declared reason, a failed attempt, or a benefit; ensure diversity of accounts.
- Supplement with search: `"I need to quit sugar"`, `"sugar is ruining my life"`, `"why can't I stop eating sugar"`.
**Evidence to capture:** Full tweet text, username (if public), date, permalink. Record any self‑described life context.
**Expected contribution:** Bank 1, Bank 2, Bank 4 (seductive moments described in short bursts), Bank 9 (hashtag‑driven slang).

---

### A7: Independent blogs and Medium — The long‑form personal essay
**Focus:** Detailed 1000+ word personal stories of quitting sugar, written for a general audience. These often include the author’s full pre‑quit belief system, the “moment of clarity”, and the post‑quit transformation.
**Rationale:** Long‑form narratives are invaluable for Bank 10 (freedom testimonies) and Bank 3 (lived experience), because the author typically reconstructs the experience with introspection.
**Target communities:** Medium (tag: “Sugar”, “Sugar Detox”, “Quitting Sugar”); WordPress blogs; sites like “Mark’s Daily Apple”, “Wellness Mama”, “Vani Hari”; personal blogs discovered via Google.
**Search queries / strategies:**
- Google search: `"I quit sugar" "my story"` or `"how I quit sugar"` or `"what happened when I quit sugar"` with `site:medium.com` or `site:wordpress.com` or general.
- Collect 15–20 distinct essays that are primarily personal narrative, not instructional/diet.
- Exclude commercial sites that are obviously selling coaching/products unless the personal story is detailed and verifiable.
**Evidence to capture:** Complete article text (or substantive excerpts); source URL; author name (if public); date; key quotes about “before” mindset, turning point, and “after” surprises.
**Expected contribution:** Bank 10, Bank 3, Bank 4, Bank 1, Bank 2.

---

### A8: Facebook public pages and groups — The supportive micro‑community
**Focus:** Supportive public posts and threads in dedicated “sugar‑free” or “quit sugar” Facebook groups where members share daily struggles and wins in a semi‑private but public‑facing space.
**Rationale:** Facebook groups often contain more sustained, diary‑like conversations than Reddit, revealing the day‑by‑day texture (Bank 3) and the social support dynamic.
**Target community:** Public/closed-but-searchable Facebook groups such as “Quit Sugar”, “Sugar Busters”, “I Quit Sugar Community”, “Sugar Free for Life”. (Retriever must use only public content or content accessible without violating terms; if a group is private, do not attempt to join or scrape; label `CANDIDATE — VALIDATION REQUIRED` if content is not reachable.)
**Search queries / strategies:**
- Facebook search for “quit sugar group” or “sugar free support” to identify open groups.
- Within identified open groups, scroll recent posts (last 12 months) and capture threads with personal experiences.
- Focus on posts where members share “today I failed” or “why I’m trying again” or “things I’ve noticed since quitting”.
**Evidence to capture:** Post text, comments (anonymized if necessary), post date, group name, post URL (if accessible).
**Expected contribution:** Bank 3, Bank 5, Bank 10, Bank 1.

---

### A9: General web search for “moderation failed” and “different for me” rationalizations
**Focus:** Specific retrieval to map the escape routes people use to keep the sugar loop alive, especially moderation attempts, special occasions, “healthy” sugars, “I can’t go without because…”
**Rationale:** Bank 5 requires exact community instances of escape‑route rationalizations. This assignment targets them directly across platforms.
**Target communities:** No single community — cross‑platform search using phrase-level queries.
**Search queries / strategies:**
- Google: `"I can't live without sugar" OR "life without sugar is not worth living"`.
- Google: `"I only eat sugar on weekends" OR "moderation works" OR "tried to cut back" OR "I can have a little"`
- Search these phrases within known communities: `site:reddit.com "moderation" "sugar" "failed"`.
- Search: `"I need sugar for energy" OR "sugar gives me energy"` to find the energy‑as‑exception narrative.
- Search: `"organic sugar" OR "natural sugar" "is different"` to surface the “health halo” escape.
- Capture 20 + distinct posts/comments that explicitly argue for or describe a moderation/special‑case rationalization.
**Evidence to capture:** Verbatim text, URL, timestamp. Note which escape route each illustrates.
**Expected contribution:** Bank 5 (escape routes), with cross‑links to persona‑associated communities.

---

### A10: Complementary source for “vivid cherished moments” (Bank 4)
**Focus:** The most seductive, cherished, or ritualistic sugar consumption scenes — the “warm cookie after a long day”, the “movie with a pint of ice cream”, the “office birthday cake”.
**Rationale:** These emotionally charged scenes are the attachment points that later belief‑change must address. They are spread across all communities; this assignment hunts them explicitly.
**Target communities:** r/sugarfree, r/loseit, r/AskReddit (threads like “What food can you not resist?”), YouTube comments, Facebook groups, blogs (general).
**Search queries / strategies:**
- Reddit: `"best part of my day" "sugar"` or `"comfort" "sugar"` or `"treat myself" "sugar"` or `"dessert after dinner"`.
- Google: `"I love sugar because"` or `"sugar makes me happy"` or `"my favorite part of the day is" sugar`.
- Within blogs, find passages that describe the sensory and emotional peak of consuming sugar.
- Collect 20 + distinct descriptions rich in sensory detail.
**Evidence to capture:** Full scene description, source, locator.
**Expected contribution:** Bank 4 (special moments), Bank 2 (the belief that sugar = pleasure/treat), cross‑referenced with persona tags later.

---

## Notes for Retrievers

- **Capture exact text, never paraphrase.** All evidence items must later be verifiable as exact quotes.
- **Log every retrieval event** with query, tool, timestamp, model (if used), results disposition, and any gaps.
- **Do not reject contradictory or unpleasant evidence** — the architecture must account for the true range of experiences.
- If a community is discovered that appears relevant but has sparse content, record it as a discovery and return what is available; the specialist can flag it as a follow‑up.
- Respect robots.txt and terms of service; if a source is inaccessible, note it as `CANDIDATE — VALIDATION REQUIRED` for the lead.

## Blind Spots & Follow‑up Hooks (to be revisited after initial returns)

- **Non‑English communities:** May host culturally distinct personas; consider supplementary retrieval if initial results are too narrow.
- **Older adults (65+):** Undergrooved in typical social‑media; might need specific searches like “retirement sugar habit” or “senior quit sugar”.
- **Shift workers / night workers:** The energy‑reliance persona might be strongly represented; search for “sugar on night shift” if not surfaced.
- **New parents:** The “survive on sugar” persona after sleep deprivation; search for “mom/dad sugar fuel” if gaps remain.
- **Socioeconomic stress personas:** “Cheapest pleasure” rationalization might appear in low‑income contexts; search `"I can't afford healthy food" sugar` or similar.
- **Eating‑disorder adjacent:** Some narratives may come from people who explicitly say they are not in ED territory but feel “addiction”; we must tread carefully and exclude clinical ED treatment spaces per brief.

The specialist will issue follow‑up retrieval assignments targeting any blind spot that initial returns indicate is materially distinct and uncovered.

---
**Output path:** `research/persona-retrieval-commission.md`
**Status:** Awaiting subagent dispatch by architecture lead.
```
