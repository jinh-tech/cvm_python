"""Contains utility functions"""
from random import random

def coin_toss(p: float) -> bool:
    """simulates a coin toss. Returns True with a probability of 'p'
    p:float - probability with which the function should return True. p should ideally be in the range [0,1]. 
    """
    return random() < p