__author__ = 'ss4192'
"""
CSCI-630:Foundation of Intelligent System
Author:Suyash Sorte(ss4192@rit.edu)

Generating optimal paths for orienteering during different seasons.

"""
from PIL import Image
from queue import PriorityQueue
import collections
from math import sqrt


def main():
    speed = {(248, 148, 18, 255): 103,
             (255, 192, 0, 255): 18,
             (255, 255, 255, 255): 38,
             (2, 208, 60, 255): 14,
             (2, 136, 40, 255): 28,
             (5, 73, 24, 255): 0,
             (0, 0, 255, 255): 0,
             (71, 51, 3, 255): 198,
             (0, 0, 0, 255): 98,
             (205, 0, 101, 255): 0,
             (0, 255, 246, 255): 13,
             (143, 116, 63, 255): 15}
    # loading image
    image = Image.open("terrain.png")

    pixel = image.load()

    elevation_array = []
    counter = 0
    # reading elevation.txt file
    file = open("elevation.txt", "r+")
    for line in file.readlines():
        sp_line = line.strip().split("   ")
        elevation_array.append(sp_line)
        elevation_array[counter] = elevation_array[counter][:len(elevation_array[counter]) - 5]
        counter += 1
    # Converting elevation file into dictionary
    elevation_array_mod = {}
    for i in range(394):
        for j in range(500):
            elevation_array_mod[i, j] = float(elevation_array[j][i])
    # Finding neighbour
    dataset_of_neighbours = {}
    for i in range(395):
        for j in range(500):
            dataset_of_neighbours[i, j] = neighbour_choice((i, j), pixel)
    select_season = int(input("Select season - 1.Summer 2.Fall 3.Winter 4.Spring: "))
    # filename=input("Enter red filename")
    select_path = int(input("Choose path - 1.White Path 2.Brown Path 3.Red Path: "))
    # f =open(filename)
    if select_path == 1:
        path_chosen = [(230, 327), (241, 347), (269, 346), (270, 353), (275, 357), (295, 360), (317, 336), (269, 309),
                       (243, 327), (230, 327)]
    elif select_path == 2:
        path_chosen = [(230, 327), (276, 279), (303, 240), (306, 286), (290, 310), (304, 331), (306, 341), (253, 372),
                       (246, 355), (288, 338), (282, 321), (243, 327), (230, 327)]
    else:
        path_chosen = [(230, 327), (276, 279), (303, 240), (322, 242), (306, 286), (319, 320), (325, 339), (312, 366),
                       (275, 353), (253, 372), (246, 355), (259, 330), (288, 338), (304, 331), (290, 310), (269, 313),
                       (282, 321), (243, 327), (230, 327)]

    if select_season == 1:
        paths = summer(dataset_of_neighbours, path_chosen, speed, pixel, elevation_array_mod)
        path_cost = 0
        for i in (paths):
            pixel[i] = (160, 82, 45, 255)
        for j in range(len(paths)):
            if j + 1 != len(paths):
                path_cost = path_cost + manhattan_distance(paths[j], paths[j + 1])
        print("cost:", path_cost)
        image.show()

    if select_season == 2:
        paths = fall(dataset_of_neighbours, path_chosen, speed, pixel, elevation_array_mod)
        for i in (paths):
            pixel[i] = (127, 255, 212, 255)
        path_cost = 0
        for j in range(len(paths)):
            if j + 1 != len(paths):
                path_cost = path_cost + manhattan_distance(paths[j], paths[j + 1])
        print("cost:", path_cost)
        image.show()
    if select_season == 3:
        winter(pixel, image, speed, dataset_of_neighbours, path_chosen, elevation_array_mod)

    if select_season == 4:
        spring(pixel, image, speed, dataset_of_neighbours, path_chosen, elevation_array_mod)

# Implementing summer
def summer(dataset_of_neighbours, path_chosen, speed, pixel, elevation_array_mod):
    season = 1
    paths = []
    for point in range(len(path_chosen)):
        if point + 1 != len(path_chosen):
            paths.extend(A_star(dataset_of_neighbours, path_chosen[point], path_chosen[point + 1],
                                speed, pixel, elevation_array_mod, season))
    return paths

# Implementing fall
def fall(dataset_of_neighbours, path_chosen, speed, pixel, elevation_array_mod):
    season = 2
    paths = []
    for point in range(len(path_chosen)):
        if point + 1 != len(path_chosen):
            paths.extend(A_star(dataset_of_neighbours, path_chosen[point], path_chosen[point + 1],
                                speed, pixel, elevation_array_mod, season))
    return paths

