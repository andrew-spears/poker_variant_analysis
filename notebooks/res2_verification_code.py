
import numpy as np
import sympy as sp
import pandas as pd

# Define symbols
x, L, U = sp.symbols('x L U', real=True, positive=True)
x2, s = sp.symbols('x2 s', real=True)

# Define c(s) and x2(U)
c_expr = (x2 - s)/(1 + s)
x2_expr = 1 - 1/(1 + U)

# Derivatives
dc_ds_expr = sp.diff(c_expr, s)
dc_dx2_expr = sp.diff(c_expr, x2)
dx2du_expr = sp.diff(x2_expr, U)

# EVU expression
c = sp.Function('c')(s)
EVU = (1/2)*c + (x - c)*(U + 1/2) + (1 - x)*(-U - 1/2)

# Derivatives of EVU
dEVU_dc = sp.diff(EVU, c)
dEVU_dU = sp.diff(EVU, U)

# Substitute symbolic derivatives
c_expr_at_U = c_expr.subs({s: U, x2: x2_expr})
dc_ds_at_U = dc_ds_expr.subs({s: U, x2: x2_expr})

# Final expression
res_expr = dEVU_dc * (dc_dx2_expr * dx2du_expr + dc_ds_at_U) + dEVU_dU
res_expr_subbed = res_expr.subs({c: c_expr_at_U}).simplify()

# Turn into numerical function
res_func = sp.lambdify((x, L, U), res_expr_subbed, modules='numpy')

# Generate sample points
samples = []
for _ in range(1000):
    L_val = np.random.uniform(0.01, 1.0)
    U_val = np.random.uniform(L_val + 0.01, L_val + 2.0)
    x5_val = 1 - 2 / (1 + U_val)**2  # conservative lower bound
    x_val = np.random.uniform(x5_val + 0.001, 0.999)
    samples.append((x_val, L_val, U_val))

# Evaluate numerically
numeric_results = []
for xv, Lv, Uv in samples:
    try:
        val = float(res_func(xv, Lv, Uv))
        numeric_results.append(val)
    except:
        numeric_results.append(np.nan)

# Combine into dataframe
df = pd.DataFrame(samples, columns=["x", "L", "U"])
df["res2_final"] = numeric_results

# Save as CSV
df.to_csv("res2_samples.csv", index=False)
