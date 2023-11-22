from sympy import *
x, y = symbols('x,y')
res = to_cnf(y >> (x & y), True)
print (str(res))