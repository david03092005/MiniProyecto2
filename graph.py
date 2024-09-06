import os
import openal
import sys
import time


sys.stdout.reconfigure(encoding='utf-8')

class node:
    def __init__(self, id, sounds, positions, gain = 1, text="", option="", final=False):
        self.__id = id
        self.__sounds = sounds
        self.__positions = positions
        self.__gain = gain
        self.__text = text
        self.__option = option
        self.__final = final
        self.__stop = False

    def get_num(self):
        return self.__id
    
    def get_text(self):
        return self.__text

    def get_option(self):
        return self.__option
    
    def get_final(self):
        return self.__final

    def set_stop(self):
        self.__stop = True
        
    def play(self):
        currentDir = os.path.dirname(os.path.abspath(__file__))
        sources = []
        i = 0
        for sound in self.__sounds:
            fileM = os.path.join(currentDir, "Music", sound)
            
            source = openal.oalOpen(fileM)
            source.set_gain(self.__gain[i])
            source.set_position(self.__positions[i])
            source.play()
            
            sources.append(source)
            i += 1;
        
        while any(source.get_state() == openal.AL_PLAYING for source in sources):
            if (self.__stop):
                n = 0
                for source in sources:
                    volum = round(self.__gain[n] * 1000)
                    for i in range(volum, 0, -1):
                        source.set_gain(i/1000)
                        time.sleep(0.0005)
                    n += 1

                    source.stop()


class graph:
    def __init__(self, graph = {}):
        self.__graph = graph

    def new_node(self, node:node):
        self.__graph[node] = []

    def get_edge_node(self, nodeI:node):
        return self.__graph[nodeI]

    def new_edge(self, edge):
        self.__graph[edge[0]].append(edge[1])

    def take_edge(self, posEdge):
        return self.__graph[posEdge]
    
    def get_node(self, nodeID):
        for key_node in self.__graph.keys():
            if key_node.get_num() == nodeID:
                return key_node
        return None