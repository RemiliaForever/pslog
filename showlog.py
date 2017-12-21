#!/bin/env python3
import sys
import matplotlib.pyplot as plt
from numpy import genfromtxt


fig, ax_list = plt.subplots(4, 1)

cpu_ax = ax_list[0]
cpu_ax.set_title('cpu')
mem_ax = ax_list[1]
mem_ax.set_title('mem')
net_ax = ax_list[2]
net_ax.set_title('net')
disk_ax = ax_list[3]
disk_ax.set_title('disk')

data = genfromtxt(sys.argv[1], delimiter=',', dtype='float64').transpose()
if len(sys.argv) >= 3:
    time = genfromtxt(sys.argv[2], delimiter=',', dtype='float64').transpose()
    time += 5
data[0] -= data[0][0]

# draw time marker
if len(sys.argv) >= 3:
    for i, t in enumerate(time):
        for a in ax_list:
            a.axvline(t, lw=1, color='purple')
            a.set_xlabel('unit: s')
# cpu
cpu_ax.axhline(100, lw=1, color='gray')
cpu_ax.plot(data[0], data[1], label='user')
cpu_ax.plot(data[0], data[2], label='system')
cpu_ax.plot(data[0], data[3], label='iowait')
cpu_ax.plot(data[0], 100 - data[4], label='use')
cpu_ax.set_ylabel('unit: %')
cpu_ax.legend(loc='upper left')
# mem
mem_ax2 = mem_ax.twinx()
mem_ax2.axhline(100, lw=1, color='gray')
mem_ax.plot(data[0], data[5], label='use')
mem_ax2.plot(data[0], data[6], label='percent', color='orange')
mem_ax.set_ylabel('unit: MB')
mem_ax2.set_ylabel('unit: %')
mem_ax.legend(loc='upper left')
mem_ax2.legend(loc='upper right')
# net
net_ax.axhline(5 * 1024, lw=1, color='gray')
net_ax.plot(data[0], data[7], label='upload')
net_ax.plot(data[0], data[8], label='download')
net_ax.set_ylabel('unit: KB/s')
net_ax.legend(loc='upper left')
# disk
disk_ax.plot(data[0], data[9], label='read')
disk_ax.plot(data[0], data[10], label='write')
disk_ax.set_ylabel('unit: KB/s')
disk_ax.legend(loc='upper left')


plt.tight_layout(h_pad=0.1)
plt.show()
