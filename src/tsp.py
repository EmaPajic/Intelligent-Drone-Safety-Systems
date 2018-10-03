import random
import numpy as np
from point import Point

probability_mat = [[0.12,  0.0835, 0.1275, 0.157,  0.2115, 0.2355, 0.2215, 0.28,   0.2895],
 [0.1685, 0.1225, 0.147,  0.1765, 0.231,  0.1,    0.241,  0.174,  0.29  ],
 [0.1445, 0.084,  0.123,  0.1575, 0.212,  0.226,  0.202,  0.3,    0.285 ],
 [0.091,  0.07,   0.0265, 0.0225, 0.106,  0.1005, 0.12,   0.164,  0.1355],
 [0.1935, 0.118,  0.225,  0.3175, 0.174,  0.1395, 0.1885, 0.15,   0.329 ],
 [0.2275, 0.186,  0.245,  0.284,  0.3235, 0.2745, 0.295,  0.271,  0.2365],
 [0.305,  0.2885, 0.3225, 0.231,  0.3,    0.246,  0.2225, 0.2085, 0.189 ],
 [0.2795, 0.284,  0.1285, 0.24,   0.2365, 0.323,  0.3085, 0.309,  0.275 ]]

def choose_points():
	point_list = []
	for row in range(0,8):
		for column in range(0,9):
			if(probability_mat[row][column] > 0.25):
				point_list.append(Point(row, column, 0))
	return point_list

def euclid(point_a,point_b):
    return np.sqrt((point_a.get_x() - point_b.get_x())**2 + (point_a.get_y() - point_b.get_y())**2)

def TSP(point_list):
    N = len(point_list)
    for it in range(0, 100):
        i = random.randint(0, N - 1)
        j = random.randint(0, N - 1)
        if abs(i - j) <= 2:
            continue
        if(euclid(point_list[i],point_list[(j + 1) % N]) + euclid(point_list[j],point_list[(i + 1) % N])  < euclid(point_list[i],point_list[(i + 1) % N]) + euclid(point_list[j],point_list[(j + 1) % N])):
            point_list[(i + 1) % N], point_list[(j + 1) % N] = point_list[(j + 1) % N], point_list[(i + 1) % N]
        if(euclid(point_list[i],point_list[j]) + euclid(point_list[(j + 1) % N],point_list[(i + 1) % N])  < euclid(point_list[i],point_list[(i + 1) % N]) + euclid(point_list[j],point_list[(j + 1) % N])):
            point_list[j], point_list[(i + 1) % N] = point_list[(i + 1) % N], point_list[j]
    return point_list

print(TSP(choose_points()))
