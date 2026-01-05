---
title: Limit Continuous Poker
date: 2025-09-03 20:00:00 -0500
categories: [game theory]
tags: [game theory, poker, nash equilibrium]
math: true
---

## Background: Von Neumann Poker

Real poker involves many strategic dimensions—position, hand types, pot odds, and countless decision points—that make formal analysis difficult. Simplified poker models address this by abstracting away details while preserving core strategic elements. By isolating specific phenomena like bluffing, value betting, and bet sizing, we can derive exact Nash equilibria and develop formal understanding of poker strategy.

One fundamental simplified model is **Continuous Poker**, also called **Von Neumann Poker** (introduced by John von Neumann). The setup is minimal:

- Two players: a bettor and a caller
- Each gets a hand strength uniformly distributed between 0 and 1 (no card suits, just a number)
- One betting round
- The bettor can either check (no bet) or bet a **fixed amount B**
- The caller either calls (matches the bet) or folds (gives up the pot)
- Highest hand strength wins

In the classical **Fixed-Bet Continuous Poker** (FBCP), the bettor's bet size is a parameter $B$ that defines the game. This constraint is what makes the game tractable: for any given $B$, there's a unique Nash equilibrium (up to indifference).

In equilibrium, the bettor divides their hands into three groups:

1. **Bluffing hands** (weak hands): Hands below threshold $\frac{B}{(1+2B)(2+B)}$ that bet despite being weak
2. **Checking hands** (medium hands): Hands in the middle that just check
3. **Value betting hands** (strong hands): Hands above threshold $\frac{1 + 4B + 2B^2}{(1+2B)(2+B)}$ that bet because they're strong

The caller responds with a simple threshold: call if your hand strength exceeds $\frac{B(3 +2B)}{(1+2B)(2+B)}$.

The bettor's value depends on $B$ and is maximized when $B = 1$ (betting exactly the pot size). Intuitively, betting too small reduces wins when the opponent folds; betting too large makes the opponent fold too often, limiting profit. The value is:
$$V_{FB}(B) = \frac{B}{2(1+2B)(2+B)}$$

This closed-form expression shows how bet size affects the bettor's advantage.

### The No-Limit Alternative

What if we take off the bet-size constraint entirely? This gives us **No-Limit Continuous Poker** (NLCP), where the bettor can choose any positive bet size after seeing their hand.

The Nash equilibrium is still solvable, despite infinite bet sizes. In equilibrium, the bettor bets the same size with both strongest and weakest hands, while making smaller bets with medium-strength hands. This seems to reveal too much information (only two hand strengths per bet size), but it is optimal because the caller's threshold is calibrated so that different bet sizes with different hands balance out.

The strategy works like this:

- For any bet size $s$ the bettor might make, there are exactly two hand strengths that bet:
  - **Bluff hands**: $x = \frac{3s+1}{7(s+1)^3}$ (very weak)
  - **Value hands**: $x = 1 - \frac{3}{7(s+1)^2}$ (very strong)
- The caller's response is a single threshold: call with hands $y > 1 - \frac{6}{7(s+1)}$

NLCP is always more profitable for the bettor than FBCP with any fixed bet size. The value is:
$$V_{NL} = \frac{1}{14}$$

This exceeds any $V_{FB}(B)$, which makes sense: the bettor adapts bet size to their hand, strictly improving over a fixed bet.

### Bridging the Extremes

These two models represent endpoints on a spectrum. FBCP fixes the bet size; NLCP allows any positive bet. A natural intermediate case is to let the bettor choose a bet size within bounds: anything between $L$ (lower) and $U$ (upper). This is more realistic—in structured poker games, players often have restricted bet sizes before going all-in.

**Limit Continuous Poker** (LCP) generalizes both models:

- When $L = U = B$, LCP reduces to FBCP
- When $U \to \infty$ (with $L$ small), LCP approaches NLCP
- For intermediate $(L, U)$, LCP is genuinely new

By analyzing LCP across all $(L, U)$ pairs, we can understand how betting flexibility affects optimal strategy and game value. How much does flexibility gain for the bettor? How does the caller adjust to variable bets? These questions have elegant answers that we explore in this paper.

## References

[1] Ferguson, C., & Ferguson, T. (2003). On the Borel and von Neumann Poker Models. _Game Theory and Applications_, 9, 2.

[2] Chen, B., & Ankenman, J. (2006). _The Mathematics of Poker_. Conjelco.
