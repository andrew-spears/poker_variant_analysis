# Appendix: Symbolic Solution (SymPy)

## Purpose
Documents the symbolic derivation of Nash equilibrium using Python/SymPy.

## Key Content

### Overview
Jupyter notebook converted to LaTeX showing step-by-step symbolic solution.

### Transformed Coordinates
- r = L/(1+L): minimum pot odds
- t = 1/(1+U): pot fraction at max bet

### Derivation Steps

**Step 1: Calling Threshold c(s)**
From bettor indifference: c(s) - (1-c(s))s = x₂
Solution: c(s) = (s + x₂)/(s + 1)

**Step 2: Value Function v(s)**
From optimality ODE: -sc'(s) - c(s) + 2v(s) - 1 = 0
Solved for v(s)

**Step 3: Bluffing Function b(s)**
From caller indifference differential equation
Integrated with boundary conditions

**Step 4: Threshold Constraints**
System of 7 equations in 7 unknowns (x₀ through x₅ plus b₀)
Solved symbolically

### Technical Details
- Uses SymPy for symbolic computation
- Imports game_utils.ContinuousPokerVariants for verification
- Extensive use of solve(), diff(), integrate()

### File Format
- Generated from Jupyter notebook via nbconvert
- Contains code cells with syntax highlighting
- LaTeX math output displayed inline

## Dependencies
- Python 3, SymPy, NumPy
- game_utils package
