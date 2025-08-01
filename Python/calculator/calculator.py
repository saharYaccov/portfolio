'''
This script implements a versatile GUI calculator application using Tkinter, SymPy, NumPy, Matplotlib, PyAutoGUI and other libraries.
It supports standard arithmetic, scientific operations, symbolic derivatives & integrals, Taylor series plotting, polynomial solving,
matrix determinants, complex number handling, base conversions, Riemann sums, 2D/3D plotting, and custom constants.

Core Features:
--------------
1. **Basic & Scientific Calculations**  
   - Buttons for digits, operators (+, –, ×, ÷, %, ^)  
   - Trigonometric functions (sin, cos, arctan) with Taylor-series approximations  
   - Logarithm (ln), exponentials (eˣ), π constant insertion  
   - Factorial via SciPy’s Gamma function  
   - Nth-root extraction with user-specified root

2. **Symbolic & Numeric Analysis**  
   - `derivative(x)`: Numerical derivative at a user-given point using h→0 limit  
   - Taylor series expansion and plotting for inputs containing ‘x’  
   - 3D surface plotting of SymPy expressions via Matplotlib/`sympy.plotting`

3. **Polynomial & Matrix Solvers**  
   - Quadratic (`huarizmi()`) and cubic (`tartaglia()`) equation solvers via SymPy  
   - Determinant of 3×3 and 4×4 matrices with user prompts

4. **Complex Number Utilities**  
   - Input complex numbers, extract real/imaginary parts  
   - Polar form conversion (r·e^{iθ})

5. **Data & Plotting**  
   - 2D function plotting (`plt(x_list, y_list, label)`)  
   - Riemann sum approximation of definite integrals  
   - Automatic screen prompts for ranges, step sizes via PyAutoGUI

6. **Custom Constants**  
   - Store up to three user-defined constants (A, B, C) and reuse in calculations

7. **User Interface**  
   - Responsive Tkinter grid of buttons, real‑time display updates  
   - Pop‑up dialogs for variable input, confirmation prompts

Dependencies:
-------------
- tkinter  
- pyautogui  
- sympy  
- numpy  
- scipy  
- matplotlib  
- keyboard  
- bidi & arabic_reshaper (if RTL support needed)  

Usage:
------
Run the script to launch the calculator window. Click buttons or use prompts for advanced operations.
@author: Sahar
'''



import tkinter
from tkinter import messagebox
import tkinter as tk
import pyautogui
import math
import keyboard
import numpy
import matplotlib.pyplot as plt
import matplotlib
import sympy as sp
constant1 = 0 # constant 1
constant2 = 0 # constant 2
constant3 = 0 # constant 3
value=""      # current value in screen
ans=0         # answer
trigVal=""
################################################################################################
#constant saver
def saveConst1(x):
    global constant1
    if ("=" in  x):
        x=x.replace("=","")
    constant1 = x
    button_Del(value)
def Addconstant1():
    global constant1
    button_clicked(constant1)
    
def saveConst2(x):
    global constant2
    if ("=" in  x):
        x=x.replace("=","")
    constant2 = x
    button_Del(value)
def Addconstant2():
    global constant2
    button_clicked(constant2)
    
def saveConst3(x):
    global constant3
    if ("=" in  x):
        x=x.replace("=","")
    constant3 = x
    button_Del(value)
def Addconstant3():
    global constant3
    button_clicked(constant3)
################################################################################################


#sqrt method
def sqrt(x):
    global value
    if ("=" in x):
        x=x.replace("=","")
    power = float(pyautogui.prompt(text="Choose root "))
    if ("x" in x):
        value= str(x)+"^(1/"+str(power)+")"
        equal(str(x)+"^(1/"+str(power)+")")
    else:
        x=eval (x)
        value = str(  round(math.pow(x , 1/power) , 5)  )
        equal( round (math.pow(x , 1/power), 5 )  )
#################################################################################################

#plot 2d method
def plt(xP,yP,fun):
    matplotlib.pyplot.plot(xP,yP)
    matplotlib.pyplot.title("function : "+fun)
    matplotlib.pyplot.xlabel("Xaxis")
    matplotlib.pyplot.ylabel("Yaxis")
    #color
    matplotlib.pyplot.plot(xP, yP, color='blue', linestyle='dashed', marker='1', label=fun,)
    #lines
    matplotlib.pyplot.grid(True)
    #lims
    #matplotlib.pyplot.xlim(-5,5)
    #matplotlib.pyplot.ylim(-5,5)
    
    matplotlib.pyplot.show()
################################################################################################

#factorial method
import scipy
def factorial(x): #3.5
    global value

    a = scipy.special.gamma(float(x))
    equal(str(round(a,5)))
    value= str(round(a,5))
#################################################################################################

#polinomial method 2nd
def huarizmi():
    a=int( pyautogui.prompt(text="a= "))
    b=int(pyautogui.prompt(text="b= "))
    c= int(pyautogui.prompt(text="c= "))
    x = sp.symbols('x')
    tar = a*x**2 + b*x + c
    x = sp.solve(tar, x)

    t= tkinter.Tk()
    t.geometry= ("500X500")
    label = tkinter.Label(t,text =x,font=("ariel",20))
    label.pack()
