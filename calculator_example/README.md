# 파이썬 계산기 예제 (3개 서브에이전트 협업)

이 예제는 하나의 작업을 **세 개의 서브에이전트**로 나누어 병렬로 구현한 결과물입니다.
각 에이전트는 서로 겹치지 않는 파일을 맡고, 미리 합의된 **인터페이스 계약**을 통해 자연스럽게 통합됩니다.

## 역할 분담

| 서브에이전트 | 담당 파일 | 역할 |
|---|---|---|
| 에이전트 1 | `engine.py` | 계산 엔진 — 사칙연산·거듭제곱·나머지, 예외 처리 |
| 에이전트 2 | `cli.py` | 대화형 REPL 인터페이스 (사용자 입력 파싱·에러 처리) |
| 에이전트 3 | `test_engine.py` | `unittest` 기반 테스트 스위트 |

## 인터페이스 계약 (통합의 핵심)

세 에이전트가 동시에 작업해도 충돌하지 않도록, 아래 계약을 사전에 고정했습니다.

- `engine.py` 가 제공:
  - `add / subtract / multiply / divide / power / modulo` — 각각 `(a: float, b: float) -> float`
  - `divide` / `modulo` 는 `b == 0` 일 때 `ZeroDivisionError` 발생
  - `OPERATIONS` — `{"+","-","*","/","**","%"}` → 함수 매핑 딕셔너리
  - `calculate(a, op, b) -> float` — 알 수 없는 연산자면 `ValueError`

## 실행 방법

```bash
# 1) 엔진 데모
python3 calculator_example/engine.py

# 2) 대화형 계산기 실행
python3 -m calculator_example.cli
#   또는
cd calculator_example && python3 cli.py

# 3) 테스트 실행
python3 -m unittest calculator_example.test_engine -v
```

## 사용 예시

```
계산식> 3 + 4
결과: 7.0
계산식> 2 ** 10
결과: 1024.0
계산식> 10 / 0
오류: 0으로 나눌 수 없습니다.
계산식> quit
계산기를 종료합니다. 안녕히 가세요!
```
