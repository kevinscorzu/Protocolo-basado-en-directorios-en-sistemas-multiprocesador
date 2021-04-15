import PySimpleGUI as sg
from threading import Thread
import concurrent.futures
import queue

import entities.l1cachedataholder as l1c
import entities.instructionsholder as ih
import entities.l2cache as l2c
import entities.memory as mem
import entities.procesor as proc

sg.theme("Reds")

proc0Column = [ [sg.Text(text="Procesador 0", justification="center", font=("Any", 10))],
                [sg.Text(text="-----------------------------------------------------------------------------------", justification="center")],
                [sg.Text(text="Ejecutando: ", justification="left", font=("Any", 10)), sg.Text(text="XXXXX XXX;XXXX", justification="right", font=("Any", 10), key="instruccion0")],
                [sg.Text(text="-----------------------------------------------------------------------------------", justification="center")],
                [sg.Text(text="Contenido de la Caché L1", justification="center", font=("Any", 10))],
                [sg.Text(text="-----------------------------------------------------------------------------------", justification="center")],
                [sg.Text(text="Set:", justification="left", font=("Any", 10)), sg.Text(text="0", justification="right", font=("Any", 10))],
                [sg.Text(text="Bloque:", justification="left", font=("Any", 10)), sg.Text(text="0", justification="right", font=("Any", 10))],
                [sg.Text(text="Estado de Coherencia:", justification="left", font=("Any", 10)), sg.Text(text="X", justification="right", font=("Any", 10), key="l1coherencia00")],
                [sg.Text(text="Dirección de Memoria:", justification="left", font=("Any", 10)), sg.Text(text="XXX", justification="right", font=("Any", 10), key="l1direccion00")],
                [sg.Text(text="Dato:", justification="left", font=("Any", 10)), sg.Text(text="0000", justification="right", font=("Any", 10), key="l1dato00")],
                [sg.Text(text="-----------------------------------------------------------------------------------", justification="center")],
                [sg.Text(text="Set:", justification="left", font=("Any", 10)), sg.Text(text="1", justification="right", font=("Any", 10))],
                [sg.Text(text="Bloque:", justification="left", font=("Any", 10)), sg.Text(text="1", justification="right", font=("Any", 10))],
                [sg.Text(text="Estado de Coherencia:", justification="left", font=("Any", 10)), sg.Text(text="X", justification="right", font=("Any", 10), key="l1coherencia01")],
                [sg.Text(text="Dirección de Memoria:", justification="left", font=("Any", 10)), sg.Text(text="XXX", justification="right", font=("Any", 10), key="l1direccion01")],
                [sg.Text(text="Dato:", justification="left", font=("Any", 10)), sg.Text(text="0000", justification="right", font=("Any", 10), key="l1dato01")] ]

proc1Column = [ [sg.Text(text="Procesador 1", justification="center", font=("Any", 10))],
                [sg.Text(text="-----------------------------------------------------------------------------------", justification="center")],
                [sg.Text(text="Ejecutando: ", justification="left", font=("Any", 10)), sg.Text(text="XXXXX XXX;XXXX", justification="right", font=("Any", 10), key="instruccion1")],
                [sg.Text(text="-----------------------------------------------------------------------------------", justification="center")],
                [sg.Text(text="Contenido de la Caché L1", justification="center", font=("Any", 10))],
                [sg.Text(text="-----------------------------------------------------------------------------------", justification="center")],
                [sg.Text(text="Set:", justification="left", font=("Any", 10)), sg.Text(text="0", justification="right", font=("Any", 10))],
                [sg.Text(text="Bloque:", justification="left", font=("Any", 10)), sg.Text(text="0", justification="right", font=("Any", 10))],
                [sg.Text(text="Estado de Coherencia:", justification="left", font=("Any", 10)), sg.Text(text="X", justification="right", font=("Any", 10), key="l1coherencia10")],
                [sg.Text(text="Dirección de Memoria:", justification="left", font=("Any", 10)), sg.Text(text="XXX", justification="right", font=("Any", 10), key="l1direccion10")],
                [sg.Text(text="Dato:", justification="left", font=("Any", 10)), sg.Text(text="0000", justification="right", font=("Any", 10), key="l1dato10")],
                [sg.Text(text="-----------------------------------------------------------------------------------", justification="center")],
                [sg.Text(text="Set:", justification="left", font=("Any", 10)), sg.Text(text="1", justification="right", font=("Any", 10))],
                [sg.Text(text="Bloque:", justification="left", font=("Any", 10)), sg.Text(text="1", justification="right", font=("Any", 10))],
                [sg.Text(text="Estado de Coherencia:", justification="left", font=("Any", 10)), sg.Text(text="X", justification="right", font=("Any", 10), key="l1coherencia11")],
                [sg.Text(text="Dirección de Memoria:", justification="left", font=("Any", 10)), sg.Text(text="XXX", justification="right", font=("Any", 10), key="l1direccion11")],
                [sg.Text(text="Dato:", justification="left", font=("Any", 10)), sg.Text(text="0000", justification="right", font=("Any", 10), key="l1dato11")] ]

