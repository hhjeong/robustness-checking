import BioToolGR
import pandas as pd
import numpy as np


if __name__ == "__main__":
    b = BioToolGR.BioToolGR()

    home = "sampling-data/"
    for k in np.arange(0.1,1,0.1):
        name = str(int(k*100))
        name += "/RandomDataSet"
        b.HynOrder5(home+name,k)
