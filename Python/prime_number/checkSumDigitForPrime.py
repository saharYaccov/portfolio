
'''
Program to check for "special prime-related numbers" within a given range based on custom criteria.

Main Functions:

- calcPrime(n):
    Checks if the number n is prime.
    Uses an efficient algorithm that tests divisibility up to the square root of n.

- sumSqureNum(num):
    Calculates the sum of the digits of num squared, adds 1, and checks if the result is prime.
    Returns True if prime, else False.

- mulTwoAddOne(num):
    Checks if (num * 2 + 1) is prime, or if the sum of its digits is prime.

- mulTwoSubOne(num):
    Checks if (num * 2 - 1) is prime, or if the sum of its digits is prime.

- main(startNum, Lastnum):
    Runs the checks for every number in the range from startNum up to Lastnum.
    Prints results and statistics about numbers that pass or fail the criteria.

Usage:

- Identifies numbers that satisfy custom prime-based properties derived from mathematical expressions.

Notes:

- The main function can be extended to include additional checks (like mulTwoAddOne and mulTwoSubOne).
- Uses numpy for digit sum calculations but can be replaced with simpler built-in functions.
- Runtime depends on the size of the input range.

'''


import numpy
import pyautogui
import keyboard
import math
import datetime
Lastnum=317
startNum=10
def main(startNum , Lastnum):
    startP = datetime.datetime.now()
    lTrue = []
    lFalse = []
    countNoPrime = 0
    for num in range (startNum,Lastnum):
        a = sumSqureNum(num)
        b = mulTwoSubOne(num)
        c = mulTwoAddOne(num)
        if    ( sumSqureNum(num)       ==True) :
            lTrue.append([num,sumSqureNum(num)])
            print (f'{num} is factor prime - { sum(numpy.array(list(str(num**2)),dtype=int)) } is prime by SqureSumDigits')
            
        #if ( mulTwoSubOne(num)     == True) :
         #   lTrue.append([ num,mulTwoSubOne(num) ])
          #  print (f'{num} is factor prime - {num*2 -1} is prime by MultiplyTwoSubOne')
            
        #if ( mulTwoAddOne(num)     == True) :
         #   lTrue.append([ num,mulTwoAddOne(num) ])
          #  print (f'{num} is factor prime - {num*2 +1} is prime by MultiplyTwoAddOne')
        else :
            #print(f'--------------------- {num} - cant Know it ---------------------------------')
            lFalse.append(num)
            countNoPrime += 1
        #print("\n")
    endP = datetime.datetime.now()
    print(f'time work - {endP-startP}')
    print(f'in range 2-{Lastnum} has {countNoPrime} not prime')
    print(f'percent - {round(countNoPrime/(Lastnum-2),5)}%')
    #print(f'{lFalse}\n')
            
        
def calcPrime(lastNum):
    if (lastNum==2 or lastNum==3 or lastNum==5): return True
    if(int(str(lastNum)[-1])==2 or int(str(lastNum)[-1])==4 or int(str(lastNum)[-1])==6 or int(str(lastNum)[-1])==8 or int(str(lastNum)[-1])==0): return False
    if( sum(numpy.array(list(str(lastNum)),dtype=int)) %3 == 0 ): return False
    if ( int(str(lastNum)[-1])==5) : return False
    
    else:
        for j in range (7,int(lastNum**0.5),2):
            if(lastNum%j==0):return False
        return True
    
def mulTwoAddOne(num):
    if( calcPrime( num*2 +1) ==True) :return True
    elif( calcPrime( sum(numpy.array(list(str(num*2+1)),dtype=int))) == True ) : return True
    else : return False
    
def mulTwoSubOne(num):
    if( calcPrime(num*2 -1) == True ) :return True
    elif( calcPrime( sum(numpy.array(list(str(num*2-1)),dtype=int))) == True ) : return True
    else: return False
    
def sumSqureNum(num):
    if( calcPrime( sum(numpy.array(list(str(num**2)),dtype=int)+1) ) == True ) : return True # sum([1,9,6]+1)
    #elif( calcPrime( sum(numpy.array(list(str(num)),dtype=int)) ) == True ) : return True
    #elif( calcPrime( sum(numpy.array(list(str(num*2)),dtype=int)) ) == True ) : return True
    #elif( calcPrime( sum(numpy.array(list(str(num)),dtype=int))+1) == True ) : return True
    else : return False

#for i in range (1,10):
  #  main(M*i*i)
main(startNum,Lastnum)
#main(M*4)
#mainPrime(5)




    