proc2Column = [ [sg.Text(text="Procesador 2", justification="center", font=("Any", 10))],
                [sg.Text(text="-----------------------------------------------------------------------------------", justification="center")],
                [sg.Text(text="Ejecutando: ", justification="left", font=("Any", 10)), sg.Text(text="XXXXX XXX;XXXX", justification="right", font=("Any", 10), key="instruccion2")],
                [sg.Text(text="-----------------------------------------------------------------------------------", justification="center")],
                [sg.Text(text="Contenido de la Caché L1", justification="center", font=("Any", 10))],
                [sg.Text(text="-----------------------------------------------------------------------------------", justification="center")],
                [sg.Text(text="Set:", justification="left", font=("Any", 10)), sg.Text(text="0", justification="right", font=("Any", 10))],
                [sg.Text(text="Bloque:", justification="left", font=("Any", 10)), sg.Text(text="0", justification="right", font=("Any", 10))],
                [sg.Text(text="Estado de Coherencia:", justification="left", font=("Any", 10)), sg.Text(text="X", justification="right", font=("Any", 10), key="l1coherencia20")],
                [sg.Text(text="Dirección de Memoria:", justification="left", font=("Any", 10)), sg.Text(text="XXX", justification="right", font=("Any", 10), key="l1direccion20")],
                [sg.Text(text="Dato:", justification="left", font=("Any", 10)), sg.Text(text="0000", justification="right", font=("Any", 10), key="l1dato20")],
                [sg.Text(text="-----------------------------------------------------------------------------------", justification="center")],
                [sg.Text(text="Set:", justification="left", font=("Any", 10)), sg.Text(text="1", justification="right", font=("Any", 10))],
                [sg.Text(text="Bloque:", justification="left", font=("Any", 10)), sg.Text(text="1", justification="right", font=("Any", 10))],
                [sg.Text(text="Estado de Coherencia:", justification="left", font=("Any", 10)), sg.Text(text="X", justification="right", font=("Any", 10), key="l1coherencia21")],
                [sg.Text(text="Dirección de Memoria:", justification="left", font=("Any", 10)), sg.Text(text="XXX", justification="right", font=("Any", 10), key="l1direccion21")],
                [sg.Text(text="Dato:", justification="left", font=("Any", 10)), sg.Text(text="0000", justification="right", font=("Any", 10), key="l1dato21")] ]

proc3Column = [ [sg.Text(text="Procesador 3", justification="center", font=("Any", 10))],
                [sg.Text(text="-----------------------------------------------------------------------------------", justification="center")],
                [sg.Text(text="Ejecutando: ", justification="left", font=("Any", 10)), sg.Text(text="XXXXX XXX;XXXX", justification="right", font=("Any", 10), key="instruccion3")],
                [sg.Text(text="-----------------------------------------------------------------------------------", justification="center")],
                [sg.Text(text="Contenido de la Caché L1", justification="center", font=("Any", 10))],
                [sg.Text(text="-----------------------------------------------------------------------------------", justification="center")],
                [sg.Text(text="Set:", justification="left", font=("Any", 10)), sg.Text(text="0", justification="right", font=("Any", 10))],
                [sg.Text(text="Bloque:", justification="left", font=("Any", 10)), sg.Text(text="0", justification="right", font=("Any", 10))],
                [sg.Text(text="Estado de Coherencia:", justification="left", font=("Any", 10)), sg.Text(text="X", justification="right", font=("Any", 10), key="l1coherencia30")],
                [sg.Text(text="Dirección de Memoria:", justification="left", font=("Any", 10)), sg.Text(text="XXX", justification="right", font=("Any", 10), key="l1direccion30")],
                [sg.Text(text="Dato:", justification="left", font=("Any", 10)), sg.Text(text="0000", justification="right", font=("Any", 10), key="l1dato30")],
                [sg.Text(text="-----------------------------------------------------------------------------------", justification="center")],
                [sg.Text(text="Set:", justification="left", font=("Any", 10)), sg.Text(text="1", justification="right", font=("Any", 10))],
                [sg.Text(text="Bloque:", justification="left", font=("Any", 10)), sg.Text(text="1", justification="right", font=("Any", 10))],
                [sg.Text(text="Estado de Coherencia:", justification="left", font=("Any", 10)), sg.Text(text="X", justification="right", font=("Any", 10), key="l1coherencia31")],
                [sg.Text(text="Dirección de Memoria:", justification="left", font=("Any", 10)), sg.Text(text="XXX", justification="right", font=("Any", 10), key="l1direccion31")],
                [sg.Text(text="Dato:", justification="left", font=("Any", 10)), sg.Text(text="0000", justification="right", font=("Any", 10), key="l1dato31")] ]

