
import sys
import numpy as np
import trimesh
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
# Build the graph
def build_vertex_graph(mesh):
    G = nx.Graph() #nx.Graph subject
    verts = mesh.vertices
    for tri in mesh.faces:
        for u, v in ((tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])):
            if not G.has_edge(u, v):
                dist = np.linalg.norm(verts[u] - verts[v])
                G.add_edge(u, v, weight=dist)
    return G

def nearest_vertex(mesh, point):
    return int(mesh.kdtree.query(point.reshape(1, 3))[1][0]) #pick out the nearest point to calculate Euclidian distance

if __name__ == "__main__":
   
    # 1) Load mesh
    mesh = trimesh.load(sys.argv[1], force='mesh')
   

    # 2) Build graph and choose A/B
    G = build_vertex_graph(mesh)
    A = np.array([0.0, 0.0, 0.0])    # edit as needed
    B = np.array([1.0, 1.0, 0.0])    # edit as needed
    idx_A = nearest_vertex(mesh, A)
    idx_B = nearest_vertex(mesh, B)

    # 3) Generate the two best paths using shortest_simple_paths
    paths_gen = nx.shortest_simple_paths(G, source=idx_A, target=idx_B, weight='weight')
    try:
        path1_inds = next(paths_gen)  # shortest
        path2_inds = next(paths_gen)
        path3_inds = next(paths_gen)# second‐shortest
    except StopIteration:
        raise RuntimeError("Could not find two distinct paths between A and B.")

    path1_pts = mesh.vertices[path1_inds]
    path2_pts = mesh.vertices[path2_inds]
    path3_pts = mesh.vertices[path3_inds]
    
    # 4) Plot setup
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 4.A) Mesh surface in light gray
    tri_verts = [mesh.vertices[f] for f in mesh.faces]
    mesh_col = Poly3DCollection(tri_verts,
                                facecolors='lightgray',
                                edgecolors='gray',
                                alpha=0.5)
    ax.add_collection3d(mesh_col)

    # 4.B) Plot second‐best path in red
    ax.plot(path2_pts[:, 0],
            path2_pts[:, 1],
            path2_pts[:, 2],
            '-o', c='red', markersize=4, label='Second‐Best Path')

    # 4.C) Plot shortest path in green
    ax.plot(path1_pts[:, 0],
            path1_pts[:, 1],
            path1_pts[:, 2],
            '-o', c='green', markersize=4, label='Shortest Path')
    
     # 4.C) Plot shortest path in blue
    ax.plot(path3_pts[:, 0],
            path3_pts[:, 1],
            path3_pts[:, 2],
            '-o', c='blue', markersize=4, label='Third-Best Path')
    
    # 4.D) Start marker (blue) and end marker (black)
    ax.scatter(*mesh.vertices[idx_A], c='blue', s=50, marker='o', label='Start')
    ax.scatter(*mesh.vertices[idx_B], c='black', s=50, marker='o', label='End')


    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Path Visualization on Triangular_Mesh')
    ax.legend()

    plt.show()
