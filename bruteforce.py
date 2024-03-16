from itertools import permutations

#lectura de datos
def leer_datos_finca(archivo):
    with open(archivo, 'r') as f:
        lineas = f.readlines()
    finca = [tuple(map(int, linea.strip().split(','))) for linea in lineas[1:]]  
    return finca

#vincular datos de archivo a una finca
finca = leer_datos_finca('datos.txt')

# Obtener todas las programaciones
indicesParcelas = list(range(len(finca)))
generarProgramaciones = list(permutations(indicesParcelas))

#obtener todas las combinaciones de riego 
numeroPermutaciones = len(generarProgramaciones)


#Funcion que se encarga de obtener los tiempos de inicio de riego
def calcularIniciosDeRiego(finca, programacion):
    iniciosDeRiego = [0] * len(finca)
    for j in range(1, len(programacion)):
        indiceTablonAnterior = programacion[j-1]
        indiceTablonActual = programacion[j]
        tiempoRiegoTablonAnterior = finca[indiceTablonAnterior][1]
        sumaTiemposRiego = iniciosDeRiego[indiceTablonAnterior] + tiempoRiegoTablonAnterior
        iniciosDeRiego[indiceTablonActual] = sumaTiemposRiego
    return iniciosDeRiego

#funcion para calcular el costo de riego de cada tablon
def calcularCostoRiegoTablon(finca, iniciosDeRiego):
    costosDeRiego = []
    for i in range(len(finca)):
        ts, tr, pri = finca[i]
        if ts - tr >= iniciosDeRiego[i]:
            cost = ts - (iniciosDeRiego[i] + tr)
        else:
            cost = pri * ((iniciosDeRiego[i] + tr) - ts)
        costosDeRiego.append(cost)
    return costosDeRiego

#sumar todos los costos para obtener costo total
def costoTotalRiego(costosDeRiego):
    cost = sum(costosDeRiego)
    return cost

todosLosCostos = []
for programacion in generarProgramaciones:
    iniciosDeRiego = calcularIniciosDeRiego(finca, programacion)
    costosDeRiego = calcularCostoRiegoTablon(finca, iniciosDeRiego)
    total_irrigation_cost = costoTotalRiego(costosDeRiego)
    todosLosCostos.append(total_irrigation_cost)


costoMinimo = min(todosLosCostos)
costoMinimoIndice = todosLosCostos.index(costoMinimo)
programacionOptima = generarProgramaciones[costoMinimoIndice]


def escribir_resultados(costo_minimo, programacion_optima, nombre_archivo):
    with open(nombre_archivo, 'w') as archivo:
        #costo minimo
        archivo.write(f"costo {costo_minimo}\n")
        
        #orden de tablones
        for tablon in programacion_optima:
            archivo.write(f"tablon {tablon}\n")  


############## salidas ############################################################
nombre_archivo = "riego-optimo.txt"
escribir_resultados(costoMinimo, programacionOptima, nombre_archivo)


print("programacion optima:", programacionOptima)
print("Costo total minimo:", costoMinimo)
print("permutaciones: ", numeroPermutaciones)