#!/usr/bin/env python3
"""PostToolUse(Edit|Write) hook: .py 파일이 바뀌면 문법 검사와 pytest 를 자동 실행합니다.

실패하면 exit 2 로 끝내 stderr 를 Claude 에게 돌려주어 바로 고치도록 합니다.
"""
import json
import os
import subprocess
import sys

PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    file_path = payload.get("tool_input", {}).get("file_path", "")
    if not file_path.endswith(".py"):
        return 0

    compile_result = subprocess.run(
        [sys.executable, "-m", "py_compile", file_path],
        capture_output=True, text=True,
    )
    if compile_result.returncode != 0:
        print(f"[run_tests] 문법 오류: {file_path}\n{compile_result.stderr}", file=sys.stderr)
        return 2

    test_result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests"],
        capture_output=True, text=True, cwd=PROJECT_DIR,
    )
    if test_result.returncode != 0:
        tail = "\n".join(test_result.stdout.splitlines()[-30:])
        print(f"[run_tests] 테스트 실패 ({file_path} 수정 후)\n{tail}", file=sys.stderr)
        return 2

    summary = test_result.stdout.strip().splitlines()[-1] if test_result.stdout.strip() else "ok"
    print(f"[run_tests] {file_path}: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
