# Nash Equilibrium Section

## Purpose
Presents the complete closed-form Nash equilibrium solution for LCP.

## Key Content

### Strategy Profile Visualization
Figure shows profiles for various (L,U) pairs:
- (0, 10): Near NLCP
- (0.1, 2): Moderate limits
- (0.3, 1.5): Tighter limits
- (0.5, 1): Near FBCP

### Main Theorem (Theorem 3.1)
Complete closed-form expressions using transformed coordinates:
- r = L/(1+L)
- t = 1/(1+U)

**Threshold values:**
- x₀ = 3t²(t-1)/(r³+t³-7)
- x₁ = (-2r³+3r²+t³-1)/(r³+t³-7)
- x₂ = (r³+t³-1)/(r³+t³-7)
- x₃ = (r³-3r+t³-4)/(r³+t³-7)
- x₄ = (r³+3r²-6r+t³-4)/(r³+t³-7)
- x₅ = (r³+t³+3t²-7)/(r³+t³-7)

**Strategy functions:**
- b(s) = [t³(s+1)³ - (3s+1)] / [(r³+t³-7)(s+1)³]
- c(s) = [r³+t³-1 + s(r³+t³-7)] / [(s+1)(r³+t³-7)]
- v(s) = [r³+t³-1 + (r³+t³-7)(2s²+4s+1)] / [2(r³+t³-7)(s+1)²]

### Key Features
- Both players use pure strategies
- Change of variables (r,t) dramatically simplifies expressions
- Reveals symmetries not obvious in (L,U)

## Images
- `images/LCP_profile_*.png` - Strategy profiles for different parameters

## Dependencies
- Solving LCP section (constraint derivation)
- Appendix for proof verification
