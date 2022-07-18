from core.preprocessing import read_data, reset_range
from utils.imgToCSV import bmp_to_csv
from core.guessing import Guessor
from core.fitting import Fitter

from utils.draw_test_data import draw_test

def main():
    
    # bmp_to_csv('sample_data/sample.bmp')
    draw_test('sample_data/drawed_function.csv')
    data = read_data('sample_data/drawed_function.csv', 0, ',')
    
    guessor = Guessor(data, background=0, method="drag")
    init_guess = guessor.guess()
    
    print(type(init_guess))

    optimizer = Fitter(data, init_guess)
    optimizer.run(method= 'polynomial', deg=2)
    optimizer.save_data(save_path='out/spectrum1.csv')
    optimizer.display_results_terminal(ci=2)
    optimizer.plot_fit()
    
def main2():
    
    from core.guessing_auto import WaveletTransform
    
    data = read_data('sample_data/sample.csv', 0, ',')
    guessor = WaveletTransform(data, fs=1, dt=1e-4)
    freqs = guessor.get_freqs()
    print(len(freqs))
    
    # mother_func = guessor.mother_func(0.01, 1, 1000, 1, 0.1, 1)
    
    # print(mother_func)
    # import matplotlib.pyplot as plt
    # fig, ax = plt.subplots()
    # ax.plot(mother_func)
    # plt.show()
    
    init_guess = guessor.transform(amp=100, width=10, deltab=1, sigma=0.005, k = 0.01)
    # guessor.plot_mother_func()
    guessor.plot()

if __name__ == "__main__":
    
    main2()