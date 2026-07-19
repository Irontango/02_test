"""engine 모듈에 대한 단위 테스트 모음.

저장소 루트에서 `python3 -m unittest` 로 실행하거나,
이 폴더 안에서 직접 실행하는 두 경우 모두를 지원하기 위해
try/except 로 엔진을 임포트한다.
"""

import unittest

try:
    from calculator_example import engine
except ImportError:  # 폴더 안에서 직접 실행하는 경우
    import engine


class TestArithmeticFunctions(unittest.TestCase):
    """개별 산술 함수의 동작을 검증한다."""

    def test_add(self):
        """덧셈: 양수, 음수, 실수 경우를 확인한다."""
        self.assertEqual(engine.add(2, 3), 5)
        self.assertEqual(engine.add(-2, -3), -5)
        self.assertAlmostEqual(engine.add(0.1, 0.2), 0.3)

    def test_subtract(self):
        """뺄셈: 양수, 음수, 실수 경우를 확인한다."""
        self.assertEqual(engine.subtract(5, 3), 2)
        self.assertEqual(engine.subtract(-5, -3), -2)
        self.assertAlmostEqual(engine.subtract(0.3, 0.1), 0.2)

    def test_multiply(self):
        """곱셈: 양수, 음수, 실수 경우를 확인한다."""
        self.assertEqual(engine.multiply(4, 3), 12)
        self.assertEqual(engine.multiply(-4, 3), -12)
        self.assertAlmostEqual(engine.multiply(2.5, 2), 5.0)

    def test_divide(self):
        """나눗셈: 양수, 음수, 실수 경우를 확인한다."""
        self.assertEqual(engine.divide(10, 2), 5)
        self.assertEqual(engine.divide(-10, 2), -5)
        self.assertAlmostEqual(engine.divide(1, 4), 0.25)

    def test_power(self):
        """거듭제곱: 양수, 음수 지수, 실수 경우를 확인한다."""
        self.assertEqual(engine.power(2, 3), 8)
        self.assertAlmostEqual(engine.power(2, -1), 0.5)
        self.assertAlmostEqual(engine.power(4, 0.5), 2.0)

    def test_modulo(self):
        """나머지: 양수, 음수, 실수 경우를 확인한다."""
        self.assertEqual(engine.modulo(10, 3), 1)
        self.assertEqual(engine.modulo(-10, 3), 2)
        self.assertAlmostEqual(engine.modulo(5.5, 2), 1.5)


class TestZeroDivision(unittest.TestCase):
    """0으로 나누는 경우 예외 처리를 검증한다."""

    def test_divide_by_zero(self):
        """나눗셈에서 divisor 가 0 이면 ZeroDivisionError 를 발생시킨다."""
        with self.assertRaises(ZeroDivisionError):
            engine.divide(1, 0)

    def test_modulo_by_zero(self):
        """나머지 연산에서 divisor 가 0 이면 ZeroDivisionError 를 발생시킨다."""
        with self.assertRaises(ZeroDivisionError):
            engine.modulo(1, 0)


class TestCalculate(unittest.TestCase):
    """calculate() 디스패치 동작을 검증한다."""

    def test_calculate_all_operators(self):
        """OPERATIONS 의 모든 연산자에 대해 올바르게 디스패치되는지 확인한다."""
        expected = {
            "+": engine.add(6, 2),
            "-": engine.subtract(6, 2),
            "*": engine.multiply(6, 2),
            "/": engine.divide(6, 2),
            "**": engine.power(6, 2),
            "%": engine.modulo(6, 2),
        }
        for op in engine.OPERATIONS:
            with self.subTest(op=op):
                self.assertAlmostEqual(engine.calculate(6, op, 2), expected[op])

    def test_calculate_unknown_operator(self):
        """알 수 없는 연산자를 넘기면 ValueError 를 발생시킨다."""
        with self.assertRaises(ValueError):
            engine.calculate(1, "?", 2)


if __name__ == "__main__":
    unittest.main()
