#!/usr/bin/env bash
# SessionStart hook: 테스트 도구를 준비하고 프로젝트 상태를 요약해 Claude 에게 알려줍니다.
set -u
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0

if ! python3 -c "import pytest" 2>/dev/null; then
  python3 -m pip install -q pytest >/dev/null 2>&1 || true
fi

echo "[session_start] 브랜치: $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '?')"
echo "[session_start] 테스트 파일: $(ls tests/test_*.py 2>/dev/null | wc -l)개"
echo "[session_start] 규칙: .py 수정 시 자동으로 pytest 가 실행되고, 위험한 Bash 명령은 차단됩니다."
exit 0
