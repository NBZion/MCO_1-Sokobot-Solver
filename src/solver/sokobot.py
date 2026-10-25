from src.solver.graph import SokBotGraph
import networkx as nx
import matplotlib.pyplot as plt
import time


class SokoBot:
    def solveSokobanPuzzle(self, width, height, mapData, itemsData):
        # YOU NEED TO REWRITE THE IMPLEMENTATION OF THIS METHOD TO MAKE THE BOT SMARTER
        # Default stupid behavior: Think (sleep) for 3 seconds, and then return a
        # sequence
        # that just moves left and right repeatedly.

        graph = SokBotGraph()

        graph.convertDataToGraph(mapData, itemsData)

        # Draw nodes and edges
        nx.draw(graph.graph, with_labels=True, node_color='skyblue', node_size=500)

        # Displays an interactive desktop GUI window
        plt.title("2D Grid Graph")
        plt.show()

        try:
            time.sleep(3)
        except Exception as ex:
            print(ex)
        return "lrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlrlr"
