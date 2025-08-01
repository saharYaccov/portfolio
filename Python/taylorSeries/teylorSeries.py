"""
Created on Tue Apr 16 12:19:07 2024

@author: Sahar
"""

'''
This script computes Taylor series expansions for a set of symbolic mathematical functions
using SymPy. For each function, it performs the following steps:

1. Computes the Taylor series around x = 0 up to a given limit (default: 20 terms).
2. Substitutes a specific value (val = 1) into the Taylor series and evaluates the result.
3. Calculates the definite integral of the Taylor series from x = 0 to x = 1.
4. Substitutes the value into the original function to compare real vs. approximated results.
5. Organizes all data (function, Taylor series, real value, integral) into a dictionary.
6. Converts the dictionary to a Pandas DataFrame and saves it as a CSV file ('TScav.csv').

Main functions:
---------------
- getDiffN(curDiff, function): Computes the n-th derivative at x=0.
- calcVal(teylorSeries, val): Substitutes a value into a symbolic expression and evaluates it.
- showTheSeries(string): Formats and prepares the Taylor series as readable text.
- main(limit, function, calcValue): Master function to generate the Taylor series, 
  evaluate it, compute the integral, and return formatted output.
- getIntegralWithBond(a, b, function): Calculates the definite integral between a and b.

Final Output:
-------------
- A CSV file with columns:
  • 'function' - The original function in string form
  • 'taylor series' - The Taylor expansion up to N terms
  • 'real value at x=val' - The actual function value at x=val
  • 'integral between 0 to 1' - The definite integral of the Taylor series from 0 to 1

@author: Sahar
'''


import math
import os

import numpy 
from sympy import Subs , diff , solve , sin , cos , tan , exp , symbols , pi ,log , Eq , sympify , atan
from sympy import acot , asin , acos ,sec , integrate , cosh , sinh 


x=symbols('x')

def getDiffN(curDiff , function):

    f = function
    for i in range (curDiff):
        f = diff(f)
    f = f.subs(x , 0)
    
    
    return f
def calcVal(teylorSeries,val):

    teylorSeries = sympify( teylorSeries )

    teylorSeries = teylorSeries.subs(x,val)
    if not teylorSeries:
        teylorSeries = teylorSeries.subs(x, val+0.000001)
    print(f'RS -----====================================={teylorSeries}')
    return teylorSeries


def showTheSeries(string):
    copyString = string
    #string = string.split("^")
    st_x = ""
    st_without_space=""
    for i in range (len(string)):
        myIndex = string[i]
        st_x += myIndex
        '''if (myIndex[0]=="-"):
            st_x += myIndex
        else:
            st_x += "+"+myIndex'''
        st_x+="\n"
    #print(f'st_without_space :\n{st_without_space}\n')
    for i in range (len(string)) :
        copyString[i] = str(copyString[i]).replace("x**","power(x,")
        copyString[i] = str(copyString[i]).replace(")+","))+")
        st_without_space += str (copyString[i])
        
        
    #print(st_without_space)
    return st_x
            
def main(limit,function , calcValue ):
    try:
        string = ""
        cons_ = []
        for i in range (limit):
            a = getDiffN(i, function)
            cons_.append( eval(str(a/math.factorial(i)))      )
            if(a!=0):
                string += "+ (("+str(a)+")"+ "/" + str(math.factorial(i)) + ")*(x**"+str(i)+")+0^"

        string = string[:-1]
        #string = string.strip("^")
        m=0
        string = string.split("^")
        for i in string:
            m += calcVal(i, calcValue)
        value = m

        print(f'value = {value}')
        print(f'value = {round(value,50)}')

        str_res =  showTheSeries(string)
        print(f'taylor series of {function} until limit={limit-1} =\n{str_res}')
        v= getIntegralWithBond(0 , 1, str_res)
        print(f'your value of bonds : {v}\n')
        print(f'my cons function list :\n{cons_}\n\n')
        print()
        return str_res,v
    except Exception as e:
        print(e)
        return e,'ERROR'

def getIntegralWithBond(a,b , function):
    integral = integrate(function)
    valA = integral.subs(x,a)
    valB = integral.subs(x,b)
    return f'integral bodes {a}-{b} = {round(valB-valA,10)}'


myFun = 1+x**2*sin(x)
myFun2 = sin(x)/(x+1)
f1 = exp(-x) * cos(x)
f2 = 1 / (1 + x**2)
f3 = log(x + 2)
f4 = (x**2 + 1)
f5 = (x**2 + 1)**0.5 * cos(x)
f6 = (x - 1)**2  * exp(-x)
f7 = exp(x)
f8 = (x**2 + 5*x + 6) / (x + 1)
f9 = exp(-sin(x))
f10 = exp(-x**2)

val = 1
res1,v1 = main(20, myFun , val)
res2,v2 = main(20, myFun2 , val)

res3,v3 = main(20, f1, val)
res4,v4 = main(20, f2, val)
res5,v5 = main(20, f3, val)
res6,v6 = main(20, f4, val)
res7,v7 = main(20, f5, val)
res8,v8 = main(20, f6, val)
res9,v9 = main(20, f7, val)
res10,v10 = main(20, f8, val)
res11,v11 = main(20, f9, val)
res12,v12 = main(20, f10, val)


real_v = myFun.subs(x,val)
real_v2 = myFun.subs(x,val)
real_v3  = f1.subs(x, val)
real_v4  = f2.subs(x, val)
real_v5  = f3.subs(x, val)
real_v6  = f4.subs(x, val)
real_v7  = f5.subs(x, val)
real_v8  = f6.subs(x, val)
real_v9  = f7.subs(x, val)
real_v10 = f8.subs(x, val)
real_v11 = f9.subs(x, val)
real_v12 = f10.subs(x, val)

print(f'real value :{real_v}')
print(f'real value :{round(real_v,50)}')
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
    f'integral between 0 to 1':[
        v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12
    ]
}

import pandas as pd
df = pd.DataFrame(dict1)
df.to_csv('TScav.csv')

        

