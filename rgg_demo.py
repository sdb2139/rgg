"""
rgg_demo.py
sean bergen

this file is a quick mockup/demo to do the following:
    - generate a random graph of some number of points within some bound
    - output the adjacency list using networkx and print the graph using 
    matplotlib
"""

"""
networkx is a library for network/graph computations
matplot is for outputing the graph
random is used for prng generation of points (nodes)
"""
import networkx as nx
import matplotlib as mp
import random as rd
import sys

# arbitrary number used as seed unless one is specified
seed = 2750

"""
gen_pts(bound, dim)
    bounds -> maximum integer that can be generated (def is 256 [-128,127])
    dim    -> number of dimensions of the point (def is 2)

function generates random coordinate point and returns it
"""
def gen_pts(bounds=256,dim=2):
    # create empty list of dimension dim
    pts = [None]*dim
    for i in range(0,dim):
        pts[i] = rd.randint(-bounds/2,bounds/2)
    return tuple(pts)

"""
pt_check(pt, mode, arg)
    pt     -> point to be checked
    mode   -> determines the form of "arg"
        circle -> arg is radius of the circle points should be in, r
        rect   -> arg is list of length and width of rectangle, [l,w]
        disk   -> arg is list of inner and outer radius of disk, [r,R]
        nbox   -> arg is list of dims for some 3+ dimension box, [l,w,h,...]
        custom -> used for defining custom boundaries, not implemented yet

RETURNS:
    1 -> POINT IN BOUND
    0 -> POINT NOT IN BOUND
   -1 -> ERROR WHEN CHECKING POINT
"""
def pt_check(pt, mode, arg):
    if mode == "circle":
        # check if points fall within radius of origin
        # arg is of format r, where r is a radius
        s = 0
        # use generalized pythagorean formula for distance from center
        for i in pt:
            s = s + i**2
        s = s**(0.5)
        if s > arg:
            # reject point
            return 0
        return 1
    if mode == "rect":
        # check if points are within rectangle
        # arg is of form [l, w]
        # rectange is centered at (0,0)
        if pt[0] <= arg[0]/2 and pt[0] >= -arg[0]/2:
            if pt[1] <= arg[1]/2 and pt[1] >= -arg[1]/2:
                return 1
        return 0
    if mode == "nbox":
        # check if points are within 3+ dimension box
        # TODO: IMPLEMENT THIS
        return -1
    if mode == "disk":
        if arg[0] > arg[1]:
            print("Error: inner radius bigger than outer radius")
            return -1
        # check if points are in outer part of a disk
        s = 0
        # use generalized pythagorean formula for distance from center
        for i in pt:
            s = s + i**2
        s = s**(0.5)
        if s > arg[1] or s < arg[0]:
            # reject point
            return 0
        return 1
    if mode == "custom":
        # check if points are within some custom defined bounds
        # TODO: IMPLEMENT THIS
        return -1
    else:
        print("Error, incorrect mode specified")
        print("Please use one of the following modes:")
        print("circle, rect, nbox, disk, custom")
        return -1

"""
gen_vert(n, range, dim, mode, arg)
    n     -> number of vertices for the graph
    bound -> range of values the vertices can have for coordinates
    dim   -> number of dimensions for the points
    mode  -> mode of the boundaries, see above function
    arg   -> changes depending on mode, see above function

function for generating a set of n vertices for a graph
returns a list of points
"""
def gen_vert(n, bound, dim, mode, arg):
    pts = []
    while(len(pts) < n):
        # generate a random point
        pt = gen_pts(bound, dim)
        # if the point is in the specified bounds
        valid = pt_check(pt, mode, arg)
        if valid == -1:
            sys.exit("Error in point generation or mode not implemented yet")
        if(valid > 0):
            # we append it to the list and give it a number to identify it
            pts.append([len(pts),pt])
    # we finish by returning the list of all points and their coordinates
    return pts

"""
function that creates and returns a dictionary of points used for drawing
vertices at the correct position in the xy plane
"""
def create_dict(pts):
    pos = {}
    for pt in pts:
        pos[pt[0]] = pt[1]
    return pos


"""
calc_edges(pts, dist)
    pts  -> list that contains a vertex name and its position
            ex:  [0, [2,-5]]
    dist -> max distance between two nodes for them to have an edge

function that calculates if there should be an edge between two vertices
given their coordinates and some distance

returns list of edges, where each edge is a 2 tuple

TODO: UPDATE THIS TO WORK BEYOND 2D POINTS
"""
def calc_edges(pts, dist):
    edges = []
    for i in range(len(pts)):
        # checking if point[i] has an edge to any other
        # we do this to avoid double adding edges
        for j in range(i+1,len(pts)):
            x = abs(pts[i][1][0] - pts[j][1][0])
            y = abs(pts[i][1][1] - pts[j][1][1])
            # we do pythagorean formula again
            if (x**2 + y**2)**(0.5) <= dist:
                edges.append((pts[i][0],pts[j][0]))
    return edges

"""
const_graph(n, bound, dim, mode, arg, dist)


function that uses most/all functions above to construct the final graph
"""
def const_graph(n, bound, dim, mode, arg, dist):
    # first, we generate n points that are within our bounds
    points = gen_vert(n, bound, dim, mode, arg)
    # then, we turn those nodes into a dictionary set for later
    pos = create_dict(points)
    # now, we calculate the edges that exist between nodes
    edges = calc_edges(points, dist)

    # now we have everything we need to build our initial graph
    G = nx.Graph()
    G.add_edges_from(edges)

    # now we return G and position data for G
    return G, pos

"""
function that does basic stuff for plotting a graph

this is mostly so i don't need to mess around with matplotlib too much
"""
def plot_graph(graph, pos):
    nx.draw_networkx(graph, pos)

    # Set margins for the axes so that nodes aren't clipped
    ax = mp.pyplot.gca()
    ax.margins(0.20)
    mp.pyplot.axis("off")
    mp.pyplot.show()


if __name__ == "__main__":
    rd.seed(seed)
    if len(sys.argv) == 1:
        # test out generating a graph
        G = const_graph(75, 128, 2, "disk", [20,40], 10)
        plot_graph(G[0], G[1])
    else:
        # number of nodes to graph
        n =  int(sys.argv[1])
        # integer bounds on the coordinates generated
        bounds =  int(sys.argv[2])
        # dimension of points
        dim =  int(sys.argv[3])
        # max distance for points to have an edge
        dist = int(sys.argv[4])
        # mode of bounds
        mode = sys.argv[5]
        # args for the mode
        if mode == "circle":
            args =  int(sys.argv[6])
        else:
            # if i implement nbox or custom ill have to change this
            # slightly
            args = [None]*2
            args[0] =  int(sys.argv[6])
            args[1] =  int(sys.argv[7])
        G = const_graph(n,bounds,dim,mode,args,dist)
        plot_graph(G[0],G[1])


