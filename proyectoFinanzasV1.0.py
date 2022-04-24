#Aplicacion creada por Cesar Augusto Perez Zapata, Diciembre 7 de 2020
# Proyecto final curso de python Ingenia
##################################################################################
#SE impornta tkinter y el modulo ttk con los cuales se construye la interfaz grafica.
import tkinter as tk
from tkinter import ttk

#se importa datetime para registrar los eventos financieros.
from datetime import datetime

#se importa matplotlib para construir graficos de reportes, el modulo específico
#de FigureCanvasTkAgg se usará para insertar figuras de matplotlib en objetos Tkinter

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#se importa numpy para convertir listas en arrays.
import numpy as np

##############################################################################
#Funciones
#Esta función guarda en un archivo de texto cada movimiento realizado.
def guardarRegistro(padre,valor,concepto,tipo):
    fecha=datetime.now().strftime("%d-%m-%y")
    finazasFile=open("finanzas.txt","a")
    valor=int(valor)
    finazasFile.write(f"{fecha},{concepto},{valor*tipo}\n")
    finazasFile.close()
    regText.set("Registro realizado")
    
    #esta funcion reporta el registro en la tabla de la primera página y la actualiza
    actualizarTabla(padre)   
    
    #se borra el contenido del enrty 
    valorEn.delete(0,'end')   

    #padre es el frame donde desde donde se llama la funcion
##############################################################################
#esta funcion escribe la tabla de visualizacion de registros en orden cronologico
#desente, se construye una tabla como un arreglo de labels, mediante un ciclo doble
#se adiciona un scrollbar para poder visualizar toda la tabla.
#basado en stack overflow para poder incorporar el scrollbar en un grid
#https://stackoverflow.com/questions/43731784/tkinter-canvas-scrollbar-with-grid

def actualizarTabla(abuelo):

    #Abuelo hace referencia al frame  desde el cual se hace el registro.
    
    padre=tk.Frame(abuelo)
    padre.grid(row=5, column=0, columnspan=4,pady=(5, 0), sticky='nw')
    
    #La tabla se construye sobre un canvas y se usa el meetodo grid para ordenar 
    #los elementos en el canvas.
    lienzo=tk.Canvas(padre)
    lienzo.grid(row=0, column=0, pady=(2, 0), sticky='nw')
    lienzo.grid_rowconfigure(0, weight=1)
    lienzo.grid_columnconfigure(0, weight=1)
    lienzo.grid_propagate(False)
    
    #se agrega el scrollbar en la columnaa la derecha de la
    #celda donde esta el canvas que contiene la tabla
    barra_y= tk.Scrollbar(padre,orient="vertical", command=lienzo.yview)
    barra_y.grid(row=0,column=1,sticky='ns')
    lienzo.configure(yscrollcommand=barra_y.set)
        
    tabla = tk.Frame(lienzo, bg="blue")
    lienzo.create_window((0, 0), window=tabla, anchor='nw')
    
    #ahora leemos el archivo con los datos, y genereamos una lista
    #de listas "una lista de renglones. 
    lst=[]
    finazasFile=open("finanzas.txt","r")
    for linea in reversed(finazasFile.readlines()):
        linea=linea.replace("\n","")
        linea=linea.split(",")
        lst.append(linea)
    finazasFile.close() 
    
    #barremos la lista en dos dimensiones filas y columnas y al
    #mismo tiempo se crea un label con el contenido de cada elemento
    total_rows = len(lst) 
    total_columns = len(lst[0])
    tablaReg = [[tk.Label() for j in range(total_columns)] for i in range(total_rows)]
    
    #Se barre cada registro (cada linea)
    for i in range(total_rows):
        colorF='green'
        sign='-'
        cadena=lst[i][2]
        if sign in cadena:
            colorF='red'            
        
        #se barren los elementos de cada registro
        for j in range(total_columns): 
            tablaReg[i][j] = tk.Label(tabla, width=16, text=lst[i][j],font=('Arial',10,'italic'),fg=colorF) 
            tablaReg[i][j].grid(row=i, column=j, sticky='news')
                
    # Update buttons frames idle tasks to let tkinter calculate buttons sizes
    tabla.update_idletasks()        
    lienzo.config(scrollregion=lienzo.bbox("all"))        
