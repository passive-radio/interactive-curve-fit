import time
import csv

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import matplotlib.patches as patches
from matplotlib.artist import Artist


# from core.detection import find_peaks
from core.preprocessing import read_data, reset_range

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

class Guessor(object):
    def __init__(self, data, method, background=0) -> None:
        self.data = data
        self.method = method
        self.background = background

    def guess(self):
        if self.method == "drag":
            # run drag guess and return guess
            peaks_guessed = self.drag_guess()
        elif self.method == "click":
            # run click guess and return guess
            peaks_guessed = self.click_guess()
        return peaks_guessed
    
    def drag_guess(self, x_scale=200, y_scale=30):
        
        x_peaks = []
        y_peaks = []
        bands = []
        
        global count, band, left, right, peak_count, texts, x1, y1, DragFlag, is_released, sx1, sx2, sy1, sy2
        
        band = 0
        left = 0
        right = 0
        peak_count = 0
        texts = []
        DragFlag = False
        # draw_count = 0
        rs = []
        is_released = False
        
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
        plt.scatter(self.data.x, self.data.y, s=2)
        plt.show()
        
        # add background info into init guess
        peaks_guessed = []
        for i in range(len(x_peaks)):
            try:
                peaks_guessed.append([x_peaks[i], y_peaks[i], bands[i]])
            except Exception as e:
                print(e)
                pass
        
        # guess_content = []
        # for i in peaks_guessed:
        #     guess_content.extend(i)
        # guess_content.append(self.background)
        peaks_guessed.append(self.background)
        return peaks_guessed
    
    def click_guess(self, x_scale=200, y_scale=30):
        
        x_peaks = []
        y_peaks = []
        bands = []
        
        global count, band, left, right, peak_count, texts
        
        count = 0
        band = 0
        left = 0
        right = 0
        peak_count = 0
        texts = []
        
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
        plt.scatter(self.data.x, self.data.y, s=2)
        plt.show()
        
        peaks_guessed = []
        for i in range(len(x_peaks)):
            try:
                peaks_guessed.append([x_peaks[i], y_peaks[i], bands[i]])
            except Exception as e:
                print(e)
                pass
        # add background info into init guess
        peaks_guessed.append(self.background)
        return peaks_guessed
        # guess_total = []
        # for i in guess:
        #     guess_total.extend(i)
        # guess_total.append(self.background)

if __name__ == "__main__":
    
    base_url = "../sample_data/"
    endpoint = "sample.csv"
    
    data= read_data(base_url + endpoint, 0, ',')
    guessor = Guessor(data, "drag", background=10)
    guess = guessor.guess()
    print(guess)