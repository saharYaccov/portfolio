# Special Prime-Related Numbers Checker

This program identifies "special prime-related numbers" within a specified range based on custom criteria. It includes several functions to check different properties related to prime numbers.

## Main Functions

- **calcPrime(n)**: Checks if the number `n` is prime using an efficient algorithm that tests divisibility up to the square root of `n`.

- **sumSqureNum(num)**: Calculates the sum of the digits of `num` squared, adds 1, and checks if the result is prime. Returns `True` if prime, else `False`.

- **mulTwoAddOne(num)**: Checks if `(num * 2 + 1)` is prime, or if the sum of its digits is prime.

- **mulTwoSubOne(num)**: Checks if `(num * 2 - 1)` is prime, or if the sum of its digits is prime.

- **main(startNum, Lastnum)**: Runs the checks for every number in the range from `startNum` up to `Lastnum`. Prints results and statistics about numbers that pass or fail the criteria.

## Usage

To use this program, simply call the `main` function with the desired range of numbers:

```python
main(startNum, Lastnum)

Identifies numbers: that satisfy custom prime-based properties derived from mathematical expressions.

Example
 CopystartNum = 10
Lastnum = 317
main(startNum, Lastnum)
Notes

The main function can be extended to include additional checks (like mulTwoAddOne and mulTwoSubOne).
Uses numpy for digit sum calculations but can be replaced with simpler built-in functions.
Runtime depends on the size of the input range.

Dependencies

numpy
pyautogui
keyboard
math
datetime

Code
 Copyimport numpy
import pyautogui
import keyboard
import math
import datetime

Lastnum = 317
startNum = 10

def main(startNum, Lastnum):
    startP = datetime.datetime.now()
    lTrue = []
    lFalse = []
    countNoPrime = 0
    for num in range(startNum, Lastnum):
        a = sumSqureNum(num)
        b = mulTwoSubOne(num)
        c = mulTwoAddOne(num)
        if sumSqureNum(num) == True:
            lTrue.append([num, sumSqureNum(num)])
            print(f'{num} is factor prime - {sum(numpy.array(list(str(num**2)), dtype=int))} is prime by SqureSumDigits')

        else:
            lFalse.append(num)
            countNoPrime += 1

    endP = datetime.datetime.now()
    print(f'time work - {endP - startP}')
    print(f'in range 2-{Lastnum} has {countNoPrime} not prime')
    print(f'percent - {round(countNoPrime / (Lastnum - 2), 5)}%')

def calcPrime(lastNum):
    if lastNum == 2 or lastNum == 3 or lastNum == 5:
        return True
    if int(str(lastNum)[-1]) in {2, 4, 6, 8, 0}:
        return False
    if sum(numpy.array(list(str(lastNum)), dtype=int)) % 3 == 0:
        return False
    if int(str(lastNum)[-1]) == 5:
        return False
    else:
        for j in range(7, int(lastNum**0.5), 2):
            if lastNum % j == 0:
                return False
        return True

def mulTwoAddOne(num):
    if calcPrime(num * 2 + 1):
        return True
    elif calcPrime(sum(numpy.array(list(str(num * 2 + 1)), dtype=int))):
        return True
    else:
        return False

def mulTwoSubOne(num):
    if calcPrime(num * 2 - 1):
        return True
    elif calcPrime(sum(numpy.array(list(str(num * 2 - 1)), dtype=int))):
        return True
    else:
        return False

def sumSqureNum(num):
    if calcPrime(sum(numpy.array(list(str(num**2)), dtype=int)) + 1):
        return True
    else:
        return False

main(startNum, Lastnum)
Potential Improvements

Allow users to input the range interactively.
Add more custom prime-related checks.
Optimize the prime-checking algorithm for better performance.

 CopyThis `README.md` provides an overview of the program, its main functions, usage instructions, and an example of how to run the script. You can copy this content into a `README.md` file in your project directory.
