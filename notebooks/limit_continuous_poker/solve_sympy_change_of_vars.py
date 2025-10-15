# %% [markdown]
"""
# Symbolic Solution for Limit Continuous Poker (LCP)

This notebook solves for the Nash equilibrium of LCP using the transformed coordinates:
- r = L/(1+L)  (minimum pot odds)
- t = 1/(1+U)  (pot fraction at max bet)

The solution provides closed-form expressions for all strategic components:
- Hand strength thresholds: x0, x1, x2, x3, x4, x5
- Calling threshold function: c(s)
- Value betting function: v(s)
- Bluffing function: b(s)
- Game value: V(r, t)
"""
import sympy as sp
from sympy import symbols, Function, Eq, solve, diff, integrate, factor, lambdify
from typing import Dict
from dataclasses import dataclass
import game_utils.ContinuousPokerVariants.ContinuousPokerUtils as poker_utils

# %% 
"""
## Symbolic Variable Definitions
We define all symbolic variables and functions used throughout the derivation.
"""
# Transformed parameters (r, t) and bet size s
r, t, s, x = symbols('r t s x')

# Original parameters in terms of r, t
L_expr = r / (1 - r)  # Minimum bet size: L = r/(1-r)
U_expr = (1 - t) / t   # Maximum bet size: U = (1-t)/t

# Hand strength thresholds
x0, x1, x2, x3, x4, x5 = symbols('x0 x1 x2 x3 x4 x5')

# Strategy functions (declared as symbolic functions)
c_func = Function('c')  # Calling threshold function
v_func = Function('v')  # Value betting function
b_func = Function('b')  # Bluffing function

# Integration constant for bluffing function
b0 = symbols('b0')

# %% [markdown]
"""
## Step 1: Derive Calling Threshold c(s)

From bettor indifference at the marginal bluffing hand x2:
The bettor must be indifferent between bluffing any size s and checking.

EV(bluff s | x2) = EV(check | x2)
c(s) - (1-c(s))·s = x2
"""
def derive_calling_threshold() -> sp.Expr:
    """
    Derive the calling threshold c(s) from bettor indifference.

    At the marginal bluffing hand x2, the bettor must be indifferent
    between bluffing any size s and checking.

    Returns:
        Symbolic expression for c(s) in terms of x2 and s
    """
    # Bettor indifference: EV(bluff s | x2) = EV(check | x2)
    # c(s) - (1-c(s))*s = x2
    bettor_indiff_eq = Eq(c_func(s) - (1 - c_func(s)) * s, x2)

    c_solution = solve(bettor_indiff_eq, c_func(s))[0]
    return c_solution

c_expr = derive_calling_threshold()
print("✓ Derived c(s):")
display(Eq(c_func(s), c_expr))

# %% [markdown]
"""
## Step 2: Derive Value Betting Function v(s)

From first-order optimality for value bets:
The bettor with hand v(s) must be indifferent about bet size,
meaning the derivative of expected value w.r.t. s equals zero.

Expected value for value bet: (x - c(s))·(1+s) - (1-x)·s + c(s)
Taking derivative w.r.t. s: -s·c'(s) - c(s) + 2·v(s) - 1 = 0
"""
def derive_value_function(c_expr: sp.Expr) -> sp.Expr:
    """
    Derive the value betting function v(s) from first-order optimality.

    The bettor with hand v(s) must be indifferent about bet size,
    meaning the derivative of expected value w.r.t. s equals zero.

    Args:
        c_expr: Calling threshold expression c(s)

    Returns:
        Symbolic expression for v(s)
    """
    # Expected value for value bet: (x - c(s))*(1+s) - (1-x)*s + c(s)
    # Taking derivative w.r.t. s and using chain rule on c(s):
    # -s*c'(s) - c(s) + 2*v(s) - 1 = 0
    optimality_ode = Eq(-s * diff(c_expr, s) - c_expr + 2 * v_func(s) - 1, 0)

    v_solution = solve(optimality_ode, v_func(s))[0]
    return v_solution

v_expr = derive_value_function(c_expr)
print("✓ Derived v(s):")
display(Eq(v_func(s), v_expr))