################################################################################################

#polinomial method 3rd
import math
def tartaglia() :
    a=int( pyautogui.prompt(text="a= ")) #1
    b= int( pyautogui.prompt(text="b= ")) #3
    c= int( pyautogui.prompt(text="c= ")) #3
    d= int( pyautogui.prompt(text="d= ")) #1

    x = sp.symbols('x')
    tar = a*x**3 + b*x**2 + c*x + d
    x = sp.solve(tar, x)
    '''
    shlis=float(1/3)
    tar = str(a)+"x^3"+"+"+str(b)+"x^2"+"+"+str(c)+"x"+"+"+str(d)
            
    q= ( (3*a*c- b**2) / (3*a)**2 )
    r= (9*a*b*c - 27*d*a**2 -2*b**3)/ (54*a**3)
    s= ( r +(q**3 +r**2)**0.5 )** (1/3)
    t=- q/s

   # print( ( "x1= " ) , (s+t)- ((b)/(a*3)) )
    x1=(s+t)- ((b)/(a*3))
    #x2=print( ( "x2= " ) , (-0.5*(s+t) - ((b)/(3*a)) + 1j*math.sqrt(0.75)* (s-t)))
    x2=(-0.5*(s+t) - ((b)/(3*a)) + 1j*math.sqrt(0.75)* (s-t))
    #x3=print( ( "x3= " ) , (-0.5*(s+t) - ((b)/(3*a)) - 1j* math.sqrt(0.75)* (s-t)))
    x3=(-0.5*(s+t) - ((b)/(3*a)) - 1j* math.sqrt(0.75)* (s-t))
'''
    t= tkinter.Tk()
    t.geometry= ("500X500")
    label = tkinter.Label(t,text =f'{tar} =0\n {x}',font=("ariel",20))
    label.pack()
##########################################################################################

#delete digit from screen
def DelDigit():
    global value
    z = int(pyautogui.prompt(text="digit number : "))
    value=value.replace(value[z-1] , "")
    equal(value)
##########################################################################################

#create function plot 2d plot
def function(function):
    #function=input("press some function with x")
    answer= ""
    a=0
    k=0
    #s= pyautogui.prompt(title="function",text=" press the starting point ") #2            starting
    #f= pyautogui.prompt(title="function",text="press the finish point ") #5               finish
    s=0
    f=20
    ju=pyautogui.prompt(title="function",text="Jumper ") #0.1 ,n= 1 / 0.1     jump
    #ju = 1
    
    const= int((float(f)-float(s))/float(ju) +1) # culcaulet tho distance

    
    xList=[]
    yList=[]
    if ("^" in function):
        function=function.replace("^","**")
    for i in range (int(f)*2+1): # the num of return (5-3)*n +1
        try:
            currentNum=int(s)+k # start poind add k
            fu = ( function.replace("x",str(currentNum) ) )  # function in f(x)#############################
        #print(fu)
        #print( "f(",currentNum, ")=",eval(fu))    # return (5-3)*n +1 times
            k+=float(ju)  # first k add jump
            answer +="f("+str(currentNum)+ ")="+str(eval(fu))+"\n"    
            xList.append(i)
            yList.append(eval(fu))
        except ZeroDivisionError as e :
            print("your x="+str(i)+ " value cannot be placed because it is an asymptote / hole in the function")
            print("f("+str(i)+") isn't exiest")
            print(e)
        
    t = tkinter.Tk()
    t.geometry= ("500X500")
    label = tkinter.Label(t,text = answer,font=("ariel",10))
    label.pack()
    plt(xList,yList,function)
    #button_Del(value)
################################################################################################################################
def button_saveAns(x):
    global value
    global ans
    #value
    value = value.replace("=","")
    ans = value
    value=""
    lab = tkinter.Label(root,text="",width=12 , height=3)
    lab.grid(row="0",column="0",columnspan=3)
    
def button_useAns(x):
    global ans
    global value
    #value=""
    lab = tkinter.Label(root,text="",width=12 , height=3)
    lab.grid(row="0",column="0",columnspan=3)
    
    button_clicked(ans)
    #value+=+str(ans)
################################################################################################################################

#got the derivative
def derivative(x):
    global value
    if "^" in x:
        x=x.replace("^","**")
        #print(fun)

    print(sp.diff(x ,))
    true=True
    while (true==True):
        str_x=str(x)                # " 5x+4 "
        h_value=str_x.replace("x","(x+h)")# " 5(x+h)+4 "
        str_value=str_x.replace( "x","x" )
        mone_value=h_value+"-"+"("+str(str_x)+")"

        #print("LIMIT ; h -> 0")
        #print("the define of derivative is")
        #print(mone_value)                      #  5(x+h)+4 - ( 5x+4 )
        #print("-"*len(mone_fun))             #  -------------------
        #print(h.center(int(len(mone_fun))))  #           h

        define= "("+mone_value+")"+"/"+"h"
        x_value=int(pyautogui.prompt(title="derivative",text = "for some X you want slope(שיפוע)") )#8
        if (x_value>=0): y=define.replace( "x",str(x_value) )
        elif (x_value<0): y=define.replace( "x","("+str(x_value)+")" )
        z=y.replace( "h","0.0000001")
        result = round(eval(z),5)
        t= tkinter.Tk()
        t.geometry= ("500X500")
        label = tkinter.Label(t,text = "derivative for function "+str(x)+" in point "+str(x_value)+" = "+str(result),font=("ariel",20))
        label.pack()
    
        true=False
        #button_Del(x)
    xList=[]
    yList=[]
    d0= define.replace("h","0.00001")
    for point in range (30):
        try:
            yList.append( eval ( d0.replace("x",str(point)) )  )
            xList.append( point )
        except ZeroDivisionError as e:
            print(e)
    plt(xList , yList , "d/dx("+x+")")