bloq0L2Column = [ [sg.Text(text="Bloque:", justification="left", font=("Any", 10)), sg.Text(text="0", justification="right", font=("Any", 10))],
                   [sg.Text(text="Estado de Coherencia:", justification="left", font=("Any", 10)), sg.Text(text="XX", justification="right", font=("Any", 10), key="l2coherencia0")],
                   [sg.Text(text="Procesador Dueño del Bloque:", justification="left", font=("Any", 10)), sg.Text(text="X", justification="right", font=("Any", 10), key="l2dueno0")],
                   [sg.Text(text="Procesadores donde se Comparte:", justification="left", font=("Any", 10)), sg.Text(text="X, X, X", justification="right", font=("Any", 10), key="l2compartidos0")],
                   [sg.Text(text="Dirección de Memoria:", justification="left", font=("Any", 10)), sg.Text(text="XXX", justification="right", font=("Any", 10), key="l2direccion0")],
                   [sg.Text(text="Dato:", justification="left", font=("Any", 10)), sg.Text(text="0000", justification="right", font=("Any", 10), key="l2dato0")] ]

bloq1L2Column = [ [sg.Text(text="Bloque:", justification="left", font=("Any", 10)), sg.Text(text="1", justification="right", font=("Any", 10))],
                   [sg.Text(text="Estado de Coherencia:", justification="left", font=("Any", 10)), sg.Text(text="XX", justification="right", font=("Any", 10), key="l2coherencia1")],
                   [sg.Text(text="Procesador Dueño del Bloque:", justification="left", font=("Any", 10)), sg.Text(text="X", justification="right", font=("Any", 10), key="l2dueno1")],
                   [sg.Text(text="Procesadores donde se Comparte:", justification="left", font=("Any", 10)), sg.Text(text="X, X, X", justification="right", font=("Any", 10), key="l2compartidos1")],
                   [sg.Text(text="Dirección de Memoria:", justification="left", font=("Any", 10)), sg.Text(text="XXX", justification="right", font=("Any", 10), key="l2direccion1")],
                   [sg.Text(text="Dato:", justification="left", font=("Any", 10)), sg.Text(text="0000", justification="right", font=("Any", 10), key="l2dato1")] ]

bloq2L2Column = [ [sg.Text(text="Bloque:", justification="left", font=("Any", 10)), sg.Text(text="2", justification="right", font=("Any", 10))],
                   [sg.Text(text="Estado de Coherencia:", justification="left", font=("Any", 10)), sg.Text(text="XX", justification="right", font=("Any", 10), key="l2coherencia2")],
                   [sg.Text(text="Procesador Dueño del Bloque:", justification="left", font=("Any", 10)), sg.Text(text="X", justification="right", font=("Any", 10), key="l2dueno2")],
                   [sg.Text(text="Procesadores donde se Comparte:", justification="left", font=("Any", 10)), sg.Text(text="X, X, X", justification="right", font=("Any", 10), key="l2compartidos2")],
                   [sg.Text(text="Dirección de Memoria:", justification="left", font=("Any", 10)), sg.Text(text="XXX", justification="right", font=("Any", 10), key="l2direccion2")],
                   [sg.Text(text="Dato:", justification="left", font=("Any", 10)), sg.Text(text="0000", justification="right", font=("Any", 10), key="l2dato2")] ]

