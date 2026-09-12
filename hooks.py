"""간단한 이벤트 hook 시스템.

사용법:
    from hooks import HookRegistry

    hooks = HookRegistry()
    hooks.register("after_calc", lambda ctx: print(ctx))
    hooks.emit("after_calc", op="add", result=3)

hook 함수는 dict 형태의 ctx 하나를 인자로 받습니다.
before_* hook에서 HookAbort 를 발생시키면 해당 작업이 중단됩니다.
"""

from collections import defaultdict
from typing import Callable, Dict, List

HookFn = Callable[[dict], None]


class HookAbort(Exception):
    """before_* hook 에서 작업을 중단시키고 싶을 때 발생시키는 예외."""


class HookRegistry:
    def __init__(self) -> None:
        self._hooks: Dict[str, List[HookFn]] = defaultdict(list)

    def register(self, event: str, fn: HookFn) -> HookFn:
        """hook 을 등록합니다. 데코레이터로도 쓸 수 있습니다."""
        self._hooks[event].append(fn)
        return fn

    def on(self, event: str) -> Callable[[HookFn], HookFn]:
        """@hooks.on("after_calc") 형태의 데코레이터."""

        def decorator(fn: HookFn) -> HookFn:
            return self.register(event, fn)

        return decorator

    def unregister(self, event: str, fn: HookFn) -> None:
        if fn in self._hooks[event]:
            self._hooks[event].remove(fn)

    def clear(self, event: str | None = None) -> None:
        if event is None:
            self._hooks.clear()
        else:
            self._hooks.pop(event, None)

    def emit(self, event: str, **ctx) -> dict:
        """등록된 순서대로 hook 을 호출하고 ctx 를 돌려줍니다."""
        for fn in list(self._hooks.get(event, [])):
            fn(ctx)
        return ctx

    def count(self, event: str) -> int:
        return len(self._hooks.get(event, []))
