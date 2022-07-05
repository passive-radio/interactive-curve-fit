from core.preprocessing import read_data, reset_range
from core.interactive import Guessor
from core.detection import Fitter


def main(data):
    
    guessor = Guessor(data, background=0, method="drag")
    guess = guessor.guess()
    print(guess)

    optimizer = Fitter(data, guess)
    popt, pcov = optimizer.run()
    print(popt)

    peaks = optimizer.display_results_terminal(ci=2)
    print(peaks)

if __name__ == "__main__":
    
    data = read_data('sample_data/sample.csv', 0, ',')
    main(data)