bloq3L2Column = [ [sg.Text(text="Bloque:", justification="left", font=("Any", 10)), sg.Text(text="3", justification="right", font=("Any", 10))],
                   [sg.Text(text="Estado de Coherencia:", justification="left", font=("Any", 10)), sg.Text(text="XX", justification="right", font=("Any", 10), key="l2coherencia3")],
                   [sg.Text(text="Procesador Dueño del Bloque:", justification="left", font=("Any", 10)), sg.Text(text="X", justification="right", font=("Any", 10), key="l2dueno3")],
                   [sg.Text(text="Procesadores donde se Comparte:", justification="left", font=("Any", 10)), sg.Text(text="X, X, X", justification="right", font=("Any", 10), key="l2compartidos3")],
                   [sg.Text(text="Dirección de Memoria:", justification="left", font=("Any", 10)), sg.Text(text="XXX", justification="right", font=("Any", 10), key="l2direccion3")],
                   [sg.Text(text="Dato:", justification="left", font=("Any", 10)), sg.Text(text="0000", justification="right", font=("Any", 10), key="l2dato3")] ]

bloq0MemColumn = [ [sg.Text(text="Bloque:", justification="left", font=("Any", 10)), sg.Text(text="0", justification="right", font=("Any", 10))],
                   [sg.Text(text="Dato:", justification="left", font=("Any", 10)), sg.Text(text="0000", justification="right", font=("Any", 10), key="memdato0")] ]

bloq1MemColumn = [ [sg.Text(text="Bloque:", justification="left", font=("Any", 10)), sg.Text(text="1", justification="right", font=("Any", 10))],
                   [sg.Text(text="Dato:", justification="left", font=("Any", 10)), sg.Text(text="0000", justification="right", font=("Any", 10), key="memdato1")] ]

bloq2MemColumn = [ [sg.Text(text="Bloque:", justification="left", font=("Any", 10)), sg.Text(text="2", justification="right", font=("Any", 10))],
                   [sg.Text(text="Dato:", justification="left", font=("Any", 10)), sg.Text(text="0000", justification="right", font=("Any", 10), key="memdato2")] ]

bloq3MemColumn = [ [sg.Text(text="Bloque:", justification="left", font=("Any", 10)), sg.Text(text="3", justification="right", font=("Any", 10))],
                   [sg.Text(text="Dato:", justification="left", font=("Any", 10)), sg.Text(text="0000", justification="right", font=("Any", 10), key="memdato3")] ]

bloq4MemColumn = [ [sg.Text(text="Bloque:", justification="left", font=("Any", 10)), sg.Text(text="4", justification="right", font=("Any", 10))],
                   [sg.Text(text="Dato:", justification="left", font=("Any", 10)), sg.Text(text="0000", justification="right", font=("Any", 10), key="memdato4")] ]

bloq5MemColumn = [ [sg.Text(text="Bloque:", justification="left", font=("Any", 10)), sg.Text(text="5", justification="right", font=("Any", 10))],
                   [sg.Text(text="Dato:", justification="left", font=("Any", 10)), sg.Text(text="0000", justification="right", font=("Any", 10), key="memdato5")] ]

bloq6MemColumn = [ [sg.Text(text="Bloque:", justification="left", font=("Any", 10)), sg.Text(text="6", justification="right", font=("Any", 10))],
                   [sg.Text(text="Dato:", justification="left", font=("Any", 10)), sg.Text(text="0000", justification="right", font=("Any", 10), key="memdato6")] ]

bloq7MemColumn = [ [sg.Text(text="Bloque:", justification="left", font=("Any", 10)), sg.Text(text="7", justification="right", font=("Any", 10))],
                   [sg.Text(text="Dato:", justification="left", font=("Any", 10)), sg.Text(text="0000", justification="right", font=("Any", 10), key="memdato7")] ]

