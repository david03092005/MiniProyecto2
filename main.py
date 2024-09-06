from graph import graph, node
import openal
import sys
import time
import threading
import json
import os

sys.stdout.reconfigure(encoding='utf-8')

def main():
    global g
    openal.oalInit()
    # Create a new graph
    g = graph()
    
    data = loadFromJson("info.json")
    processNodes(data)

    paths = loadFromJson("paths.json")
    processEdges(paths)

    currentNode = g.get_node(0)
    while (not currentNode.get_final()):
        textThread = threading.Thread(target=writeMachine, args=(currentNode.get_text(), 0.001))
        musicThread = threading.Thread(target=currentNode.play)
        musicThread.start()
        textThread.start()
        textThread.join()
        paths = g.get_edge_node(currentNode)
        for i, n in enumerate(paths):
            text = str(i+1) + " --> " + n.get_option()
            writeMachine(text, 0.001)
    
        writeMachine("Que deseas Hacer: ", 0.001)
        next = -1
        error = True
        while (error):
            next = input()
            try:
                next = int(next)
                if (next >= 1 and next <= len(paths)):
                    error = False
                else:
                    raise ValueError()
            except ValueError:
                print("Entrada inválida. Asegúrate de ingresar un número entero entre 1 y", len(paths))
        
        currentNode.set_stop()
        musicThread.join()
        currentNode = paths[int(next) - 1]

    writeMachine(currentNode.get_text(), 0.05)
    currentNode.play()
    writeMachine("El juego a terminado, Muchas gracias por jugar, vuelve cuando quieras.", 0.04)

    openal.oalQuit()


def writeMachine(text, delay):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def loadFromJson(name):
    currentDir = os.path.dirname(os.path.abspath(__file__))
    fileName = os.path.join(currentDir, "infoHistory", name)
    with open(fileName, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def processNodes(data):
    global g
    for n in data:
        g.new_node(node(n['id'], n['sound'], list(n['position']), n['volume'], n['text'], n['option'], n['gameOver']))


def processEdges(data):
    global g
    for edge in data:
        nodeOut = g.get_node(edge['from'])
        for inEdge in edge['path']:
            nodeIn = g.get_node(inEdge)
            g.new_edge((nodeOut, nodeIn))


main()