import matplotlib.pyplot as plt
import numpy as np

from pathlib import Path

source_dir = Path(__file__).resolve().parent
file_name = input("File Name: ")
source_dir = source_dir / file_name

if not source_dir.is_file():
    print("Not a file...")
    print(source_dir)
    exit()
else:
    csv = np.loadtxt(str(source_dir), delimiter=',')
    plt.plot(csv[:,0])
    plt.plot(csv[:,1])
    plt.plot(csv[:,2])
    plt.show()
