"""hook 을 지원하는 계산기 모듈.

모든 연산은 실행 전에 ``before_calc``, 실행 후에 ``after_calc`` 이벤트를 발생시킵니다.
``hooks`` 레지스트리에 함수를 등록하면 로깅, 기록, 입력 검증 등을 끼워 넣을 수 있습니다.
"""

from hooks import HookRegistry

intro = "계산기 모듈을 불러왔습니다"
hooks = HookRegistry()


def _run(op: str, a, b, fn):
    ctx = hooks.emit("before_calc", op=op, a=a, b=b)
    # before_calc hook 이 a, b 를 바꿀 수 있도록 ctx 값을 다시 읽습니다.
    result = fn(ctx["a"], ctx["b"])
    hooks.emit("after_calc", op=op, a=ctx["a"], b=ctx["b"], result=result)
    return result


def add(a, b):
    return _run("add", a, b, lambda x, y: x + y)


def subtract(a, b):
    return _run("subtract", a, b, lambda x, y: x - y)


def multiply(a, b):
    return _run("multiply", a, b, lambda x, y: x * y)


def divide(a, b):
    def _div(x, y):
        if y == 0:
            raise ZeroDivisionError("0으로 나눌 수 없습니다")
        return x / y

    return _run("divide", a, b, _div)
