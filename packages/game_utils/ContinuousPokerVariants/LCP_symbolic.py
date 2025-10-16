from sympy import symbols, solve, diff, integrate, Dummy, simplify
import sympy as sp
from game_utils.ContinuousPokerVariants.ContinousPokerTemplate import ContinuousPokerTemplate
from scipy.optimize import root_scalar
import numpy as np


class LCP_symbolic(ContinuousPokerTemplate):
    solved = False
    sol_dict = None
    
    # Class variables for symbols and functions
    r, t, s = sp.symbols('r t s')   # r = L/(1+L), t = 1/(1+U)
    x0, x1, x2, x3, x4, x5, b0 = sp.symbols('x0 x1 x2 x3 x4 x5, b0')
    c = sp.Function('c')
    v = sp.Function('v')
    b = sp.Function('b')

    @staticmethod
    def extract_rt(**kwargs):
        """
        Normalize parameters so that only (r,t) are returned.
        Accepts either (L,U) or (r,t), but not both or neither.
        Returns a dict with keys {'r': r_val, 't': t_val}.
        """
        rt_params = {'r', 't'}
        lu_params = {'L', 'U'}
        provided_params = set(kwargs.keys())

        if provided_params == rt_params:
            return float(kwargs['r']), float(kwargs['t'])
        elif provided_params == lu_params:
            L = float(kwargs['L'])
            U = float(kwargs['U'])
            assert L >= 0 and U >= L, "L and U must be non-negative and U must be greater than or equal to L"
            r = L / (1 + L)
            t = 1 / (1 + U)
            return r, t
        else:
            raise ValueError("Must provide exactly (r,t) or exactly (L,U), no other combinations.")


    @staticmethod
    def get_LU(r, t):
        L = r/(1-r)
        U = (1-t)/t
        return L, U


    @classmethod
    def solve_neq(cls, verbose=True):
        '''
        Solve the constraint equations to find Nash Equilibrium.
        Returns a dictionary of the relevant variables as sympy expressions, which will be depenedent on the game parameters.
        '''
        if cls.solved:
            return cls.sol_dict
        
        cls.solved = True
        
        # --- symbols ---
        r, t, s = cls.r, cls.t, cls.s   
        x0,x1,x2,x3,x4,x5 = cls.x0, cls.x1, cls.x2, cls.x3, cls.x4, cls.x5
        c = cls.c
        v = cls.v
        b = cls.b

        # --- L and U in terms of r,t ---
        L, U = cls.get_LU(r, t)

        # --- Bettor indifference equations ---
        bettor_indiff_2 = sp.Eq(c(s) - (1-c(s))*s, x2)

        # --- solve for c(s) ---
        c_s = sp.solve(bettor_indiff_2, c(s))[0]

        # --- Bettor optimality ODE ---
        bettor_optimality_ode = sp.Eq(-s*sp.diff(c_s, s) - c_s + 2*v(s) - 1, 0)

        # --- solve for v(s) ---
        v_s = sp.solve(bettor_optimality_ode, v(s))[0]

        # --- Solving for x0,x1,x3,x4,x5 in terms of x2 ---
        # --- Evaluate at boundaries ---
        cL = c_s.subs(s, L)
        vL = v_s.subs(s, L)
        vU = v_s.subs(s, U)

        # --- Equations ---
        eq1 = sp.Eq(x2 - x1 - r*(x4 - x3), 0)           # caller indiff 1
        eq2 = sp.Eq(x0 - (1 - x5)*(1 - t), 0)           # caller indiff 2
        eq3 = sp.Eq(x3 - (1 + cL)/2, 0)                 # bettor indiff
        eq4 = sp.Eq(vL, x4)                             # v(L)=x4
        eq5 = sp.Eq(vU, x5)                             # v(U)=x5

        # Solve for x0,x1,x3,x4,x5 in terms of free parameter x2
        sol = sp.linsolve([eq1, eq2, eq3, eq4, eq5], (x0, x1, x3, x4, x5))

        # Extract solution set (linsolve returns FiniteSet of tuples)
        sol_tuple = list(sol)[0]

        # Build dict mapping
        sol_dict = {var: expr for var, expr in zip([x0, x1, x3, x4, x5], sol_tuple)}

        # --- Solving for b(s) in terms of x_2 and b0 ---
        # --- Caller indifference constraint ---
        caller_indiff_ode = sp.Eq(sp.diff(b(s), s) * (1 + s) + sp.diff(v_s, s) * s, 0)

        # --- solve for b(s) ---
        b0 = sp.symbols('b0')
        b_s = sp.dsolve(caller_indiff_ode, b(s)).subs("C1", b0).rhs

        # --- Solving for b0 and x2 using boundary conditions ---
        bL = b_s.subs(s, L)
        bU = b_s.subs(s, U)

        # --- Equations ---
        eq6 = sp.Eq(bU, x0).subs(x0, sol_dict[x0])
        eq7 = sp.Eq(bL, x1).subs(x1, sol_dict[x1])

        # Solve for b0 and x2
        sol = sp.linsolve([eq6, eq7], (b0, x2))

        # Extract solution set (linsolve returns FiniteSet of tuples)
        sol_tuple = list(sol)[0]

        # extend the sol_dict with the solution
        sol_dict.update({b0: sol_tuple[0], x2: sol_tuple[1]})

        # Substituting x2 back into the other variables
        sol_dict = {k: expr.subs(x2, sol_dict[x2]).simplify() for k, expr in sol_dict.items()}
        sol_dict[b] = sp.factor(b_s-b0)+b0
        sol_dict[c] = c_s
        sol_dict[v] = sp.numer(v_s)/sp.factor(sp.denom(v_s))

        # Display results
        if verbose:
            for k, expr in sol_dict.items():
                print(k)
                display(expr)

        cls.sol_dict = sol_dict
        return sol_dict

    
    @classmethod
    def inverse_b(cls, x, bracket=(1e-6, 100), **kwargs):
        # numerically solve b(s) = x for s
        r, t = cls.extract_rt(**kwargs)
        x2 = float(cls.sol_dict[cls.x2].subs("r", r).subs("t", t))
        b0 = float(cls.sol_dict[cls.b0].subs("r", r).subs("t", t))
        f = sp.lambdify(sp.symbols('s'), cls.sol_dict[cls.b].subs(cls.b0, b0).subs(cls.x2, x2) - x, 'numpy')

        sol = root_scalar(f, bracket=bracket, method='brentq')
        if sol.converged:
            return sol.root
        else:
            raise ValueError("Root finding did not converge")


    @classmethod
    def inverse_v(cls, x, **kwargs):
        r, t = cls.extract_rt(**kwargs)
        x2 = float(cls.sol_dict[cls.x2].subs("r", r).subs("t", t))
        return -1 - np.sqrt( (4*x-4) * (-2 + 2*x2) ) / (4*x-4)


    @classmethod
    def call_threshold(cls, s, **kwargs):
        assert cls.solved, "Must solve the equations first"
        s = float(s) # to avoid some weird numpy-sympy type issue
        r, t = cls.extract_rt(**kwargs)
        x2 = float(cls.sol_dict[cls.x2].subs("r", r).subs("t", t))
        c = cls.sol_dict[cls.c].subs(cls.s, s).subs(cls.x2, x2)
        return c
    

    @classmethod
    def bluff_threshold(cls, **kwargs):
        assert cls.solved, "Must solve the equations first"
        r, t = cls.extract_rt(**kwargs)
        x2 = float(cls.sol_dict[cls.x2].subs("r", r).subs("t", t))
        return x2
    

    @classmethod
    def value_threshold(cls, **kwargs):
        assert cls.solved, "Must solve the equations first"
        r, t = cls.extract_rt(**kwargs)
        x3 = float(cls.sol_dict[cls.x3].subs("r", r).subs("t", t))
        return x3

    @classmethod
    def bluff_size(cls, x, **kwargs):
        assert cls.solved, "Must solve the equations first"
        x = float(x) # to avoid some weird numpy-sympy type issue
        r, t = cls.extract_rt(**kwargs)
        L, U = cls.get_LU(r, t)
        x0 = float(cls.sol_dict[cls.x0].subs("r", r).subs("t", t))
        x1 = float(cls.sol_dict[cls.x1].subs("r", r).subs("t", t))
        if x < x0:
            return U
        elif x < x1:
            return cls.inverse_b(x, r=r, t=t)
        else:
            return L


    @classmethod
    def value_size(cls, x, **kwargs):
        assert cls.solved, "Must solve the equations first"
        x = float(x) # to avoid some weird numpy-sympy type issue
        r, t = cls.extract_rt(**kwargs)
        L, U = cls.get_LU(r, t)
        x4 = float(cls.sol_dict[cls.x4].subs("r", r).subs("t", t))
        x5 = float(cls.sol_dict[cls.x5].subs("r", r).subs("t", t))
        if x < x4:
            return L
        elif x < x5:
            return cls.inverse_v(x, r=r, t=t)
        else:
            return U


    @classmethod
    def solve_game_value(cls, verbose=True):
        '''
        Solve for the game value.
        Returns a dictionary of the game value as a sympy expression, which will be depenedent on the game parameters.
        '''
        raise NotImplementedError("This runs for an hour and doesnt work. Use mathematica instead.")
        assert cls.solved, "Must solve the equations first"
        
        def vinv(x):
            return -1 - sp.sqrt((4*x - 4)*(-2 + 2*cls.sol_dict[cls.x2]))/(4*x - 4)

        # Define payoff functions
        bluff_payoff = lambda x: cls.sol_dict[cls.x2] - 1/2
        check_payoff = lambda x: x - 1/2
        min_bet_payoff = lambda x: x * (2*L + 1) - L * (cls.sol_dict[cls.c].subs(cls.s, L) + 1) - 1/2
        max_bet_payoff = lambda x: x * (2*U + 1) - U * (cls.sol_dict[cls.c].subs(cls.s, U) + 1) - 1/2
        intermediate_bet_payoff = lambda x: (x * (2*vinv(x) + 1) - vinv(x) * (cls.sol_dict[cls.c].subs(cls.s, vinv(x)) + 1) - 1/2).simplify()

        # Compute total payoffs by integrating over vertical strips
        assumptions = [
        0 <= bU,
        cls.sol_dict[cls.bL] < cls.sol_dict[cls.x2],
        cls.sol_dict[cls.x3] < cls.sol_dict[cls.vL],
        cls.sol_dict[cls.vU] < 1,
        U > L,
        L > 0,
        1 > cls.sol_dict[cls.cU],
        cls.sol_dict[cls.cL] > 0
        ]
        total_bluff_payoff = integrate(bluff_payoff(x), (x, 0, cls.sol_dict[cls.x2])).simplify(assumptions=assumptions)
        total_check_payoff = integrate(check_payoff(x), (x, cls.sol_dict[cls.x2], cls.sol_dict[cls.x3])).simplify(assumptions=assumptions)
        total_min_bet_payoff = integrate(min_bet_payoff(x), (x, cls.sol_dict[cls.x3], cls.sol_dict[cls.v(L)])).simplify(assumptions=assumptions)
        total_intermediate_bet_payoff = integrate(intermediate_bet_payoff(x), (x, cls.sol_dict[cls.v].subs(cls.s, L), cls.sol_dict[cls.v].subs(cls.s, U))).simplify(assumptions=assumptions)
        total_max_bet_payoff = integrate(max_bet_payoff(x), (x, cls.sol_dict[cls.v(U)], 1)).simplify(assumptions=assumptions)

        return total_bluff_payoff + total_check_payoff + total_min_bet_payoff + total_intermediate_bet_payoff + total_max_bet_payoff


    @classmethod
    def game_value_symbolic(cls, **kwargs):
        '''
        Compute the game value using a reduced formula of just r and t.
        Much faster than the numerical integration.
        Formula found using mathematica.
        '''
        r, t = cls.extract_rt(**kwargs)
        numer = 1-t**3-r**3
        denom = 2 * (7 - r**3 - t**3)
        return numer / denom