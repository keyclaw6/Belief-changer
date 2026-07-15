"""Console rendering for score.py."""
import judges


def report(p):
    print(f"[score] campaign={p['campaign']} instrument={p['instrument_version']} "
          f"chapters={p['chapters_checked']}")
    c = p["checks"]["originality"]
    if c.get("overlap_ratio") is None:
        print(f"[hard] originality: {c.get('mode', 'N/A')}")
    else:
        print(f"[hard] originality overlap {c['overlap_ratio']*100:.3f}% "
              f"(tripwire {c['tripwire']*100:.1f}%) -> {'TRIPPED' if c['tripped'] else 'ok'}")
    mr = p["checks"]["mantra"]
    if mr is not None:
        print(f"[hard] mantra: {len(mr['mantras'])} parsed, {len(mr['failures'])} failures; "
              f"no-mantra chapters {mr['chapters_without_mantra']}")
    nrep = len(p["checks"]["repetition_within"]["hard_fails"])
    tag = "diagnostic (control)" if p.get("control_ref") else "hard"
    print(f"[{'diag' if p.get('control_ref') else 'hard'}] repetition: {nrep} "
          f">=12-gram non-mantra repeats ({tag})")
    print("[hard] length: " + " | ".join(
        f"ch{r['n']} {r['words']}w/{r.get('budget') or '-'} "
        f"{'ok' if r['ok'] else 'FAIL'}" for r in p["checks"]["length"]))
    print("[diag] stylometrics (ours vs matched reference positions):")
    for row in p["diagnostics"]["stylometrics"]:
        print(f"        {row['metric']:<26}{str(row['ours']):>10}{str(row['ref']):>10}")
    block = p["judges"]
    if block["status"] == "WAITING-FOR-VERDICTS":
        print(f"[reward] WAITING-FOR-VERDICTS — {len(block['missing'])} verdicts missing "
              "(task -> verdict mapping printed above); missing stems: "
              + ", ".join(block["missing"][:12]))
    else:
        rubric = block["rubric"]
        print(f"[reward] carr-likeness composite = {rubric['reward']}  "
              f"({rubric['n_verdicts']} verdicts, k={rubric['judge_k']}, "
              f"judge={rubric['judge_model']})")
        for chapter in rubric["per_chapter"]:
            dims = "  ".join(f"{d.split('_')[0]}={chapter['dims'][d]}" for d in judges.DIMS)
            print(f"         {chapter['chapter']} composite={chapter['composite']}  {dims}")
        if rubric["worst_dimensions"]:
            print("[gap]    worst-dimension votes: " + ", ".join(
                f"{x['dimension']} x{x['votes']}" for x in rubric["worst_dimensions"]))
        for suggestion in rubric["suggestions"]:
            print(f"[sugg]   ({suggestion['owner']}, x{suggestion['count']}) "
                  f"{suggestion['suggestion'][:140]}")
    print(f"[verdict] HARD CHECKS: {'PASS' if p['hard_ok'] else 'FAIL'} "
          f"({len(p['hard_fails'])} failures)")
    for failure in p["hard_fails"]:
        print(f"          - {failure}")
