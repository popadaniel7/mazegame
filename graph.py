#graph class
#this designs the map and the maze
#contains a set of vertices and a list of directed edges
#edges are modelled as tuples (u,v) of vertices
#uses adjacency list representation

class Graph:

  def __init__(self, Vertices = set(), Edges = list()):

    """
    Makes a graph with a copy of the given set of vertices and given list of edges

    >>> g = Graph({1,2,3}, [(1,2), (2,3)])
    >>> g.alist.keys() == {1,2,3}
    >>> g.alist[1] == [2]
    >>> g.alist[3] == []
    >>> h1 = Graph()
    >>> h2 = Graph()
    >>> h1.add_vertex(1)
    >>> h1.alist.keys() == {1}
    >>> h2.alist.keys() == set()
    """

    self.alist = {}

    for v in Vertices:
      self.add_vertex(v)
    for e in Edges:
      self.add_edge(e)

  def get_vertices(self):

    """
    Returns the set of vertices in the graph

    >>> g = Graph({1,2,3}, [(1,2), (2,3)])
    >>> g.get_vertices() == {1, 2, 3}
    >>> h = Graph()
    >>> h.get_vertices() == set()
    """

    return set(self.alist.keys())

  def get_edges(self):#returns a list of all edges

    edges = []
    for v,l in self.alist.items():
      edges += l
    return edges

  def add_vertex(self, v):

    """
    >>> g = Graph()
    >>> len(g.get_vertices())
    >>> g.add_vertex(1)
    >>> g.add_vertex("vertex")
    >>> "vertex" in g.get_vertices()
    >>> 2 in g.get_vertices()
    """

    if v not in self.alist:
      self.alist[v] = []

  def add_edge(self, e):

    """
    >>> g = Graph()
    >>> g.add_vertex(1)
    >>> g.add_vertex(2)
    >>> g.add_edge((1,2))
    >>> 2 in g.alist[1]
    >>> 1 in g.alist[2]
    >>> g.add_edge((1,2))
    >>> g.alist[1] == [2, 2]
    """

    if not self.is_vertex(e[0]) or not self.is_vertex(e[1]):
      raise ValueError("An endpoint is not in graph")
    self.alist[e[0]].append(e[1])

  def is_vertex(self, v):

    """
    >>> g = Graph({1,2})
    >>> g.is_vertex(1)
    >>> g.is_vertex(3)
    >>> g.add_vertex(3)
    >>> g.is_vertex(3)
    """

    return v in self.alist

  def is_edge(self, e):

    """
    >>> g = Graph({1,2}, [(1,2)])
    >>> g.is_edge((1,2))
    >>> g.is_edge((2,1))
    >>> g.add_edge((1,2))
    >>> g.is_edge((1,2))
    """

    if e[0] not in self.alist:
      return False

    return e[1] in self.alist[e[0]]

  def neighbours(self, v):

    """
    >>> Edges = [(1,2),(1,4),(3,1),(3,4),(2,4),(1,2)]
    >>> g = Graph({1,2,3,4}, Edges)
    >>> g.neighbours(1)
    >>> g.neighbours(4)
    >>> g.neighbours(3)
    >>> g.neighbours(2)
    """

    if not self.is_vertex(v):
      raise ValueError("Vertex not in graph")

    return self.alist[v]


def is_walk(g, walk):

  """
  >>> Edges = [(1,2),(1,3),(2,5),(3,4),(4,2),(5,4)]
  >>> g = Graph({1,2,3,4,5}, Edges)
  >>> is_walk(g, [3,4,2,5,4,2])
  >>> is_walk(g, [5,4,2,1,3])
  >>> is_walk(g, [2])
  >>> is_walk(g, [])
  >>> is_walk(g, [1,6])
  >>> is_walk(g, [6])
  """

  if not walk:
    return False

  if len(walk) == 1:
    return g.is_vertex(walk[0])

  for i in range(len(walk)-1):
    if not g.is_edge((walk[i], walk[i+1])):
      return False

  return True


def is_path(g, path):

  """
  >>> Edges = [(1,2),(1,3),(2,5),(3,4),(4,2),(5,4)]
  >>> g = Graph({1,2,3,4,5}, Edges)
  >>> is_path(g, [3,4,2,5,4,2])
  >>> is_path(g, [3,4,2,5])
  """

  if len(set(path)) < len(path):
    return False

  return is_walk(g, path)

if __name__ == "__main__":

  import doctest
  doctest.testmod()
