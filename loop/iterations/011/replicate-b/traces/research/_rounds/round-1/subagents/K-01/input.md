You are a fresh research SUBAGENT. Your system prompt is the research doctrine. You receive ONLY: the brief and your specific commission. Execute the commission exactly — search and fetch as wide and deep as still brings results (no ceilings), and deliver in the exact output format the commission and doctrine require, with full provenance.

# THE BRIEF

# Brief — Quit Sugar (working title)

## Target behavior
Compulsive consumption of refined/added sugar and junk carbs ("bad sugar") — the craving–snacking loop and its grip, not nutrition pedantry.

## Reader / audience
An adult who feels trapped in the sugar loop; has tried diets, moderation rules, and willpower and watched them all fail; suspects something is wrong with the whole approach. General adult edition (one clear reader).

## Goal & stance — decide explicitly (style guide §4 forks)
Forks are decided in `framing.md`; expected axes are listed here but not preempted:
- **Outcome (Fork 2):** autonomy-led total freedom vs explicit moderation — where the Bad-Sugar line sits IS the redefinition decision.
- **Void (Fork 5):** natural baseline vs positive replacement — <framing>
- **Science weight (Fork 3):** <framing>
- **Villain (Fork 4):** the engineered trap to name (sugar industry / product engineering) — <framing>
- **Inner state (Fork 1):** full Carr personification — the two mechanism characters, original behavior-fitted names frozen in the mantra sheet (style guide v3 default).

## The load-bearing false belief (style guide §10, step 1)
<one sentence, fixed in framing: what the reader believes bad sugar GIVES them — expected neighborhood: "sugar is a pleasure/treat/energy-lift that makes life sweeter and I'd be deprived without it">

## Scope / non-goals
Covers the everyday sugar/junk-carb trap for a general adult reader. Non-goals: medical nutrition therapy, diabetes management advice, eating-disorder treatment (crisis-pointer territory, not method territory), weight-loss-program mechanics.


# YOUR COMMISSION

You are a Lane A sub-agent: LIVED EXPERIENCE — App-store reviews for sugar-cessation, food-tracking, and sugar-detox apps.

**TARGET BEHAVIOR:** Compulsive consumption of refined/added sugar and junk carbs ("bad sugar") — the craving–snacking loop.

**YOUR JOB:** Mine app-store reviews (Apple App Store, Google Play) for apps in the following categories. Reviews are a dense, permitted first-person vein. Harvest verbatim quotes that capture ANY of:
- The craving experience in the user's own words
- Failed attempts to moderate or quit
- The private shame/secret-eating moments
- Triggers (stress, boredom, time of day, social situations)
- What the user believed sugar gave them before quitting
- The moment they realized something was wrong
- Post-quit surprises, freedom moments, relief
- Relapse stories and what triggered them
- Physical withdrawal symptoms described sensorily
- What specific method/app finally helped (and why)

**APP CATEGORIES TO SEARCH (search each app name + "reviews"):**
- Quit sugar / sugar detox: "I Quit Sugar," "Sugar Detox," "Quit Sugar," "Sugar Free," "Beat Sugar," "SugarBreak," "Sugar Addiction"
- Fasting / food tracking: "Zero," "LIFE Fasting," "MyFitnessPal," "Cronometer," "Lose It," "Carb Manager," "Noom," "Fooducate"
- Habit / addiction: "Quitzilla," "Habitica," "Sober," "I Am Sober" (used for sugar), "Days Since"
- Whole30 / elimination: "Whole30," any Whole30 companion apps

**SEARCH PATTERNS (use web_search for each, then web_fetch the review pages):**
- `"[app name]" app store review quit sugar`
- `"[app name]" sugar cravings review`
- `"[app name]" sugar addiction review app`
- For Google Play: `site:play.google.com "[app name]" sugar review`
- For Apple: search for review roundup articles on third-party sites that quote multiple reviews

**OUTPUT FORMAT:**
For EACH accepted source page, produce:
1. A complete `research/sources/S-NNN-slug.md` packet following the exact schema from the research doctrine (Source ID, URL, title, type, retrieved UTC, access/license basis, excerpt/redistribution basis, required attribution, retention/deletion sensitivity, privacy/personal-data basis, disposition; then Minimum retained excerpt with C-NNN blocks containing the unchanged passage; then Evidence items E-NNN with ALL fields: Kind EXACT_QUOTE or INTERPRETATION, Text, Excerpt ID, Locator, Persona tags, Bank slots, Evidence grade, Use/limits, Situation, Emotion, Brief beliefs, Style slots, Safety relevance, Grade rationale, Scope, Counterevidence, Permitted inference, Prohibited inference, Testimonial qualification).
2. After all packets, a raw-bank line section showing how EACH evidence item maps to banks (Bank 1-10), using the exact format:
   ```
   - [Bank N] <finding or verbatim quote> — Persona IDs: P-XX — Source IDs: S-NNN#E-NNN [slot: slot-name]
   ```

**PERSONAS TO TAG (discover more; start with these):**
- P-SNACKER: stress/boredom snacker
- P-ENERGY: afternoon energy-seeker
- P-NIGHT: nighttime secret binger
- P-DIETER: yo-yo dieter, chronic restriction-binge cycle
- P-SOCIAL: can't imagine life without desserts/celebrations
- P-HEALTHY: "healthy-ish" moderate consumer who doesn't think they have a problem
- P-EMOTIONAL: uses sugar as primary emotional comfort
- P-ADDICT: self-identified sugar addict, full loss-of-control

**VOLUME TARGET:** Deliver ≥80 lived-experience entries from app reviews. Dig deep into review pages — scroll, paginate, fetch multiple pages. Every review that contains a specific moment, specific language, or concrete experience is worth banking.

**PROVENANCE:** Every quote must be EXACT — copy character-for-character from the review. Never smooth, never composite. If a review is too vague ("this app is great!"), skip it. We need texture.