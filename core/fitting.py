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
        
    def run(self, method='gaussian', ci:int=2, deg: int = None):
        if method == 'gaussian':
            self.method = 'gaussian'
            self.fit_by_gaussian_func()

        elif method == 'polynomial':
            self.method = 'polynomial'
            self.deg = deg
            self.fit_by_polynomial_func()
            
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
    
    """
    todo: 
    - Use the fititng functions imported from fitting_functions.py module 
    
    """
    def fit_by_gaussian_func(self):
        
        from .fitting_functions import gaussian_func
        
        guess_list = []
        for val in self.guess[:-1]:
            guess_list.extend(val)
        guess_list.append(self.guess[-1])
        self.num_peaks = int((len(guess_list)-1)/3)
        
        self.popt, self.pcov = curve_fit(gaussian_func, self.data.x, self.data.y, p0=guess_list)
        return self.popt, self.pcov
    
    def fit_by_polynomial_func(self):
        
        from .fitting_functions import Polynomial
        polynomial = Polynomial(deg=self.deg)
        
        guess_list = []
        for content in self.guess[:-1]:
            guess_list.extend(content)
        guess_list.append(self.guess[-1])
        self.num_peaks = int((len(guess_list)-1)/(self.deg*2))
        
        self.popt, self.popv = curve_fit(polynomial.polynomial_func, self.data.x, self.data.y, p0=guess_list, )
        return self.popt, self.popv
    
    def plot_fit(self):
        x = self.data.x
        y = self.data.y
        params = self.popt
        plt.scatter(x, y, s=20)
        
        if self.method == 'gaussian':
            
            num_func = int((len(params)-1)/3)
            baseline = np.zeros_like(x) + params[-1]
            y_sum = np.zeros_like(x)
            
            for i in range(num_func):
                yp = np.zeros_like(x)
                param_range = list(range(3*i,3*(i+1),1))
                ctr = params[int(param_range[0])]
                amp = params[int(param_range[1])]
                wid = params[int(param_range[2])]
                yp += amp * np.exp( -((x - ctr)/wid)**2)
                y_sum += yp
                
                plt.fill_between(x, yp+baseline, baseline, facecolor=cm.rainbow(i/num_func), alpha=0.6)
            
            plt.plot(x, y_sum+baseline, ls='-', c='black', lw=1)
            plt.show()
        
        elif self.method == 'polynomial':
            
            deg = self.deg
            
            num_func = int((len(params)-1)/deg/2)
            baseline = np.zeros_like(x) + params[-1]
            y_sum = np.zeros_like(x)
            
            for i in range(num_func):
                yp = np.zeros_like(x)
                for j in range(i, deg):
                    # params[2+deg*i + 2*j+1]       amp
                    # params[2+deg*i + 2*j]         pos
                    # j+1                           deg
                    yp += np.array(params[2*deg*i + 2*j+1] * (x-params[2*deg*i + 2*j]) ** (j+1), dtype="float64")
                
                y_sum += yp
                plt.fill_between(x, yp+baseline, baseline, facecolor=cm.rainbow(i/num_func), alpha=0.6)
            
            plt.plot(x, y_sum+baseline, ls='-', c='black', lw=1)
            plt.show()

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