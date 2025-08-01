
# Taylor Series Expansion Calculator

This script computes Taylor series expansions for a set of symbolic mathematical functions using SymPy. It evaluates the Taylor series at a specific point, calculates the definite integral of the series over a specified interval, and compares the results with the actual function values. The results are organized into a dictionary and saved as a CSV file.

## Features

- Computes the Taylor series expansion of a function around \( x = 0 \) up to a specified number of terms.
- Evaluates the Taylor series at a specific value.
- Calculates the definite integral of the Taylor series from \( x = 0 \) to \( x = 1 \).
- Compares the Taylor series approximation with the actual function value.
- Saves the results in a CSV file for further analysis.

## Main Functions

- **getDiffN(curDiff, function)**: Computes the \( n \)-th derivative of the function at \( x = 0 \).

- **calcVal(taylorSeries, val)**: Substitutes a value into a symbolic expression and evaluates it.

- **showTheSeries(string)**: Formats and prepares the Taylor series as readable text.

- **main(limit, function, calcValue)**: Master function to generate the Taylor series, evaluate it, compute the integral, and return formatted output.

- **getIntegralWithBond(a, b, function)**: Calculates the definite integral of the function between \( a \) and \( b \).

## Dependencies

- SymPy
- NumPy
- Pandas

## Usage

1. **Define the Functions**: Specify the functions you want to analyze in the script.

2. **Run the Script**: Execute the script in a Python environment where the required dependencies are installed.

3. **View the Results**: The script will output the Taylor series, evaluated results, and integral values. The results will also be saved in a CSV file named `TScav.csv`.

## Example

```python
import math
import numpy as np
from sympy import Subs, diff, sin, cos, tan, exp, symbols, pi, log, Eq, sympify, atan, acot, asin, acos, sec, integrate, cosh, sinh
import pandas as pd

x = symbols('x')

def getDiffN(curDiff, function):
    f = function
    for i in range(curDiff):
        f = diff(f)
    f = f.subs(x, 0)
    return f

def calcVal(taylorSeries, val):
    taylorSeries = sympify(taylorSeries)
    taylorSeries = taylorSeries.subs(x, val)
    if not taylorSeries:
        taylorSeries = taylorSeries.subs(x, val + 0.000001)
    print(f'RS -----====================================={taylorSeries}')
    return taylorSeries

def showTheSeries(string):
    copyString = string
    st_x = ""
    st_without_space = ""
    for i in range(len(string)):
        myIndex = string[i]
        st_x += myIndex
        st_x += "\n"
    for i in range(len(string)):
        copyString[i] = str(copyString[i]).replace("x**", "power(x,")
        copyString[i] = str(copyString[i]).replace(")+", "))+")
        st_without_space += str(copyString[i])
    return st_x

def main(limit, function, calcValue):
    try:
        string = ""
        cons_ = []
        for i in range(limit):
            a = getDiffN(i, function)
            cons_.append(eval(str(a / math.factorial(i))))
            if a != 0:
                string += "+ ((" + str(a) + ")" + "/" + str(math.factorial(i)) + ")*(x**" + str(i) + ")+0^"
        string = string[:-1]
        m = 0
        string = string.split("^")
        for i in string:
            m += calcVal(i, calcValue)
        value = m
        print(f'value = {value}')
        print(f'value = {round(value, 50)}')
        str_res = showTheSeries(string)
        print(f'taylor series of {function} until limit={limit - 1} =\n{str_res}')
        v = getIntegralWithBond(0, 1, str_res)
        print(f'your value of bonds: {v}\n')
        print(f'my cons function list:\n{cons_}\n\n')
        print()
        return str_res, v
    except Exception as e:
        print(e)
        return e, 'ERROR'

def getIntegralWithBond(a, b, function):
    integral = integrate(function)
    valA = integral.subs(x, a)
    valB = integral.subs(x, b)
    return f'integral bounds {a}-{b} = {round(valB - valA, 10)}'

# Define the functions
myFun = 1 + x**2 * sin(x)
myFun2 = sin(x) / (x + 1)
f1 = exp(-x) * cos(x)
f2 = 1 / (1 + x**2)
f3 = log(x + 2)
f4 = (x**2 + 1)
f5 = (x**2 + 1)**0.5 * cos(x)
f6 = (x - 1)**2 * exp(-x)
f7 = exp(x)
f8 = (x**2 + 5 * x + 6) / (x + 1)
f9 = exp(-sin(x))
f10 = exp(-x**2)
val = 1

# Compute Taylor series and integrals
res1, v1 = main(20, myFun, val)
res2, v2 = main(20, myFun2, val)
res3, v3 = main(20, f1, val)
res4, v4 = main(20, f2, val)
res5, v5 = main(20, f3, val)
res6, v6 = main(20, f4, val)
res7, v7 = main(20, f5, val)
res8, v8 = main(20, f6, val)
res9, v9 = main(20, f7, val)
res10, v10 = main(20, f8, val)
res11, v11 = main(20, f9, val)
res12, v12 = main(20, f10, val)

# Compute real values
real_v = myFun.subs(x, val)
real_v2 = myFun2.subs(x, val)
real_v3 = f1.subs(x, val)
real_v4 = f2.subs(x, val)
real_v5 = f3.subs(x, val)
real_v6 = f4.subs(x, val)
real_v7 = f5.subs(x, val)
real_v8 = f6.subs(x, val)
real_v9 = f7.subs(x, val)
real_v10 = f8.subs(x, val)
real_v11 = f9.subs(x, val)
real_v12 = f10.subs(x, val)

print(f'real value: {real_v}')
print(f'real value: {round(real_v, 50)}')

# Organize results into a dictionary and save to CSV
dict1 = {
    'function': [
        str(myFun), str(myFun2),
        str(f1), str(f2), str(f3), str(f4), str(f5),
        str(f6), str(f7), str(f8), str(f9), str(f10)
    ],
    'taylor series': [
        res1, res2,
        res3, res4, res5, res6, res7,
        res8, res9, res10, res11, res12
    ],
    f'real value at x={val}': [
        real_v, real_v2,
        real_v3, real_v4, real_v5, real_v6,
        real_v7, real_v8, real_v9, real_v10, real_v11, real_v12
    ],
    f'integral between 0 to 1': [
        v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12
    ]
}

df = pd.DataFrame(dict1)
df.to_csv('TScav.csv')
Output
The script generates a CSV file named TScav.csv with the following columns:

function: The original function in string form.
taylor series: The Taylor expansion up to ( N ) terms.
real value at ( x = \text{val} ): The actual function value at ( x = \text{val} ).
integral between 0 to 1: The definite integral of the Taylor series from 0 to 1.

Notes

The script uses SymPy for symbolic mathematics and Pandas for data manipulation.
Ensure all dependencies are installed before running the script.
The script can be extended to include additional functions or custom criteria for analysis.

 CopyThis `README.md` provides an overview of the script, its main functions, usage instructions, an
