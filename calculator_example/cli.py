"""계산기 CLI / REPL 인터페이스.

이 모듈은 대화형 계산기 셸을 제공한다. 사용자는 ``3 + 4`` 형태의
수식을 입력하고, 내부적으로 ``engine`` 모듈을 통해 계산 결과를 얻는다.

표준 라이브러리만 사용한다.
"""

from __future__ import annotations

# ``engine`` 모듈은 두 가지 실행 방식 모두를 지원해야 한다.
#   1) 패키지로 실행: ``python -m calculator_example.cli``
#   2) 폴더 안에서 직접 실행: ``python cli.py``
try:  # 패키지 형태로 임포트 시도
    from calculator_example import engine
except ImportError:  # 같은 폴더에서 직접 실행하는 경우 대비
    import engine  # type: ignore[no-redef]


def parse_expression(text: str) -> tuple[float, str, float]:
    """``"3 + 4"`` 같은 문자열을 ``(3.0, "+", 4.0)`` 튜플로 변환한다.

    입력은 "숫자 연산자 숫자" 형식이며 공백으로 구분되어야 한다.

    Args:
        text: 파싱할 수식 문자열.

    Returns:
        ``(왼쪽 피연산자, 연산자, 오른쪽 피연산자)`` 형태의 튜플.

    Raises:
        ValueError: 토큰 개수가 3개가 아니거나 피연산자가 숫자가 아닐 때.
    """
    tokens = text.split()
    if len(tokens) != 3:
        raise ValueError(
            "입력 형식이 올바르지 않습니다. '숫자 연산자 숫자' 형태로 입력하세요."
        )

    left_str, op, right_str = tokens
    try:
        left = float(left_str)
        right = float(right_str)
    except ValueError:
        raise ValueError(
            f"피연산자는 숫자여야 합니다: '{left_str}', '{right_str}'"
        ) from None

    return left, op, right


def _print_banner() -> None:
    """환영 배너와 간단한 사용법을 출력한다."""
    print("=" * 40)
    print("  간단 계산기 (Python Calculator)")
    print("=" * 40)
    print("사용법: 숫자 연산자 숫자  (예: 3 + 4)")
    print("지원 연산자: +  -  *  /  **  %")
    print("종료: quit, exit, q  (또는 Ctrl-D / Ctrl-C)")
    print("-" * 40)


def run() -> None:
    """대화형 REPL 루프를 시작한다.

    사용자로부터 수식을 반복적으로 입력받아 계산 결과를 출력한다.
    잘못된 입력, 알 수 없는 연산자, 0으로 나누기 등의 오류는
    친절한 한국어 메시지를 출력한 뒤 루프를 계속한다.

    ``quit``/``exit``/``q`` 입력, EOF(Ctrl-D), KeyboardInterrupt(Ctrl-C)로
    루프를 종료한다.
    """
    _print_banner()

    while True:
        try:
            raw = input("계산식> ")
        except (EOFError, KeyboardInterrupt):
            print()  # 프롬프트 줄을 깔끔하게 마무리
            print("계산기를 종료합니다. 안녕히 가세요!")
            break

        text = raw.strip()
        if not text:
            continue

        if text.lower() in {"quit", "exit", "q"}:
            print("계산기를 종료합니다. 안녕히 가세요!")
            break

        try:
            left, op, right = parse_expression(text)
            result = engine.calculate(left, op, right)
        except ValueError as exc:
            print(f"오류: {exc}")
            continue
        except ZeroDivisionError:
            print("오류: 0으로 나눌 수 없습니다.")
            continue

        print(f"결과: {result}")


if __name__ == "__main__":
    run()
