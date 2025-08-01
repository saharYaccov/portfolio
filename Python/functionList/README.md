# Polynomial Curve Fitting and Visualization

A Python script designed to fit a 4th-degree polynomial curve to user-provided data points using NumPy's polyfit functionality. The script visualizes both the original data points and the fitted curve using Matplotlib, providing a clear graphical representation of the polynomial fit.

## Features

- **User Input Handling**: Prompts the user to input the number of data points and their respective y-values.
- **Automatic X-Value Assignment**: Automatically assigns x-values as sequential integers starting from a negative range based on the number of inputs.
- **Polynomial Curve Fitting**: Utilizes NumPy's `polyfit` to fit a 4th-degree polynomial curve to the input data points.
- **Visualization**: Plots the original data points and the fitted polynomial curve using Matplotlib, with clear labels and a legend.

## Dependencies

- NumPy
- Matplotlib

## Usage

1. **Run the Script**: Execute the script in a Python environment where NumPy and Matplotlib are installed.
2. **Input Data Points**: Follow the prompts to enter the number of data points and their y-values.
3. **View the Plot**: The script will display a plot of the data points and the fitted polynomial curve.

## Example

```plaintext
How many points do you have? 3
Enter y value for point 1: 1
Enter y value for point 2: 4
Enter y value for point 3: 9



<img width="586" height="449" alt="image" src="https://github.com/user-attachments/assets/f2955382-e3f2-4802-976d-dd3d026f16d9" />
