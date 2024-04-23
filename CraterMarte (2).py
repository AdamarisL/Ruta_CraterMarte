import numpy as np
import time 
import plotly.graph_objects as px 

class Point(object):
    def __init__(self, point, mars, max_diff=2.0):
        self.max_diff = max_diff
        self.point = point 
        self.map = mars
        self.pos_direct = [
            (0, 1),   # Derecha
            (0, -1),  # Izquierda
            (1, 0),   # Abajo
            (-1, 0),  # Arriba
            (1, 1),   # Abajo-Derecha
            (-1, 1),  # Arriba-Derecha
            (1, -1),  # Abajo-Izquierda
            (-1, -1)  # Arriba-Izquierda
        ]

    def neighbor(self):
        neighbors = []
        for dy, dx in self.pos_direct:
            y, x = self.point[0] + dy, self.point[1] + dx
            if 0 <= y < len(self.map) and 0 <= x < len(self.map[0]):
                if self.map[y][x] >= 0 and abs(self.map[y][x] - self.map[self.point[0]][self.point[1]]) <= self.max_diff:
                    neighbors.append(Point((y, x), self.map))
        return neighbors
        
    def cost(self):
        return self.map[self.point[0]][self.point[1]]
    

mars_map = np.load("/Users/admon/crater_map.npy")
nr, nc = mars_map.shape

scale = 10.045
row_ini = nr - round(5456 / scale)
col_ini = round(2345 / scale)

current_point = Point((row_ini, col_ini), mars_map)

costo_actu = current_point.cost()   
print("Costo inicial: ", costo_actu)  
step = 0                    
start_time = time.time()

moves = []
while costo_actu > 1: 
    step += 1
    print("Iteración:", step)
    print("Punto:", current_point.point)
    print("Costo:", costo_actu)

    neighbors = current_point.neighbor()
    min_cost_neighbor = min(neighbors, key=lambda x: x.cost())

    neighbor_cost = min_cost_neighbor.cost()
    if neighbor_cost >= costo_actu:
        break
    
    current_point = min_cost_neighbor
    costo_actu = neighbor_cost
    
    moves.append(list(current_point.point))
    

end_time = time.time()
elapsed_time = end_time - start_time

print("Total distance:", len(moves) * scale)

path_x = []
path_y = []
path_z = []
for y, x in moves:
    path_x.append(x * scale)
    path_y.append((nr - y) * scale)
    path_z.append(mars_map[y][x] + 1)

x = scale * np.arange(mars_map.shape[1])
y = scale * np.arange(mars_map.shape[0])
X, Y = np.meshgrid(x, y)

fig = px.Figure(data=[
    px.Surface(x=X, y=Y, z=np.flipud(mars_map), colorscale='hot', cmin=0,
               lighting=dict(ambient=0.0, diffuse=0.8, fresnel=0.02, roughness=0.4, specular=0.2),
               lightposition=dict(x=0, y=nr / 2, z=2 * mars_map.max())),
    px.Scatter3d(x=path_x, y=path_y, z=path_z, name='path', mode='markers',
                 marker=dict(color=np.linspace(0, 1, len(path_x)), colorscale="Bluered", size=4))
],
    layout=px.Layout(scene_aspectmode='manual',
                     scene_aspectratio=dict(x=1, y=nr / nc, z=max(mars_map.max() / x.max(), 0.2)),
                     scene_zaxis_range=[0, mars_map.max()])
)
fig.show()