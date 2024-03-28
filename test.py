from itertools import permutations
from customtkinter import *

class Finca:
    def __init__(self, archivo_datos):
        self.finca = self.leer_datos_finca(archivo_datos)
        
    def leer_datos_finca(self, archivo):
        with open(archivo, 'r') as f:
            lineas = f.readlines()
        finca = [tuple(map(int, linea.strip().split(','))) for linea in lineas[1:]]
        return finca

    def calcular_inicios_de_riego(self, programacion):
        iniciosDeRiego = [0] * len(self.finca)
        for j in range(1, len(programacion)):
            indiceTablonAnterior = programacion[j-1]
            indiceTablonActual = programacion[j] 
            tiempoRiegoTablonAnterior = self.finca[indiceTablonAnterior][1]
            sumaTiemposRiego = iniciosDeRiego[indiceTablonAnterior] + tiempoRiegoTablonAnterior
            iniciosDeRiego[indiceTablonActual] = sumaTiemposRiego
        return iniciosDeRiego

    def calcular_costo_riego_tablon(self, iniciosDeRiego):
        costosDeRiego = []
        for i in range(len(self.finca)):
            ts, tr, pri = self.finca[i]
            if ts - tr >= iniciosDeRiego[i]:
                cost = ts - (iniciosDeRiego[i] + tr)
            else:
                cost = pri * ((iniciosDeRiego[i] + tr) - ts)
            costosDeRiego.append(cost)
        return costosDeRiego

    def costo_total_riego(self, costosDeRiego):
        return sum(costosDeRiego)

    def voraz(self):
        # Ordenar tablones por la division tr/p mas baja
        iniciosRiegoV = sorted(range(len(self.finca)), key=lambda i: self.finca[i][1] / self.finca[i][2])
        iniciosDeRiego = self.calcular_inicios_de_riego(iniciosRiegoV)
        costosDeRiego = self.calcular_costo_riego_tablon(iniciosDeRiego)
        totalCost = self.costo_total_riego(costosDeRiego)
        return totalCost, iniciosRiegoV


#variables de datos
archivo_datos = r'BateriaPruebas\Prueba1.txt'
finca = Finca(archivo_datos)

costo_minimo_voraz, programacion_optima_voraz = finca.voraz()


print("Costo método voraz:", costo_minimo_voraz)
print("Mejor programación obtenida: ", programacion_optima_voraz)