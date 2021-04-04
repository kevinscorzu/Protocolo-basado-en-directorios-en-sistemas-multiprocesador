import l1cache as l1c
import l2cache as l2c
import memory as mem
import l1cachedataholder as l1cHolder

import random
import time

class Control:
    def __init__(self):
        self.l1cache = l1c.L1Cache()
        self.l1cdata = l1cHolder.L1CacheDataHolder()

        self.l1getCoherence0Dictionary = {
                                        0: self.l1cdata.getCoherence00,
                                        1: self.l1cdata.getCoherence10,
                                        2: self.l1cdata.getCoherence20,
                                        3: self.l1cdata.getCoherence30
                                      }
        self.l1getCoherence1Dictionary = {
                                        0: self.l1cdata.getCoherence01,
                                        1: self.l1cdata.getCoherence11,
                                        2: self.l1cdata.getCoherence21,
                                        3: self.l1cdata.getCoherence31
                                      }
        self.l1setCoherence0Dictionary = {
                                        0: self.l1cdata.setCoherence00,
                                        1: self.l1cdata.setCoherence10,
                                        2: self.l1cdata.setCoherence20,
                                        3: self.l1cdata.setCoherence30
                                      }
        self.l1setCoherence1Dictionary = {
                                        0: self.l1cdata.setCoherence01,
                                        1: self.l1cdata.setCoherence11,
                                        2: self.l1cdata.setCoherence21,
                                        3: self.l1cdata.setCoherence31
                                      }
        self.l1getAddress0Dictionary = {
                                        0: self.l1cdata.getAddress00,
                                        1: self.l1cdata.getAddress10,
                                        2: self.l1cdata.getAddress20,
                                        3: self.l1cdata.getAddress30
                                    }
        self.l1getAddress1Dictionary = {
                                        0: self.l1cdata.getAddress01,
                                        1: self.l1cdata.getAddress11,
                                        2: self.l1cdata.getAddress21,
                                        3: self.l1cdata.getAddress31
                                    }
        self.l1setAddress0Dictionary = {
                                        0: self.l1cdata.setAddress00,
                                        1: self.l1cdata.setAddress10,
                                        2: self.l1cdata.setAddress20,
                                        3: self.l1cdata.setAddress30
                                    }
        self.l1setAddress1Dictionary = {
                                        0: self.l1cdata.setAddress01,
                                        1: self.l1cdata.setAddress11,
                                        2: self.l1cdata.setAddress21,
                                        3: self.l1cdata.setAddress31
                                    }
        self.l1getData0Dictionary = {
                                    0: self.l1cdata.getData00,
                                    1: self.l1cdata.getData10,
                                    2: self.l1cdata.getData20,
                                    3: self.l1cdata.getData30
                                 }
        self.l1getData1Dictionary = {
                                    0: self.l1cdata.getData01,
                                    1: self.l1cdata.getData11,
                                    2: self.l1cdata.getData21,
                                    3: self.l1cdata.getData31
                                 }
        self.l1setData0Dictionary = {
                                    0: self.l1cdata.setData00,
                                    1: self.l1cdata.setData10,
                                    2: self.l1cdata.setData20,
                                    3: self.l1cdata.setData30
                                 }
        self.l1setData1Dictionary = {
                                    0: self.l1cdata.setData01,
                                    1: self.l1cdata.setData11,
                                    2: self.l1cdata.setData21,
                                    3: self.l1cdata.setData31
                                 }

    def handleOperation(self, operation, procNumber, address, data):
        self.updateLocalCache(procNumber)
        if not (address % 2):
            l1block = self.l1cache.getL1BlockBySet(0)
            return self.handleOperationAux(l1block, operation, procNumber, address, data, 0)
        else:
            l1block = self.l1cache.getL1BlockBySet(1)
            return self.handleOperationAux(l1block, operation, procNumber, address, data, 1)

    def handleOperationAux(self, l1block, operation, procNumber, address, data, l1set):
        if (operation == "R"):
            return self.handleRead(procNumber, address, l1block, l1set)
        else:
            return self.handleWrite(procNumber, address, data, l1block, l1set)

    def updateLocalCache(self, procNumber): 
        l1blocks = self.l1cache.getAllBlocks()
        l1blocks[0].setCoherence(self.l1getCoherence0Dictionary.get(procNumber)())
        l1blocks[1].setCoherence(self.l1getCoherence1Dictionary.get(procNumber)())

        l1blocks[0].setAddress(self.l1getAddress0Dictionary.get(procNumber)())
        l1blocks[1].setAddress(self.l1getAddress1Dictionary.get(procNumber)())

        l1blocks[0].setData(self.l1getData0Dictionary.get(procNumber)())
        l1blocks[1].setData(self.l1getData1Dictionary.get(procNumber)())

        return

    def updateHolderCache(self, procNumber, l1set):
        l1blocks = self.l1cache.getAllBlocks()

        if not (l1set):
            l1block = l1blocks[0]
            self.l1setCoherence0Dictionary.get(procNumber)(l1block.getCoherence())
            self.l1setAddress0Dictionary.get(procNumber)(l1block.getAddress())
            self.l1setData0Dictionary.get(procNumber)(l1block.getData())
            return
        else:
            l1block = l1blocks[1]
            self.l1setCoherence1Dictionary.get(procNumber)(l1block.getCoherence())
            self.l1setAddress1Dictionary.get(procNumber)(l1block.getAddress())
            self.l1setData1Dictionary.get(procNumber)(l1block.getData())
            return

    def invalidateHolderCache(self, procNumber, l1set):
        if not (l1set):
            self.l1setCoherence0Dictionary.get(procNumber)("I")
            return
        else:
            self.l1setCoherence1Dictionary.get(procNumber)("I")
            return
    
    def handleRead(self, procNumber, address, l1block, l1set):
        coherence = l1block.getCoherence()
        if (coherence == "I"):
            return self.handleMissRead(procNumber, address, l1block, l1set)
        elif (address == l1block.getAddress()):
            return l1block.getData()
        else:
            return self.handleMissRead(procNumber, address, l1block, l1set)

    def handleMissRead(self, procNumber, address, l1block, l1set):
        l2cache = l2c.L2Cache()
        l2set = l2cache.getL2SetByNumber(l1set)
        l2blocks = l2set.getAllBlocks()
        i = 0
        j = -1
        while (i != len(l2blocks)):
            l2block = l2blocks[i]
            if (l2block.getCoherence() == "DI"):
                j = i
                i += 1
            elif (l2block.getAddress() == address):
                self.setL1Block(l1block, "S", address, l2block.getData())
                self.updateHolderCache(procNumber, l1set)

                sharers = []
                if (l2block.getCoherence() == "DM"):
                    self.updateHolderCache(l2block.getOwner(), l1set)
                    sharers.append(l2block.getOwner())
                    sharers.append(procNumber)
                    self.setL2Block(l2block, "DS", -1, sharers, l2block.getAddress(), l2block.getData())
               
                    return

                else:
                    sharers += l2block.getSharers()
                    sharers.append(procNumber)
                    self.setL2Block(l2block, "DS", -1, sharers, l2block.getAddress(), l2block.getData())
               
                    return
                
            else:
                i += 1

        if (j == -1):
            j = random.randint(0, 1)

        l2block = l2blocks[j]
        if (l2block.getCoherence() != "DI"):
            self.setDataToMemory(l2block.getAddress(), l2block.getData())

        data = self.getDataFromMemory(address)

        self.setL2Block(l2block, "DS", -1, [procNumber], address, data)
        self.setL1Block(l1block, "S", address, data)
        self.updateHolderCache(procNumber, l1set)
        
        return

    def handleWrite(self, procNumber, address, data, l1block, l1set):
        coherence = l1block.getCoherence()
        if (coherence == "I" or coherence == "S"):
            return self.handleMissWrite(procNumber, address, data, l1block, l1set)
        elif (address == l1block.getAddress()):
            l1block.setData(data)
            return
        else:
            return self.handleMissWrite(procNumber, address, data, l1block, l1set)

    def handleMissWrite(self, procNumber, address, data, l1block, l1set):
        l2cache = l2c.L2Cache()
        l2set = l2cache.getL2SetByNumber(l1set)
        l2blocks = l2set.getAllBlocks()
        i = 0
        j = -1
        while (i != len(l2blocks)):
            l2block = l2blocks[i]
            if (l2block.getCoherence() == "DI"):
                j = i
                i += 1
            elif (l2block.getAddress() == address):
                self.setL1Block(l1block, "M", address, data)
                self.updateHolderCache(procNumber, l1set)

                return self.handleCacheInvalidations(procNumber, number, address, data, l2block, l1set)
            else:
                i += 1

        if (j == -1):
            j = random.randint(0, 1)

        l2block = l2blocks[j]
        if (l2block.getCoherence() != "DI"):
            self.setDataToMemory(l2block.getAddress(), l2block.getData())

        self.setL2Block(l2block, "DM", procNumber, [], address, data)
        self.setL1Block(l1block, "M", address, data)
        self.updateHolderCache(procNumber, l1set)
        
        return

    def handleCacheInvalidations(self, procNumber, address, data, l2block, l1set):
        sharers = l2block.getSharers()
        self.setL2Block(l2block, "DM", procNumber, [], address, data)

        for procesor in sharers:
            self.invalidateHolderCache(procesor, l1set)
        
        return

    def getDataFromMemory(self, address):
        memory = mem.Memory()
        memblock = memory.getBlockByNumber(address)
        return memblock.getData()

    def setDataToMemory(self, address, data):
        memory = mem.Memory()
        memblock = memory.getBlockByNumber(address)
        memblock.setData(data)
        return

    def setL2Block(self, l2block, coherence, owner, sharers, address, data):
        l2block.setCoherence(coherence)
        l2block.setOwner(owner)
        l2block.setSharers(sharers)
        l2block.setAddress(address)
        l2block.setData(data)
        return

    def setL1Block(self, l1block, coherence, address, data):
        l1block.setCoherence(coherence)
        l1block.setAddress(address)
        l1block.setData(data)
        return