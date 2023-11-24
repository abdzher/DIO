''' ======================= SOLUCION POR METODO DE JORDAN ======================= '''
''' =======================       - VERSION 0.5 -         ======================= '''


import numpy as np
#import sympy as sp
import pandas as pd


# Variables globales que se usan solo si se eligio obtener cada iteracion.
desarrollo = False
iteracion = 0
resultado = np.array([0,0])
n_decimales = 3
simbol = False
iniciado_desde_listas = False
log = ''


def iniciar_desde_texto(texto = '', mostrar_desarrollo = False, simbolico = False, numero_de_decimales = 3):
    '''
    """
    INICIAR DESDE TEXTO: Lee una cadena de texto, se tienen que hacer separaciones con coma y punto y coma.
    
    Args:
        texto(str) : Cadena de texto que se leera para obtener los datos.
        mostrar_desarrollo(bool) : True o False, si se coloca True entonces se mostraran todas las iteraciones del programa.
        simbolico(bool) : True o False, si se coloca True entonces se usaran matematicas simbolicas, es decir, los cocientes se expresaran como tal, en cambio, con False se usaran valores decimales.
        numero_de_decimales(int): Indica la cantidad de decimales que se mostraran en caso de elegir trabajar con decimales.
    
    Returns:
        Llama a la funcion 'iniciar' para continuar el programa.
    """
    
    '''
    global log
    log = ''
    
    if simbolico == False:
        try:
            lista = np.mat(texto)
        except SyntaxError:
            log += '\n = Los datos indicados no son validos ='
        except ValueError:
            log += '\n = Los datos indicados no son validos ='
        else:
            try:
                mtrx = np.array(lista, dtype=float)
            except ValueError:
                log += '\n = Los datos indicados no son validos ='
            else:
                iniciar(mtrx, mostrar_desarrollo, simbolico, numero_de_decimales)
    elif simbolico == True:
        try:
            #mtrx = sp.Matrix([list(map(int, fila.split(','))) for fila in texto.split(';')])
        #except SyntaxError:
            log += '\n = Los datos indicados no son validos ='
        except ValueError:
            log += '\n = Los datos indicados no son validos ='
        else:
            try:
                temp = np.array(mtrx, dtype=float)
            except ValueError:
                log += '\n = Los datos indicados no son validos ='
            else:
                iniciar(mtrx, mostrar_desarrollo, simbolico, numero_de_decimales)


def iniciar_desde_csv(ubicacion, mostrar_desarrollo = False, simbolico = False, numero_de_decimales = 3):
    """
    INICIAR DESDE CSV: Obtiene un archivo csv dada una ubicacion, luego esta sera convertida en un archivo array o matriz segun lo elegido.
    
    Args:
        ubicacion(str) : Cadena de texto que indica donde se encuentra el archivo requerido, se debe tener especial cuidado con indicarlo correctamente.
        mostrar_desarrollo(bool) : True o False, si se coloca True entonces se mostraran todas las iteraciones del programa.
        simbolico(bool) : True o False, si se coloca True entonces se usaran matematicas simbolicas, es decir, los cocientes se expresaran como tal, en cambio, con False se usaran valores decimales.
        numero_de_decimales(int): Indica la cantidad de decimales que se mostraran en caso de elegir trabajar con decimales.
    
    Returns:
        Llama a la funcion 'iniciar' para continuar el programa.
    """

    global log
    log = ''
    log += f'======= Se importara el archivo {ubicacion} =========\n\n'
    
    try:
        archivo = pd.read_csv(ubicacion)
    except FileNotFoundError:
        log += f'{ubicacion} no es un directorio de archivo valido'
    else:
        a, b = archivo.shape
        
        listas = []

        for j in range(1,a):
            lista = []
            for i in range(1,b):
                lista.append(archivo.iloc[j,i])
            listas.append(lista)

        if simbolico == False:
            mtrx = np.array(listas, dtype=float)
            iniciar(mtrx, mostrar_desarrollo, simbolico, numero_de_decimales)
        
        #elif simbolico == True:
            #mtrx = sp.Matrix(listas)
            #iniciar(mtrx, mostrar_desarrollo, simbolico, numero_de_decimales)
        

