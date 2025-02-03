
from sympy import symbols, diff, sin, cos, pi, solve, Eq, nonlinsolve, simplify, nsolve, lambdify
from sympy.polys.polytools import is_zero_dimensional
import numpy as np
from scipy.optimize import fsolve, least_squares

J = symbols("J")    # exchange constant
K_1, K_2 = symbols("K_1, K_2")     # anisotropy constants
M_1, Theta_1, Phi_1 = symbols("M_1, Theta_1, Phi_1")  # 1st lattice magnetization params
M_2, Phi_2, Theta_2 = symbols("M_2, Phi_2, Theta_2")  # 2nd lattice magnetization params
H, Theta_H, Phi_H = symbols("H, Theta_H, Phi_H")   # ext. field params


E_zeeman = -M_1*H*(sin(Theta_1)*cos(Phi_1)*sin(Theta_H)*cos(Phi_H) + 
                   sin(Theta_1)*sin(Phi_1)*sin(Theta_H)*sin(Phi_H) +
                   cos(Theta_1)*cos(Theta_H)) - M_2*H*(sin(Theta_2)*cos(Phi_2)*sin(Theta_H)*cos(Phi_H) + 
                                                       sin(Theta_2)*sin(Phi_2)*sin(Theta_H)*sin(Phi_H) +
                                                       cos(Theta_2)*cos(Theta_H))

E_exchange = -J*M_1*M_2*(sin(Theta_1)*cos(Phi_1)*sin(Theta_2)*cos(Phi_2) + 
                         sin(Theta_1)*sin(Phi_1)*sin(Theta_2)*sin(Phi_2) + 
                         cos(Theta_1)*cos(Theta_2))

E_anisotropy = K_1*sin(Theta_1)**2 + K_2*sin(Theta_2)**2

E_demag = -2*pi*(cos(Theta_1) + cos(Theta_2))**2

E = E_zeeman + E_exchange + E_anisotropy + E_demag   # полная энергия

# Производные(частные) полной энергии по Theta_1, Theta_2, Phi_1, Phi_2, соответственно
E_differ_Theta_1 = diff(E, Theta_1)  
E_differ_Theta_2 = diff(E, Theta_2)    
E_differ_Phi_1 = diff(E, Phi_1)        
E_differ_Phi_2 = diff(E, Phi_2)         
 

# Подстановка известных констант и упрощение уравнений
eq_Theta_1 = simplify(E_differ_Theta_1.subs({J: 1, M_1: 1, M_2: 1, H: 1, K_1: 1, K_2: 1, Theta_H: pi/2, Phi_H: 0})) 
eq_Theta_2 = simplify(E_differ_Theta_2.subs({J: 1, M_1: 1, M_2: 1, H: 1, K_1: 1, K_2: 1, Theta_H: pi/2, Phi_H: 0}))
eq_Phi_1 = simplify(E_differ_Phi_1.subs({J: 1, M_1: 1, M_2: 1, H: 1, K_1: 1, K_2: 1, Theta_H: pi/2, Phi_H: 0}))
eq_Phi_2 = simplify(E_differ_Phi_2.subs({J: 1, M_1: 1, M_2: 1, H: 1, K_1: 1, K_2: 1, Theta_H: pi/2, Phi_H: 0}))

# Преобразование в функцию Python (SymPy -> NumPy)
equations_numpy = lambdify((Theta_1, Theta_2, Phi_1, Phi_2), [eq_Theta_1, eq_Theta_2, eq_Phi_1, eq_Phi_2], 'numpy')

# Определение функции для `least_squares`
def equations(vars):
    return equations_numpy(*vars)    # vars=[Theta_1, Theta_2, Phi_1, Phi_2]

# Функция для решения системы уравнений
def solve_system(starting_guess):
    res = least_squares(equations, starting_guess)
    if res.success:
        return tuple(map(lambda x: round(float(x), 5), res.x))
    else:
        return None

solutions = []

# Перебор значений для поиска всех возможных решений      # Начальные приближения:
for Theta1 in np.linspace(-np.pi/2, np.pi/2, 3):          # 7 = от -pi/2 до pi/2 с шагом pi/6
    for Theta2 in np.linspace(-np.pi/2, np.pi/2, 3):      # 7 = от -pi/2 до pi/2 с шагом pi/6
        for Phi1 in np.linspace(-np.pi, np.pi, 5):       # 13 = от -pi до pi с шагом pi/6
            for Phi2 in np.linspace(-np.pi, np.pi, 5):   # 13 = от -pi до pi с шагом pi/6
                # Численное решение системы
                sol = solve_system([Theta1, Theta2, Phi1, Phi2])
                if sol not in solutions:
                    solutions.append(sol)

# На данный момент находятся все экстремумы производной полной энергии, 
# для расчета истинного минимума энергии необходимо вычислить вторые производые(частные), 
# если вторая производная положительная, то корни - истинные минимумы


if __name__ ==  '__main__':
    print(solutions)