# finding manhattan distance
def manhattan_distance(point1, point2):
    if point2 == point1:
        pass
    else:
        dist = (abs(point1[0] - point2[0]) * 10.29) + (abs(point1[1] - point2[1]) * 7.55)
        return dist

# backtracking the path list
def find_path(start, end, parent):
    current = end
    path = []
    while current != start:
        path.append(current)
        current = parent[current]
    path.append(start)
    return path


def terrain_dist(next, current):
    if abs(next[0] - current[0]) == 1:
        return 10.29
    if abs(next[1] - current[1]) == 1:
        return 7.55

#  Implementing A*
def A_star(dataset_of_neighbours, start, end, speed, pixel, elevation_array_mod, season):
    pq = PriorityQueue()
    pq.put(start, 0)
    parent = {}
    parent[start] = None
    total_cost = {}
    total_cost[start] = 0
    while not pq.empty():
        current = pq.get()
        if current == end:
            path = find_path(start, end, parent)
            return path
        for next in dataset_of_neighbours[current]:
            vel_next = speed[pixel[next]]
            #if next != None:
            new_cost = total_cost[current] + (terrain_dist(next, current))
            if next not in total_cost or new_cost < total_cost[next]:
                parent[next] = current
                total_cost[next] = new_cost
                # ele_cur = elevation_array_mod[current]
                # ele_next = elevation_array_mod[next]
                # if season == 2 and pixel[current] == (255, 255, 255, 255):
                #     vel_next = vel_next - 15
                # if ele_next > ele_cur:
                #     vel_next = vel_next - 10
                # else:
                #     vel_next = vel_next + 10
                vel_next = 0
                priority = new_cost + heuristic(next, end, elevation_array_mod, vel_next)

                pq.put(next, priority)


def heuristic(next, end, elevation_array_mod, vel_next):

    # distance = sqrt((next[0]-end[0])**2+(next[1]-end[1])**2)
    distance = manhattan_distance(next, end)
    # distance = sqrt(((end[0] - next[0]) * 10.29) ** 2 + ((end[1] - next[1]) * 7.5) ** 2)
    if distance == None:
        return 0
    else:
        h = distance
    return h

# Finding neighbour
def neighbour_choice(src, pixel):
    mod = []
    mod_src1 = src[0] + 1, src[1]
    mod_src2 = src[0], src[1] + 1
    mod_src3 = src[0] - 1, src[1]
    mod_src4 = src[0], src[1] - 1
    if mod_src1[0] < 395 and mod_src1[0] > 0:
        if (pixel[mod_src1] != (5, 73, 24, 255) and pixel[mod_src1] != (0, 0, 255, 255) and pixel[mod_src1] != (
                205, 0, 101, 255)):
            mod.append(mod_src1)
    if mod_src2[1] < 499 and mod_src1[1] > 0:
        if (pixel[mod_src2] != (5, 73, 24, 255) and pixel[mod_src2] != (0, 0, 255, 255) and pixel[mod_src2] != (
                205, 0, 101, 255)):
            mod.append(mod_src2)
    if mod_src3[0] < 395 and mod_src3[0] > 0:
        if (pixel[mod_src3] != (5, 73, 24, 255) and pixel[mod_src3] != (0, 0, 255, 255) and pixel[mod_src3] != (
                205, 0, 101, 255)):
            mod.append(mod_src3)
    if mod_src4[1] < 499 and mod_src4[1] > 0:
        if (pixel[mod_src4] != (5, 73, 24, 255) and pixel[mod_src4] != (0, 0, 255, 255) and pixel[mod_src4] != (
                205, 0, 101, 255)):
            mod.append(mod_src4)
    return mod

# Finding neighbour of water edges
def neighbour_choice_for_water(src, pixel):
    mod = []
    count = 0
    mod_src1 = src[0] + 1, src[1]
    mod_src2 = src[0], src[1] + 1
    mod_src3 = src[0] - 1, src[1]
    mod_src4 = src[0], src[1] - 1
    if mod_src1[0] < 395 and mod_src1[0] > 0:
        if pixel[mod_src1] == (0, 0, 255, 255):
            count += 1
    if mod_src2[1] < 499 and mod_src1[1] > 0:
        if pixel[mod_src2] == (0, 0, 255, 255):
            count += 1
    if mod_src3[0] < 395 and mod_src3[0] > 0:
        if pixel[mod_src3] == (0, 0, 255, 255):
            count += 1
    if mod_src4[1] < 499 and mod_src4[1] > 0:
        if pixel[mod_src4] == (0, 0, 255, 255):
            count += 1
    if count != 0 and count != 4:
        mod.append(src)
        return mod
    else:
        return

