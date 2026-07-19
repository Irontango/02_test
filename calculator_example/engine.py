"""계산기 엔진 모듈.

이 모듈은 계산기 프로젝트의 핵심 엔진(core engine)입니다.
기본적인 산술 연산(더하기, 빼기, 곱하기, 나누기, 거듭제곱, 나머지)을
순수 함수로 제공하며, 연산자 기호를 함수에 매핑하는 OPERATIONS 딕셔너리와
연산자 기호로 계산을 수행하는 calculate() 함수를 제공합니다.

표준 라이브러리만 사용하며 외부 의존성이 없습니다.
"""

from typing import Callable, Dict


def add(a: float, b: float) -> float:
    """두 수를 더한 결과를 반환합니다."""
    return a + b


def subtract(a: float, b: float) -> float:
    """첫 번째 수에서 두 번째 수를 뺀 결과를 반환합니다."""
    return a - b


def multiply(a: float, b: float) -> float:
    """두 수를 곱한 결과를 반환합니다."""
    return a * b


def divide(a: float, b: float) -> float:
    """첫 번째 수를 두 번째 수로 나눈 결과를 반환합니다.

    b가 0이면 ZeroDivisionError를 발생시킵니다.
    """
    if b == 0:
        raise ZeroDivisionError("0으로 나눌 수 없습니다")
    return a / b


def power(a: float, b: float) -> float:
    """첫 번째 수를 두 번째 수만큼 거듭제곱한 결과를 반환합니다."""
    return a ** b


def modulo(a: float, b: float) -> float:
    """첫 번째 수를 두 번째 수로 나눈 나머지를 반환합니다.

    b가 0이면 ZeroDivisionError를 발생시킵니다.
    """
    if b == 0:
        raise ZeroDivisionError("0으로 나눌 수 없습니다")
    return a % b


# 연산자 기호를 해당 연산 함수에 매핑하는 딕셔너리
OPERATIONS: Dict[str, Callable[[float, float], float]] = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
    "**": power,
    "%": modulo,
}


def calculate(a: float, op: str, b: float) -> float:
    """연산자 기호 op를 사용하여 a와 b에 대한 계산을 수행합니다.

    op를 OPERATIONS에서 찾아 해당 함수를 호출하고 결과를 반환합니다.
    지원하지 않는 연산자인 경우 ValueError를 발생시킵니다.
    """
    if op not in OPERATIONS:
        raise ValueError(f"지원하지 않는 연산자입니다: {op}")
    return OPERATIONS[op](a, b)


if __name__ == "__main__":
    # 각 연산을 시연하는 예제 계산
    print("계산기 엔진 예제")
    print(f"3 + 4 = {calculate(3, '+', 4)}")
    print(f"10 - 6 = {calculate(10, '-', 6)}")
    print(f"5 * 7 = {calculate(5, '*', 7)}")
    print(f"20 / 4 = {calculate(20, '/', 4)}")
    print(f"2 ** 10 = {calculate(2, '**', 10)}")
    print(f"17 % 5 = {calculate(17, '%', 5)}")

    # 0으로 나누기 예외 시연
    try:
        calculate(1, "/", 0)
    except ZeroDivisionError as exc:
        print(f"예외 발생: {exc}")

    # 지원하지 않는 연산자 예외 시연
    try:
        calculate(1, "?", 2)
    except ValueError as exc:
        print(f"예외 발생: {exc}")
