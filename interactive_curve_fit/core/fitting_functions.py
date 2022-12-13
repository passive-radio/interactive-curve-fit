"""
collection of the fititng functions

- gaussian function 
- polynomial function

"""

import numpy as np

def exp_func(x, *params_guess):
    params = params_guess
    #paramsの長さでフィッティングする関数の数を判別。
    num_func = int(len(params)/3)
    
    #ガウス関数にそれぞれのパラメータを挿入してy_listに追加。
    y_list = []
    for i in range(num_func):
        y = np.zeros_like(x)
        param_range = list(range(3*i,3*(i+1),1))
        ctr = params[int(param_range[0])]
        amp = params[int(param_range[1])]
        wid = params[int(param_range[2])]
        y = y + amp * np.exp( -((x - ctr)/wid)**2)
        y_list.append(y)

    #y_listに入っているすべてのガウス関数を重ね合わせる。
    y_sum = np.zeros_like(x)
    for i in y_list:
        y_sum = y_sum + i

    #最後にバックグラウンドを追加。
    y_sum = y_sum + params[-1]

    return y_sum


def plynomi_func(x, *params_guess, deg):
    # params_guess = [[pos, amp1, pos, amp2],[pos, amp1, pos, amp2],...]
    if type(params_guess)==list:
        params = params_guess
    elif type(params_guess)==tuple:
        params = list(params_guess)
    
    num_func = int((len(params_guess)-1)/(deg*2))
    for i in range(num_func):
        y = np.zeros_like(x)
        for j in range(i, deg):
            # params[2+deg*i + 2*j+1]       amp
            # params[2+deg*i + 2*j]         pos
            # j+1                           deg
            y = y + np.array(params[2*deg*i + 2*j+1] * (x-params[2*deg*i + 2*j]) ** (j+1), dtype="float64")
        y_sum += y

    y_sum += params[-1]
    return y_sum