# Implementing winter
def winter(pixel, image, speed, dataset_of_neighbours, path, elevation_array_mod):
    dataset_of_water_border = []
    paths = []
    for i in range(0, 395):
        for j in range(0, 500):
            d = neighbour_choice_for_water((i, j), pixel)
            if d != None:
                dataset_of_water_border.extend(d)

    for i in dataset_of_water_border:
        breadth_first_search(i, pixel)

    for point in range(len(path)):
        if point + 1 != len(path):
            paths.extend(
                A_star(dataset_of_neighbours, path[point], path[point + 1],
                       speed, pixel, elevation_array_mod, 3))
    for i in paths:
        pixel[i] = (255, 0, 0, 255)

    path_cost = 0
    for j in range(len(paths)):
        if j + 1 != len(paths):
            path_cost = path_cost + manhattan_distance(paths[j], paths[j + 1])
    print("cost:", path_cost)

    image.show()


# Implementing bfs for winter
def breadth_first_search(root, pixel):
    visited, queue = set(), collections.deque([root])

    while queue:
        vertex = queue.popleft()
        if vertex[0] - 7 <= root[0] <= vertex[0] + 7 and vertex[1] - 7 <= root[1] <= vertex[1] + 7:
            if pixel[vertex[0], vertex[1]] == (0, 0, 255, 255):
                pixel[vertex[0], vertex[1]] = (0, 255, 246, 255)
            lists = []
            if vertex[0] < 395 and vertex[0] > 0:
                root1 = vertex[0] + 1, vertex[1]
                lists.append(root1)
            if vertex[1] < 499 and vertex[1] > 0:
                root2 = vertex[0], vertex[1] + 1
                lists.append(root2)
            if vertex[0] < 395 and vertex[0] > 0:
                root3 = vertex[0] - 1, vertex[1]
                lists.append(root3)
            if vertex[1] < 499 and vertex[1] > 0:
                root4 = vertex[0], vertex[1] - 1
                lists.append(root4)
            for neighbour in lists:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)
    return visited

# Implementing spring
def spring(pixel, image, speed, dataset_of_neighbours, path, elevation_array_mod):
    dataset_of_water_border = []
    paths = []
    for i in range(0, 395):
        for j in range(0, 500):
            d = neighbour_choice_for_water((i, j), pixel)
            if d != None:
                dataset_of_water_border.extend(d)

    for i in dataset_of_water_border:
        bfs_spring(i, pixel, elevation_array_mod)

    for point in range(len(path)):
        if point + 1 != len(path):
            paths.extend(
                A_star(dataset_of_neighbours, path[point], path[point + 1],
                       speed, pixel, elevation_array_mod, 3))

    for i in paths:
        pixel[i] = (0, 128, 128, 255)

    path_cost = 0
    for j in range(len(paths)):
        if j + 1 != len(paths):
            path_cost = path_cost + manhattan_distance(paths[j], paths[j + 1])
    print("cost:", path_cost)
    image.show()

# # Implementing bfs for spring
def bfs_spring(root, pixel, elevation_array_mod):
    visited, queue = set(), collections.deque([root])

    while queue:
        vertex = queue.popleft()
        if vertex[0] - 15 <= root[0] <= vertex[0] + 15 and vertex[1] - 15 <= root[1] <= vertex[1] + 15:
            difference_in_height = elevation_array_mod[root] - elevation_array_mod[vertex]
            if difference_in_height > -1 and pixel[vertex] != (205, 0, 101, 255):
                if pixel[vertex[0], vertex[1]] != (0, 0, 255, 255):
                    pixel[vertex[0], vertex[1]] = (143, 116, 63, 255)
                lists = []

                if vertex[0] < 395 and vertex[0] > 0:
                    root1 = vertex[0] + 1, vertex[1]
                    lists.append(root1)
                if vertex[1] < 499 and vertex[1] > 0:
                    root2 = vertex[0], vertex[1] + 1
                    lists.append(root2)
                if vertex[0] < 395 and vertex[0] > 0:
                    root3 = vertex[0] - 1, vertex[1]
                    lists.append(root3)
                if vertex[1] < 499 and vertex[1] > 0:
                    root4 = vertex[0], vertex[1] - 1
                    lists.append(root4)
                for neighbour in lists:
                    if neighbour not in visited:
                        visited.add(neighbour)
                        queue.append(neighbour)
    return visited


if __name__ == '__main__':
    main()