layout = [ [sg.Column(layout=proc0Column, element_justification="center", key="procesador0"), sg.Column(layout=proc1Column, element_justification="center"), sg.Column(layout=proc2Column, element_justification="center"), sg.Column(layout=proc3Column, element_justification="center")],
           [sg.Text(text="Contenido de la Caché L2", size=(149, 1), justification="center", font=("Any", 10))],
           [sg.Text(text="Set 0", size=(70, 1), justification="center", font=("Any", 10)), sg.Text(text="Set 1", size=(50, 1), justification="center", font=("Any", 10))],
           [sg.Column(layout=bloq0L2Column, element_justification="center"), sg.Column(layout=bloq1L2Column, element_justification="center"), sg.Column(layout=bloq2L2Column, element_justification="center"), sg.Column(layout=bloq3L2Column, element_justification="center")],
           [sg.Text(text="Contenido de la Memoria", size=(105, 1), justification="center", font=("Any", 10)), sg.Text(text="Última Instrucción Generada:", size=(40, 1), justification="center", font=("Any", 10)), sg.Text(text="XX: XXXXX XXX;XXXX", justification="center", font=("Any", 10), key="ultimaInstruccion")],
           [sg.Column(layout=bloq0MemColumn, element_justification="center"), sg.Column(layout=bloq1MemColumn, element_justification="center"), sg.Column(layout=bloq2MemColumn, element_justification="center"), sg.Column(layout=bloq3MemColumn, element_justification="center"), sg.Column(layout=bloq4MemColumn, element_justification="center"), sg.Column(layout=bloq5MemColumn, element_justification="center"), sg.Column(layout=bloq6MemColumn, element_justification="center"), sg.Column(layout=bloq7MemColumn, element_justification="center"), sg.Text(text="Siguiente Instrucción:", size=(40, 1), justification="center", font=("Any", 10)), sg.Text(text="XX: XXXXX XXX;XXXX", justification="center", font=("Any", 10), key="siguienteInstruccion")],
           [sg.Button(button_text="Ejecución Continua", font=("Any", 10), disabled=False, key="reanudar"), sg.Button(button_text="Pausa", font=("Any", 10), disabled=True, key="pausa"), sg.Button(button_text="Paso", font=("Any", 10), disabled=False, key="paso"), sg.InputText(disabled=False, key="nuevaInstruccion"), sg.Button(button_text="Aceptar", font=("Any", 10), disabled=False, key="aceptar")] ]

window = sg.Window(title="Protocolo Basado en Directorios en Sistemas Multiprocesador", layout=layout)

def listToString(sharers):
    if not (sharers):
        return ""
    else:
        return ", ".join([str(proc) for proc in sharers])

def decimalToBinary(decimalNumber):
    return bin(decimalNumber).replace("0b", "")

def decimalToHexadecimal(hexadecimalNumber):
    return hex(hexadecimalNumber).replace("0x", "")

def updateL1Data():
    l1cachedata = l1c.L1CacheDataHolder()
    procinstrdata = ih.InstructionsHolder()

    window["instruccion0"].update(procinstrdata.getInstruction0())
    window["l1coherencia00"].update(l1cachedata.getCoherence00())
    window["l1direccion00"].update(decimalToBinary(l1cachedata.getAddress00()))
    window["l1dato00"].update(decimalToHexadecimal(l1cachedata.getData00()))
    window["l1coherencia01"].update(l1cachedata.getCoherence01())
    window["l1direccion01"].update(decimalToBinary(l1cachedata.getAddress01()))
    window["l1dato01"].update(decimalToHexadecimal(l1cachedata.getData01()))

    window["instruccion1"].update(procinstrdata.getInstruction1())
    window["l1coherencia10"].update(l1cachedata.getCoherence10())
    window["l1direccion10"].update(decimalToBinary(l1cachedata.getAddress10()))
    window["l1dato10"].update(decimalToHexadecimal(l1cachedata.getData10()))
    window["l1coherencia11"].update(l1cachedata.getCoherence11())
    window["l1direccion11"].update(decimalToBinary(l1cachedata.getAddress11()))
    window["l1dato11"].update(decimalToHexadecimal(l1cachedata.getData11()))

    window["instruccion2"].update(procinstrdata.getInstruction2())
    window["l1coherencia20"].update(l1cachedata.getCoherence20())
    window["l1direccion20"].update(decimalToBinary(l1cachedata.getAddress20()))
    window["l1dato20"].update(decimalToHexadecimal(l1cachedata.getData20()))
    window["l1coherencia21"].update(l1cachedata.getCoherence21())
    window["l1direccion21"].update(decimalToBinary(l1cachedata.getAddress21()))
    window["l1dato21"].update(decimalToHexadecimal(l1cachedata.getData21()))

    window["instruccion3"].update(procinstrdata.getInstruction3())
    window["l1coherencia30"].update(l1cachedata.getCoherence30())
    window["l1direccion30"].update(decimalToBinary(l1cachedata.getAddress30()))
    window["l1dato30"].update(decimalToHexadecimal(l1cachedata.getData30()))
    window["l1coherencia31"].update(l1cachedata.getCoherence31())
    window["l1direccion31"].update(decimalToBinary(l1cachedata.getAddress31()))
    window["l1dato31"].update(decimalToHexadecimal(l1cachedata.getData31()))

    return

