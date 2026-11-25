"""Two Days of Quiet Dread entry.

Writes a single code review comment (one line, at most 140 characters)
that approves a pull request with quiet existential dread, to entry.txt
in the output directory the grader provides, and prints it for the log.

Output directory order, as the make.fun preflight requires:
1. $MAKEFUN_OUTPUT_DIR when it is set,
2. /output when it exists (or can be created),
3. a local "output" directory next to this file, only as a last resort.
"""

import os
import sys
from pathlib import Path

COMMENT = (
    "LGTM. The tests pass, the types check out, and I have never felt "
    "further from understanding what any of this actually does."
)

MAX_CHARS = 140


def resolve_output_dir() -> Path:
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if env_dir:
        return Path(env_dir)
    if os.path.isdir("/output"):
        return Path("/output")
    try:
        os.makedirs("/output", exist_ok=True)
        return Path("/output")
    except OSError:
        return Path(__file__).resolve().parent / "output"


def main() -> int:
    comment = COMMENT.strip()
    if "\n" in comment or "\r" in comment:
        print("comment must be a single line", file=sys.stderr)
        return 1
    if not 1 <= len(comment) <= MAX_CHARS:
        print(
            f"comment is {len(comment)} characters, must be 1-{MAX_CHARS}",
            file=sys.stderr,
        )
        return 1
    out_dir = resolve_output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "entry.txt"
    out_path.write_text(comment, encoding="utf-8")
    # Round-trip check: what landed on disk must be exactly the comment,
    # with no added newline or encoding surprise.
    if out_path.read_text(encoding="utf-8") != comment:
        print("written entry.txt does not match the comment", file=sys.stderr)
        return 1
    print(comment)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
