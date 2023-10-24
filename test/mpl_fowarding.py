import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt

plt.figure()
plt.plot([1, 2, 3], [1, 2, 3])

plt.savefig("./fig.png")

plt.show()
