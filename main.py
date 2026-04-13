import graphvis
import graph

if __name__ == "__main__":
    g = graph.Graph(is_directed=False)
    
    edges = [
        ["A", "B", 10], ["B", "C", 15], 
        ["C", "D", 12], ["D", "E", 10],
        ["E", "A", 8],  ["A", "C", 20], 
        ["B", "D", 25], ["C", "E", 18]
    ]
    g.add_edges(edges)
    
    viz = graphvis.Visualizer(backend_graph=g)
    viz.render()