################################################################################################################

def button_DelLast(x):
    global value
    lab = tkinter.Label(root,text=str(value)[0:len(value)-1],width=12 , height=3,font=("Helvetica",15,"bold"))
    lab.grid(row="0",column="0",columnspan=3)
    value=str(value)[0:len(value)-1]
def button_Del(x):
    global value
    global ans
    ans=value
    value=""
    lab = tkinter.Label(root,text="",width=12 , height=3)
    lab.grid(row="0",column="0",columnspan=3)

def shift(z):
    x=3
    y=10
    t= tkinter.Tk()
    t.geometry("500x380")
    t.title("arcsin / arccos ?")
    l=tkinter.Label(t,text="arcsin / arccos ?",width=15,height=x,font=("ariel", 20),bg="green")
    l.grid(row=0,column=0)
    asin = tkinter.Button(t, text="arcsin", command=lambda: (arcsin(z),t.destroy()), width=y,height=x,font=("ariel", 20),bg="gray")
    asin.grid(row=1,column=0)

    acos = tkinter.Button(t, text="arccos", command=lambda: (arccos(z),t.destroy()), width=y,height=x, font=("ariel", 20),bg="gray")
    acos.grid(row=1,column=1)
def cheak_pi(res):
    global value
    mon=0
    for i in range(1,20):
        whole_V = i*eval(res) /math.pi
        #print(i,") ",whole_V," - ",whole_V%1)
        if( whole_V.is_integer()  or 0.999<whole_V%1 <=1.01 or 0<whole_V%1 <=0.001 ):
            mon=1
            break
    if (mon==1 ):
    
        a =" π/"+str(i) 
        equal(a  )
        return a
    elif (res=="1"):
        a =" π/2" 
        equal(a  )
        return a
    elif (res=="-1"):
        a =" -π/2"
        equal(a  )
        return a
    else:
        equal( value )
        #print(value)
        return (res)

################################################################################################
#trigonometry functions
def arcsin(z):
    global value
    '''
    if (float(z)>1.0 or float(z)<-1.0):
        tkinter.messagebox.showerror(message="No value")
        equal("No value")
        return "no value"
    res = ""
    for asin in range (70):
        asin=int( asin )
        dem = (4**asin)*(2*asin+1)*(math.factorial(asin)**2)
        mathod  = str ( math.factorial(2*asin) ) + "*(" +str(1/dem)+")"+"*"+"(x)"+"**"+str(2*asin+1)+"+"
        res+= str(mathod)
    res= res[0:len(res)-1]
    res = res.replace("x",z)
    '''
    try:
        value = sp.asin(z)
        x = sp.symbols('x')
        taylor_s = sp.series(value, x, 0, 5)
        res = str(taylor_s)
        equal = value
        print(value)
        if ( "x" in z ):
            a = messagebox.askyesno( "Confirmation", "Draw your function?" )
            if (a) :
                function( res )
            else :
                value = res
                equal("arcsin ("+str(z)+")" )
        else:
            value= str ( round(eval(res)  , 5 ) )
    except Exception as e:
        print("f("+str(z)+") isn't exiest")
        return "no value"
    cheak_pi(value)
def arccos(z):
    global value
    res = ""
    for asin in range (80):
        asin=int( asin )
        dem = (4**asin)*(2*asin+1)*(math.factorial(asin)**2)
        mathod  = str ( math.factorial(2*asin) ) + "*(" +str(1/dem)+")"+"*"+"(x)"+"**"+str(2*asin+1)+"+"
        res+= str(mathod)
    res= res[0:len(res)-1]
    res = res.replace("x",z)
    
    if ( "x" in z ):
        a = messagebox.askyesno( "Confirmation", "Draw your function?" )
        if (a) :
            function( res )
        else :
            value = res
            equal("arccos ("+str(z)+")" )
    else:
        value= str (round(1.5708 - eval(res) , 5 )  )
    cheak_pi(value)       
