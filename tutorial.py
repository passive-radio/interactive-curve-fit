from interactive_curve_fit import read_data, Guessor, Fitter

def main():
    
    # you may use bmp_to_csv when your spectrum data is bmp file.
    # bmp_to_csv('sample_data/sample.bmp')
    data = read_data('sample_data/sample.csv', 0, ',')
    
    guessor = Guessor(data, background=0, method="drag")
    init_guess = guessor.guess()

    optimizer = Fitter(data, init_guess)
    optimizer.run(method= 'gaussian')
    optimizer.save_data(save_path='out/spectrum0.csv')
    optimizer.display_results_terminal(ci=2)
    optimizer.plot_fit()

if __name__ == "__main__":
    main()