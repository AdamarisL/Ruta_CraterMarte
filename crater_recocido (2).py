import random
import numpy as np
import math 
import time 
import plotly.graph_objects as px 

class Point(object):
    def __init__(self, point, mars, max_diff = 2.0):
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
        while True:
            dy, dx = random.choice(self.pos_direct)
            y, x = self.point[0] + dy, self.point[1] + dx
            if self.map[y][x] >= 0 and abs(self.map[y][x] - self.map[self.point[0]][self.point[1]]) < self.max_diff:
                return Point((y, x), self.map)
        
    def costo(self):
        return self.map[self.point[0]][self.point[1]]
    

mars_map = np.load("/Users/admon/crater_map.npy")
nr, nc = mars_map.shape

scale = 10.045
row_ini = nr-round(5456/scale) 
col_ini = round(2345/scale)


current_point = Point((row_ini, col_ini), mars_map)
  
costo_actu = current_point.costo() # Initial cost  
print("Costo inicial: ", costo_actu)  
step = 0                    # Step count

alpha = 0.999997              # Coefficient of the exponential temperature schedule        
t0 = 1                        # Initial temperature
t = t0    
moves = []
start_time = time.time()
while t > 0.0005 and costo_actu > 1: # 

    # Calculate temperature
    t = t0 * math.pow(alpha, step)
    step += 1
        
    # Get random neighbor
    neighbor_point = current_point.neighbor()
    costo_actu = current_point.costo()

    neighbor_cost = neighbor_point.costo()

    # Test neighbor
    
    if neighbor_cost < costo_actu:
        current_point = neighbor_point

    else:
        # Calculate probability of accepting the neighbor
        p = math.exp((costo_actu - neighbor_cost) / t)
        if p >= random.random():
            current_point = neighbor_point

    moves.append(list(current_point.point))
    print("Punto: ", current_point.point, "Iteration: ", step, "    Cost: ", costo_actu, "    Temperature: ", t)

end_time = time.time()
elapsed_time = end_time - start_time  

path_x = []
path_y = []
path_z = []
prev_state = []
distance = 0
for y,x in moves:    
        path_x.append( x * scale  )            
        path_y.append((nr - y)*scale  )
        path_z.append(mars_map[y][x]+1)
        
        if len(prev_state) > 0:
            distance +=  math.sqrt(
            scale*scale*(y - prev_state[0])**2 + scale*scale*(x - prev_state[1])**2 + (
                mars_map[y, x] - mars_map[prev_state[0], prev_state[1]])**2)

        prev_state = (y,x)

print("Total distance", distance)

x = scale*np.arange(mars_map.shape[1])
y = scale*np.arange(mars_map.shape[0])
X, Y = np.meshgrid(x, y)

fig = px.Figure(data = [px.Surface(x=X, y=Y, z=np.flipud(mars_map), colorscale='hot', cmin = 0, 
                                        lighting = dict(ambient = 0.0, diffuse = 0.8, fresnel = 0.02, roughness = 0.4, specular = 0.2),
                                        lightposition=dict(x=0, y=nr/2, z=2*mars_map.max())),
                        
                            px.Scatter3d(x = path_x, y = path_y, z = path_z, name='path', mode='markers',
                                            marker=dict(color=np.linspace(0, 1, len(path_x)), colorscale="Bluered", size=4))],
                
                    layout = px.Layout(scene_aspectmode='manual', 
                                        scene_aspectratio=dict(x=1, y=nr/nc, z=max(mars_map.max()/x.max(), 0.2)), 
                                        scene_zaxis_range = [0,mars_map.max()])
                    )
fig.show()