################################################################################################
def sin(z):
    global value
    global trigVal
    
    res=""
    for sin in range (80):
        sin=int( sin )
        mathod = str((-1)**sin) +"*"+ str(1/math.factorial(2*sin +1) ) +"*"+"x**"+str(2*sin+1)+"+"
        res+= str(mathod)    
    res= res[0:len(res)-1]
    res = res.replace("x",z)
    trigVal=res
    
    if ( "x" in z ):
        a = messagebox.askyesno( "Confirmation", "Draw your function?" )
        button_Del(value)
        if (a) :
            #button_Del(value)
            function( res )
        else :
            value = "("+res+")"
            equal("sin("+str(z)+")") 
    else:
        value = str( round( math.sin(float(z)*math.pi/180) , 5)   )
        #print(str(res)+"="+str(eval(res)))
        #for i in range(1,20):
          #  if( math.sin(float(z)) /math.pi == 1/i):                                #evilable in arc
            #    equal("~ pi/"+str(i)  )
              #  break
        cheak_pi(value)
        #equal("~ "+value  )
        
    
    
def cos(z):
    global value
    res = ""
    for sin in range (10):
        sin=int( sin )
        mathod = str((-1)**sin) +"*"+ str(1/ math.factorial((2*sin ))  ) +"*"+"x**"+str(2*sin)+"+"
        res+= str(mathod)    
    res= res[0:len(res)-1]
    #res = res.replace("x",z)
    trigVal=res
    if ( "x" in z ):
        a = messagebox.askyesno( "Confirmation", "Draw your function?" )
        if (a) :
            button_Del(value)
            function( res )
        else :
            value = res
            equal("cos("+str(z)+")" )
    else:
        value= str(round( math.cos(float(z)*math.pi/180) , 5) )                                             #evilable in arc
        #for i in range(1,20):
          #  if( math.sin(float(z)*math.pi/180) /math.pi == 1/i):
            #    equal("~ pi/"+str(i)  )
              #  break
        cheak_pi(value) 

        
def arctan(z):
    global value
    res = ""
    for tan in range (60):
        tan=int( tan )
        mathod = "(-1)**"+str(tan)+"*"+str(1 / (2*tan +1)  ) +"*(x)**"+str(1+2*tan)+"+"
        res+= str(mathod)
    res= res[0:len(res)-1]
    res = res.replace("x",z)
    
    if ( "x" in z ):
        a = messagebox.askyesno( "Confirmation", "Draw your function?" )
        if (a) :
            function( res )
        else :
            value = res
            equal("Atan("+str(z)+")" )
    else:
        value= str (  round( math.atan(eval(z)) , 5  )   )
        mon=0
    cheak_pi(value)

################################################################################################
def ln_e(z):
     global value


     res = ""
     for ln in range (1,700):
         mathod = "(-1)**"+str(ln-1)+"*"+str(1/ln  ) +"*(x)**"+str(ln)+"+"
         res+= str(mathod)
     res= res[0:len(res)-1]
     
     if ("x" in z):
         value= res
         equal(value)
     else:
         A=sp.ln(z)
         A = str(round(A,5))
         value = A
         equal(A)
         '''
         z=str( int(z)-1 )
         res = res.replace("x",z)
    
         if ( "x" in z ):
             a = messagebox.askyesno( "Confirmation", "Draw your function?" )
             if (a) :
                 function( res )
             else :
                 value = res
                 equal("ln("+str(z)+")" )
         else:
             print(z)
             print(res)
             a=eval(res)
             value=str(round(eval(res),5))
             equal( "~"+str(round (a,5)) )
             #print(round (a,5))
'''
def button_clicked(x):
    global value
    if(x=="="):
        value=str(round(eval(value),5))
        equal( value)
    value+=str(x)
    if ("=" in value):
        value=value.replace("=","")
    lab = tkinter.Label(root,text=str(value),width=12 , height=3,font=("Helvetica",15,"bold"))
    lab.grid(row="0",column="0",columnspan=3)


# view answer in the screen
def equal(x):
    try:
        lab = tkinter.Label(root,text=x,compound='center',width=12 , height=3, font=("Helvetica",15,"bold"))
        lab.grid(row="0",column="0",columnspan=3)
    except ArithmeticError as e :
        print(e)
        print("Error ")
    except Exception as e :
        print(e)
        print("Error ")
###########################################################################################

# function to draw function
def functionMathod():
    series=[]
    mone=int(pyautogui.prompt("How much number - ") )
    for i in range (mone):
        xx=pyautogui.prompt("number "+str(i)+"-")              #  אפשר לשנות לקלוט את הסדרה כפרמטר
        series.append(float(xx))
                                
     #מציאת מקדמי המספרים
    list_1=[]
    add_list_1=[]

    for i in range (len(series)): 
        for j in range (len(series)):
            list_1.append(i**j)
        #print(list_1)
        add_list_1.append(list_1)
        list_1=[]
    #print(add_list_1)


    #השמה במטריצה
    ans=[]
    matrix_1=numpy.array(add_list_1)
    for num in series:
        ans.append([num])
    #print(ans)
    ans_series=numpy.array(ans)
    #print(ans_series)
    #print(matrix_1)


    #פתרון מטריצה
    answer=numpy.dot(numpy.linalg.inv(matrix_1),ans_series)
         
    #print(answer)
    
    #הדפסת סיום-פונקציה שמקיימת את הסדרה
    length=len(series)
    mone=0
    st="f(x)="
    for i in range (length):
        mone+=1
        power=mone
        par=round(float(answer[i]),6)
        st+=str(par)+"x^"+str(power-1)+" +"
    st=st[:len(st)-1]
    #print(st)
    #print(mone)
    
    #סידור הפונקציה
    if ( "-[+"in st   or   "+[-"in st ) :
        st=st.replace("-[+","-")
        st=st.replace("+[-","-")
    if ( "-+"in st   or   "+-"in st ) :
        st=st.replace("-+","-")
        st=st.replace("+-","-")
    if ("["in st     or    "]"in st )   :
        st=st.replace("[","")
        st=st.replace("]","")
    if ".x^0" in st:
        st=st.replace(".x^0","")
    if "x^0" in st:
        st=st.replace("x^0","")
