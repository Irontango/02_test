#!/usr/bin/env python3
"""PreToolUse(Bash) hook: 파괴적인 명령을 실행 전에 차단합니다.

Claude Code 는 stdin 으로 JSON 을 넘겨줍니다.
exit 2 로 끝내면 명령이 차단되고 stderr 내용이 Claude 에게 전달됩니다.
"""
import json
import re
import sys

BLOCKED = [
    (r"\brm\s+-[a-zA-Z]*r[a-zA-Z]*f?\s+(/|~|\*|\.)(\s|$)", "루트/홈/현재 디렉터리 전체 삭제"),
    (r"\bgit\s+push\b.*(--force\b|-f\b)", "force push"),
    (r"\bgit\s+reset\s+--hard\b", "git reset --hard"),
    (r"\bgit\s+clean\s+-[a-zA-Z]*f", "git clean -f"),
    (r"\bmkfs\b|\bdd\s+if=", "디스크 파괴 명령"),
]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    command = payload.get("tool_input", {}).get("command", "")
    for pattern, label in BLOCKED:
        if re.search(pattern, command):
            print(f"[guard_bash] 차단됨: {label}\n  명령: {command}", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
