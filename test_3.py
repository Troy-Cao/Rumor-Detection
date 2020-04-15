# from mpi4py import MPI
#
# comm = MPI.COMM_WORLD
# size = comm.Get_size()
# rank = comm.Get_rank()
#
# file_name = "/Users/troycao/Documents/GitHub/COMP90024_assignment1/test.txt"
# text_row = 10
# count = 0
# list = []
# with open(file_name, "r") as file:
#     while count <= text_row:
#         rep = []
#         while len(rep) < size:
#             line = file.readline()
#             rep.append(line)
#         for id in range(len(rep)):
#             if rank == id:
#                 rank_list = []
#                 rank_list.append(rep[id])
#         data = comm.scatter(rank_list)
#         for item in data:
#             list.append(item)
#         count += 3
# print(list)



# num = 0
# start_point = end_point[2]
# count = start_point
# print(int(end_point[3]))
# while start_point <= count < int(end_point[3]):
#       num += 1
#       count += 1
# print(num)
from collections import Counter

import numpy as np
import matplotlib.pyplot as plt



# 生成测试数据
x = np.linspace(0, 10, 10)
y = 11-x



# 绘制柱状图
plt.bar(x, y)
# 循环，为每个柱形添加文本标注

# 居中对齐
for xx, yy in zip(x,y):
  plt.text(xx, yy+0.1, str(yy), ha='center')



# 显示图形
plt.show()

plt.show()

