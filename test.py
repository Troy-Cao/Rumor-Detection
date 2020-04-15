from mpi4py import MPI
import numpy as np


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    data = np.linspace(0, 10, 2)
else:
    data = None

rec_data = comm.bcast(data, root=0)

for i in range(size):
    if rank == i:
        print(rec_data)


