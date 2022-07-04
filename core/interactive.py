import time
import csv

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import matplotlib.patches as patches
from matplotlib.artist import Artist


from core.detection import find_peaks
from core.preprocessing import read_data, reset_range


x_list = []
y_list = []

X_SCALE = 200
Y_SCALE = 30
count = 0
band = 0
left = 0
right = 0
peak_count = 0
texts = []
DragFlag = False
draw_count = 0
rs = []
is_released = False

def click_guess(data, background, ci=2):
    
    x_list = data.x
    y_list = data.y
    
    # print(xy_list)
    #xy_list = np.array(xy_list, dtype="float")
    #print(xy_list[0][0], type(xy_list[0][0]))
    
    x_peaks = []
    y_peaks = []
    bands = []
    
    def button_pressed_motion(event):
        is_click_off = False
        global count
        global band
        global left
        global right
        global texts
        global peak_count
        
        #[event] event.button
        # value | info
        #   1   |   left-click
        #   2   |   mouse wheeling
        #   3   |   right-click
        
        if (event.xdata is  None) or (event.ydata is  None):
            return
        
        if event.button == 1 and count == 0:
            count = 1
            x = event.xdata
            y = event.ydata
            
            x_peaks.append(x)
            y_peaks.append(y)
            plt.title(f"Peak selected! at ({int(x)},{int(y)})")
            #texts.append(ax.text(100, 30, "Next, Please select the bandwidth by clicking the edge of the peak! (left->right)"))
            
        elif event.button == 1 and count == 1:
            left = event.xdata
            count =2
            
        elif event.button == 1 and count == 2:
            right = event.xdata
            band = abs(left- right)
            bands.append(band)
            #texts[peak_count].remove()
            plt.title(f"Bandwidth selected!: {band}")
            ax.text(100, 30, "You can now close this window! or right-click for marking another peak!")
        
        if event.button == 3 and count == 2:
            plt.title(f"Now, select next peak!")
            peak_count += 1
            count = 0
            
        plt.draw()
    
    fig = plt.figure()
    ax = fig.add_subplot()
    plt.title("Please click the top of the peak! :)")
    plt.connect('button_press_event', button_pressed_motion)
    plt.scatter(x_list, y_list, s=2)
    plt.show()
    
    
        
    #data = reset_range(data_origin, 1600)
    findpeaks = find_peaks(data)
    
    #初期値のリストを作成
    #[amp,ctr,wid]
    guess = []
    for i in range(len(x_peaks)):
        try:
            guess.append([x_peaks[i], y_peaks[i], bands[i]])
        except Exception as e:
            print(e)
            pass

    #初期値リストの結合
    guess_total = []
    for i in guess:
        guess_total.extend(i)
    guess_total.append(background)
    
    # run scipy.optimize.curve_fit
    popt, pcov = findpeaks.exp_func_fit(*guess_total, mode="g")
    opt_background = popt[-1]
    # visualize optimized functions with the original spectrum
    findpeaks.fit_plot(*popt, func="exp")
    
    peaks = []
    for i in range(len(x_peaks)):
        
        peaks.append([findpeaks.peakxs[i], findpeaks.peakys[i], findpeaks.bandwidth_list_test[i], opt_background])
        
        print(f"Fitting result: Peak No.{i+1}")
        print("-"*10, "your guess", "-"*10)
        print("x y bandwidth")
        print(x_peaks[i], y_peaks[i], bands[i], background)
        print("x y bandwidth background (Fitting result)")
        print(findpeaks.peakxs[i], findpeaks.peakys[i], findpeaks.peak_width(ci)[i], popt[-1])
        print("-"*30)
    
    # write peaks onto csv file
    
    plt.show()
    
    peaks = pd.DataFrame(peaks, columns=["x", "y", "width", "background"])
    return peaks
    