def iniciar_desde_listas(lista = [], mostrar_desarrollo = False, simbolico = False, numero_de_decimales = 3):
    """
    INICIAR DESDE LISTAS: Obtiene una lista de listas, luego esta sera convertida en un archivo array o matriz segun lo elegido.
    
    Args:
        lista(list) : Lista que contiene las listas con los valores deseados.
        mostrar_desarrollo(bool) : True o False, si se coloca True entonces se mostraran todas las iteraciones del programa.
        simbolico(bool) : True o False, si se coloca True entonces se usaran matematicas simbolicas, es decir, los cocientes se expresaran como tal, en cambio, con False se usaran valores decimales.
        numero_de_decimales(int): Indica la cantidad de decimales que se mostraran en caso de elegir trabajar con decimales.
    
    Returns:
        Llama a la funcion 'iniciar' para continuar el programa.
    """
    global iniciado_desde_listas
    iniciado_desde_listas = True
    global log
    log = ''
    
    a = len(lista[0])
    for i in lista:
        b = len(i)
        if a != b:
            log += 'Los elementos de la lista tienen diferentes longitudes, intente otra vez.\n'
            exit()
    
    if simbolico == False:
        mtrx = np.array(lista, dtype=float)
        iniciar(mtrx, mostrar_desarrollo, simbolico, numero_de_decimales)
    
    #elif simbolico == True:
        #mtrx = sp.Matrix(lista)
        #iniciar(mtrx, mostrar_desarrollo, simbolico, numero_de_decimales)
            



    
def iniciar(mtrx, mostrar_desarrollo=False, simbolico = False, numero_de_decimales = 3):
    """
    INICIAR: Inicia el programa, obtiene el numero de hileras y de columnas.
    
    Args:
        mtrx(array o matrix): En este espacio se coloca la matriz a operar, ya sea del tipo array (numpy) o matrix (sympy) para el uso de matematicas simbolicas.
        mostrar_desarrollo(bool) : True o False, si se coloca True entonces se mostraran todas las iteraciones del programa
    
    Returns:
        Llama a la funcion 'comprobar_resultado' para continuar el programa.
    """
    
    global desarrollo
    global log
    global iteracion
    iteracion = 0
    desarrollo = mostrar_desarrollo
    
    global n_decimales
    n_decimales = numero_de_decimales
    np.set_printoptions(suppress=True, precision = n_decimales)
    
    global simbol
    simbol = simbolico
    
    m = mtrx.shape[0] - 1 # Num de hileras
    n = mtrx.shape[1] - 1 # Num de columnas
    
    log += '====== EL PROCESO SERA INICIADO =======\n'
    log += f'La matriz inicial es \n{np.array(mtrx, dtype = str)}\n'
    log += f'La matriz es de {m+1}X{n+1}\n'
    
    if desarrollo == True: log += 'Se mostrara cada iteracion del programa\n'
    if simbolico == True: log += 'Se usaran matematicas simbolicas\n'
    else: log += f'Se usaran valores decimales con {n_decimales} de precision\n'
    
    obtener_indice(mtrx,m,n)
    
    
    

def obtener_indice(mtrx,m,n):
    """
    OBTENER INDICE: Funcion para obtener la columna con valor negativo en Z.
    
    Args:
        mtrx(array o matrix): En este espacio se coloca la matriz a operar, ya sea del tipo array (numpy) o matrix (sympy) para el uso de matematicas simbolicas.
        m(int) : Valor entero que indica el numero de hileras de la matriz menos 1, para asi tener la correcta indexacion.
        n(int) : Valor entero que indica el numero de columnas de la matriz menos 1, para asi tener la correcta indexacion.
    
    Returns:
        Llama a la funcion 'obtener_pivote' para continuar el programa.
    """
    
    resultados = []
    indice = -1
    
    for i in range(0,n): resultados.append(mtrx[m,i])
    
    for i in resultados: 
        if i < 0:
            indice = resultados.index(i)
            break
        
    if indice == -1: final(mtrx)
    else: obtener_pivote(indice,mtrx,m,n)