# %% [markdown]
"""
## Step 3: Derive Bluffing Function b(s)

From caller indifference at threshold c(s):
The caller must be indifferent, meaning the ratio of bluffing to
value betting density matches the pot odds.

Caller indifference: |b'(s)| · (1+s) = |v'(s)| · s
Since b is decreasing and v is increasing: -b'(s)·(1+s) = v'(s)·s
"""
def derive_bluffing_function(v_expr: sp.Expr) -> sp.Expr:
    """
    Derive the bluffing function b(s) from caller indifference.

    The caller must be indifferent at threshold c(s), meaning the ratio
    of bluffing to value betting density matches the pot odds.

    Args:
        v_expr: Value betting function v(s)

    Returns:
        Symbolic expression for b(s) with integration constant b0
    """
    # Caller indifference: |b'(s)| * (1+s) = |v'(s)| * s
    # Since b is decreasing and v is increasing: -b'(s)*(1+s) = v'(s)*s
    caller_indiff_ode = Eq(diff(b_func(s), s) * (1 + s) + diff(v_expr, s) * s, 0)

    # Solve ODE (produces solution with integration constant C1)
    b_solution = sp.dsolve(caller_indiff_ode, b_func(s))

    # Replace generic constant C1 with our named constant b0
    b_solution_expr = b_solution.rhs.subs("C1", b0)

    return b_solution_expr

b_expr = derive_bluffing_function(v_expr)
print("✓ Derived b(s):")
display(Eq(b_func(s), b_expr))

# %% [markdown]
"""
## Step 4: Solve for Hand Strength Thresholds

We now solve for the six threshold values x0-x5 using:
1. Caller indifference at boundaries L and U
2. Bettor indifference at x3
3. Continuity conditions at boundaries
"""
print("Solving for hand strength thresholds...")

# Evaluate functions at boundaries
c_at_L = c_expr.subs(s, L_expr)
v_at_L = v_expr.subs(s, L_expr)
v_at_U = v_expr.subs(s, U_expr)

# System of equations for thresholds
equations = [
    Eq(x2 - x1 - r * (x4 - x3), 0),          # Caller indifference at L
    Eq(x0 - (1 - x5) * (1 - t), 0),          # Caller indifference at U
    Eq(x3 - (1 + c_at_L) / 2, 0),            # Bettor indifference at x3
    Eq(v_at_L, x4),                          # Continuity: v(L) = x4
    Eq(v_at_U, x5),                          # Continuity: v(U) = x5
]

# Solve for x0, x1, x3, x4, x5 in terms of x2
threshold_solution = sp.linsolve(equations, (x0, x1, x3, x4, x5))
threshold_tuple = list(threshold_solution)[0]

# Build initial threshold dictionary
thresholds = {
    var: expr
    for var, expr in zip([x0, x1, x3, x4, x5], threshold_tuple)
}

print("✓ Solved for x0, x1, x3, x4, x5 in terms of x2")
print("\nThresholds (in terms of x2):")
for name in ['x0', 'x1', 'x3', 'x4', 'x5']:
    sym = symbols(name)
    display(Eq(sym, thresholds[sym]))

# %% [markdown]
"""
## Step 5: Solve for x2 and b0

Using boundary conditions for the bluffing function:
- b(U) = x0
- b(L) = x1
"""
b_at_L = b_expr.subs(s, L_expr)
b_at_U = b_expr.subs(s, U_expr)

# Boundary conditions for bluffing function
boundary_equations = [
    Eq(b_at_U, thresholds[x0]),  # b(U) = x0
    Eq(b_at_L, thresholds[x1]),  # b(L) = x1
]

b0_x2_solution = sp.linsolve(boundary_equations, (b0, x2))
b0_val, x2_val = list(b0_x2_solution)[0]

print("✓ Solved for x2 and b0:")
display(Eq(x2, x2_val))
display(Eq(b0, b0_val))

# %% 
"""
## Step 6: Substitute and Simplify

Substitute x2 back into all expressions and simplify to get the final solution.
"""

print("Simplifying expressions...")
thresholds[x2] = x2_val
thresholds[b0] = b0_val

# Substitute x2 into other thresholds
for key in [x0, x1, x3, x4, x5]:
    thresholds[key] = thresholds[key].subs(x2, x2_val).simplify()

# Simplify strategy functions
c_expr_final = c_expr.subs(x2, x2_val).simplify()
v_expr_final = v_expr.subs(x2, x2_val).simplify()
b_expr_final = b_expr.subs(b0, b0_val).subs(x2, x2_val).simplify().factor()

print("✓ Simplified all expressions")

# %%
"""
## Step 7: Get v inverse function for convenience
"""
def derive_inverse_value_function(v_expr):
    # found analytically
    v_inv_expr = -1 - sp.sqrt( (4*x-4) * (-2 + 2*x2) ) / (4*x-4)

    # check that it really inverts v
    assert x == v_expr.subs(s, v_inv_expr).simplify()
    return v_inv_expr.subs(x2, x2_val).simplify()

v_inv_expr = derive_inverse_value_function(v_expr)

# %% [markdown]
"""
## Complete Solution

Below is the complete Nash equilibrium solution for Limit Continuous Poker.
"""