def drag_guess(data, background, ci=2):
    
    x_list = data.x
    y_list = data.y
    
    # print(xy_list)
    #xy_list = np.array(xy_list, dtype="float")
    #print(xy_list[0][0], type(xy_list[0][0]))
    
    x_peaks = []
    y_peaks = []
    bands = []
    DragFlag = False    
    
    def button_pressed_motion(event):
        is_click_off = False
        global count
        global band
        global left
        global right
        global texts
        global peak_count
        global x1, y1
        global DragFlag
        global is_released
        global sx1, sx2, sy1, sy2
        
        #[event] event.button
        # value | info
        #   1   |   left-click
        #   2   |   mouse wheeling
        #   3   |   right-click
        
        if (event.xdata is  None) or (event.ydata is  None):
            return
        
        # if event.button == 1 and not DragFlag:
        #     count = 1
        #     x1 = event.xdata
        #     y1 = event.ydata
            
        #     DragFlag = True
        plt.title("mouse clicked!")
        
        if DragFlag == False:        
            x1 = event.xdata
            y1 = event.ydata
            DragFlag = True
            
            # x_peaks.append(x)
            # y_peaks.append(y)
            # plt.title(f"Peak selected! at ({int(x)},{int(y)})")
            #texts.append(ax.text(100, 30, "Next, Please select the bandwidth by clicking the edge of the peak! (left->right)"))
            
        if event.button == 3 and count == 1:
            plt.title(f"Now, select next peak!")
            peak_count += 1
            count = 0
            
        if is_released == True:
            plt.title("right click to verify if this select is fine or select peak again!")
            
        if event.button == 3:
            plt.title("Close this window or select another peak")
            iy1,iy2 = sorted([sy1,sy2])
            x_peaks.append((sx1+sx2)/2)
            y_peaks.append(iy2)
            bands.append(abs(sx1-sx2))
            
        plt.draw()
        
    # 四角形を描く関数
    def DrawRect(x1,x2,y1,y2):
        global rs,rold, draw_count
        global sx1, sx2, sy1, sy2
        try:
            rs[-2].remove()
        except:
            pass
        # Rect = [ [ [x1,x2], [y1,y1] ],
        #         [ [x2,x2], [y1,y2] ],
        #         [ [x1,x2], [y2,y2] ],
        #         [ [x1,x1], [y1,y2] ] ]
        # print(Rect[0][0])
        sx1 = x1
        sx2 = x2
        sy1 = y1
        sy2 = y2
        ix1, ix2 = sorted([x1,x2])
        iy1, iy2 = sorted([y1,y2])
        width = abs(ix2-ix1)
        height = abs(iy2-iy1)
        rs.append(patches.Rectangle(xy=(ix1, iy1), width=width, height=height, ec='#000000', fill=False))
        ax.add_patch(rs[-1])
        
        
        #draw_count += 1
        # for i, rect in enumerate(Rect):
        #     #lns[i].set_data(rect[0],rect[1])
        #     ln, = plt.plot(rect[0],rect[1],color="r",lw=2)
            
        # for rect in Rect:
        #     ln, = plt.plot(rect[0],rect[1],color='r',lw=2)
        #     lns.append(ln)
        #     plt.show()
        
    def mouse_dragged_motion(event):
        plt.title("Right click to verify if this select is fine or select the peak again!")
        global x1,y1,x2,y2,DragFlag,r

        # ドラッグしていなければ終了
        if DragFlag == False:
            return

        # 値がNoneなら終了
        if (event.xdata is None) or (event.ydata is None):
            return 

        x2 = event.xdata
        y2 = event.ydata

        # ソート
        # x1, x2 = sorted([x1,x2])
        # y1, y2 = sorted([y1,y2])

        # 四角形を更新
        DrawRect(x1,x2,y1,y2)

        # 描画
        plt.draw()
        if 1 < len(rs):
            for i in range(len(rs)):
                try:
                    Artist.remove(rs[-2])
                    del rs[-2]
                except:
                    pass
        
    # 離した時
    def Release(event):
        global DragFlag
        global is_released
        # フラグをたおす
        DragFlag = False
        is_released = True
        
    
    fig = plt.figure()
    ax = fig.add_subplot()
    plt.title("Please wrap the peak by mouse dragging! :)")
    plt.connect('button_press_event', button_pressed_motion)
    plt.connect("button_release_event", Release)
    plt.connect("motion_notify_event", mouse_dragged_motion)
    plt.scatter(x_list, y_list, s=2)
    plt.show()
    
    #初期値のリストを作成
    #[amp,ctr,wid]
    guess = []
    for i in range(len(x_peaks)):
        try:
            guess.append([x_peaks[i], y_peaks[i], bands[i]])
        except Exception as e:
            print(e)
            pass

    #初期値リストの結合
    guess_total = []
    for i in guess:
        guess_total.extend(i)
    guess_total.append(background)
    
    findpeaks = find_peaks(data, ci=ci)
    
    popt, pcov = findpeaks.exp_func_fit(*guess_total, mode="g")
    opt_background = popt[-1]
    findpeaks.fit_plot(*popt, func="exp")
    
    peaks = []
    
    for i in range(len(x_peaks)):
        
        peaks.append([findpeaks.peakxs[i], findpeaks.peakys[i], findpeaks.bandwidth_list_test[i], opt_background])
        
        print(f"Fitting result: Peak No.{i+1}")
        print("-"*10, "your initial guess", "-"*10)
        print("x y bandwidth background")
        print(x_peaks[i], y_peaks[i], bands[i], background)
        print("-"*10, "optimized results", "-"*10)
        print(f"x y bandwidth(ci: {ci}sigma) background")
        print(findpeaks.peakxs[i], findpeaks.peakys[i], findpeaks.bandwidth_list_test[i], popt[-1])
        print("-"*30)
    
    # write peaks onto csv file
    
    plt.show()
    
    peaks = pd.DataFrame(peaks, columns=["x", "y", f"bandwidth(ci: {ci}sigma)", "background"])
    return peaks