#    if "x^1" in st :
 #       st=st.replace("x^1","x")

        
    length2=len(st)
    st+="120"
    st=st[:len(st)-3]
    #print("series is",series)
    #print("function is",st)
    t= tkinter.Tk()
    t.geometry= ("500X500")
    label = tkinter.Label(t,text =str(st),font=("ariel",20))
    label.pack()


    #תוצאות שונות של הסדרה
    st=st[5:]
    for num in st:
        if num=="^":
            st=st.replace(num,"**")
    save_st=st
    
    for j in range (0,15,1):
        a=eval(st.replace("x","*"+str(j)))
        MulInTen=str(int(10*a))
        
        if (MulInTen[-1]=="0"):
            a=int(a)
        elif (MulInTen[-1]=="9"):
            a=int(a+1)
        else:
            a=a

        if (j>5 and MulInTen[-1]!="9"):
            a=int(a)
        elif (j>5 and MulInTen[-1]=="9"):
            a=int(a+1)
        print("f(",j,")=",a )
        label2 = tkinter.Label(t,text ="f("+str(j)+")="+str(a),font=("ariel",20))
        label2.pack()
    st=save_st

#matrix solve
def d2(num, l1, l2):
    #print(l1," || ",l2)
    mon_plus = l1[0] * l2[1]
    mon_minus = -l1[1] * l2[0]
    return num * (mon_plus + mon_minus)

def det3():
    l=[]
    lHelp=[]
    for i in range (3) :
        z=pyautogui.prompt(text="add digit "+str(i+1))
        lHelp.append(int(z))
    l.append(lHelp)
    lHelp=[]
    for i in range (3) :
        z=pyautogui.prompt(text="add digit "+str(i+5))
        lHelp.append(int(z))
    l.append(lHelp)
    lHelp=[]
    for i in range (3) :
        z=pyautogui.prompt(text="add digit "+str(i+9))
        lHelp.append(int(z))
    l.append(lHelp)
    lHelp=[]
    
    a = d2(l[0][0], [l[1][1], l[1][2]], [l[2][1], l[2][2]])
    b = d2(-1 * l[0][1], [l[1][0], l[1][2]], [l[2][0], l[2][2]])
    c = d2(l[0][2], [l[1][0], l[1][1]], [l[2][0], l[2][1]])
    equal(a + b + c)

    t= tkinter.Tk()
    t.geometry= ("500X500")
    label = tkinter.Label(t,text =str(l[0])+"\n"+str(l[1])+"\n"+str(l[2]),font=("ariel",20))
    label.pack()

def d3(num , l1 , l2 ,l3):
    #print("number mul =",num)
    #print("d3-",l1,"\n",l2,"\n",l3 )
    a = d2(l1[0], [l2[1], l2[2]], [l3[1], l3[2]]) *num
    bMinus = d2( -l1[1] ,[l2[0], l2[2]], [l3[0], l3[2]]) *num
    c = d2(l1[2], [l2[0], l2[1]], [l3[0], l3[1]]) *num
    return(a+bMinus+c)
#[1,2,3]
#[4,5,3]
#[9,8,1]
def det4():
    l=[]
    lHelp=[]
    for i in range (4) :
        z=pyautogui.prompt(text="add digit "+str(i+1))
        lHelp.append(int(z))
    l.append(lHelp)
    lHelp=[]
    for i in range (4) :
        z=pyautogui.prompt(text="add digit "+str(i+5))
        lHelp.append(int(z))
    l.append(lHelp)
    lHelp=[]
    for i in range (4) :
        z=pyautogui.prompt(text="add digit "+str(i+9))
        lHelp.append(int(z))
    l.append(lHelp)
    lHelp=[]
    for i in range (4) :
        z=pyautogui.prompt(text="add digit "+str(i+13))
        lHelp.append(int(z))
    l.append(lHelp)
    
        
    a = d3(l[0][0], [l[1][1], l[1][2], l[1][3]], [l[2][1], l[2][2], l[2][3]], [l[3][1], l[3][2], l[3][3]])
    bM = d3(-1 * l[0][1], [l[1][0], l[1][2], l[1][3]], [l[2][0], l[2][2], l[2][3]], [l[3][0], l[3][2], l[3][3]])
    c = d3(l[0][2], [l[1][0], l[1][1], l[1][3]], [l[2][0], l[2][1], l[2][3]], [l[3][0], l[3][1], l[3][3]])
    dM = d3(-1 * l[0][3], [l[1][0], l[1][1], l[1][2]], [l[2][0], l[2][1], l[2][2]], [l[3][0], l[3][1], l[3][2]])
    equal(str(a + bM + c +dM))
    t= tkinter.Tk()
    t.geometry= ("500X500")
    label = tkinter.Label(t,text =str(l[0])+"\n"+str(l[1])+"\n"+str(l[2])+"\n"+str(l[3]),font=("ariel",20))
    label.pack()
    
