# <b>interactive_curve_fit</b>
A Python project enables you to do curve fitting on spectrum data interactively on GUI.
You can visualize your spectrum and fit the optional number of peaks on GUI using Scipy.optimize.curve_fit method.

## <b>How to install</b>

```bash
pip install interactive-curve-fit==0.0.1
```

## <b>How to use</b>

Try [tutorial.py](tutorial.py) with your spectrum data!

## <b>Spectrum data format must be like the table below</b>

| x | y |
|---|---|
|0  | 1  |
|1  | 13 |
|2  | 30 |
|3  | 43 |
|4  | 31 |
|5  | 11 |
|...|...|

## <b>Steps to curve-fit</b>

1. Teach your initial guess of the positions of each peaks roughly to Fitter.

    ```python
    from interactive_curve_fit import read_data, Guessor, Fitter
    
    data = read_data(data, headers=2, sep=',')
    guessor = Guessor(data, background=10, method='drag')
    guess = guessor.guess()
    ```

    ### Initial Guess method
    - mouse-dragging (wrap up peak area by mouse-dragging)
    - click (click the top and the both edges of each peaks)

    ### Screenshot
    ![Guessing peak pos interactively](img/mouse-dragging-step0.png)
    ![Guessing another peak pos](img/mouse-dragging-step2.png)
    ![Fitting results (by Fitter class)](img/peak_found.png)
    ![Peak information on terminal](img/peak_terminal.png)

1. Give your spectrum data and your guess to Fitter.
    
    ```python
    fitter = Fitter(data, guess)
    fitter.run(method='gaussian')
    ```
    ### Supported fitting functions
    - gaussian function
    - polynomial function

    ### Output information includes
    - position (x, y) of each peaks
    - baseline height of the spectrum
    - bandwidth of each peaks with its CI (confidential interval)

1. Save the fitting results
    ```python
    fitter.save_data('out/fitting_result.csv')
    ```

1. Other features
    
    bmp_to_csv converts bmp file to csv file.
    ```python
    from interactive_curve_fit import bmg_to_csv
    bmp_to_csv('data/line_spectrum.bmp')
    data = read_data('data/line_spectrum.csv')
    ```
    
    Fitter can visualize fitting results
    ```
    fitter.plot_fit()
    ```

    Fitter can also display fitting results on terminal
    ```
    fitter.display_results_terminal(ci=2)
    ```

## <b>Supported supectrum file format</b>

- ascii file(.asc .csv .txt etc..)
- bmp image(.bmp .jpg .png .jpeg etc..)

    excel sheet files, table of html are planed to be suported in the near future.

## <b>Features that are planned to be supported!</b>

- baseline correlation
- other fitting functions (e.g. binomical distribution function)
- automated guessor method using wavelet transform and CNN