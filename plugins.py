"""calculator 의 hook 에 끼워 넣을 수 있는 플러그인 모음."""

from numbers import Number

from calculator import hooks
from hooks import HookAbort


class History:
    """after_calc hook 으로 모든 연산 결과를 기록합니다."""

    def __init__(self) -> None:
        self.records: list[dict] = []

    def __call__(self, ctx: dict) -> None:
        self.records.append(dict(ctx))

    def last(self) -> dict | None:
        return self.records[-1] if self.records else None


def logger(ctx: dict) -> None:
    """after_calc hook 으로 연산 내용을 출력합니다."""
    print(f"[log] {ctx['op']}({ctx['a']}, {ctx['b']}) = {ctx['result']}")


def validate_numbers(ctx: dict) -> None:
    """before_calc hook 으로 숫자가 아닌 입력을 거부합니다."""
    for key in ("a", "b"):
        value = ctx[key]
        if isinstance(value, bool) or not isinstance(value, Number):
            raise HookAbort(f"{key}={value!r} 는 숫자가 아닙니다")


def coerce_strings(ctx: dict) -> None:
    """before_calc hook 으로 '3' 같은 문자열 숫자를 실제 숫자로 바꿉니다."""
    for key in ("a", "b"):
        value = ctx[key]
        if not isinstance(value, str):
            continue
        for convert in (int, float):
            try:
                ctx[key] = convert(value)
                break
            except ValueError:
                continue  # 변환 불가 → 그대로 두고 validate_numbers 가 처리


def install_defaults() -> History:
    """기본 플러그인(문자열 변환 → 숫자 검증 → 기록 → 로그)을 한 번에 등록합니다."""
    history = History()
    hooks.register("before_calc", coerce_strings)
    hooks.register("before_calc", validate_numbers)
    hooks.register("after_calc", history)
    hooks.register("after_calc", logger)
    return history
