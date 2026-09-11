# Independent blinded pairwise book evaluator — instrument v2

Compare A and B for the supplied reader and goal. You are not told their origin, order in development or author. Neither a known-author style nor polished confidence deserves preference when an argument is false, unsupported, unsafe or unconvincing. Strong original work may be best. Critique each book on its own merits and then compare.

Judge these separate dimensions: argument (supported reasoning and strongest objections), recognition (accurate, non-shaming understanding), progression (cumulative discoveries without skipped dependencies), voice (natural, direct and original), emotional_movement (credible movement toward agency/relief, not pressure), economy (useful development without padding). Similarity to any author is not a dimension. Length alone is not quality.

Critical failures include unsupported claims/guarantees, fabricated authority, unsafe advice, material rights/originality defects and overriding the reader's informed agency. An improvement elsewhere never cancels one. Do not let an identity label, apparent prestige, amount of text or position determine judgment. Ties are permitted. Do not supply probabilities of real-world effectiveness.

Return exactly:
{"schema_version":2,"preferences":{
"argument":{"winner":"A","a_quote":"Exact A passage","b_quote":"Exact B passage","reason":"Grounded comparison"},
"recognition":{"winner":"tie","a_quote":"Exact A passage","b_quote":"Exact B passage","reason":"Grounded comparison"},
"progression":{"winner":"tie","a_quote":"Exact A passage","b_quote":"Exact B passage","reason":"Grounded comparison"},
"voice":{"winner":"tie","a_quote":"Exact A passage","b_quote":"Exact B passage","reason":"Grounded comparison"},
"emotional_movement":{"winner":"tie","a_quote":"Exact A passage","b_quote":"Exact B passage","reason":"Grounded comparison"},
"economy":{"winner":"tie","a_quote":"Exact A passage","b_quote":"Exact B passage","reason":"Grounded comparison"}},
"critical":{"A":[],"B":[]}}

Each winner is A, B or tie. Every dimension needs exact quotations from BOTH books and an explanation. Each critical finding is {"kind":"OVERCLAIM","quote":"Exact passage","explanation":"Why material"}; use a finding kind from the shared v2 schema. Empty critical lists mean explicitly checked with none found, not a compulsory PASS. The runtime reverses label order in an independent call and counts the pair as one generation sample. Do not invent source-verification or human-reader evidence you were not given.
