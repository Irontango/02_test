# Hook 계산기

hook 을 두 층위에서 사용하는 작은 Python 프로젝트입니다.

## 1. 애플리케이션 hook (Python)

| 파일 | 역할 |
| --- | --- |
| `hooks.py` | `HookRegistry` — 이벤트별 콜백 등록/해제/실행 |
| `calculator.py` | 모든 연산 전후에 `before_calc` / `after_calc` 이벤트 발생 |
| `plugins.py` | hook 에 끼우는 플러그인: 문자열 변환, 숫자 검증, 기록, 로그 |
| `main.py` | 데모 |

```python
import calculator, plugins

history = plugins.install_defaults()   # 플러그인 등록
calculator.multiply("6", "7")          # coerce → validate → 계산 → history → log
print(history.last())                  # {'op': 'multiply', 'a': 6, 'b': 7, 'result': 42}
```

`before_calc` hook 은 `ctx["a"]`, `ctx["b"]` 를 바꿀 수 있고, `HookAbort` 를 발생시켜 연산을 막을 수 있습니다.

## 2. Claude Code hook (`.claude/settings.json`)

| 이벤트 | 스크립트 | 동작 |
| --- | --- | --- |
| `SessionStart` | `.claude/hooks/session_start.sh` | pytest 준비, 브랜치/테스트 요약 출력 |
| `PreToolUse` (Bash) | `.claude/hooks/guard_bash.py` | `rm -rf /`, force push 등 파괴적 명령 차단 |
| `PostToolUse` (Edit/Write) | `.claude/hooks/run_tests.py` | `.py` 수정 시 문법 검사 + pytest 자동 실행, 실패 시 Claude 에게 피드백 |

hook 스크립트는 stdin 으로 JSON 을 받고, `exit 2` 로 끝내면 stderr 가 Claude 에게 전달됩니다.

## 실행

```bash
pip install pytest
python main.py
pytest
```
