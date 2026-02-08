# Strategic Comparison Section

## Purpose
Proves that LCP strategies converge to FBCP and NLCP at appropriate parameter limits.

## Key Content

### Notation
- S_FB(x,B), C_FB(s,B): FBCP strategies with bet size B
- S_NL(x), C_NL(s): NLCP strategies
- S_LCP(x,L,U), C_LCP(s,L,U): LCP strategies

### FBCP Strategies (Reference)
Bluff: x < B/[(1+2B)(2+B)]
Check: middle range
Value: x > (1+4B+2B²)/[(1+2B)(2+B)]
Call threshold: C_FB(B) = B(3+2B)/[(1+2B)(2+B)]

### NLCP Strategies (Reference)
Bluff: x < 1/7, bet b_NL^(-1)(x)
Check: 1/7 < x < 4/7
Value: x > 4/7, bet v_NL^(-1)(x)
Call: C_NL(s) = 1 - 6/[7(s+1)]

### Convergence to FBCP
As L, U → B:
- Intermediate regions collapse (x₀=x₁, x₄=x₅)
- Only fixed bet B remains
- Thresholds match FBCP exactly
- x₂|_{B,B} = B/[(1+2B)(2+B)]

### Convergence to NLCP
As L → 0, U → ∞:
- Boundary regions collapse (x₀→0, x₅→1)
- x₁ = x₂ → 1/7
- x₃ = x₄ → 4/7
- b(s) → 3s+1/[7(s+1)³]
- v(s) → 1 - 3/[7(s+1)²]
- c(s) → 1 - 6/[7(1+s)]

## Mathematical Method
Direct substitution of limits into rational strategy functions.

## Dependencies
- Nash equilibrium section (LCP formulas)
- Introduction (FBCP/NLCP reference strategies)
