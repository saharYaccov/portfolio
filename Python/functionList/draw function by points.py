##import matplotlib.pyplot as plt
##
### Data
##x_values = [1, 2, 3, 4, 5]
##y_values = [1, 4, 9, 16, 25]
##
### Create a figure and axis
##fig, ax = plt.subplots()
##
### Plot the data
##ax.plot(x_values, y_values)
##
### Set the title and axis labels
##ax.set_title("My Line Graph")
##ax.set_xlabel("X-axis Label")
##ax.set_ylabel("Y-axis Label")
##
### Show the graph
##plt.show()

"""
Polynomial Curve Fitting and Plotting from User Input

@description:
    This script prompts the user to enter a number of (x, y) data points.
    It then fits a 4th-degree polynomial curve to the points using NumPy's polyfit,
    and visualizes both the original points and the smooth fitted curve using Matplotlib.

Libraries:
    - numpy
    - matplotlib.pyplot
    - math (not used, can be removed)

Functionality:
    - Prompts the user to enter how many points to input.
    - Accepts '000' as a signal to stop early.
    - Automatically assigns x-values as sequential integers starting from -N (based on number of inputs).
    - Fits a 4th-degree polynomial curve to the input points.
    - Displays the result as a graph with:
        - Blue dots for user-entered points
        - Red curve for the fitted polynomial
        - Labeled axes and legend

Instructions:
    - Run the script
    - Input the number of points you'd like to enter
    - Provide only y-values (x-values are auto-generated: -N to 0)

Notes:
    - `x=mon` line sets x values automatically from negative range to 0.
    - If you want to manually enter x-values too, comment out `x = mon` and uncomment the input line.

Potential Improvements:
    - Allow full manual (x, y) input
    - Let user choose the polynomial degree
    - Export the fitted function
    - Save the plot as an image

Example Input:
    How point do you have? 3
    Enter y value for point 1: 1
    Enter y value for point 2: 4
    Enter y value for point 3: 9

Output:
    A graph with 3 points and a polynomial curve passing through/near them

"""


import numpy as np
import matplotlib.pyplot as plt
import math


# Get 5 user input points
points=[]
i=0
print("Enter 000 for continue to Graph ")
num_input=int(input("How point do you have? "))
mon=-num_input-1
num_s=0
while num_s!=num_input :
    num_s+=1
    mon+=1
    x=mon
    #x = str(input(f"Enter x value for point {i+1}: "))
    y = str(input(f"Enter y value for point {i+1}: "))
    print()
    if x=="000" or y=="000" :
        break
    else: x=float(x); y=float(y)
    i+=1
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

