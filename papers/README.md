# Papers

This directory contains research papers and their associated LaTeX source files.

## Limit Continuous Poker

**Location:** [limit_continuous_poker/](limit_continuous_poker/)

A game-theoretic analysis of Limit Continuous Poker (LCP), a variant of Von Neumann poker with bounded bet sizes. This paper derives the Nash equilibrium strategy profile and game value formula, revealing surprising mathematical structure and strategic insights.

**Key Results:**
- Closed-form Nash equilibrium with elegant structure
- Game value formula with remarkable symmetry: V(r,t) = V(t,r)
- Counterintuitive strategic effects of changing bet limits
- Smooth convergence to classical variants (FBCP and NLCP)

**Building the Paper:**

```bash
cd limit_continuous_poker/main
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Or simply view the pre-compiled PDF: [main/main.pdf](limit_continuous_poker/main/main.pdf)

**Associated Notebooks:**
- See [../../notebooks/limit_continuous_poker/](../../notebooks/limit_continuous_poker/) for numerical analysis and visualizations

## Other LaTeX

**Location:** [other_latex/](other_latex/)

Contains LaTeX source for other poker-related documents and analyses.
