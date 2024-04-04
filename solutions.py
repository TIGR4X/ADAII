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

    def roFB(self):
        self.permutacionProgramaciones = list(permutations(range(len(self.finca))))
        todosLosCostos = []
        for programacion in self.permutacionProgramaciones:
            iniciosDeRiego = self.calcular_inicios_de_riego(programacion)
            costosDeRiego = self.calcular_costo_riego_tablon(iniciosDeRiego)
            total_irrigation_cost = self.costo_total_riego(costosDeRiego)
            todosLosCostos.append(total_irrigation_cost)
            
        costoMinimo = min(todosLosCostos)
        costoMinimoIndice = todosLosCostos.index(costoMinimo)
        programacionOptima = self.permutacionProgramaciones[costoMinimoIndice]
        
        return costoMinimo, programacionOptima
    
    def roV(self):
        # Ordenar tablones por la division tr/p mas baja
        iniciosRiegoV = sorted(range(len(self.finca)), key=lambda i: self.finca[i][1] / self.finca[i][2])
        iniciosDeRiego = self.calcular_inicios_de_riego(iniciosRiegoV)
        costosDeRiego = self.calcular_costo_riego_tablon(iniciosDeRiego)
        totalCost = self.costo_total_riego(costosDeRiego)
        return totalCost, iniciosRiegoV
    
    def calcular_costo(self,tablon,tiempo):
        if (tablon[0]-tablon[1]>=tiempo):
            return tablon[0]-(tiempo + tablon[1])
        else:
            return tablon[2]*((tiempo+tablon[1])-tablon[0])

    def roPD(self):
        memoTablon={}
        memoprogram={}
        combinaciones=list(permutations(self.finca))
    

        def dp(programacion,t):
            #condicion de parada
            if(len(programacion)==0): 
                return 0
            #verificar si ya está el costo de la programacion en el tiempo t
            if ( tuple(programacion) , t ) in memoprogram:
                return memoprogram[(tuple(programacion),t)]
            #declarar la informacion del tablon
            tablon_actual=programacion[0]
            #calcular el costo del tablon en el tiempo t en el memo tablon
            if((tablon_actual,t)) not in memoTablon:
                memoTablon[(tablon_actual,t)]=self.calcular_costo(tablon_actual,t)
            costoTablonActual=memoTablon[(tablon_actual,t)]
            #declarar las variables de la siguiente iteracion
            t_nuevo=t+tablon_actual[1]
            restoProgram=programacion[1:]
            #guardar el costo del resto de tablones en el tiempo t en el memo program
            memoprogram[(tuple(restoProgram),t_nuevo)]=dp(restoProgram,t_nuevo)
            return costoTablonActual+memoprogram[(tuple(restoProgram),t_nuevo)]

        candidatos=[dp(combinaciones[i],0) for i in range(len(combinaciones))]
        ##valor_minimo, indice_minimo = min((valor, indice) for indice, valor in enumerate(lista))
        costo,indicess=min((valor,indice) for indice, valor in enumerate(candidatos))
        return costo,combinaciones[indicess]


    def escribir_resultados(self, costo_minimo, programacion_optima, nombre_archivo):
        with open(nombre_archivo, 'w') as archivo:
            archivo.write(f"costo {costo_minimo}\n")
            for tablon in programacion_optima:
                archivo.write(f"tablon {tablon}\n")

#variables de datos
archivo_datos = 'BateriaPruebas/Prueba2.txt'
finca = Finca(archivo_datos)

######## ui ############
app = CTk(fg_color="#FCF4EE")
app.geometry("1230x690")
app.resizable(False, False)

#Caja de texto que muestra entrada
textEntrada = CTkTextbox(master=app, width=318, height=370, fg_color="#F4DBC9",corner_radius=13,text_color="black",font=('Arial bold', 20))
textEntrada.place(x=115, y=209)

#lectura de finca
with open(archivo_datos, 'r') as file:
    # Read the entire content of the file into a variable
    file_content = file.read()

#añade el texto y luego no se puede editar
textEntrada.configure(state='normal')
textEntrada.insert("1.0",file_content)
textEntrada.configure(state='disabled')


#estilizacion de titulo caja de entrada
entradaTitle = CTkTextbox(master=app, width=318, height=23, fg_color="#F79753",corner_radius=13,text_color="#FCF4EE",font=('Arial black', 48))
entradaTitle.place(x=115, y=90)
entradaTitle.insert("0.0", "Entrada")

#estilizacion de titulo caja de salida
salidaTitle = CTkTextbox(master=app, width=318, height=23, fg_color="#F79753",corner_radius=13,text_color="#FCF4EE",font=('Arial black', 48))
salidaTitle.place(x=805, y=90)
salidaTitle.insert("0.0", "Salida")

#NOMBRE ARCHIVOS DE SALIDA
salidaFB = 'roFB.txt'
salidaVoraz = 'roV.txt'
salidaPD = 'roPD.txt'

def solucionar():
    metodo_seleccionado = opcion.get()
    if metodo_seleccionado == "Fuerza bruta":
        costo_minimo, programacion_optima = finca.roFB()
        finca.escribir_resultados(costo_minimo, programacion_optima, salidaFB)
        with open(salidaFB, 'r') as file:
            contenidoArchivo = file.read()
        
        textSalida.delete("1.0","end")
        textSalida.insert("1.0",contenidoArchivo)
        print("Se creó la solución con el nombre", salidaFB)

    elif metodo_seleccionado == "Voraz":
        costo_minimo, programacion_optima = finca.roV()
        
        finca.escribir_resultados(costo_minimo, programacion_optima, salidaVoraz)
        with open(salidaVoraz, 'r') as file:
            contenidoArchivo = file.read()

        textSalida.delete("1.0", "end")
        textSalida.insert("1.0", contenidoArchivo)
        print("Se creó la solución con el nombre", salidaVoraz)
    elif metodo_seleccionado == 'Prog. dinámica':
        costo_minimo, programacion_optima= finca.roPD()
        
        finca.escribir_resultados(costo_minimo, programacion_optima, salidaPD)
        with open(salidaPD, 'r') as file:
            contenidoArchivo = file.read()

        textSalida.delete("1.0", "end")
        textSalida.insert("1.0", contenidoArchivo)
        print("Se creó la solución con el nombre", salidaPD)

## lista metodosOpt ####
metodos = ["Fuerza bruta","Voraz","Prog. dinámica"]
opcion = CTkOptionMenu(master=app, corner_radius=13, fg_color="#F79753", font=('Arial bold', 20), text_color= "#FCF4EE", width=200, height=44,
                        values=metodos, button_color="#F79753")
opcion.place(x=620, y=300, anchor="center")

##BOTON SOLUCIONAR#####
btnSol = CTkButton(master=app, text="Solucionar", corner_radius=13, fg_color="#F79753", hover_color="#f5a369", font=('Arial bold', 20), text_color= "#FCF4EE", width=130, height=44, command=solucionar)
btnSol.place(x=620, y=490, anchor="center")

#caja de texto salida
textSalida = CTkTextbox(master=app, width=318, height=370, fg_color="#F4DBC9",corner_radius=13,text_color="black",font=('Arial bold', 20))
textSalida.place(x=805, y=209)

app.mainloop()