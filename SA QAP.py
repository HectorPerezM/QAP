#-*- coding: cp1252 -*-
import numpy
import matplotlib.pyplot as plt
import random
import math

# Funciones

# Función que lee el archivo con los datos
def leeArchivo(nombre):
    nombre = nombre + ".txt"
    archivo = open(nombre,'r')
    matriz = [] 
    fila = []
    for linea in archivo:
        fila = linea.split()
        filaInt = []
        for elemento in fila:
            filaInt.append(int(elemento))
        matriz.append(filaInt)
    archivo.close()
    return matriz


# Función que construye una solución inicial aleatoria 
def solucionInicialAleatoria(instalaciones):
    solucionInicial = list(range(1, instalaciones + 1))
    random.shuffle(solucionInicial)
    return solucionInicial


# Función que evalúa una solución 
def funcionObjetivo(permutacion, matrizF, matrizD):
    n = len(permutacion)
    suma = 0
    for i in range(n):
        #for j in range(n): para toda la matriz
        for j in range(i + 1, n):
            suma = suma + matrizF[i,j] * matrizD[permutacion[i] - 1,permutacion[j] - 1]
    return suma



def generaVecino(vecino):
    i = random.randint(2, len(vecino) - 1)
    j = random.randint(0, len(vecino) - i)
    vecino[j: (j + i)] = reversed(vecino[j: (j + i)])
    return(vecino)
    
def probablidadAceptacion(delta, temperaturaActual):
    probabilidad = math.e ** -(delta/temperaturaActual)
    return probabilidad

# Función que grafica la convergencia del valor objetivo
def graficar(valoresObjetivo, listaMejores, listaProbabilidades, mejorObjetivo):
    plt.figure(1)
    plt.subplot(3, 1, 1)
    graficoMejores = plt.plot(listaMejores)
    plt.setp(graficoMejores,"linestyle","none","marker","s","color","b","markersize","1")
    plt.title(u"Simulated annealing QAP") 
    plt.ylabel(u"Valor objetivo")
    plt.subplot(3, 1, 2)
    grafico = plt.plot(valoresObjetivo)
    plt.setp(grafico,"linestyle","none","marker","s","color","r","markersize","1")
    plt.ylabel(u"Valor actual")
    plt.subplot(3, 1, 3)
    grafico = plt.plot(listaProbabilidades)
    plt.setp(grafico,"linestyle","none","marker","s","color","g","markersize","1")
    plt.ylabel(u"Probabilidad")
    plt.xlabel(u"Valor Óptimo : " + str(mejorObjetivo))
    return True




# Ingreso nombre de archivos
distancias = input('Ingrese nombre del archivo de distancias: ')
flujos = input('Ingrese nombre del archivo de flujos: ')
temperaturaActual = int(input('Ingrese temperatura inicial: '))
temperaturaMinima = int(input('Ingrese temperatura final: '))
estadoEquilibrio = int(input('Ingrese número de iteraciones por estado de equilibrio: '))
enfriamiento = int(input('Seleccione el tipo de enfriamiento \n1 Lineal \n2 Geométrico\n'))
if enfriamiento == 1:
    beta = float(input('Ingrese el valor de beta: '))
else:
    alpha = float(input('Ingrese el valor de alpha: '))


# lectura archivo
matrizD = numpy.array(leeArchivo(distancias))
matrizF = numpy.array(leeArchivo(flujos))

# Solución inicial
solucionInicial = solucionInicialAleatoria(len(matrizD))
solucionActual = solucionInicial.copy() 
mejorSolucion = solucionActual.copy()

objetivoActual = funcionObjetivo(mejorSolucion, matrizF, matrizD)
mejorObjetivo = objetivoActual

listaObjetivos = [objetivoActual]
listaMejores = [objetivoActual]
listaProbabilidades = []


while temperaturaActual > temperaturaMinima:
    i = 0
    while i < estadoEquilibrio:
        solucionCandidata = generaVecino(solucionActual)
        objetivoCandidata = funcionObjetivo(solucionCandidata, matrizF, matrizD)
        delta = objetivoCandidata - objetivoActual     
        if delta < 0:
            solucionActual = solucionCandidata.copy()
            objetivoActual = objetivoCandidata
            if objetivoCandidata < mejorObjetivo:     
                mejorObjetivo = objetivoCandidata
                mejorSolucion = solucionCandidata.copy()
        else:
            probabilidad = probablidadAceptacion(delta, temperaturaActual)
            listaProbabilidades.append(probabilidad)
            if random.random() < probabilidad:
                solucionActual = solucionCandidata.copy()
                objetivoActual = objetivoCandidata
        listaMejores.append(mejorObjetivo)
        listaObjetivos.append(objetivoActual) 
        i = i + 1
    if enfriamiento == 1:
        temperaturaActual = temperaturaActual - beta
    else:
        temperaturaActual = temperaturaActual * alpha 


# Gráficos
graficar(listaObjetivos, listaMejores, listaProbabilidades, mejorObjetivo)
plt.show()