def obtener_pivote(indice,mtrx,m,n):
    """
    OBTENER PIVOTE: Funcion para obtener el pivote bajo el principio de que resulte en el minimo cociente.
    
    Args:
        indice(int) : Se trata de la columna con valor negativo en Z, este va a ser la base para buscar el cociente minimo
        mtrx(array o matrix): En este espacio se coloca la matriz a operar, ya sea del tipo array (numpy) o matrix (sympy) para el uso de matematicas simbolicas.
        m(int) : Valor entero que indica el numero de hileras de la matriz menos 1, para asi tener la correcta indexacion.
        n(int) : Valor entero que indica el numero de columnas de la matriz menos 1, para asi tener la correcta indexacion.
    
    Returns:
        Llama a la funcion 'resolver' para continuar el programa.
    """
    
    global desarrollo
    global iteracion
    global log
    
    iteracion += 1
    lista = []
    
    
    for i in range(0,m):
        if mtrx[i,indice] <= 0:
            lista.append(999999999999999999999999999999999999)
            continue
        lista.append(mtrx[i,n]/mtrx[i,indice])
    
    try:
        r = lista.index(min(lista))
    except TypeError:
        log += '=== SE HAN INDICADO VALORES NO NUMERICOS PARA LA MATRIZ ===\n'
        exit()
    
    if desarrollo == True: 
        log += f'\n==== Iteracion numero: {iteracion}\nEl pivote elegido es: \n({r},{indice}) con valor {mtrx[r,indice]}\n'
    
    resolver(r,indice,mtrx,m,n)


# Esta funcion realiza las operaciones del procedimiento dado el pivote seleccionado
def resolver(r,s,mtrx,m,n):
    """
    RESOLVER: Funcion para obtener una iteracion del intercambio de Jordan.
    
    Args:
        r(int) : Indice hilera del pivote.
        s(int) : Indice columna del pivote.
        mtrx(array o matrix): En este espacio se coloca la matriz a operar, ya sea del tipo array (numpy) o matrix (sympy) para el uso de matematicas simbolicas.
        m(int) : Valor entero que indica el numero de hileras de la matriz menos 1, para asi tener la correcta indexacion.
        n(int) : Valor entero que indica el numero de columnas de la matriz menos 1, para asi tener la correcta indexacion.
    
    Returns:
        Llama a la funcion 'obtener_indice' para continuar el programa.
    """
    
    global desarrollo
    global simbol
    global log
    matrix = mtrx
    clon = np.copy(mtrx)
    pivote = mtrx[r,s]
    
    matrix[r,s] = 1/pivote
    
    for i in range(0,m+1):
        if i == r: continue
        matrix[i,s] = - clon[i,s]/pivote
    
    for j in range(0,n+1):
        if j == s: continue
        matrix[r,j] = clon[r,j]/pivote
    
    for i in range(0,m+1):
        if i == r: continue
        else:
            for j in range(0,n+1):
                if j == s: continue
                else: matrix[i,j] = clon[i,j] - ((clon[i,s]*clon[r,j])/pivote)
                
    if desarrollo == True: 
        log += f'El resultado de la iteracion es:\n'
        if simbol == True: log += f'{np.array(matrix, dtype = str)}\n'
        else: log += f'{matrix}'
    obtener_indice(matrix,m,n)    
    

def final(mtrx):
    global iteracion
    global resultado
    global log
    resultado = mtrx
    log += f'''
=====================================================
El proceso se ha finalizado, solucion en 
{iteracion} iteraciones. La matriz resultante es:\n
'''
    if simbol == True: log += f'{np.array(mtrx, dtype = str)}\n'
    else: log += f'{mtrx}\n'
    
