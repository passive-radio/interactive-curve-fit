from core.preprocessing import read_data, reset_range
from utils.bmptocsv import bmp_to_csv
from core.interactive import Guessor
from core.detection import Fitter


def main():
    
    data = bmp_to_csv('sample_data/sample.bmp')
    data = read_data('sample_data/sample.csv', 0, ',')
    
    guessor = Guessor(data, background=0, method="drag")
    guess = guessor.guess()

    optimizer = Fitter(data, guess)
    optimizer.run()
    optimizer.save_data(save_path='result/spectrum0.csv')
    peaks = optimizer.display_results_terminal(ci=2)

if __name__ == "__main__":
    
    main()