# %% Display complete solution
@dataclass
class LCPSolution:
    """
    Complete symbolic solution for Limit Continuous Poker.

    Attributes:
        thresholds: Dictionary mapping threshold symbols (x0-x5) to expressions
        c_expr: Calling threshold function c(s)
        v_expr: Value betting function v(s)
        b_expr: Bluffing function b(s)
    """
    thresholds: Dict[sp.Symbol, sp.Expr]
    c_expr: sp.Expr
    v_expr: sp.Expr
    b_expr: sp.Expr

    def display(self):
        """Display the solution in readable format."""
        print("=" * 70)
        print("LIMIT CONTINUOUS POKER - Nash Equilibrium Solution")
        print("=" * 70)
        print()

        print("Hand Strength Thresholds:")
        print("-" * 70)
        for name in ['x0', 'x1', 'x2', 'x3', 'x4', 'x5']:
            sym = symbols(name)
            expr = self.thresholds[sym]
            display(Eq(sym, expr))
        print()

        print("Strategy Functions:")
        print("-" * 70)
        display(Eq(c_func(s), self.c_expr))
        display(Eq(v_func(s), self.v_expr))
        display(Eq(b_func(s), self.b_expr))
        print()

    def to_latex(self) -> Dict[str, str]:
        """Convert solution to LaTeX format."""
        latex_dict = {}

        for sym, expr in self.thresholds.items():
            latex_dict[str(sym)] = sp.latex(Eq(sym, expr))

        latex_dict['c(s)'] = sp.latex(Eq(c_func(s), self.c_expr))
        latex_dict['v(s)'] = sp.latex(Eq(v_func(s), self.v_expr))
        latex_dict['b(s)'] = sp.latex(Eq(b_func(s), self.b_expr))

        return latex_dict

solution = LCPSolution(
    thresholds=thresholds,
    c_expr=c_expr_final,
    v_expr=v_expr_final,
    b_expr=b_expr_final
)

solution.display()

# %% Plot result
# Strategy function implementations using the symbolic solution

def _convert_params(**kwargs):
    """
    Convert between (L, U) and (r, t) parameterizations.

    Returns:
        Tuple of (r_val, t_val) for substitution into symbolic expressions
    """
    if 'L' in kwargs and 'U' in kwargs:
        L_val = kwargs['L']
        U_val = kwargs['U']
        r_val = L_val / (1 + L_val)
        t_val = 1 / (1 + U_val)
        return r_val, t_val
    elif 'r' in kwargs and 't' in kwargs:
        return kwargs['r'], kwargs['t']
    else:
        raise ValueError("Must provide either (L, U) or (r, t) parameters")

def call_threshold(s_val, **kwargs):
    """
    Compute the calling threshold for a bet of size s_val.

    Args:
        s_val: Bet size
        **kwargs: Either L and U, or r and t

    Returns:
        Calling threshold c(s_val)
    """
    r_val, t_val = _convert_params(**kwargs)

    c_numeric = lambdify(s, solution.c_expr.subs({r: r_val, t: t_val}))
    return float(c_numeric(s_val))

def bluff_threshold(**kwargs):
    """
    Return the marginal bluffing threshold x2.

    Args:
        **kwargs: Either L and U, or r and t

    Returns:
        Threshold value x2
    """
    r_val, t_val = _convert_params(**kwargs)

    x2_expr = solution.thresholds[x2].subs({r: r_val, t: t_val})
    return float(x2_expr)

def value_threshold(**kwargs):
    """
    Return the marginal value betting threshold x3.

    Args:
        **kwargs: Either L and U, or r and t

    Returns:
        Threshold value x3
    """
    r_val, t_val = _convert_params(**kwargs)

    x3_expr = solution.thresholds[x3].subs({r: r_val, t: t_val})
    return float(x3_expr)

def bluff_size(x_val, **kwargs):
    """
    Compute the bet size for a bluffing hand of strength x_val.

    Inverts b(s) to find the bet size s such that b(s) = x_val.

    Args:
        x_val: Hand strength in [x0, x2]
        **kwargs: Either L and U, or r and t

    Returns:
        Bet size s for bluffing with hand x_val
    """
    r_val, t_val = _convert_params(**kwargs)

    # Compute L and U from r and t
    L_val = r_val / (1 - r_val)
    U_val = (1 - t_val) / t_val

    # Get thresholds
    x0_val = solution.thresholds[x0].subs({r: r_val, t: t_val})
    x1_val = solution.thresholds[x1].subs({r: r_val, t: t_val})
    x2_val = solution.thresholds[x2].subs({r: r_val, t: t_val})
    b0_val = solution.thresholds[b0].subs({r: r_val, t: t_val})

    if x_val < x0_val:
        return U_val
    elif x_val < x1_val:
        # Invert b(s) = x_val by solving numerically
        from scipy.optimize import brentq

        # Substitute parameters into bluffing expression
        b_substituted = solution.b_expr.subs({
            r: r_val,
            t: t_val,
            x2: x2_val,
            b0: b0_val
        })

        # Create numerical function
        b_numeric = lambdify(s, b_substituted)

        # b is monotone decreasing, so we can use root finding
        try:
            result = brentq(lambda s_test: b_numeric(s_test) - x_val, L_val, U_val)
            return result
        except:
            return None
    else:
        return L_val

