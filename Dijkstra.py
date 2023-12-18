
from bridges.graph_adj_list import *
import heapq

class Dijkstra():
    def __init__(self, inputFile, startingVertex, goalVertex):
        # an initially empty dictionary containing mapping: vertex: [child, weight]
        self.adjacency = {}
        # collection of vertices
        self.vertices = []
        # each dictionary entry contains mapping of vertex:parent
        self.parent = {}
        # startingVertex, goalVertex
        self.startingVertex, self.goalVertex = startingVertex, goalVertex

        # The following reads in the input file and constructs an adjacency list of the graph.
        graph = open(inputFile)
        for line in graph:
            entry = line.split()

            # get the vertices
            self.vertices.append(entry[0])
            self.vertices.append(entry[1])

            if entry[0] not in self.adjacency:
                self.adjacency[entry[0]] = []

            # construct an edge for the adjacency list
            edge = (entry[1], int(entry[2]))
            self.adjacency[entry[0]].append(edge)

        # remove duplication in vertices
        self.vertices = list(set(self.vertices))

        # checking if start and goal are in vertices
        if startingVertex not in self.vertices:
            print('Starting vertex', startingVertex, 'not present in graph')
            quit()
        elif goalVertex not in self.vertices:
            print('Goal vertex', goalVertex, 'not present in graph')
            quit()

        # create Bridges graph
        self.g = GraphAdjList()
        for vertex in self.vertices:
            self.g.add_vertex(vertex, str(vertex))
            self.g.get_visualizer(vertex).color = "red"
        
        for vertex in self.adjacency:
            for edge in self.adjacency[vertex]:
                self.g.add_edge(vertex, edge[0], edge[1])

    # solve it using Dijkstra algorithm
    def solve(self):
        # make a priority queue
        pqueue = []
        heapq.heappush(pqueue, (0, self.startingVertex, None))
        visited = [] # list containing visited nodes
        while pqueue:
            current_item = heapq.heappop(pqueue)
            current = current_item[1]
            if current not in visited:
                self.parent[current] = current_item[2]

                if current == self.goalVertex:
                    return True

                visited.append(current)
                for child in self.adjacency[current]:
                    # all the children are added to the subtree
                    # priority of vertex will be cost_from_start + weight_from_vertex_to_child
                    priority = current_item[0] + child[1]
                    heapq.heappush(pqueue, (priority, child[0], current))


    # retrieve the path from start to the goal 
    def find_path(self):
        self.path = []
        # your code goes here:
        vertex = self.goalVertex
        while vertex != self.startingVertex:
            self.path.append(vertex)
            vertex = self.parent[vertex]
        self.path.append(self.startingVertex)
        self.path.reverse()
    
    # draw the path as red
    def draw_path(self):
        print(self.path)
        for i in range(len(self.path)-1):
            self.g.get_link_visualizer(self.path[i], self.path[i+1]).color = "red"

    # return the Bridges object
    def get_graph(self):
        return self.g