def Complex_I(x):
    global value
    lab = tkinter.Label(root,text=str(x+"j")  ,width=12 , height=3,font=("Helvetica",15,"bold"))
    lab.grid(row="0",column="0",columnspan = 3)
    value +="j"
    print(value)

def Complex_solve(complex_):
    global value
    try:
        comp = eval((complex_))
        C= Complex_digit(complex_)
        R= Real_digit(complex_)
        lab = tkinter.Label(root,text=str(complex(float(R),float(C)))  ,width=12 , height=3,font=("Helvetica",15,"bold"))
        lab.grid(row="0",column="0",columnspan = 3)
        value = str(comp)
    except Exception as e :
        button_Del(2)
        equal(e)
        print(e)
def Complex_digit(C):
    global value
    x = round( numpy.imag(eval(C)) , 5)
    value=str(round(x,5))
    equal(x)
    return value

def Real_digit(C):
    global value
    x = round( numpy.real( eval(C) ) , 5)
    value=str(round(x,5))
    equal(x)
    return value
def polar_form(complex_):
    global value
    R = Real_digit(complex_)
    C= Complex_digit(complex_)
    value = complex_
    equal(value)
    radius =( float(R)**2+float(C)**2  )**0.5 
    angel = round( math.atan( float(C) / float(R) ) , 5)
    #piValue = cheak_pi (str(angel))
    a=tkinter.messagebox.showinfo("Answer" , "~"+str(round( radius ,5 ))+"e^("+str(angel)+"i)")
    #a.show()
    #equal("~"+str(round( radius ,5 ))+"e^("+str(angel)+"i)")
    #value = complex_
    #equal(value)
import sympy as sp
def plot3D_sympy(fun):
    a=-10
    b=10
    try:
        x , y = sp.symbols('x y')
        function = sp.sympify(fun)
        sp.plotting.plot3d(function, (x, float(a), float(b)), (y, float(a), float(b)) , title = f'f(x,y) = {function}'  )
        plt.show()
    except Exception as e:
        print(e)
def Button_Base(x):
    global value
    prom = pyautogui.prompt(title = "Changge base ",text = "Add base - ")
    strNumBase = numpy.base_repr(int(x),int (prom)  )
    equal( strNumBase )
    value = strNumBase

def integral_reimmanSum(x): #x^3+2*x^2
    global value
    mon=0
    Area=0
    n=4000
    a = pyautogui.prompt(title = "Limit A ",text = "press limit a - ")
    b = pyautogui.prompt(title = "Limit B ",text = "press limit b - ")
    disAB = (float(b)-float(a))/n
    for reimanSum in range (1,n):
        YvalueForm = x.replace ("x","("+str(a)+"+"+str(reimanSum)+"*(("+b+"-"+a+")/"+str(n)+"))")
        YvalueForm = YvalueForm.replace("^","**")
        try:
            phrase= eval(YvalueForm)*disAB
        except Exception as e:
            equal("DNE")
            value= "DNE"
            mon+=1
        Area+=phrase
    if (mon==0) :
        value = str(Area)
        equal(str(round(Area,3)))


    
geo = 500
root = tk.Tk()
root.geometry(str(geo*3)+"x"+str(geo*2))
root.title(" ~made by : Sahar~   calculetor" )
root.option_add('*TButton*font', ('Helvetica', 15, 'bold'))


w=geo//30 
h=5
lab = tkinter.Label(root,text="  ",width=20 , height=5,font=("Helvetica" , 3,"bold"))
lab.grid(row="0",column="2",columnspan=3)
font = ("algerian",12, "bold")

