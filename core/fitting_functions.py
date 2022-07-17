"""
collection of the fititng functions

- gaussian function 
- polynomial function

"""

import numpy as np

def gaussian_func(x, *params_guess):
    
    params = params_guess
    # calculate the number of gaussian functions by params length
    num_func = int(len(params)/3)
    # overlap all hte gaussian functions into one sequence.
    y_total = np.zeros_like(x)
    
    for i in range(num_func):
        y = np.zeros_like(x)
        param_range = list(range(3*i,3*(i+1),1))
        ctr = params[int(param_range[0])]
        amp = params[int(param_range[1])]
        wid = params[int(param_range[2])]
        y += amp * np.exp(-1*((x - ctr)/wid)**2)
        y_total += y

    # add init backgroud to y_total
    y_total += params[-1]

    return y_total

class Polynomial:
    def __init__(self, deg:int=3):
        self.deg = deg
        pass
    def polynomial_func(self, x, *params_guess):
        
        if type(params_guess)==list:
            params = params_guess
        elif type(params_guess)==tuple:
            params = list(params_guess)

        y_total = np.zeros_like(x)
        num_func = int((len(params_guess)-1)/(self.deg*2))

        for i in range(num_func):
            y = np.zeros_like(x)
            for j in range(i, self.deg):
                # params[2+deg*i + 2*j+1]       amp
                # params[2+deg*i + 2*j]         pos
                # j+1                           deg
                y += np.array(params[2*self.deg*i + 2*j+1] * (x-params[2*self.deg*i + 2*j]) ** (j+1), dtype="float64")
            y_total += y

        y_total += params[-1]
        return y_total

def polynomial_func(x, *params_guess, deg):
    # params_guess = [[pos, amp1, pos, amp2],[pos, amp1, pos, amp2],...]
    if type(params_guess)==list:
        params = params_guess
    elif type(params_guess)==tuple:
        params = list(params_guess)
    
    y_total = np.zeros_like(x)
    num_func = int((len(params_guess)-1)/(deg*2))
    
    for i in range(num_func):
        y = np.zeros_like(x)
        for j in range(i, deg):
            # params[2+deg*i + 2*j+1]       amp
            # params[2+deg*i + 2*j]         pos
            # j+1                           deg
            y += np.array(params[2*deg*i + 2*j+1] * (x-params[2*deg*i + 2*j]) ** (j+1), dtype="float64")
        y_total += y

    y_total += params[-1]
    return y_total