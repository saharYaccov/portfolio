import numpy as np
import matplotlib.pyplot as plt

# Get user input points
points = []
i = 0
print("Enter 000 to continue to Graph")
num_input = int(input("How many points do you have? "))
mon = -num_input - 1
num_s = 0

while num_s != num_input:
    num_s += 1
    mon += 1
    x = mon
    y = str(input(f"Enter y value for point {i + 1}: "))
    print()
    if y == "000":
        break
    else:
        y = float(y)
    i += 1
    points.append((x, y))

# Create arrays for x and y values
x_values = [p[0] for p in points]
y_values = [p[1] for p in points]

# Generate curve points using numpy's polyfit function
z = np.polyfit(x_values, y_values, 4)
f = np.poly1d(z)
x_curve = np.linspace(min(x_values), max(x_values), 100)
y_curve = f(x_curve)

# Plot the points and curve
plt.plot(x_values, y_values, 'bo', label="User Points")
plt.plot(x_curve, y_curve, 'r-', label="Curve")
plt.legend()
plt.xlabel("x")
plt.ylabel("y")
plt.title("Curve from User Points")

# Display the plot
plt.show()

