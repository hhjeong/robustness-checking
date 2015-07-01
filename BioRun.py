import BioToolGR
import pandas as pd
import numpy as np


if __name__ == "__main__":
    b = BioToolGR.BioToolGR()

    home = "sampling-data/"
    for k in np.arange(0.1,1,0.1):
        name = str(int(k*100))
        name += "/RandomDataSet"
        for i in range(100):
            b.HynOrder5(home+name+str(i),k)

        print "Done"
