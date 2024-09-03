from graph import graph, node

def main():
    # Create a new graph
    g = graph()
    nodeList = [    
        node(1, "sil.wav", 0.5, "Eres un cientifico que descubrio como viajar en el tiempo, te entro una gran curiosidad por lo que pasaria si cambias algo del pasado, y puedes viajar a estas epocas: "), 
        node(2, "time.wav", 1, "Epoca medieval"), 
        node(3, "disparos.wav", 1, "Epoca del antiguo egipto")
    ]
    for i in nodeList:
        g.new_node(i)

    nodeSound = g.get_node(nodeList[0])
    print(nodeSound.get_text())
    nodeSound.play()

    g.new_edge((nodeList[0], nodeList[1]))
    g.new_edge((nodeList[0], nodeList[2]))


    currentNode = g.get_node(nodeList[0])
    finishNode = g.get_node(nodeList[-1])
    while (currentNode != finishNode):
        print(currentNode.get_text())
        paths = g.get_edge_node(currentNode)
        print("Puedes hacer lo siguiente: ")
        for i, n in enumerate(paths):
            print(i+1, "-->", n.get_text())
    
        next = input("Que deseas Hacer: ")



main()