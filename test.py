import numpy as np
import scipy
import scipy.integrate as integrate

def integral(function, start, stop):
    return integrate.quad(function, start, stop)[0]


# def update_f(g, other):
#     a = g(0)
#     b = integral(other, 0, 1)
#     def f(x):
#         return a + b - x + g(x)
#     return f

# def update_g(f):
#     c = f(1)
#     def g(x):
#         I = integral(f, 0, 2)
#         return c - x + f(x) + I
#     return g

def update_f(g, other):
    print(g)
    a = 1 - integral(g, 0, 1)
    b = integral(other, 0, 1)

    def BR(x):
        print('running f')
        win_prob_given_call = a
        return win_prob_given_call * x + g(2)
    return BR

def update_g(f):
    def BR(x):
        print("running g")
        # I1 = integral(f, 0, x)
        I1 = f(x)
        # I2 = integral(f, 0, 1)
        # I1 = 2
        I2 = 3
        if I1 > 1/4 * I2:
            return 1
        else:
            return 0
    return BR


g0 = lambda x: x  # Start with initial g
other = lambda x: 1  # Start with initial f

# f0 = update_f(g0, other)  # Update f based on g0
# g1 = update_g(f0)  # Update g based on f0
# f2 = update_f(g1, other)  # Update f based on g1
# g2 = update_g(f2)  
# f3 = update_f(g2, other) 
# g3 = update_g(f3)  

# print(g2(1))
f = update_f(g0, other)
print(integral(f, 0, 1))