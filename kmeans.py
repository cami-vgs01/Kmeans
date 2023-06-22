import random
from collections import Counter
from tkinter import filedialog
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import scipy.spatial.distance as dist

dataframe = pd.DataFrame()
def lecturaArchivo():

    global dataframe
    archivo_csv = filedialog.askopenfilename(filetypes=[("Archivo CSV", "*.csv")])
    # Leer el archivo CSV seleccionado
    try:
        dataframe.drop(index=dataframe.index, columns=dataframe.columns, inplace=True)
        datos = pd.read_csv(archivo_csv)
        dataframe = pd.concat([dataframe, datos], ignore_index=True)
        print("Datos ingresados correctamente")
        return dataframe
    except FileNotFoundError:
        print("No se eligió el archivo")


def kmeans(k):
    num_filas, num_columnas = dataframe.shape
    print("Numero de variables: ", num_columnas)
    #Tomar los centroides iniciales de manera aleatoria y almacenarlos los restantes en otro
    """centroides = dataframe.sample(k)
    datosGrupar = dataframe.drop(centroides.index)"""
    #Toma los centroides iniciales de manera ordenada del dataframe
    indice = int(dataframe.shape[0]-k)
    centroides = dataframe.head(k)
    datosGrupar = dataframe.tail(indice)
    if num_columnas <3:
        dibujar2D(centroides,datosGrupar)
    elif num_columnas == 3:
        dibujar3D(centroides,datosGrupar)
    #calculamos la distancia con cada dato de los datosGrupar con cada centroide
    datosGrupar_resultado = datosGrupar.copy()  # Crear una copia de datosGrupar para almacenar los resultados
    for i in range(0, centroides.shape[0]):
        distancia = []  # Reiniciar la lista en cada iteración del bucle exterior
        for j in range(0, datosGrupar.shape[0]):
            distancia.append(dist.euclidean(centroides.iloc[i, :].values, datosGrupar.iloc[j, :].values))
        datosGrupar_resultado['DistanciaCentroide' + str(i)] = distancia

    print("Distancias de las observaciones con cada centroide")
    print(datosGrupar_resultado.iloc[:, 2:])

def dibujar2D(centroides,datosGrupar):
    plt.scatter(x=datosGrupar.iloc[:,0], y=datosGrupar.iloc[:,1],c='blue')
    plt.scatter(x=centroides.iloc[:,0], y=centroides.iloc[:,1], c='red')
    plt.legend(['Observaciones','Centroides'])
    plt.show()

def dibujar3D(centroides,datosGrupar):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(xs=datosGrupar.iloc[:,0], ys=datosGrupar.iloc[:,1], zs=datosGrupar.iloc[:,2], c='blue')
    ax.scatter(xs=centroides.iloc[:,0], ys=centroides.iloc[:,1], zs=centroides.iloc[:,2], c='red')
    plt.legend(['Observaciones','Centroides'])
    plt.show()

def menu():
    mejorK = 0
    while True:
        print("*******************Algoritmo de K-Means*******************")
        print("1. Ingresar datos desde archivo .csv")
        print("2. Mostrar Datos")
        print("3. Calcular K-Means")
        print("4. Predecir nuevo dato")
        print("5. Salir")
        try:
            opc = int(input("Opcion: "))
            if opc == 1:
                try:
                    dataframe.drop(index=dataframe.index, columns=dataframe.columns, inplace=True)
                    # Crear la ventana principal
                    root = tk.Tk()
                    # Agregar un botón para abrir el cuadro de diálogo de selección de archivos
                    boton_abrir = tk.Button(root, text="Abrir archivo CSV", command=lecturaArchivo)
                    boton_abrir.pack()
                    # Mostrar la ventana principal
                    root.mainloop()
                except:
                    print("No se eligió el archivo")
            elif opc == 2:
                print(dataframe)
            elif opc == 3:
                try:
                    k = int(input("Ingrese el valor de k: "))
                    kmeans(k)
                except:
                    print("No se ingresó un valor de k correcto")
            elif opc == 4:
                pass
                #predecirClasificacion(mejorK)
            elif opc == 5:
                print("Finalizando...")
                break
        except ValueError:
            print("Opcion invalida")

menu()