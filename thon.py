# coding: utf-8
import serial
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np

# Constantes
PORTA 	= "COM6"
BAUD 	= 9600
DT 		= 1./10
MARGIN 	= 8

# Variáveis
t 	 = 0
teto1 = -9999
teto2 = -9999
piso1 = 9999
piso2 = 9999

# Configuração da Serial
arduino = serial.Serial(PORTA, BAUD)

# Configuração da Janela
fig = plt.figure()
fig.canvas.set_window_title('Osciloscópio')

# Configuração da Plotagem
ax1 = plt.subplot(2, 1, 1)
#ax = plt.axes(xlim=(0, 10), ylim=(-1000, 1000))
ax2 = plt.subplot(2, 1, 2)

# Canais
canal0, = ax1.plot([], [], color='#FFF700', lw=2, label='Canal 0')
canal1, = ax2.plot([], [], color='#00E5FF', lw=2, label='Canal 1')

def init():
	canal0.set_data([], [])
	canal1.set_data([], [])

	return canal0, canal1

def animate(i):
	global t, teto1, piso1, teto2, piso2

	x0 = canal0.get_xdata()
	x1 = canal1.get_xdata()

	y0 = canal0.get_ydata()
	y1 = canal1.get_ydata()

	x0.append(t)
	x1.append(t)

	arduino.flush()
	data = arduino.readline()
	if "ArduinoScopio:" in data:
		data = data.replace("ArduinoScopio:", "")
		data = data.split()

	data0 = float(data[0])
	data1 = float(data[1])

	y0.append(data0)
	y1.append(data1)

	canal0.set_data(x0, y0)
	canal1.set_data(x1, y1)

	teto1 = max(teto1, data0)
	piso1 = min(piso1, data0)

	teto2 = max(teto2, data1)
	piso2 = min(piso2, data1)
	
	ax1.set_xlim( [t - MARGIN, t] )
	ax1.set_ylim( [piso1 - MARGIN, teto1 + MARGIN] )

	ax2.set_xlim( [t - MARGIN, t] )
	ax2.set_ylim( [piso2 - MARGIN, teto2 + MARGIN] )

	t += DT

	return canal0, canal1

anim = animation.FuncAnimation(
	fig, 
	animate, 
	init_func=init, 
	frames=200, 
	interval=5, 
	blit=False
)


# Customização do Gráfico
plt.grid()

rect = fig.patch
rect.set_facecolor('#232626')
rect = ax1.patch
rect.set_facecolor('#232626')
ax1.spines['bottom'].set_color('#ffffff')
ax1.spines['top'].set_color('#ffffff')
ax1.spines['left'].set_color('#ffffff')
ax1.spines['right'].set_color('#ffffff')
ax1.xaxis.label.set_color('#ffffff')
ax1.tick_params(axis='x', colors='#ffffff')
ax1.tick_params(axis='y', colors='#ffffff')
ax1.xaxis.grid(color='#ffffff')
ax1.yaxis.grid(color='#ffffff')

rect = fig.patch
rect.set_facecolor('#232626')
rect = ax2.patch
rect.set_facecolor('#232626')
ax2.spines['bottom'].set_color('#ffffff')
ax2.spines['top'].set_color('#ffffff')
ax2.spines['left'].set_color('#ffffff')
ax2.spines['right'].set_color('#ffffff')
ax2.xaxis.label.set_color('#ffffff')
ax2.tick_params(axis='x', colors='#ffffff')
ax2.tick_params(axis='y', colors='#ffffff')
ax2.xaxis.grid(color='#ffffff')
ax2.yaxis.grid(color='#ffffff')

plt.show()