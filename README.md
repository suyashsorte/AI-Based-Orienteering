# AI-Based-Orienteering
The goal of the project is to find the best route between given set of paths consisting specific location in the park considering the height,terrain and seasons. 
The path to follow is mentioned in white.txt which contains the coordinates to follows in the map (terrain.png). The heuristic I used was Manhattan distance for 
the cost function to decide which location to move from the origin.The route to follow the paths were displayed on the map. The seasons had affects like the winter
would freeze the lake edges and spring would flood the coastal area with mud which was implemented on the map using BFS. During winter the path can be taken on the 
ice but during spring robot cannot travel on mud. 
