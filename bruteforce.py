from itertools import permutations

#Datos de la finca y tablones
finca = [(10, 3, 4), (5, 3, 3), (2, 2, 1), (8, 1, 1),(6, 4, 2)]

# Obtener todas las programaciones
indicesParcelas = list(range(len(finca)))
generarProgramaciones = list(permutations(indicesParcelas))

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

print("programacion optima:", programacionOptima)
print("Costo total minimo:", costoMinimo)
print("permutaciones: ", numeroPermutaciones)