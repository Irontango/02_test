import pytest

from hooks import HookAbort, HookRegistry


def test_register_and_emit_in_order():
    hooks = HookRegistry()
    calls = []
    hooks.register("evt", lambda ctx: calls.append("first"))
    hooks.register("evt", lambda ctx: calls.append("second"))
    hooks.emit("evt")
    assert calls == ["first", "second"]


def test_decorator_registration():
    hooks = HookRegistry()

    @hooks.on("evt")
    def handler(ctx):
        ctx["seen"] = True

    assert hooks.count("evt") == 1
    assert hooks.emit("evt")["seen"] is True


def test_unregister_and_clear():
    hooks = HookRegistry()
    fn = lambda ctx: None  # noqa: E731
    hooks.register("evt", fn)
    hooks.unregister("evt", fn)
    assert hooks.count("evt") == 0

    hooks.register("a", fn)
    hooks.register("b", fn)
    hooks.clear("a")
    assert hooks.count("a") == 0 and hooks.count("b") == 1
    hooks.clear()
    assert hooks.count("b") == 0


def test_emit_without_hooks_returns_ctx():
    hooks = HookRegistry()
    assert hooks.emit("nothing", x=1) == {"x": 1}


def test_hook_can_abort():
    hooks = HookRegistry()

    def block(ctx):
        raise HookAbort("blocked")

    hooks.register("evt", block)
    with pytest.raises(HookAbort):
        hooks.emit("evt")
