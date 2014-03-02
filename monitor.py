#coding: utf-8
import serial
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import math

arduino = serial.Serial('COM6', 9600)

fig = plt.figure()
fig.canvas.set_window_title('Osciloscópio')
rect = fig.patch
rect.set_facecolor('darkgray')
ax = plt.axes(xlim=(0, 10), ylim=(0, 1000))

rect = ax.patch
rect.set_facecolor('gray')
line, = ax.plot([], [], 'Yellow')

lastx = 0

def init():
    line.set_data([], [])
    return line,

def animate(i):
	global lastx
	x = line.get_xdata()
	x.append(lastx)
	lastx += 0.1
	data = float(arduino.readline())
	y = line.get_ydata()
	y.append(data)
	line.set_data(x, y)
	ax.set_xlim([lastx-20, lastx])
	#ax.set_ylim([np.min(y)-20, np.amax(y)+20])
	return line,

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=200, 
	interval=5, blit=True)

plt.grid()
plt.show()