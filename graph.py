import os
import openal

class node:
    def __init__(self, num, sound, gain = 1, text=""):
        self.__num = num
        self.__sound = sound
        self.__text = text
        self.__gain = gain

    def get_num(self):
        return self.__num
    
    def get_text(self):
        return self.__text
    
    def play(self):
        currentDir = os.path.dirname(os.path.abspath(__file__))
        fileM = os.path.join(currentDir, "Music", self.__sound)
        openal.oalInit()
        source = openal.oalOpen(fileM)
        source.set_gain(self.__gain)
        source.play()
        while source.get_state() == openal.AL_PLAYING:
            pass
        openal.oalQuit()


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
    
    def get_node(self, node:node):
        for key_node in self.__graph.keys():
            if key_node == node:
                return key_node
        return None