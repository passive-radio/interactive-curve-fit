import csv

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib.cm as cm


class Fitter(object):
    """
    ## init params
    - data: spectrum data
    - ci: confidential interval (unit: sigma, default: 2*sigma)
    - num_peaks: number of the peaks you want to fit (default: None)
    """
    
    def __init__(self, data, guess, ci=2, num_peaks=None) -> None:
        if type(num_peaks) == int:
            self.num_peaks = num_peaks
        else:
            self.num_peaks = None
        self.data = data
        self.guess = guess
        self.ci = ci
        
    def run(self, method='gauss', ci:int=2):
        if method == 'gauss':
            popt, pcov = self.gauss_func_fit()
        elif method == 'polynomial':
            popt, pcov = self.polynomial_func_fit()
            
        peakx = self.peakxs
        peaky = self.peakys
        bandwidth = self.bandwidth_list(ci)
        bg = self.background
        
        peaks = []
        for i in range(self.get_num_peaks):
            peaks.append([peakx[i], peaky[i], bandwidth[i], bg])
        
        peaks = pd.DataFrame(peaks, columns=["x", "y", f"bandwidth(ci: {ci}sigma)", "background"])
        self.peaks = peaks
        return True
    
    def gauss_func_fit(self):
        
        def exp_func(x=self.data.x, *params_guess):
            params = params_guess
            #paramsの長さでフィッティングする関数の数を判別。
            num_func = int(len(params)/3)
            self.num_peaks = num_func
            
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
        
        guess_list = []
        for content in self.guess[:-1]:
            guess_list.extend(content)
        guess_list.append(self.guess[-1])
        
        popt, pcov = curve_fit(exp_func, self.data.x, self.data.y, p0=guess_list)
        self.popt = popt
        self.pcov = pcov
        return popt, pcov
    
    def polynomial_func_fit(self, *params, deg, mode="g"):
        
        x = self.data.x
        params_raw = params
        params_guess = params[0:-1]
        
        num_func = int(len(params_guess)/2)
        self.num_peaks = num_func
        params_new = []
        for i in range(num_func):
            for _ in range(deg):
                params_new.append(params_guess[2*i])
                params_new.append(params_guess[2*i+1])
        params_new.append(params_raw[-1])

        def plynomi_func(x=x, *params_guess):
            # params_guess = [[pos, amp1, pos, amp2],[pos, amp1, pos, amp2],...]
            if type(params_guess)==list:
                params = params_guess
            elif type(params_guess)==tuple:
                params = list(params_guess)
            
            num_func = int((len(params)-1)/(deg*2))
            y_list = []
            for i in range(num_func):
                y = np.zeros_like(x)
                for j in range(i, deg):
                    # params[2+deg*i + 2*j+1]       amp
                    # params[2+deg*i + 2*j]         pos
                    # j+1                           deg
                    y = y + np.array(params[2*deg*i + 2*j+1] * (x-params[2*deg*i + 2*j]) ** (j+1), dtype="float64")
                y_list.append(y)

            y_sum = np.zeros_like(x)
            for i in y_list:
                y_sum = y_sum + i
                
            # add background
            y_sum = y_sum + params[-1]
            return y_sum
        
        # return plynomi_func(x, params_new)
        popt, pcov = curve_fit(plynomi_func, x, self.data.y, p0=params_new)
        self.popt = popt
        self.pcov = pcov
        return popt, pcov
    
    def polynomial_func_fit_mode_f(self, *params, deg, mode='f'):
        params = params
        x = self.data.x

        num_func = int((len(params)-1)/(deg*2))
        y_list = []
        for i in range(num_func):
            y = np.zeros_like(x)
            for j in range(i, deg):
                # params[2+deg*i + 2*j+1]       amp
                # params[2+deg*i + 2*j]         pos
                # j+1                           deg
                y = y + np.array(params[2*deg*i + 2*j+1] * (x-params[2*deg*i + 2*j]) ** (j+1), dtype="float64")
            y_list.append(y)
        
        y_sum = np.zeros_like(x)
        for i in y_list:
            y_sum = y_sum + i
            
        # add backfround
        y_sum = y_sum + params[-1]
        return y_sum
    
    """
    exp_func_fit is the old fitting method and will be deprecated.
    Use gauss_func_fit instead.
    """
    def exp_func_fit(self, *params, mode="g"):
        
        def exp_func(x=self.data.x, *params_guess):
            params = params_guess
            #paramsの長さでフィッティングする関数の数を判別。
            num_func = int(len(params)/3)
            self.num_peaks = num_func
            
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
        
        popt, pcov = curve_fit(exp_func, self.data.x, self.data.y, p0=params)
        self.popt = popt
        self.pcov = pcov
        return popt, pcov
        
    def exp_func_fit_mode_f(self, *params, mode='f'):
        x = self.data.x
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
        
    def exp_fit_plot(self,*params):
        x = self.data.x
        num_func = int(len(params)/3)
        y_list = []
        for i in range(num_func):
            y = np.zeros_like(x)
            param_range = list(range(3*i,3*(i+1),1))
            ctr = params[int(param_range[0])]
            amp = params[int(param_range[1])]
            wid = params[int(param_range[2])]
            y = y + amp * np.exp( -((x - ctr)/wid)**2) + params[-1]
            y_list.append(y)
        return y_list
    
    def fit_plot(self, *params, func="exp", deg=None):
        x = self.data.x
        y = self.data.y
        
        if func=="exp":
            num_func = int(len(params)/3)
            y_list = []
            fit = self.exp_func_fit(*params, mode="f")
            plt.scatter(x, y, s=20)
            # plt.plot(x, fit , ls='-', c='black', lw=1)
            
            for i in range(num_func):
                y = np.zeros_like(x)
                param_range = list(range(3*i,3*(i+1),1))
                ctr = params[int(param_range[0])]
                amp = params[int(param_range[1])]
                wid = params[int(param_range[2])]
                y = y + amp * np.exp( -((x - ctr)/wid)**2) + params[-1]
                y_list.append(y)
            
            baseline = np.zeros_like(x) + params[-1]
            for n,i in enumerate(y_list):
                plt.fill_between(x, i, baseline, facecolor=cm.rainbow(n/len(y_list)), alpha=0.6)
                
        if func=="poly":
            
            params = params
            # params_guess = [[pos, amp1, pos, amp2],[pos, amp1, pos, amp2],...]
            # return params
            num_func = int((len(params)-1)/(deg*2))
            # y_list = []
            
            
            # y_sum = np.zeros_like(x)
            # for i in y_list:
            #     y_sum = y_sum + i
                
            # #最後にバックグラウンドを追加。
            # y_sum = y_sum + params[-1]
            # return y_sum
            y_list = []
            fit = self.plynomi_func_fit(*params, mode="f", deg=deg)
            plt.scatter(x, y, s=20)
            plt.plot(x, fit , ls='-', c='black', lw=1)
            
            for i in range(num_func):
                y = np.zeros_like(x)
                for j in range(i, deg):
                    # params[2+deg*i + 2*j+1]       amp
                    # params[2+deg*i + 2*j]         pos
                    # j+1                           deg
                    y = y + np.array(params[2*deg*i + 2*j+1] * (x-params[2*deg*i + 2*j]) ** (j+1), dtype="float64")
                y_list.append(y)
            
            # baseline = np.zeros_like(x) + params[-1]
            # plt.plot(x, baseline, ls='-', c='gray', alpha=0.6, lw=1)
            # for n,i in enumerate(y_list):
            #     plt.fill_between(x, i, baseline, facecolor=cm.rainbow(n/len(y_list)), alpha=0.6)
    
    def display_results_terminal(self, ci=2):
        
        peaks = []
        
        for i in range(self.get_num_peaks):
            
            peaks.append([self.peakxs[i], self.peakys[i], self.bandwidth_list(ci)[i], self.background])
            
            print(f"Fitting result: Peak No.{i+1}")
            print("-"*10, "your initial guess", "-"*10)
            print("x y bandwidth background")
            print(self.guess[i][0], self.guess[i][1], self.guess[i][2], self.guess[-1])
            print("-"*10, "optimized results", "-"*10)
            print(f"x y bandwidth(ci: {ci}sigma) background")
            print(self.peakxs[i], self.peakys[i], self.bandwidth_list(ci)[i], self.background)
            print("-"*30)
        
        peaks = pd.DataFrame(peaks, columns=["x", "y", f"bandwidth(ci: {ci}sigma)", "background"])
        self.peaks = peaks
        return peaks

    
    @property
    def get_num_peaks(self):
        return int(self.num_peaks)
    
    @property
    def peakxs(self):
        popt = self.popt
        peakxs = [popt[i] for i in range(len(popt)) if i % 3 ==0]
        return peakxs
    
    @property
    def peakys(self):
        popt = self.popt
        peakys = [popt[i] for i in range(len(popt)) if i % 3 ==1]
        return peakys
    
    @property
    def peak_width(self):
        popt = self.popt
        peakwidth = [popt[i] for i in range(len(popt)) if i % 3 ==2]
        return peakwidth
    
    @property
    def background(self):
        return self.popt[-1]
    
    def out_result(self, ci:int=2):
        return self.peaks
    
    def bandwidth_list(self, ci):
        self.ci = ci
        popt = self.popt
        width_list = [popt[i] for i in range(len(popt)) if i % 3 ==2]
        width_list = [width_list[i]/(2**0.5) * 2*ci for i in range(len(width_list))]
        return width_list
    
    def save_data(self, dir_path:str=None, save_path:str=None):
        self.peaks.to_csv(save_path, sep=',')