##############################################################################
#Funcion para realizar el reporte mensual de ingresos.
# 
def infMensual(mes):
    #creo una lista de ingresos fijos
    IngreFijos=["Salario","Comision"]
    
    #creo una lista de ingresos variables
    EgreFijos=["Alquiler","Agua","Energia","TV","Movil","Internet","Impuestos"]
    
    #Diccionario que permite intercambiar mes en letra a mes en numero
    Meses={'Ene':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',
           'Jul':'07','Ago':'08','Sep':'09','Oct':'10','Nov':'11','Dic':'12',}
    
    #Diccionario que permite intercambiar mes abreviado  a mes largo
    MesesLong={'Ene':'Enero','Feb':'Febrero','Mar':'Marzo','Apr':'Abril',
               'May':'Mayo','Jun':'Junio','Jul':'Julio','Ago':'Agosto',
               'Sep':'Septiembre','Oct':'Oct','Nov':'Noviembre','Dic':'Diciembre',}
    
    mes_num=Meses[mes]
    #se lee el archivo de datos, y se buscan los registros correspondientes
    #al mes de interes, para esto se buscan los elementos del tipo: -05-
    
    #construyo lo que voy a buscar
    cadena='-'+mes_num+'-'
    
    finazasFile=open("finanzas.txt","r")
    i=0
    lista=[]
    for linea in finazasFile.readlines():
        linea=linea.replace("\n","")
        linea=linea.split(",")
        
        #lista va guardar ls registros encontrados del mes 
        #lista2 solo guarda el concepto y el valor
        lista2=[]
        if cadena in linea[0]:
            lista2.append(linea[1])
            lista2.append(linea[2])
            lista.append(lista2)
            i+=1
    finazasFile.close() 
    
    
    
    #En la siguiente seccion se haran los calculos
    emt=0       #egreso mes total
    imt=0       #ingreso mes total
    egf=0       #egreso mes fijo
    egv=0       #egreso mes variable
    igf=0       #ingreso mes fijo
    igv=0       #ingreso mes variable
    sm=0        #saldo mes total
    
    for k in range(0,len(lista)):
        sm=sm+int(lista[k][1])
        if  int(lista[k][1])<0:
            emt = emt + int(lista[k][1])
        else:
            imt = imt + int(lista[k][1])
        #calculo de ingresos fijos
        for fijo in IngreFijos:
            if  lista[k][0] == fijo:
                igf=igf+int(lista[k][1])
                        
        for gasto in EgreFijos:
            if  lista[k][0] == gasto:
                egf=egf+int(lista[k][1])
    igv=imt-igf
    egv=emt-egf
    
    #se guardan las variables declaradas de tkinter, para los label del reporte
    
    SaldoMes.set(sm)
    EgresoMes.set(emt)
    IngresoMes.set(imt)
    IngresoFijo.set(igf)
    IngresoVari.set(igv)
    EgresoFijo.set(egf)
    EgresoVari.set(egv)
    colorSaldo=''
    
    TextoSaldoMensual.set('El saldo mensual de '+MesesLong[mes]+' es $'+str(sm))
    
    #si el saldo es negativo un label se pone rojo si  es positivo se pone verde
    if sm < 0:
        labelColor.config(bg='#ed0928',text='PIERDE')
        colorSaldo='#ed0928'
    else:
        labelColor.config(bg='#12ba06',text='GANA')
        colorSaldo='#12ba06'
    ################################# grafico mensual
    
    #este segmento construye el grafico de barras por mes
    
    #se definen las varibles del grafico
    concepto = ['Saldo','Ingresos','Egresos','Ingreso Fijo','Egreso Fijo','Ingreso Var', 'Egreso V']
    valor = [sm,imt,emt,igf,egf,igv,egv]
    
    #se define la figura donde se hará el grafico, se define el tamaño y la 
    # resolucion
    figure1 = plt.figure(figsize=(4,3), dpi=100)
    
    #se hace el grafico
    plotBars = figure1.add_subplot(111)
    plotBars.bar(concepto,valor,color=colorSaldo)
    
    #se amplia el espacio abajo para los labels. 
    figure1.subplots_adjust(bottom=0.2)
    
    #estos ciclos barren cada tic de los ejes y define sus propiedades 
    for label in plotBars.xaxis.get_ticklabels():
        #label.set_color('red')
        label.set_rotation(45)
        label.set_fontsize(8)
    for label in plotBars.yaxis.get_ticklabels():
        label.set_fontsize(8)
        
    #se captura el tamaño de la figura en pulgadas     
    w,h = figure1.get_size_inches()
    
    #se carga la figura en un cavas
    canvas = FigureCanvasTkAgg(figure1, sheet2)
    #se definen las dimensiones del canvas con base en el tamaño de la figura
    canvas.get_tk_widget().config(width=(4*figure1.dpi),height=(1.1*h*figure1.dpi ))      
    #se ubica el canvas en el sheet2.
    canvas.get_tk_widget().grid(row=8,rowspan=6 ,column=0,columnspan=6)

