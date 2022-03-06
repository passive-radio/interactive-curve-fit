from core.preprocessing import read_data, reset_range
from core.interactive import click_guess, drag_guess
from utils.visualize import see_spectrum

if __name__ == "__main__":
    
    base_url = "sample_data/"
    endpoint = "sample04.csv"
    
    data= read_data(base_url + endpoint, 0, ',')
    see_spectrum(data) #function to see spectrum visually
    data = reset_range(data, 0, 512)
    
    peaks = drag_guess(data, background=0, ci=2) #teaching aprox positions of peaks by mouse drag 
    print(peaks)
    # output_url = "output/"
    # filename, ext = os.path.splitext(endpoint)
    
    # peaks.to_pickle(output_url+filename+"_peaks.pkl")
    # peaks.to_csv(output_url+filename+"_peaks.csv", sep=",")
    