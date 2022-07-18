"""
# ピークの位置を wavelet transform を用いてコンピューターが予測できるようにする

## 手法
- wavelet transform で 位相-強度空間のスペクトルを位相-周波数-強度空間に変換する
- このときピークに対して周波数強度が高くなるような畳み込み積分の関数形を選ぶ
- ある閾値を超えた強度の区間をピークの幅、その区間の強度最大位置をピーク位置、scalogram のピーク位置に対応するスペクトル位置の強度をピークの高さとする
- ベースラインの推定も今後やる予定である

## wavelet transform 
- １回の wavelet transform だけでピーク検知するものをまず実装する
- 最新のウェーブレット変換を使ったピーク検知手法は、 ridge method と呼ばれる多重のウェーブレット変換を行う方法がかなり良い検出精度である
- ridge method を次に実装する
- 1回 wavelet transform の関数クラスタが ridge method で使えるように気をつけて実装する

"""

import numpy as np

class WaveletTransform:
    def __init__(self, signal, fs:float=10, dt=1):
        self.signal = signal
        self.fs = fs
        self.dt = dt
        # pass

    def guess(self):
        pass
    
    def get_freqs(self):
        
        N = len(self.signal)
        # self.dt sampling dt
        freqs = np.fft.fftfreq(N, d=self.dt)
        freqs = freqs[np.where(freqs > 0)]
        freqs = np.sort(freqs)
        
        return freqs
    
    def transform(self, amp, width, deltab, sigma:float = 1.0, k:float = 1.0):
        
        self.mother_amp = amp
        self.mother_width = width
        self.mother_deltab = deltab
        self.mother_sigma = sigma
        self.mother_k = k
        
        import matplotlib.pyplot as plt
        
        Ts = 1/self.fs
        freqs = self.get_freqs()
        
        length = len(freqs)
        wn = np.zeros([len(freqs), len(self.signal)])
        
        signal = self.signal['y'] - 22
        
        for i, freq in enumerate(freqs):
            
            conv = np.abs(np.convolve(signal, self.mother_func(freq, amp=amp, width=width, deltab=deltab, sigma=sigma, k=k), mode='same'))
            
            wn[length-1-i, :] = conv
            wn[length-1-i, :] = (2 * wn[length-1-i, :]/self.fs)**2
        
        self.sequence = np.sum(wn, axis=0)
        
        return self.sequence
    
    def mother_func(self, freq:float=0.01, amp:float = 1.0, width:float = 1, deltab:float = 1, sigma:float = 1, k:float = 1):
        # freqs = self.get_freqs()
        # width = 0.4
        scale_space = np.arange(-1* width/2 + deltab/2, width/2 + deltab/2, deltab)
        # wab = np.zeros([len(freqs), len(scale_space)])
        # wab = np.power(amp, -1/2) * np.exp(-np.power(scale_space, 2)/np.power(amp/freqs, 2))
        cor = amp * sigma * np.power(np.pi, -1/4)
        wab = cor * np.exp(-1/2 * np.power(scale_space, 2) / np.power(amp/freq, 2)) * (np.cos(sigma * scale_space) - k*sigma)
        # wab = np.power(amp, -1/2) * np.exp(-np.power(scale_space, 2) * np.sin() /np.power(amp/freq, 2))
        # for i, freq in enumerate(freqs):
        #     wab[i, :] = np.power(amp, -1/2) * np.exp(-np.power(scale_space, 2)/np.power(amp/freq, 2))
        return wab
    
    def plot(self):
        
        import matplotlib.pyplot as plt
        
        height = np.max(self.signal['y'])
        height_multi = height / np.max(self.sequence)
        sequence = height_multi * self.sequence
        
        signal = self.signal['y'] - 22
        
        plt.plot(signal)
        plt.plot(sequence)
        plt.legend(['original', 'convoluted signal'])
        plt.show()
        
        return sequence
    
    def plot_mother_func(self):
        
        import matplotlib.pyplot as plt
        
        freq = self.get_freqs()[0]
        
        # mother_func = self.mother_func(10, 200, 100, 1, 0.5, 0.01)
        mother_func = self.mother_func(freq, self.mother_amp, self.mother_width, self.mother_deltab, self.mother_sigma, self.mother_k)

        plt.plot(mother_func)
        plt.legend([f"mother function ({str(freq)} Hz)"])
        plt.show()