"""
find_peaks class が 今は独立して実装されている fit_dataとか display_results_terminal を持っていたほうがいい気がする
なぜなら find_peaks class 自体が init guess by user と fitting resutls を持っているから
"""

def fit_data(data, guess):
    optimizer = find_peaks(data)
    popt, pcov = optimizer.exp_func_fit(*guess)
    opt_background = popt[-1]
    
    peaks = []
    for i in range(optimizer.get_num_peaks):
        peaks.append([optimizer.peakxs[i], optimizer.peakys[i], optimizer.bandwidth_list_test[i], opt_background])

    return peaks

def display_results_terminal(results: find_peaks, ci=2, init_guess: list = None):
    
    for i in range(results.get_num_peaks):
        
        
        
        print(f"Fitting result: Peak No.{i+1}")
        print("-"*10, "your initial guess", "-"*10)
        print("x y bandwidth background")
        print(x_peaks[i], y_peaks[i], bands[i], background)
        print("-"*10, "optimized results", "-"*10)
        print(f"x y bandwidth(ci: {ci}sigma) background")
        print(findpeaks.peakxs[i], findpeaks.peakys[i], findpeaks.bandwidth_list_test[i], popt[-1])
        print("-"*30)
    
    # write peaks onto csv file
    
    plt.show()
    
    peaks = pd.DataFrame(peaks, columns=["x", "y", f"bandwidth(ci: {ci}sigma)", "background"])
    return peaks
    

if __name__ == "__main__":
    
    base_url = "sample_data/"
    endpoint = "sample02.csv"
    
    # x_list = []
    # y_list = []
    # with open(base_url+endpoint, 'r', newline='') as file:
    #     csv_val = csv.reader(file, delimiter=',')
    #     for row in csv_val:
    #         x_list.append(float(row[0]))
    #         y_list.append(float(row[1]))
    
    data= read_data(base_url + endpoint, 0, ',')
    drag_guess(data, 0)