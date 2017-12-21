#!/bin/python3
import psutil
import time

# 配置外网网卡接口
eth_name = 'eth0'
# 配置工作盘设备路径
sd_name = 'sda2'
# 轮寻间隔
tick = 1


# 记录上一次数据，用以计算速率
last = time.time()
net = psutil.net_io_counters(pernic=True)[eth_name]
net_sent = net.bytes_sent
net_recv = net.bytes_recv
disk = psutil.disk_io_counters(perdisk=True)[sd_name]
disk_read = disk.read_bytes
disk_write = disk.write_bytes

'''
输出格式

time
cpu.user, cpu.system, cpu.iowait, cpu.idle,
vm.used, vm.used_percent,
net.upload, net.download,
disk.read, disk.write

'''

# 开始循环
while True:
    current = time.time()
    diff = (current - last)
    last = current

    # CPU
    cpu = psutil.cpu_times_percent()
    print('{},{},{},{},{}'.format(
        current,
        cpu.user,
        cpu.system,
        cpu.iowait,
        cpu.idle
    ), end=',')

    # 内存
    vm = psutil.virtual_memory()
    print('{},{}'.format(
        int(vm.used / 1024 / 1024),
        vm.percent
    ), end=',')

    # 网络IO
    net = psutil.net_io_counters(pernic=True)[eth_name]
    net_s = net.bytes_sent
    net_r = net.bytes_recv
    print('{},{}'.format(
        (net_s - net_sent) / diff / 1024,
        (net_r - net_recv) / diff / 1024
    ), end=',')
    net_sent = net_s
    net_recv = net_r

    # 硬盘IO
    disk = psutil.disk_io_counters(perdisk=True)[sd_name]
    disk_r = disk.read_bytes
    disk_w = disk.write_bytes
    print('{},{}'.format(
        (disk_r - disk_read) / diff / 1024,
        (disk_w - disk_write) / diff / 1024
    ))
    disk_read = disk_r
    disk_write = disk_w

    time.sleep(tick)