#0
button_0 = tkinter.Button(root , text="0" , command=lambda: button_clicked("0"), width=w , height=h,bg="yellow", font=font)
button_0.grid(row="4",column="0")
#1
button_1 = tkinter.Button(root , text="1" , command=lambda: button_clicked("1"),width=w , height=h,bg="yellow", font=font)
button_1.grid(row="1",column="0")
#2
button_2 = tkinter.Button(root , text="2" , command=lambda: button_clicked("2") , width=w, height=h,bg="yellow", font=font)
button_2.grid(row="1",column="1")
#3
button_3 = tkinter.Button(root , text="3" , command=lambda: button_clicked("3"),width=w , height=h,bg="yellow", font=font)
button_3.grid(row="1",column="2")
#4
button_4 = tkinter.Button(root , text="4" , command=lambda: button_clicked("4") , width=w , height=h,bg="yellow", font=font)
button_4.grid(row="2",column="0")
#5
button_5 = tkinter.Button(root , text="5" , command=lambda: button_clicked("5"),width=w , height=h,bg="yellow", font=font)
button_5.grid(row="2",column="1")
#6
button_6 = tkinter.Button(root , text="6" , command=lambda: button_clicked("6") , width=w, height=h,bg="yellow", font=font)
button_6.grid(row="2",column="2")
#7
button_7 = tkinter.Button(root , text="7" , command=lambda: button_clicked("7"),width=w , height=h,bg="yellow", font=font)
button_7.grid(row="3",column="0")
#8
button_8 = tkinter.Button(root , text="8" , command=lambda: button_clicked("8") , width=w , height=h,bg="yellow", font=font)
button_8.grid(row="3",column="1")
#9
button_9 = tkinter.Button(root , text="9" , command=lambda: button_clicked("9") , width=w , height=h,bg="yellow", font=font)
button_9.grid(row="3",column="2")
#=
button_equal = tkinter.Button(root , text="=" , command=lambda: button_clicked("=") , width=w , height=h,bg="white", font=font)
button_equal.grid(row="4",column="2")
#+
button_plus= tkinter.Button(root , text="+" , command=lambda: button_clicked("+") , width=w , height=h,bg="gold", font=font)
button_plus.grid(row="3",column="3")
#-
button_minus = tkinter.Button(root , text="-" , command=lambda: button_clicked("-") , width=w , height=h,bg="gold", font=font)
button_minus.grid(row="3",column="4")
#*
button_mul = tkinter.Button(root , text="*" , command=lambda: button_clicked("*") , width=w , height=h,bg="gold", font=font)
button_mul.grid(row="2",column="3")
#/
button_devide = tkinter.Button(root , text="/" , command=lambda: button_clicked("/") , width=w , height=h,bg="gold", font=font)
button_devide.grid(row="2",column="4")
#%
button_mod = tkinter.Button(root , text="%" , command=lambda: button_clicked("%") , width=w , height=h,bg="gold", font=font)
button_mod.grid(row="3",column="5")
#cos
button_cos = tkinter.Button(root , text="cos" , command=lambda:  cos(value) , width=w , height=h,bg="silver", font=font)
button_cos.grid(row="6",column="7")
#sin
button_sin = tkinter.Button(root , text="sin" , command=lambda:  sin(value) , width=w , height=h,bg="silver", font=font)
button_sin.grid(row="6",column="5")
#arctan
button_arctan = tkinter.Button(root , text="arctan" , command=lambda: arctan(value) , width=w , height=h,bg="silver", font=font)
button_arctan.grid(row="6",column="6")
#shift
button_tan = tkinter.Button(root , text="Shift" , command=lambda: shift(value) , width=w , height=h,bg="gray", font=font)
button_tan.grid(row="0",column="5")
#pi
button_pi = tkinter.Button(root , text="π" , command=lambda: button_clicked(str(round(math.pi,5))) , width=w , height=h,bg="blue", font=font)
button_pi.grid(row="5",column="7")
#e
button_e = tkinter.Button(root , text="e" , command=lambda: button_clicked(str(round(math.e,3))) , width=w , height=h,bg="blue", font=font)
button_e.grid(row="5",column="6")
#ln
button_ln = tkinter.Button(root , text="ln" , command=lambda: ln_e(str(value)) , width=w , height=h,bg="blue", font=font)
button_ln.grid(row="5",column="5")
#(
button_r = tkinter.Button(root , text="(" , command=lambda: button_clicked("(") , width=w , height=h,bg="gray", font=font)
button_r.grid(row="5",column="0")
#)
button_l = tkinter.Button(root , text=")" , command=lambda: button_clicked(")") , width=w , height=h,bg="gray", font=font)
button_l.grid(row="5",column="1")
#AC
button_ac = tkinter.Button(root , text="AC" , command=lambda: button_Del("AC") , width=w , height=h,bg="red", font=font)
button_ac.grid(row="1",column="4")
#del
button_ac = tkinter.Button(root , text="del" , command=lambda: button_DelLast("del") , width=w , height=h,bg="gray", font=font)
button_ac.grid(row="1",column="3")
#derivative
button_exit = tkinter.Button(root , text="d/dx" , command=lambda: derivative(str(value)) , width=w , height=h,bg="gray", font=font)
button_exit.grid(row="1",column="5")
#^
button_pow= tkinter.Button(root , text="^" , command=lambda: button_clicked("^") , width=w , height=h,bg="gold", font=font)
button_pow.grid(row="2",column="5")
#x
button_deri = tkinter.Button(root , text="x" , command=lambda: button_clicked("x") , width=w , height=h,bg="gray", font=font)
button_deri.grid(row="5",column="2")
#y
button_deri = tkinter.Button(root , text="y" , command=lambda: button_clicked("y") , width=w , height=h,bg="gray", font=font)
button_deri.grid(row="8",column="0")
#.
button_dot = tkinter.Button(root , text="." , command=lambda: button_clicked(".") , width=w , height=h,bg="yellow", font=font)
button_dot.grid(row="4",column="1")
#saveAns
button_Ans = tkinter.Button(root , text="saveAns" , command=lambda: button_saveAns(value) , width=w , height=h,bg="pink", font=font)
button_Ans.grid(row="7",column="2")
#useAns
button_Ans = tkinter.Button(root , text="useAns" , command=lambda: button_useAns(ans) , width=w , height=h,bg="pink", font=font)
button_Ans.grid(row="7",column="3")
#function
button_function = tkinter.Button(root , text="function" , command=lambda: function(value), width=w , height=h,bg="gray", font=font)
button_function.grid(row="4",column="5")
#delDig
button_delDig = tkinter.Button(root , text="delete digit" , command=lambda: DelDigit(), width=w , height=h,bg="gray", font=font)
button_delDig.grid(row="0",column="3")
#squere
button_squere = tkinter.Button(root , text="x^2 solve" , command=lambda: huarizmi(), width=w, height=h,bg="green", font=font)
button_squere.grid(row="6",column="0")
#tarteglia
button_tr = tkinter.Button(root , text="x^3 solve" , command=lambda: tartaglia(), width=w, height=h,bg="green", font=font)
button_tr.grid(row="6",column="1")
#factorial
button_fact = tkinter.Button(root , text="Factorial" , command=lambda: factorial(value), width=w, height=h,bg="pink", font=font)
button_fact.grid(row="7",column="4")
#sqrt
button_sqrt= tkinter.Button(root , text="sqrt" , command=lambda: sqrt(value), width=w, height=h,bg="pink", font=font)
button_sqrt.grid(row="0",column="4")

