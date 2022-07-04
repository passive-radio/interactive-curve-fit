# <b>Interactive Scipy Curve_fit</b>
A Python project enables you to fit peaks interactively on GUI.
You can visualize your spectrum and fit the optional number of the peaks on GUI using Scipy.optimize.curve_fit method.

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

## <b>Features</b>

1. Fitting spectrum in GUI window

    You can obtain the information of each peaks in the spectrum by using [interactive.py](core/interactive.py)
    ### Output information includes:
    - peak position (x, y)
    - baseline height of the spectrum
    - bandwidth of each peaks with its CI (confidential interval)

    ### Guess methods available:
    - click (click the top and the both edge of each peaks)
    - drag (wrap up the peak area by dragging mouse)

    ### Click example
    ![interactive peak guessing](img/interactive_step1.png)
    ![selecting another peak](img/interactive_another_peak.png)
    ![results](img/peak_found.png)


2. Converting bmp image files to csv files

    You can directly find and fit peaks from the image(which contains spectrum data) by [interacive.py](interactive.py) without additional hassle of converting bmp images into csv files.

    Notice: file format of the images must be bmp(.bmp, .jpg, .png, .jpeg). Vector format isn't supported.

## <b>Supported approximation curve functions</b>

- gaussian function
- polynomial function

## <b>Supported supectrum files format</b>
* ascii file(.asc .csv .txt etc..)
* bmp image(.bmp .jpg .png .jpeg etc..)

    excel sheet files, table of html are planed to be suported in the near future.

## <b>Features that are planned to be supported!</b>

- baseline correlation
- other fitting functions (e.g. binomical distribution function)