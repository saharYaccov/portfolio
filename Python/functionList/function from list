import numpy as np
import matplotlib.pyplot as plt
import math
import random

#mathod for divide
def divide(xx):
    xx = xx.split("/")
    xx = int(xx[0])/int(xx[1])
    print(f'choose : x= {xx}')
    return xx
#mathod for sqr 
def sqr(xx):
    sqrt= float(input ("                      which sqrt ? ")) 
    xx = xx.split("(")
    xx = xx[1]
    xx= float(xx [:-1])
    xx = math.pow(xx, 1/sqrt)
    print(f'                      choose : x={xx}')
    return xx

def create_scatter(data_List_X_Y , nameXAxis , nameYAxis , nameSaveAndType) : # [[1,2,3],[4,5,2]]
    x = data_List_X_Y[0]
    y = data_List_X_Y[1]
    if len(x)!=len(y): 
        if len(x)>len(y):
            dif = len(x) - len(y)
            for i in range (dif):
                x.remove(x[-i])
        if len(x)<len(y):
            dif = -(len(x) - len(y))
            for i in range (dif):
                y.remove(y[-i])
    print(x[::-1])
    print(y[::-1])
    plt.scatter(x, y )
    plt.xlabel(nameXAxis)
    plt.ylabel(nameYAxis)
    plt.title('scatter of points')
    plt.grid()
    #plt.savefig(nameSaveAndType)
    plt.show()

    print("Done")
    
    
def create_plot(data_List_X_Y): # [[1,2,3],[4,5,2]]
    x = data_List_X_Y[0]
    y = data_List_X_Y[1]
    if len(x)!=len(y): 
        if len(x)>len(y):
            dif = len(x) - len(y)
            for i in range (dif):
                x.remove(x[-i])
        if len(x)<len(y):
            dif = -(len(x) - len(y))
            for i in range (dif):
                y.remove(y[-i])
    #print(x)
    #print(y)
    color = ["b","p",'y','g','b','r','s','g']
    line = ['--','+','*']
    rand = random.randint(0, len(color)-2)
    plt.plot_date(x, y, color[rand] )
    #print(color[rand])

    
    plt.xlabel('xAxis')
    plt.ylabel('yAxis')
    plt.title('function of points')
    plt.grid()
    plt.show()
    print("Done")


def a():
    series=[]
    mone=int(input("How much num in series? "))
    for i in range (mone):
        xx=(input("number to series- "))              #  אפשר לשנות לקלוט את הסדרה כפרמטר
        
        if "/" in xx : xx = divide(xx)                #  זוהי שליחה לפונקציית חילוק
        
        elif "sqrt" in xx : xx = sqr(xx)              # זוהי שליחה לפונקציית שורש מסדר איקס
            
        series.append(float(xx))
                       
     #מציאת מקדמי המספרים
    list_1=[]
    add_list_1=[]

    for i in range (len(series)): 
        for j in range (len(series)):
            list_1.append(i**j)
        #print(list_1) # מטריצה המקדמים של המערכת משוואות
        add_list_1.append(list_1)
        list_1=[]
    #print(add_list_1) # חיבורם לליסט


    #השמה במטריצה
    ans=[]
    matrix_1=np.array(add_list_1)
    for num in series:
        ans.append([num])
    #print(ans) # מספרי המשתמש 
    ans_series=np.array(ans)
    #print(ans_series) # מספרי משתמש במטריצת עמודה
    #print(matrix_1) # מטריצת מקדמים של המערכת משוואות


    #פתרון מטריצה
    answer=np.dot(np.linalg.inv(matrix_1),ans_series)
         
    #print(answer) #פתונות המערכת משוואות בתור ליסט של נאמפי
    
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
    print("function is",st)


    #תוצאות שונות של הסדרה
    st=st[5:]
    for num in st:
        if num=="^":
            st=st.replace(num,"**")
    save_st=st
    
    pointNum = 12
    arrNumpy_x= np.ones(pointNum)
    arrNumpy_y = np.ones(pointNum)
    for j in range (0,pointNum,1):
        
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
        arrNumpy_x[j] = j
        arrNumpy_y[j] = a
        print("f(",j,")=",a )
    #print(arrNumpy_x)
    #print(arrNumpy_y)
    st=save_st
    create_scatter([arrNumpy_x , arrNumpy_y], 'series to function', 'result', 'seriesToFunction.pdf')
    create_plot([arrNumpy_x , arrNumpy_y])
    
a()