##############################################################################

def graficoG():
   
    #Se predefine listas 
    
    mes=['Ene','Feb','Mar','Apr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
    ingresoMes=[0,0,0,0,0,0,0,0,0,0,0,0]
    egresoMes=[0,0,0,0,0,0,0,0,0,0,0,0]
    saldoMes=[0,0,0,0,0,0,0,0,0,0,0,0]
    
    #se abre el archivo
    
    finazasFile=open("finanzas.txt","r")
    i=0    
    for linea in finazasFile.readlines():
        #se lee cada linea
        linea=linea.replace("\n","")
        #se capturan los valores 
        _fecha,_causa,_valor=linea.split(",")
        #se lee la fecha y se captura el mes.  12-05-2020 (se captur el 05)
        dum1,_mes,dum2=_fecha.split('-')  
        
        #se acumula el ingreso y el egreso segun el signo
        if int(_valor)>0:
            ingresoMes[int(_mes)-1] += int(_valor)
        else:
            egresoMes[int(_mes)-1] += int(_valor)
    finazasFile.close() 

    #se calcula el saldo por cada mes
    for i in range(0,12):
        saldoMes[i]+=ingresoMes[i]+egresoMes[i]

    # Plot
    
    #Se crea la figura
    figure1 = plt.figure(figsize=(4,3), dpi=100)
    
    #se crea grafico en la figura
    plotAnual = figure1.add_subplot(111)
    
    #se construye los graficos.
    plotAnual.plot(mes, ingresoMes,'g-o') 
    plotAnual.plot(mes, egresoMes,'r-o')
    plotAnual.plot(mes, saldoMes,'k-o')
    
    #se define la legenda del grafico
    plotAnual.legend(['Ingresos', 'Egresos','Saldo'], loc="upper center",ncol=3,
                     fontsize=7,bbox_to_anchor=(0.5, 1.15))
    
    #se ajustan las propiedades de los tics.
    for label in plotAnual.xaxis.get_ticklabels():
        label.set_fontsize(8)
    for label in plotAnual.yaxis.get_ticklabels():
        label.set_fontsize(8)
    
    #se crea el canvas que contendra la figura
    canvas = FigureCanvasTkAgg(figure1, sheet3)
    w,h = figure1.get_size_inches()
    canvas = FigureCanvasTkAgg(figure1, sheet3)
    canvas.get_tk_widget().config(width=(4*figure1.dpi),height=(0.9*h*figure1.dpi ))      
    canvas.get_tk_widget().grid(row=0,rowspan=5,column=0,columnspan=6)
    
    ##############
    
    #se construye el label que indica el saldo total del año
    saldoTotal=np.array(saldoMes).sum()
    if saldoTotal<=0:
        texto='Has quebrado!!! tienes deudas por '+str(saldoTotal)+' coins'
    else:
        texto='Tienes Ganancias!! has ahorrado '+str(saldoTotal)+' coins'
    labelSaldoFinal.configure(text=texto,font=('Arial',12,'bold'))
##############################################################################
#Esta funcion construye el grafico anual por concepto, el cual se carga desde
#un menu.

def graficoConcepto():
    #se lee el concepto desde el menu
    concepto=variableOpt.get()
    #se abre el archivo de datos almacenados.
    finazasFile=open("finanzas.txt","r")
    mes=['Ene','Feb','Mar','Apr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
    acumMes=[0,0,0,0,0,0,0,0,0,0,0,0]
    
    #se lee el archivo y se captura la informacion y se almacena de forma 
        #acumulada por mes.
    for linea in finazasFile.readlines():
        linea=linea.replace("\n","")
        _fecha,_causa,_valor=linea.split(",")
        dum1,_mes,dum2=_fecha.split('-')  
        if _causa==concepto:
            acumMes[int(_mes)-1] += int(_valor)
    finazasFile.close() 
    
    #se ha creado una lista llamada acumMes que contiene e valor acumulado
    #por mes del concepto buscado
    # Plot
    #Se crea la figura 
    figure2 = plt.figure(figsize=(4,3), dpi=100)
    plotAnual = figure2.add_subplot(111)
    
    #se crea el grafico
    plotAnual.plot(mes, acumMes,'b-o') 
    
    #se define la legenda
    plotAnual.legend([concepto, ], loc="upper center",fontsize=7,bbox_to_anchor=(0.5, 1.15))
    
    #Se ajustan las propiedades de lo stics
    for label in plotAnual.xaxis.get_ticklabels():
        label.set_fontsize(8)
    for label in plotAnual.yaxis.get_ticklabels():
        label.set_fontsize(8)


    #se crea el canvas donde se ubicaraá l a figura.
    w,h = figure2.get_size_inches()
    canvas2 = FigureCanvasTkAgg(figure2, sheet3)
    canvas2.get_tk_widget().config(width=(4*figure2.dpi),height=(0.8*h*figure2.dpi ))      
    canvas2.get_tk_widget().grid(row=9,rowspan=3,column=0,columnspan=6)
######################################################################################

lst=[] 
#esta variable contiene todos los conceptos de ingresos o egresos
OptionList = [
"Seleccione...",
"Agua",
"Alquiler",
"Credito",
"Compras",
"Energia",
"Familia",
"Impuestos",
"Internet",
"Medicina",
"Mercado",
"Movil",
"Seguros",
"Transporte",
"TV",
"Vida Social",
"Otro",
"Comision",
"Bonificacion",
"Pago a favor",
"Premio",
"Prestamo",
"Reembolso",
"Salario"
]
#lista de opciones para un menu option
mesNum=['Seleccione...','Ene','Feb','Mar','Apr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']

#se define la ventana y sus propiedades generales
raiz=tk.Tk()
raiz.iconbitmap("images.ico")
raiz.title("FINANZAS PERSONALES")
raiz.geometry("410x650")
raiz.resizable(0,0)

#se definen variables asociadas a los wdigets
regText=tk.StringVar(value="Se acaba de iniciar el programa")
SaldoMes=tk.StringVar(value='')
EgresoMes=tk.StringVar(value='')
IngresoMes=tk.StringVar(value='')
IngresoFijo=tk.StringVar(value='')
IngresoVari=tk.StringVar(value='')
EgresoFijo=tk.StringVar(value='')
EgresoVari=tk.StringVar(value='')
TextoSaldoMensual=tk.StringVar(value='')
saldoColor=tk.StringVar(value='white')


#Se usa el modulo ttk en en cual se encuentra la opcion notebook, para estos 
#notebooks se debe definir el estilo.
s1 = ttk.Style()
s1.configure('new.TFrame', background='#7fa19e', fontground='#000000')

#se crea el notebook donde cada sheet del notebook es un frame.
notebook=ttk.Notebook(raiz)
#se crea el primer sheet
sheet1=ttk.Frame(notebook,style='new.TFrame')
s1.configure('new.TFrame', background='#7fa19e')

#Se crean dos sheets adicionales
sheet2=ttk.Frame(notebook,style='new.TFrame')
sheet3=ttk.Frame(notebook,style='new.TFrame')

#Se empacan los sheets en la ventana
sheet1.pack(fill='both',expand=1)
sheet2.pack(fill='both',expand=1)
sheet3.pack(fill='both',expand=1)

#Se nombran los sheets y se muestran en la ventana
notebook.add(sheet1,text='Registros')
notebook.add(sheet2,text='Informe Mensual')
notebook.add(sheet3,text='Informe Anual')

##############################################################################
#EN el sheet1 se orgnizan los elementos que permiten los registros
#todos se ordenan en el sheet usando el metodo grid

#Letrero de bienvenida
LetreroSheet1=tk.Label(sheet1,text="Realice aqui el registro de sus operaciones",
                       width=40,
                       bg='#7fa19e')

LetreroSheet1.grid(column=0,row=0,sticky='W'+'E'+'N',columnspan=4,pady=1,padx=1)

#Se usa un par de radiobutons para definir si el registro es un ingreso o egreso.
#de aqui se defien una varible llamada tipoReg
tipoReg=tk.IntVar(sheet1)
radioB1=tk.Radiobutton(sheet1,text='Ingreso',variable=tipoReg,value=+1)
radioB1.grid(column=0,row=1,pady=1,padx=2)
radioB2=tk.Radiobutton(sheet1,text='Egreso ',variable=tipoReg,value=-1)
radioB2.grid(column=0,row=2,pady=1,padx=2)

#Letrero para indicar que se ingrese el valor del registro
valorLb=tk.Label(sheet1,text='Valor')
valorLb.grid(column=1,row=1,sticky='W'+'E'+'N',pady=1,padx=1)

#se usa un entry para ingresar el valor del registro
valorEn=tk.Entry(sheet1,width=15)
valorEn.grid(column=1,row=2,pady=1,padx=1)

#se define ua variable para almacenar la seleccion en un menu de los valores de 
#concepto de registro. 
variableOpt = tk.StringVar(sheet1)
#la variable toma el primer elemento de la lista
variableOpt.set(OptionList[0])

#la variable se asocia al menu
optMenuMesVar = tk.StringVar(sheet2)
optMenuMesVar.set(mesNum[0])

#Letrero para inidicar que se escoja el concepto
valorLb2=tk.Label(sheet1,text='Concepto')
valorLb2.grid(column=2,row=1,pady=1,padx=1,sticky='W'+'E'+'N')

#Se define el menu de conceptos de ingreso o egreso
optConcepto = tk.OptionMenu(sheet1, variableOpt, *OptionList)
optConcepto.grid(column=2,row=2,pady=1,padx=1)

#se define un boton de guardar donde se llama a la funcion de guardar registro
#y dentro de ella la funcion de acutalizar tabla.
bttnGuardar=tk.Button(sheet1, text="Guardar registro",height=3,
                      command=lambda:guardarRegistro(sheet1,
                                                     valorEn.get(),
                                                     variableOpt.get(),
                                                      tipoReg.get()))

bttnGuardar.grid(column=3,row=1,rowspan=2,pady=1,padx=1)
####
#este es un label para indicar que se ha realizado un registro.
letConf=tk.Label(sheet1,textvariable=regText,bg='#7fa19e',height=3)
letConf.grid(column=0, row=3,columnspan=5,sticky='W'+'E'+'N'+'S',pady=1,padx=1)

#frame para ubicar los encabezados de la tabla
Encabezado=tk.Frame(sheet1,bg='#7fa19e')
Encabezado.grid(row=4,column=0,columnspan=6,sticky='W'+'E'+'N'+'S',pady=1,padx=1)

#encabezado primer columna
headTabla1=tk.Label(Encabezado,text='Fecha Registro',width=15,font=('Arial',10,'bold'))
headTabla1.grid(row=0,column=0,sticky='W'+'E'+'N'+'S',pady=1,padx=1)

#encabezado segunda columna
headTabla2=tk.Label(Encabezado,text='Concepto',width=15,font=('Arial',10,'bold'))
headTabla2.grid(row=0,column=1,sticky='W'+'E'+'N'+'S',pady=1,padx=1)

#encabezado segunda columna
headTabla3=tk.Label(Encabezado,text=' Valor ',width=15,font=('Arial',10,'bold'))
headTabla3.grid(row=0,column=2,sticky='NEWS',pady=1,padx=1)
actualizarTabla(sheet1)
##############################################################################
#Reporte en el segundo sheet2, informe mensual

#Letrero que muestra el saldo del mes seleccionado.
labelST=tk.Label(sheet2,textvariable=TextoSaldoMensual,width=45)
labelST.grid(row=0,column=0,columnspan=5,sticky='NEWS',pady=1,padx=1)
#Letrero indicador con color y texto si el saldo es ganancia o perdida
labelColor=tk.Label(sheet2,bg=saldoColor.get(),width=10)
labelColor.grid(row=0,column=5,sticky='NEWS',pady=1,padx=1)


##### Calcular ingresos y egresos mensuales
#letrero para indicar que se seleccione un mes
labelMes=tk.Label(sheet2,text='Seleccione el mes',width=10)
labelMes.grid(row=1,column=0,columnspan=2,sticky='NEWS',pady=1,padx=1)

#Menu de opcion del mes  a consultar
optMenuMes = tk.OptionMenu(sheet2, optMenuMesVar, *mesNum)
optMenuMes.grid(row=1,column=2,columnspan=2,sticky='NEWS',pady=1,padx=1)

#Boton para realizar la busqueda, hacer el calculo y actualizar graficos    
botonMes=tk.Button(sheet2,text='Generar',width=10,
                   command=lambda:infMensual(optMenuMesVar.get()))
botonMes.grid(row=1,column=4,columnspan=2,sticky='NEWS',pady=1,padx=1)

#los siguientes son letreros para los reportes. su texto se alimenta de 
#valores de las variable tk que salen desde la funcion infMensual
label_Itot0=tk.Label(sheet2,text="Ingresos Mensuales",width=10)
label_Itot0.grid(row=2,column=0,columnspan=4,sticky='NEWS',pady=1,padx=1)
label_Itot=tk.Label(sheet2,textvariable=IngresoMes,width=10)
label_Itot.grid(row=2,column=4,columnspan=2,sticky='NEWS',pady=1,padx=1)
labelIngFix0=tk.Label(sheet2,text="Ingresos Fijos Mensuales",width=10)
labelIngFix0.grid(row=3,column=0,columnspan=4,sticky='NEWS',pady=1,padx=1)
labelIngFix=tk.Label(sheet2,textvariable=IngresoFijo,width=10)
labelIngFix.grid(row=3,column=4,columnspan=2,sticky='NEWS',pady=1,padx=1)

labelIngVari0=tk.Label(sheet2,text="Ingresos Variables Mensuales",width=10)
labelIngVari0.grid(row=4,column=0,columnspan=4,sticky='NEWS',pady=1,padx=1)
labelIngVari=tk.Label(sheet2,textvariable=IngresoVari,width=10)
labelIngVari.grid(row=4,column=4,columnspan=2,sticky='NEWS',pady=1,padx=1)

label_Etot0=tk.Label(sheet2,text="Egresos Mensuales Totales",width=10)
label_Etot0.grid(row=5,column=0,columnspan=4,sticky='NEWS',pady=1,padx=1)
label_Etot=tk.Label(sheet2,textvariable=EgresoMes,width=10)
label_Etot.grid(row=5,column=4,columnspan=2,sticky='NEWS',pady=1,padx=1)

labelEgrFix0=tk.Label(sheet2,text="Egresos Fijos Mensuales",width=10)
labelEgrFix0.grid(row=6,column=0,columnspan=4,sticky='NEWS',pady=1,padx=1)
labelEgrFix=tk.Label(sheet2,textvariable=EgresoFijo,width=10)
labelEgrFix.grid(row=6,column=4,columnspan=2,sticky='NEWS',pady=1,padx=1)

labelEgrVari0=tk.Label(sheet2,text="Egresos Variables Mensuales",width=10)
labelEgrVari0.grid(row=7,column=0,columnspan=4,sticky='NEWS',pady=1,padx=1)
labelEgrVari=tk.Label(sheet2,textvariable=EgresoVari,width=10)
labelEgrVari.grid(row=7,column=4,columnspan=2,sticky='NEWS',pady=1,padx=1)

##############################################################################
#Reporte Mensual en sheet3
################################# grafico mensual

#Letrero que indica el salto total del año su valor de texto se actualiza desde
#la funcion graficoG
labelSaldoFinal=tk.Label(sheet3)
labelSaldoFinal.grid(row=7,column=0,columnspan=6,sticky='NEWS',pady=1,padx=1)

# el llamado a la funcion graficoG, genera el grafico del balance globlal de
#ingresos y egresos 
graficoG()

##############################################################################
#Letrero par indicar seleccion de concepto
labelFiltro=tk.Label(sheet3,text='Seleccione un concepto para revisar su variacion anual',anchor='w')
labelFiltro.grid(row=8,column=0,columnspan=4,sticky='NEWS',pady=1,padx=1)

#Menu de seleccion de concepto, con la seleccion automaticamente se ejecuta la 
#funcion graficoConcepto
optConceptos3 = tk.OptionMenu(sheet3, variableOpt, *OptionList,command=lambda _:graficoConcepto())
optConceptos3.grid(column=5,row=8,pady=1,padx=1)

notebook.pack(expand=1, fill='both')
raiz.mainloop()