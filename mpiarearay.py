from mpi4py import MPI
import numpy as np
import matplotlib.pyplot as plt

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size() 

def f(x):
    fxi = np.sqrt(x)*np.sin(x)
    return(fxi)


def integral(a,b,n,h):
    integral = (f(a) + f(b))/2.0
    x = a
    for i in range(1,int(n)):
        x = x + h
        integral = integral + f(x)
    return integral*h
    

a = 1
b = 4
n=10
dest=0
total=0
integral_suma=0.0

h = (b-a)/n 
new_n = n/size 

new_a = a + rank *new_n*h
new_b = new_a + new_n*h

integ=integral(new_a,new_b,new_n,h)

if rank == 0:
    total = integ
    for source in range(1,size):
        integ = comm.recv(source=source)
        print("PE ",rank,"<-",source,",",integ,"\n")
        total = total + integ
else :
    print("maquina ",rank," area: ",integ,"\n")
    comm.send(integ, dest=0)

if (rank == 0):
    print("tramos: ",n)
    print("respuesta: ",total,"\n")
    

muestras = n + 1
xi = np.linspace(a, b, muestras)
fi = f(xi)
    
xig = np.linspace(a, b, muestras * 10)
fig = f(xig)
plt.plot(xig, fig)
# Trapecios
plt.fill_between(xi, 0, fi, color = 'y')
plt.title('Integral: Regla de Trapecios')
for i in range(0, muestras, 1):
    plt.axvline(xi[i], color = 'w')
plt.plot(xi, fi, 'o') 
plt.xlabel('x')
plt.ylabel('f(x)')
plt.savefig("grafica.jpg")
