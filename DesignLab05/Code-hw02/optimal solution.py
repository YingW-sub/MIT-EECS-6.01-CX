import lib601.optimize as optimize


def f1(x):
    return x*x-x

def f2(x):
    return x**5-7*x**3+6*x**2+2

def Finder(f,xmin,xmax,numXsteps):
    print (optimize.optOverLine(f,xmin,xmax,numXsteps))

Finder(f1,-5,5,1000)
Finder(f2,1,2,100)

