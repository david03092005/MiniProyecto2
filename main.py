from graph import graph, node
import openal
import sys
import time
import threading
import json
import os


def main():
    global g
    openal.oalInit()
    # Create a new graph
    g = graph()
    
    data = loadFromJson("info.json")
    # nodeList = processNodes(data)
    processNodes(data)

    paths = loadFromJson("paths.json")
    processEdges(paths)

    currentNode = g.get_node(0)
    finishNode = g.get_node(3)
    while (currentNode != finishNode):
        textThread = threading.Thread(target=writeMachine, args=(currentNode.get_text(), 0.01))
        musicThread = threading.Thread(target=currentNode.play)
        musicThread.start()
        textThread.start()
        musicThread.join()
        textThread.join()
        paths = g.get_edge_node(currentNode)
        for i, n in enumerate(paths):
            text = str(i+1) + " --> " + n.get_option()
            writeMachine(text, 0.005)
    
        writeMachine("Que deseas Hacer: ", 0.003)
        next = int(input())
        currentNode = paths[next - 1]

    writeMachine(currentNode.get_text(), 0.01)
    currentNode.play()
    writeMachine("El juego a terminado, Muchas gracias por jugar, vuelve cuando quieras.", 0.06)

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
    with open(fileName, 'r') as file:
        data = json.load(file)
    return data


def processNodes(data):
    global g
    for n in data:
        g.new_node(node(n['id'], n['sound'], list(n['position']), n['volume'], n['text'], n['option']))


def processEdges(data):
    global g
    for edge in data:
        nodeOut = g.get_node(edge['from'])
        for inEdge in edge['path']:
            nodeIn = g.get_node(inEdge)
            g.new_edge((nodeOut, nodeIn))


main()