import calculator
import plugins
from hooks import HookAbort

print(calculator.intro)

history = plugins.install_defaults()

result1 = calculator.add(10, 5)
print("덧셈결과:", result1)
print("문자열 입력도 처리:", calculator.multiply("6", "7"))

try:
    calculator.add("abc", 1)
except HookAbort as e:
    print("검증 hook 이 막음:", e)

print("기록된 연산 수:", len(history.records))
print("마지막 연산:", history.last())
