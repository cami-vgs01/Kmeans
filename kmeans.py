from tkinter import filedialog
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import scipy.spatial.distance as dist
import numpy as np
import seaborn as sns

dataframe = pd.DataFrame()
def lecturaArchivo():

    global dataframe
    archivo_csv = filedialog.askopenfilename(filetypes=[("Archivo CSV", "*.csv")])
    # Leer el archivo CSV seleccionado
    try:
        dataframe.drop(index=dataframe.index, columns=dataframe.columns, inplace=True)
        datos = pd.read_csv(archivo_csv, header=None)
        dataframe = pd.concat([dataframe, datos], ignore_index=True)
        dataframe=dataframe.iloc[1:]
        for i in range(0, dataframe.shape[1]):
            dataframe = dataframe.rename(columns={i: "X" + str(i)})
        dataframe = dataframe.astype(float)
        print("Datos ingresados correctamente")
        return dataframe
    except FileNotFoundError:
        print("No se eligió el archivo")


def kmeans(k, centroides):
    num_filas, num_columnas = dataframe.shape
    print("Numero de variables: ", num_columnas)
    datosGrupar = None
    cont = 0

    while True:
        cont += 1
        if centroides is None:
            #Tomar los centroides iniciales de manera aleatoria y almacenarlos los restantes en otro
            """centroides = dataframe.sample(k)
            datosGrupar = dataframe.drop(centroides.index)"""
            #Toma los centroides iniciales de manera ordenada del dataframe
            indice = int(dataframe.shape[0]-k)
            centroides = dataframe.head(k)
            datosGrupar = dataframe.tail(indice)

            if num_columnas <3:
                plt.scatter(x=datosGrupar.iloc[:,0], y=datosGrupar.iloc[:,1],c='blue')
                plt.scatter(x=centroides.iloc[:,0], y=centroides.iloc[:,1], c='red')
                plt.legend(['Observaciones','Centroides'])
                plt.show()
            elif num_columnas == 3:
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                ax.scatter(xs=datosGrupar.iloc[:,0], ys=datosGrupar.iloc[:,1], zs=datosGrupar.iloc[:,2], c='blue')
                ax.scatter(xs=centroides.iloc[:,0], ys=centroides.iloc[:,1], zs=centroides.iloc[:,2], c='red')
                plt.legend(['Observaciones','Centroides'])
                plt.show()
        #calculamos la distancia con cada dato de los datosGrupar con cada centroide
        datosGrupar_resultado = datosGrupar.copy()  # Crear una copia de datosGrupar para almacenar los resultados
        for i in range(0, centroides.shape[0]):
            distancia = []  # Reiniciar la lista en cada iteración del bucle exterior
            for j in range(0, datosGrupar.shape[0]):
                distancia.append(dist.euclidean(centroides.iloc[i, :].values, datosGrupar.iloc[j, :].values))
            datosGrupar_resultado['DistanciaCentroide' + str(i)] = distancia

        print("Distancias de las observaciones con cada centroide")
        # Encontrar el índice del centroide más cercano para cada fila con axis=1
        datosGrupar_resultado['Grupo'] = np.argmin(datosGrupar_resultado.iloc[:, num_columnas:].values, axis=1)
        print(datosGrupar_resultado.iloc[:, num_columnas:])
        nombre_ultima_columna = datosGrupar_resultado.columns[-1]
        palette = sns.color_palette("bright", len(datosGrupar_resultado[nombre_ultima_columna].unique()))
        color_dict = dict(zip(datosGrupar_resultado[nombre_ultima_columna].unique(), palette))
        nombres_columnas = list(dataframe.columns)
        if num_columnas <3:
            dibujar2D(centroides,nombres_columnas,datosGrupar_resultado, color_dict, nombre_ultima_columna)
        elif num_columnas == 3:
            dibujar3D(centroides,nombres_columnas,datosGrupar_resultado,nombre_ultima_columna)
        # Calcular los nuevos centroides
        centroides_nuevos = datosGrupar_resultado.groupby(['Grupo']).mean().iloc[:, :num_columnas]
        print("Nuevos centroides")
        # Comprobar si los centroides han cambiado
        if centroides.equals(centroides_nuevos):
            print("Los centroides no han cambiado")
            print("El algoritmo ha convergido en la iteración: ", cont)
            break
        else:
            print("Los centroides han cambiado")
            centroides=centroides_nuevos
    print(centroides)
    return centroides

def datoAGrupar(centroides):
    print(centroides)
    if centroides is None:
        print("No se han calculado los centroides")
        return
    else:
        dato = input("Ingrese dato a agrupar separado por comas: ")
        dato = dato.split(",")
        dato = [float(i) for i in dato]
        print(dato)
        distancia = []
        for i in range(0, centroides.shape[0]):
            distancia.append(dist.euclidean(centroides.iloc[i, :].values, dato))
        print(distancia)
        grupo = np.argmin(distancia)
        print("El dato pertenece al grupo: ", grupo)


def dibujar2D(centroides,nombres_columnas,datosGrupar_resultado,color_dict, nombre_ultima_columna):
    sns.scatterplot(x=nombres_columnas[0], y=nombres_columnas[1], hue=nombre_ultima_columna, data=datosGrupar_resultado, palette=color_dict)
    plt.scatter(datosGrupar_resultado.iloc[:,0], datosGrupar_resultado.iloc[:,1], c=datosGrupar_resultado[nombre_ultima_columna].apply(lambda x: color_dict[x]), marker='s')
    plt.scatter(x=centroides.iloc[:, 0], y=centroides.iloc[:, 1], c='black')
    plt.show()


def dibujar3D(centroides,nombres_columnas,datosGrupar_resultado,nombre_ultima_columna):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    clases = datosGrupar_resultado[nombre_ultima_columna].unique()
    color_dict = {clase: np.random.rand(3,) for clase in clases} # generamos un diccionario con un color aleatorio por cada clase
    for clase, color in color_dict.items():
        temp_df = datosGrupar_resultado[datosGrupar_resultado[nombre_ultima_columna] == clase]
        ax.scatter(temp_df[nombres_columnas[0]], temp_df[nombres_columnas[1]], temp_df[nombres_columnas[2]], color=color, marker='s', label=str(clase))
    ax.scatter(xs=centroides[nombres_columnas[0]],ys=centroides[nombres_columnas[1]],zs=centroides[nombres_columnas[2]],c='black')
    ax.set_xlabel(nombres_columnas[0])
    ax.set_ylabel(nombres_columnas[1])
    ax.set_zlabel(nombres_columnas[2])
    plt.legend()
    plt.show()

def menu():
    centroides = None
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
                    centroides=kmeans(k, centroides)
                except Exception as e:
                    print(e)
                    print("No se ingresó un valor de k correcto")
            elif opc == 4:
                pass
                datoAGrupar(centroides)
            elif opc == 5:
                print("Finalizando...")
                break
        except ValueError:
            print("Opcion invalida")

menu()