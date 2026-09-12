import pytest

import calculator
import plugins
from hooks import HookAbort


@pytest.fixture(autouse=True)
def clean_hooks():
    calculator.hooks.clear()
    yield
    calculator.hooks.clear()


def test_basic_operations():
    assert calculator.add(10, 5) == 15
    assert calculator.subtract(10, 5) == 5
    assert calculator.multiply(3, 4) == 12
    assert calculator.divide(9, 3) == 3


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        calculator.divide(1, 0)


def test_before_and_after_hooks_fire():
    events = []
    calculator.hooks.register("before_calc", lambda ctx: events.append(("before", ctx["op"])))
    calculator.hooks.register("after_calc", lambda ctx: events.append(("after", ctx["result"])))
    calculator.add(1, 2)
    assert events == [("before", "add"), ("after", 3)]


def test_history_plugin_records_every_call():
    history = plugins.History()
    calculator.hooks.register("after_calc", history)
    calculator.add(1, 1)
    calculator.subtract(5, 2)
    assert len(history.records) == 2
    assert history.last() == {"op": "subtract", "a": 5, "b": 2, "result": 3}


def test_validate_plugin_blocks_non_numbers():
    calculator.hooks.register("before_calc", plugins.validate_numbers)
    with pytest.raises(HookAbort):
        calculator.add("x", 1)
    with pytest.raises(HookAbort):
        calculator.add(True, 1)


def test_coerce_plugin_converts_strings():
    calculator.hooks.register("before_calc", plugins.coerce_strings)
    assert calculator.multiply("6", "7") == 42
    assert calculator.add("1.5", 1) == 2.5


def test_coerce_plugin_leaves_non_numeric_strings_alone():
    calculator.hooks.register("before_calc", plugins.coerce_strings)
    calculator.hooks.register("before_calc", plugins.validate_numbers)
    with pytest.raises(HookAbort):
        calculator.add("abc", 1)


def test_install_defaults_pipeline(capsys):
    history = plugins.install_defaults()
    assert calculator.add("2", 3) == 5
    assert history.last()["a"] == 2
    assert "[log] add(2, 3) = 5" in capsys.readouterr().out
