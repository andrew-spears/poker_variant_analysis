from scipy.optimize import linprog
import numpy as np

def solve_normal_zero_sum(payoffs, player=0):
    '''
    Solves a normal-form zero-sum game using linear programming.
    Parameters:
    payoffs (numpy.ndarray): A 2D array representing the payoff matrix for player 1. 
                             The rows correspond to player 1's strategies, and the columns 
                             correspond to player 2's strategies.
    player: 0 for row chooser, 1 for column chooser.
    Returns:
    tuple: A tuple containing:
        - numpy.ndarray: The optimal mixed strategy for player 1.
        - float: The value of the game.
    Raises:
    ValueError: If the linear programming solver fails to find a solution.
    '''
    if player == 1:
        payoffs = -payoffs.T
    # decision vector is [[x], [v]] where x is a column vector of p1 frequencies 
    # and v is the game value
    # objective function is to maximize the game value v
    # minimize -v = [0, ..., 0, -1] @ [[x], [v]]
    c = np.zeros(payoffs.shape[0] + 1)
    c[-1] = -1

    # constraint of the form A^Tx >= v
    # rearranges into A_ub [[x], [v]] <= 0
    # A_ub is the block matrix [-A^T, 1]
    A_ub = np.concat([-payoffs.T, np.ones((payoffs.shape[0], 1))], axis=1)
    b_ub = np.zeros(payoffs.shape[1])

    # constraint on probabilities sum to 1
    A_eq = np.concat([np.ones((1, payoffs.shape[0])), np.zeros((1, 1))], axis=1)
    b_eq = np.array([1])

    # bounds on x_i >= 0
    bounds = [(0, None) for _ in range(payoffs.shape[0])] + [(None, None)]

    res = linprog(c=c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds)

    if res.success:
        return res.x[:-1], res.x[-1]
    else:
        print("ERROR IN LINEAR PROGRAMMING")
        print(res)
        raise ValueError("Linear programming failed to find a solution.")