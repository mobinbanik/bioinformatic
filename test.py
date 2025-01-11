import matplotlib.pyplot as plt

arr = [-1.24, -0.22, -1.26, -0.345, -0.15, -0.34]

plt.plot(arr, label="volt")
plt.show()
plt.savefig("fig", dpi=100)