#determinant 3 
button_det3 = tkinter.Button(root , text="Det -3-" , command=lambda: det3(), width=w, height=h,bg="green", font=font)
button_det3.grid(row="7",column="0")
#determinant 4
button_det4 = tkinter.Button(root , text="Det -4-" , command=lambda: det4(), width=w, height=h,bg="green", font=font)
button_det4.grid(row="7",column="1")
#Saveconstant1
button_Saveconstant1 = tkinter.Button(root , text="Save A" , command=lambda: saveConst1(str(value) ), width=w, height=h,bg="green", font=font)
button_Saveconstant1.grid(row="2",column="6")
#saveconstant2
button_Saveconstant2 = tkinter.Button(root , text="Save B" , command=lambda: saveConst2(str(value) ), width=w, height=h,bg="green", font=font)
button_Saveconstant2.grid(row="3",column="6")
#saveconstant3
button_Saveconstant3 = tkinter.Button(root , text="Save C" , command=lambda: saveConst3(str(value)), width=w, height=h,bg="green", font=font)
button_Saveconstant3.grid(row="4",column="6")

#Addconstant1
button_addconstant1 = tkinter.Button(root , text="Use A" , command=lambda: Addconstant1( ), width=w, height=h,bg="green", font=font)
button_addconstant1.grid(row="2",column="7")
#Addconstant2
button_addconstant2 = tkinter.Button(root , text="Use B" , command=lambda: Addconstant2( ), width=w, height=h,bg="green", font=font)
button_addconstant2.grid(row="3",column="7")
#Addconstant3
button_addconstant3 = tkinter.Button(root , text="Use C" , command=lambda: Addconstant3( ), width=w, height=h,bg="green", font=font)
button_addconstant3.grid(row="4",column="7")
#functionMathod
button_functionMathod = tkinter.Button(root , text="functionMathod" , command=lambda: functionMathod( ), width=w, height=h,bg="green", font=font)
button_functionMathod.grid(row="6",column="2")
#i
button_i = tkinter.Button(root , text="i" , command=lambda: Complex_I(value), width=w, height=h,bg="gold", font=font)
button_i.grid(row="4",column="3")
#Complex_solve
button_Complex_solve = tkinter.Button(root , text="Complex Solve" , command=lambda: Complex_solve(value), width=w, height=h,bg="white", font=font)
button_Complex_solve.grid(row="5",column="3")
#Complex_digit
button_Complex_digit = tkinter.Button(root , text="Complex Digit" , command=lambda: Complex_digit(value), width=w, height=h,bg="gold", font=font)
button_Complex_digit.grid(row="5",column="4")
#Real_digit
button_Real_digit = tkinter.Button(root , text="Real Digit" , command=lambda: Real_digit(value), width=w, height=h,bg="gold", font=font)
button_Real_digit.grid(row="4",column="4")
#polar_form
button_polar_form = tkinter.Button(root , text="Polar Form" , command=lambda: polar_form(value), width=w, height=h,bg="gold", font=font)
button_polar_form.grid(row="6",column="3")
#base
button_Base = tkinter.Button(root , text="Base" , command=lambda: Button_Base(value), width=w, height=h,bg="pink", font=font)
button_Base.grid(row="7",column="5")
#integral - reimman sum
button_integral = tkinter.Button(root , text="integral" , command=lambda: integral_reimmanSum(value), width=w, height=h,bg="pink", font=font)
button_integral.grid(row="7",column="6")
#3D plot
button_integral = tkinter.Button(root , text="plot3D" , command=lambda: plot3D_sympy(value), width=w, height=h,bg="white", font=font)
button_integral.grid(row="8",column="1")

root.mainloop()
                

