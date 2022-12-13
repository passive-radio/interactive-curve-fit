import csv
import pandas as pd
import matplotlib.pyplot as plt

def read_data(file: str, headers=None, sep=",") -> pd.DataFrame:
    """read_data

    Parameters
    ----------
    file : str
        path to spectrum data file you want to do curve fitting.
    headers : None or int, optional
        The last row number of headers. This value has to be None if there's no header, by default None
    sep : str, optional
        separater that is used to separate values in the given file, by default ","

    Returns
    -------
    pd.DataFrame
        dataframe shape may be like
        | x | y |
        | 0 | 0.0 |
        | 1 | 1.0 |
        | 2 | 3.0 |
    """    
    data = []
    with open(file, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=sep)
        if headers == None:
            for i, row in enumerate(reader):
                data.append([float(row[0].replace('\n', '').replace(' ', '')), float(row[1].replace('\n', '').replace(' ', ''))])
        else:
            for i, row in enumerate(reader):
                if i > headers:
                    data.append([float(row[0].replace('\n', '').replace(' ','')), float(row[1].replace('\n', '').replace(' ',''))])
        
    data = pd.DataFrame(data, columns=['x', 'y'])
    return data

def reset_range(data: pd.DataFrame, start=None, end=None) -> pd.DataFrame:
    """reset_range

    Parameters
    ----------
    data : pd.DataFrame
        spectrum data that you want to reser its range to be analyzed
    start : None or int, optional
        the number of initial row to reset its range, by default None
    end : None or int, optional
        the number of last row to reset its range, by default None

    Returns
    -------
    pd.DataFrame
        range-reseted dataframe
    """
    if type(start) == int and type(end)==int:
        return data[start:end]
    elif start == None and type(end)==int:
        return data[:end]
    elif type(start)==int and end==None:
        return data[start:]
    else:return data

def check_spectrum(data: pd.DataFrame) -> None:
    """check_spectrum

    Parameters
    ----------
    data : pd.DataFrame
        data you want to visualize
    """
    x_list = data.x
    y_list = data.y
    
    plt.title("")
    plt.scatter(x_list, y_list, s=2)
    plt.show()