def updateL2Data():
    l2cache = l2c.L2Cache()
    l2set0 = l2cache.getSet0()
    l2set1 = l2cache.getSet1()
    l2block0 = l2set0.getBlock0()
    l2block1 = l2set0.getBlock1()
    l2block2 = l2set1.getBlock0()
    l2block3 = l2set1.getBlock1()

    window["l2coherencia0"].update(l2block0.getCoherence())
    window["l2dueno0"].update(str(l2block0.getOwner()))
    window["l2compartidos0"].update(listToString(l2block0.getSharers()))
    window["l2direccion0"].update(decimalToBinary(l2block0.getAddress()))
    window["l2dato0"].update(decimalToHexadecimal(l2block0.getData()))

    window["l2coherencia1"].update(l2block1.getCoherence())
    window["l2dueno1"].update(str(l2block1.getOwner()))
    window["l2compartidos1"].update(listToString(l2block1.getSharers()))
    window["l2direccion1"].update(decimalToBinary(l2block1.getAddress()))
    window["l2dato1"].update(decimalToHexadecimal(l2block1.getData()))

    window["l2coherencia2"].update(l2block2.getCoherence())
    window["l2dueno2"].update(str(l2block2.getOwner()))
    window["l2compartidos2"].update(listToString(l2block2.getSharers()))
    window["l2direccion2"].update(decimalToBinary(l2block2.getAddress()))
    window["l2dato2"].update(decimalToHexadecimal(l2block2.getData()))

    window["l2coherencia3"].update(l2block3.getCoherence())
    window["l2dueno3"].update(str(l2block3.getOwner()))
    window["l2compartidos3"].update(listToString(l2block3.getSharers()))
    window["l2direccion3"].update(decimalToBinary(l2block3.getAddress()))
    window["l2dato3"].update(decimalToHexadecimal(l2block3.getData()))

    return

def updateMemoryData():
    memory = mem.Memory()
    memblock0 = memory.getBlock0()
    memblock1 = memory.getBlock1()
    memblock2 = memory.getBlock2()
    memblock3 = memory.getBlock3()
    memblock4 = memory.getBlock4()
    memblock5 = memory.getBlock5()
    memblock6 = memory.getBlock6()
    memblock7 = memory.getBlock7()

    window["memdato0"].update(decimalToHexadecimal(memblock0.getData()))
    window["memdato1"].update(decimalToHexadecimal(memblock1.getData()))
    window["memdato2"].update(decimalToHexadecimal(memblock2.getData()))
    window["memdato3"].update(decimalToHexadecimal(memblock3.getData()))
    window["memdato4"].update(decimalToHexadecimal(memblock4.getData()))
    window["memdato5"].update(decimalToHexadecimal(memblock5.getData()))
    window["memdato6"].update(decimalToHexadecimal(memblock6.getData()))
    window["memdato7"].update(decimalToHexadecimal(memblock7.getData()))

    return  

def createProcessorsAux(number):
    procesor = proc.Procesor(number)
    procesor.readOperation()

def createProcessors():
    process0 = Thread(target=createProcessorsAux, args=(0,), daemon=True)
    process1 = Thread(target=createProcessorsAux, args=(1,), daemon=True)
    process2 = Thread(target=createProcessorsAux, args=(2,), daemon=True)
    process3 = Thread(target=createProcessorsAux, args=(3,), daemon=True)
    
    process0.start()
    #process1.start()
    #process2.start()
    #process3.start()
    return

#def analyzeInstruction(instruction):


def main():
    #gui_queue = queue.Queue()

    createProcessors()

    while True:
        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED or event == "Cancel":
            break
        if event == "pausa":
            window["reanudar"].update(disabled=False)
            window["pausa"].update(disabled=True)
            window["paso"].update(disabled=False)
            window["nuevaInstruccion"].update(disabled=False)
            window["aceptar"].update(disabled=False)
        if event == "reanudar":
            window["reanudar"].update(disabled=True)
            window["pausa"].update(disabled=False)
            window["paso"].update(disabled=True)
            window["nuevaInstruccion"].update(disabled=True)
            window["aceptar"].update(disabled=True)
        if event == "aceptar":
            window["siguienteInstruccion"].update(values["nuevaInstruccion"])

        updateL1Data()
        updateL2Data()        
        updateMemoryData()

    window.close()

if __name__ == "__main__":
    main()