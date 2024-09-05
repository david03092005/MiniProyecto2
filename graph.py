import os
import openal
import sys
import time

class node:
    def __init__(self, id, sound, position, gain = 1, text="", option=""):
        self.__id = id
        self.__sound = sound
        self.__position = position
        self.__gain = gain
        self.__text = text
        self.__option = option

    def get_num(self):
        return self.__id
    
    def get_text(self):
        return self.__text

    def get_option(self):
        return self.__option
    
    def play(self):
        currentDir = os.path.dirname(os.path.abspath(__file__))
        fileM = os.path.join(currentDir, "Music", self.__sound)
        source = openal.oalOpen(fileM)
        source.set_gain(self.__gain)
        source.set_position(self.__position)
        source.play()
        while source.get_state() == openal.AL_PLAYING:
            pass
        


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