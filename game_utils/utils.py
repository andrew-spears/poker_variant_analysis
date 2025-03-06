import numpy as np
import matplotlib.pyplot as plt
from game_utils.InfoSet import InfoSet
import pandas as pd
from game_utils.Strategy import MixedStrategy

def cond_print(s, cond):
    if cond:
        print(s)

def multiline_print(s):
    '''
    s is any iterable. split the iterable by \n and print each element.
    '''
    
    if isinstance(s, dict):
        for k, i in s.items():
            print(f"{k} : {i}")
        return
    for line in s:
        print(line)

def normalize(vector):
    total = sum(vector)
    if total == 0:
        return np.ones(len(vector)) / len(vector)
    return vector / total

def if_not_none(var, if_none):
    return var if var is not None else if_none

def heatmap(data, x_label=None, x_ticks=None, y_label=None, y_ticks=None, z_ticks=None, title=None, figsize=(10, 5)):
    '''
    data: 2D numpy array or pandas DataFrame
    x_label: label for the x-axis
    x_ticks: list of labels for the x-axis
    y_label: label for the y-axis
    y_ticks: list of labels for the y-axis
    figsize: tuple of the figure size
    '''
    if isinstance(data, pd.DataFrame):
        x_ticks = if_not_none(x_ticks, data.columns)
        y_ticks = if_not_none(y_ticks, data.index)
        data = data.to_numpy()

    plt.figure(figsize=figsize)
    im = plt.imshow(data, cmap='hot', aspect='auto')

    # Annotate each cell with its value
    for (i, j), val in np.ndenumerate(data):
        if val > 0.5:
            plt.text(j, i, f"{val:.2f}", ha='center', va='center', color="black")
        else:
            plt.text(j, i, f"{val:.2f}", ha='center', va='center', color="white")

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if x_ticks is not None:
        plt.xticks(range(len(x_ticks)), x_ticks, rotation=90)
    if y_ticks is not None:
        plt.yticks(range(len(y_ticks)), y_ticks)

    if z_ticks is not None:
        tick_values = np.linspace(0, 1, len(z_ticks))
        cbar = plt.colorbar(im, ticks=tick_values)
        cbar.ax.set_yticklabels(z_ticks)  # Label the ticks
    if title is not None:
        plt.title(title)
    plt.show()

def binaryStrategyArr(strategy):
    '''
    strategy: dict which maps InfoSets to lists of exactly 2 probabilities.
    card is the card of the player who is acting.
    history is the sequence of actions that have been taken as a string of characters.
    return:
        a 2D numpy array where the rows are the types of the player and the columns are the histories.
        a list of the distinct types of the player (rows)
        a list of the distinct histories (columns)
    '''
    types_distinct = sorted(list({infoSet.type for infoSet in strategy.keys()}))
    n = len(types_distinct)
    histories_distinct = sorted(list({infoSet.history for infoSet in strategy.keys()}), key=lambda x: x[::-1])
    m = len(histories_distinct)
    strategy_arr = np.zeros((n, m))

    for i, history in enumerate(histories_distinct):
        for type in range(n):
            infoSet = InfoSet(type, history)
            if infoSet in strategy:
                freqs = strategy[infoSet]
                aggressive_freq = freqs[1]
                strategy_arr[type, i] = aggressive_freq
    return strategy_arr, types_distinct, histories_distinct

def binaryStrategyHeatmap(strategy, figsize=(10, 5), transpose=False, title=None):
    '''
    strategy: dict which maps InfoSets to lists of exactly 2 probabilities.
    card is the card of the player who is acting.
    history is the sequence of actions that have been taken as a string of characters.
    '''
    strategy_arr, types_distinct, histories_distinct = binaryStrategyArr(strategy)
    if transpose:
        strategy_arr = strategy_arr.T
        heatmap(
            strategy_arr, 
            x_label="Card", 
            x_ticks=types_distinct, 
            y_label="History", 
            y_ticks=histories_distinct, 
            figsize=figsize, 
            z_ticks=["Fold/Check", "Call/Bet"],
            title=title
        )
    else:
        heatmap(
            strategy_arr, 
            x_label="History", 
            x_ticks=histories_distinct, 
            y_label="Card", 
            y_ticks=types_distinct, 
            figsize=figsize, 
            z_ticks=["Fold/Check", "Call/Bet"],
            title=title
        )
