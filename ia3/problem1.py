import matplotlib.pyplot as plt
import numpy as np
import cvxpy as cp

# Define the data points
points = [(1, 3), (2, 5), (3, 7), (5, 11), (7, 14), (8, 15), (10, 19)]
x_val = np.array([p[0] for p in points])
y_val = np.array([p[1] for p in points])

a = cp.Variable()
b = cp.Variable()
t = cp.Variable()

constraints = [cp.abs(a * x_val[i] + b - y_val[i]) <= t for i in range(len(points))]

objective = cp.Minimize(t)
prob = cp.Problem(objective, constraints)
prob.solve()

    # display the results
print("Optimal a:", a.value)
print("Optimal b:", b.value)
print("Optimal t (max absolute deviation):", t.value)

    # Plot the data points and the regression line
plt.figure()
plt.plot([x for (x, y) in points], [y for (x, y) in points], 'ro', label="Data points")
plt.plot([x for (x, y) in points], [a.value * x + b.value for (x, y) in points], 'b-', label="Regression line")
plt.legend()
plt.show()

    # Save the plot
plt.savefig("regression_plot.png")
print("Plot saved as regression_plot.png")