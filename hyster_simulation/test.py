from sympy import symbols, Eq, sin, cos, solve

# Определяем переменные
x, y = symbols('x y')

# Определяем систему уравнений
eq1 = Eq(sin(x) + cos(y), 0)


# Решаем систему
solutions = solve(eq1, x, dict=True)

# Выводим решение
print("Аналитическое решение:", solutions)
