from entities import control as ctrl
from entities import instructionsholder as instrHolder

import time
from multiprocessing import Process

class Procesor:
    def __init__(self, number, memory, l2cache, instructionsHolder, l1cachedataholder, mutex):
        self.number = number
        self.control = ctrl.Control(l1cachedataholder, l2cache, memory, mutex)
        self.instrData = instructionsHolder
        self.memory = memory
        self.l2cache = l2cache

        self.getInstructionDictionary = {
            0: self.instrData.getInstruction0,
            1: self.instrData.getInstruction1,
            2: self.instrData.getInstruction2,
            3: self.instrData.getInstruction3
        }
                                                                              
        self.getInstructionReadDictionary = {
            0: self.instrData.getInstruction0Read,
            1: self.instrData.getInstruction1Read,
            2: self.instrData.getInstruction2Read,
            3: self.instrData.getInstruction3Read
        }
                                              
        self.setInstructionReadDictionary = {
            0: self.instrData.setInstruction0Read,
            1: self.instrData.setInstruction1Read,
            2: self.instrData.setInstruction2Read,
            3: self.instrData.setInstruction3Read
        }
                                                
                                              
        self.hexadecimalDictionary = {
            "0": 0,
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "a": 10,
            "b": 11,
            "c": 12,
            "d": 13,
            "e": 14,
            "f": 15
        }
                                        
        self.binaryDictionary = {
            "0": 0,
            "1": 1
        }

    def getNumber(self):
        return self.number

    def setNumber(self, number):
        self.number = number
        return

    def binaryToDecimal(self, binaryNumber):
        try:
            result = 0
            exp = 0
            binaryNumber = binaryNumber[::-1]
            for digit in binaryNumber:
                result += self.binaryDictionary.get(digit) * (2**exp)
                exp += 1
            return result
        except:
            print("P" + str(self.number) + ": El address de la instruccion no es válido")
            return -1
                    

    def hexadecimalToDecimal(self, hexadecimalNumber):
        try:    
            result = 0
            exp = 0
            hexadecimalNumber = hexadecimalNumber[::-1]
            for digit in hexadecimalNumber:
                result += self.hexadecimalDictionary.get(digit) * (16**exp)
                exp += 1
            return result
        except:
            print("P" + str(self.number) + ": El dato de la instruccion no es válido")
            return -1

    def readOperation(self):
        while (True):
            state = self.getInstructionReadDictionary.get(self.number)()
            if not (state):
                instr = self.getInstructionDictionary.get(self.number)()
                wait = round(self.instrData.getInstructionTime() / 2)
                if (instr[:5] == "write"):
                    address = self.binaryToDecimal(instr[6:9])
                    data = self.hexadecimalToDecimal(instr[10:14])
                    if (address != -1 and data != -1):
                        time.sleep(wait)
                        self.control.handleOperation("W", self.number, address, data)
                        time.sleep(wait)
                        print("P" + str(self.number) + ": Instrucción ejecutada")
                    self.setInstructionReadDictionary.get(self.number)(1)
                elif (instr[:4] == "read"):
                    address = self.binaryToDecimal(instr[5:8])
                    if (address != -1):    
                        time.sleep(wait)
                        self.control.handleOperation("R", self.number, address, -1)
                        time.sleep(wait)
                        print("P" + str(self.number) + ": Instrucción ejecutada")
                    self.setInstructionReadDictionary.get(self.number)(1)
                elif (instr[:4] == "calc"):
                    time.sleep(wait)
                    time.sleep(wait)
                    print("P" + str(self.number) + ": Instrucción ejecutada")
                    self.setInstructionReadDictionary.get(self.number)(1)
                else:
                    print("P" + str(self.number) + ": Instrucción no Válida, no se pudo identificar la operación")
                    self.setInstructionReadDictionary.get(self.number)(1)