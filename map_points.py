from heapq import *

#every point of the map is designed here

#formula used to place points
def heuristic(start, end):

    return abs(start[0]-end[0])+abs(start[1]-end[1])

#core functions for map points
def map_points(start, end, grid):

    closedSet = set()
    openSet = []
    cameFrom = {}
    gScore = {}
    fScore = {}

    for i in grid.get_vertices():
        gScore[i] = float("inf")
        fScore[i] = float("inf")

    gScore[start] = 0
    fScore[start] = heuristic(start, end)
    heappush(openSet, (start, fScore[start]))

    while openSet:
        current = heappop(openSet)[0]
        if current == end:
            return reconstruct_path(cameFrom, current)

        closedSet.add(current)
        for neighbour in grid.neighbours(current):
            if neighbour in closedSet:
                continue
            if neighbour not in [i[0] for i in openSet]:
                heappush(openSet, (neighbour, fScore[neighbour]))
            tentative_gScore = gScore[current] + heuristic(current, neighbour)
            if tentative_gScore >= gScore[neighbour]:
                continue

            cameFrom[neighbour] = current
            gScore[neighbour] = tentative_gScore
            fScore[neighbour] = gScore[neighbour] + heuristic(neighbour, end)

#the path of the said point
def reconstruct_path(cameFrom, current):

    total_path = [current]

    while current in cameFrom.keys():
        current = cameFrom[current]
        total_path.append(current)
    return total_path[::-1]
