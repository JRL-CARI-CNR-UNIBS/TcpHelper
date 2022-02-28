import struct
import time

a=[1.4,2,3,6,3.14]

#binary=pack(a)
print(f'{len(a)}f')
binary = struct.pack(f'{len(a)}f', *a)
print(binary)

print(list(struct.unpack(f'{len(a)}f',binary)))


import time
from ctypes import cdll

print('usleep')
for i in range(0,10000):
    glibc = cdll.LoadLibrary("libc.so.6")
    glibc.usleep(int(1000))

print('time.sleep')
for i in range(0,10000):
    glibc = cdll.LoadLibrary("libc.so.6")
    time.sleep(0.001)