def value_size(x_val, **kwargs):
    """
    Compute the bet size for a value betting hand of strength x_val.

    Inverts v(s) to find the bet size s such that v(s) = x_val.

    Args:
        x_val: Hand strength in [x3, 1]
        **kwargs: Either L and U, or r and t

    Returns:
        Bet size s for value betting with hand x_val
    """
    r_val, t_val = _convert_params(**kwargs)

    # Compute L and U from r and t
    L_val = r_val / (1 - r_val)
    U_val = (1 - t_val) / t_val

    # Get thresholds
    x4_val = solution.thresholds[x4].subs({r: r_val, t: t_val})
    x5_val = solution.thresholds[x5].subs({r: r_val, t: t_val})

    if x_val < x4_val:
        return L_val
    elif x_val < x5_val:
        vinv_numeric = lambdify(x, v_inv_expr.subs({r: r_val, t: t_val}))
        return float(vinv_numeric(x_val))
    else:
        return U_val

# Plot the strategies for a specific L and U
poker_utils.generate_strategy_plot(
    bluff_threshold,
    bluff_size,
    value_threshold,
    value_size,
    call_threshold,
    L=0, U=10
)

# %%
"""
## LaTeX Output

Generate LaTeX code for the solution equations.
"""

# %% Print LaTeX format
print("=" * 70)
print("LaTeX Format:")
print("=" * 70)
latex_output = solution.to_latex()
for key, latex_str in latex_output.items():
    print(f"\n{key}:")
    print(latex_str)

# %%
"""
## Game Value Computation

Computing the game value requires integrating expected payoffs over all hand regions.
"""
def compute_game_value(solution: LCPSolution) -> sp.Expr:
    """
    Compute the game value V(r,t) by integrating expected payoffs.

    The game value is computed by integrating the bettor's expected payoff
    over all hand strengths, accounting for different strategic regions.

    Args:
        solution: LCPSolution object

    Returns:
        Symbolic expression for partial game value
    """

    # Define payoff functions for each region
    bluff_payoff = solution.thresholds[x2] - sp.Rational(1, 2)
    check_payoff = x - sp.Rational(1, 2)
    min_bet_payoff = (x * (2*L_expr + 1) - L_expr * (solution.c_expr.subs(s, L_expr) + 1) - sp.Rational(1, 2)).simplify()
    max_bet_payoff = (x * (2*U_expr + 1) - U_expr * (solution.c_expr.subs(s, U_expr) + 1) - sp.Rational(1, 2)).simplify()
    
    # this one needs extra simplification:
    intermediate_bet_payoff = (x * (2*v_inv_expr + 1) - v_inv_expr * (solution.c_expr.subs(s, v_inv_expr) + 1) - sp.Rational(1, 2)).simplify()
    q = sp.Symbol('q')
    q_expr = (x-1)/(r**3+t**3-7)
    intermediate_bet_payoff = intermediate_bet_payoff.subs(q_expr, q).collect(q).collect(x).subs(q, q_expr)


    # Integrate over bluffing region
    bluff_integral = integrate(
        bluff_payoff,
        (x, 0, thresholds[x2])
    ).simplify()

    # Integrate over checking region
    check_integral = integrate(
        check_payoff,
        (x, thresholds[x2], thresholds[x3])
    ).simplify()
    
    # Integrate over min bet region
    min_bet_integral = integrate(
        min_bet_payoff,
        (x, thresholds[x3], thresholds[x4])
    ).simplify()

    # Integrate over max bet region
    max_bet_integral = integrate(
        max_bet_payoff,
        (x, thresholds[x5], 1)
    ).simplify()

    # Integrate over intermediate bet region - done by hand
    D = r**3 + t**3 - 7
    a = (r**3 + 3*r**2 - 6*r + t**3 - 4)/D
    b = (r**3 + t**3 + 3*t**2 - 7)/D
    intermediate_bet_integral = (sp.Rational(3,2) - 6/D)* (b-a) - sp.Rational(1,2)*(b**2 - a**2) \
         - 24*(r**(sp.Rational(3,2)) + t**(sp.Rational(3,2)) - 7)*(t**3 - (r-1)**3)/D**3

    game_value = bluff_integral + check_integral + min_bet_integral + max_bet_integral + intermediate_bet_integral
    known_form = (1-r**3-t**3)/(14-2*r**3-2*t**3)
    # assert (known_form - game_value).simplify() == 0

    return game_value.simplify()

# Uncomment to compute partial game value
game_value = compute_game_value(solution)
# display(Eq(symbols('V_partial'), partial_value))

# %%
