import pandas as pd
import numpy as np
import gurobipy as gp
from gurobipy import GRB
import matplotlib.pyplot as plt

data = pd.read_csv("Corvallis.csv", delimiter=";")

d_values = data['day.1'].values
T_values = data['average'].values

P_season = 365.25         
P_solar = 365.25 * 10.7   

model = gp.Model("Temperature_Fit")

x = model.addVars(6, lb=-GRB.INFINITY, name="x")
t = model.addVar(lb=0, name="t")

for i in range(len(d_values)):
    T_pred = (x[0] + x[1] * d_values[i] +
              x[2] * np.cos(2 * np.pi * d_values[i] / P_season) +
              x[3] * np.sin(2 * np.pi * d_values[i] / P_season) +
              x[4] * np.cos(2 * np.pi * d_values[i] / P_solar) +
              x[5] * np.sin(2 * np.pi * d_values[i] / P_solar))

    model.addConstr(T_pred - T_values[i] <= t)
    model.addConstr(T_values[i] - T_pred <= t)

model.setObjective(t, GRB.MINIMIZE)

model.optimize()

x_values = [x[i].X for i in range(6)]
t_value = t.X

print("Optimal solution found:")
print(f"x0 = {x_values[0]}")
print(f"x1 = {x_values[1]}  (daily drift in °C)")
print(f"x2 = {x_values[2]}")
print(f"x3 = {x_values[3]}")
print(f"x4 = {x_values[4]}")
print(f"x5 = {x_values[5]}")
print(f"Minimum maximum absolute deviation (E) = {t_value}")
print(f"Estimated annual drift (x1 * 365.25) = {x_values[1] * 365.25} °C/year")

plt.figure(figsize=(14, 6))

plt.plot(d_values, T_values, 'ro', label="Data points")
plt.xlabel("Day")
plt.ylabel("Temperature (°C)")

d_values_sorted = np.sort(d_values)
T_model_values = (x_values[0] + x_values[1] * d_values_sorted +
                  x_values[2] * np.cos(2 * np.pi * d_values_sorted / P_season) +
                  x_values[3] * np.sin(2 * np.pi * d_values_sorted / P_season) +
                  x_values[4] * np.cos(2 * np.pi * d_values_sorted / P_solar) +
                  x_values[5] * np.sin(2 * np.pi * d_values_sorted / P_solar))
plt.plot(d_values_sorted, T_model_values, 'b-', label="Fitted model")

T_trend_values = x_values[0] + x_values[1] * d_values_sorted
plt.plot(d_values_sorted, T_trend_values, 'g--', label="Linear trend")

plt.title("Temperature Fit with Seasonal and Solar Components (Gurobi)")
plt.legend()
plt.grid()
plt.show()

plt.savefig("temperature_fit_gurobi.png")
print("Plot saved as 'temperature_fit_gurobi.png'")

temp_change_per_century = x_values[1] * 365.25 * 100
trend = "warming" if temp_change_per_century > 0 else "cooling"
print(f"Temperature change per century: {temp_change_per_century:.2f}°C ({trend})")
