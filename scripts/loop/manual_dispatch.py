"""Emit agent instructions that pin relative paths to one operation root."""
import shlex
from pathlib import Path


def _cwd(root):
    return f"cd -- {shlex.quote(str(Path(root).absolute()))}"


def writer(cfg, operation, book, selected):
    operation, book = Path(operation).absolute(), Path(book).absolute()
    relative = book.relative_to(operation)
    print("[run] NO writer key (OPENROUTER_API_KEY / LITELLM_API_KEY) — MANUAL MODE.")
    print(f"[run] Mandatory pinned operation cwd: {_cwd(operation)}")
    print("[run] From that cwd, dispatch prompts/chapter-writer.md once PER CHAPTER,")
    print(f"      fresh context each, for chapters {','.join(map(str, selected))}; model "
          f"{cfg['writer_model']} (reasoning={cfg.get('writer_reasoning', 'none')}).")
    print(f"      Inputs: prompts/style-guide.md, {relative}/master-plan.md, and only")
    print(f"      {relative}/chapters/chapter-NN.md for the immediately previous chapter.")
    print(f"      Save each output to {relative}/chapters/chapter-NN.md (zero-padded),")
    print("      then re-run the same command with --no-write.")


def reviewer(operation):
    operation = Path(operation).absolute()
    return (f"mandatory cwd `{_cwd(operation)}`; dispatch "
            "`prompts/chapter-reviewer.md` from that cwd")


def resume(args, script, python):
    """Render only the pinned, non-secret invocation plus --no-write."""
    command = [python, str(Path(script).absolute()),
               "--book", args.book, "--chapters", args.chapters,
               "--iter", str(args.iter), "--hypothesis", args.hypothesis]
    if args.config is not None:
        command.extend(("--config", args.config))
    if args.accepted_root is not None:
        command.extend(("--accepted-root", str(Path(args.accepted_root).absolute())))
    if args.decision_timestamp is not None:
        command.extend(("--decision-timestamp", args.decision_timestamp))
    if args.promote_pair:
        command.append("--promote-pair")
    command.extend(("--redesign-authorized", "--rf-stage", args.rf_stage,
                    "--candidate-root", str(Path(args.candidate_root).absolute()),
                    "--no-write"))
    return shlex.join(command)
