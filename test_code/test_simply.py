from sympy import *
from sympy import symbols
from sympy.logic.boolalg import to_cnf
from sympy.logic.utilities.dimacs import load
x, y, z = symbols('x,y,z')
boolean_formulation = (~x & y) & (y | (~x & y))
v_P = to_cnf(boolean_formulation,True)
print(v_P)

#x_1_0,x_1_1,x_1_2 = symbols('x_1_0,x_1_1,x_1_2')
x_1_0 = symbols('x_1_0')
x_1_1 = symbols('x_1_1')
x_1_2 = symbols('x_1_2')
boolean_formulation = (~x_1_2 & x_1_1) & (x_1_0 | (~x_1_0 & x_1_0))
v_respuesta = to_cnf(boolean_formulation,True)
print(v_respuesta)

#LOAD FROM TEXT
#exp = load("11 21 3\n 11 -3")
#res = to_cnf(exp, True)