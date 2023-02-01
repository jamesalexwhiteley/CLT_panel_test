import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation

def open_led():
	''' open led text file and extract relevant part ''' 
	led = open("led.txt", "r")
	led = led.read()
	led = led.split()

	start = 437
	led = np.array(led[start:],dtype=float)
	numcol = 146
	numrow = 5439

	led = led.reshape((numrow, numcol))
	time = led[:,0]
	load = led[:,-1]
	data = led[:,1:numcol-1]
	return data, time, load 

def open_tr():
	''' open transducer text file and extract relevant part '''
	tr = open("transducer.txt", "r")
	tr = tr.read()
	tr = tr.split()

	start = 29
	tr = np.array(tr[start:],dtype=float)
	numcol = 5
	numrow = 1351

	tr = tr.reshape((numrow, numcol))
	time = tr[:,0]
	load = tr[:,-1]
	data = tr[:,1:numcol-1]

	print(tr)

def get_coords(t, scale=False):
	''' extract xyz coordinate data '''
	dt = data[int(t),:]

	dtx = dt[::3]
	dty = np.roll(dt,-1)[::3]
	dtz = np.roll(dt,-2)[::3]

	if scale == True: 
		sfactor = 10

		d0 = data[0,:]
		d0x = d0[::3]
		d0y = np.roll(d0,-1)[::3]
		d0z = np.roll(d0,-2)[::3]

		diffx = dtx - d0x
		diffy = dty - d0y
		diffz = dtz - d0z

		dtx = d0x + sfactor * diffx
		dty = d0y + sfactor * diffy
		dtz = d0z + sfactor * diffz

	return dtx, dty, dtz

def plot_data(t, scale=False):
	''' plot xyz data in space for some t ''' 
	dtx, dty, dtz = get_coords(t, scale)
	fig = plt.figure(figsize=(8, 8))
	ax = fig.add_subplot(projection='3d')
	label = np.linspace(0,len(dtx)-1,len(dtx))+1

	for i in range(len(dtx)):
		if abs(dtx[i]) < 20:
			ax.scatter(dtx[i], dty[i], dtz[i], s=20)
			label = ax.text(dtx[i], dty[i], dtz[i], '%s' % (i), size=9, zorder=1, color='k')
			label.set_alpha(.7)

		ax.set_xlabel('x')
		ax.set_ylabel('y')
		ax.set_zlabel('z')
		ax.set_xlim(-5e2,5e2)
		ax.set_zlim(-4e2,5e2)

	ax.view_init(30, -30)
	ax.set_facecolor("white")
	plt.savefig('3D_plot.png', format='png', dpi=1000, bbox_inches='tight', pad_inches = 0)
	plt.show()

def get_load_disp(i, data, load):
	''' get load-disp data for one led (the led with index i+1) '''
	xpts = []
	dtx, dty, dtz = get_coords(0)
	int_z = dtz[i]

	for t in range(len(data)):
		dtx, dty, dtz = get_coords(t)
		xpts.append(abs(dtz[i]-int_z))

	xpts = np.array(xpts)
	ypts = load
	return xpts, ypts 

def plot_load_disp(xpts, ypts):
	''' plot 2D graph ''' 
	step = 50
	plt.plot(xpts[1::step], ypts[1::step])
	plt.xlabel('Displacement (mm)')
	plt.ylabel('Load (kN)')
	plt.savefig('2D_plot.png', format='png', dpi=1000, bbox_inches='tight', pad_inches = 0)
	plt.show()

def animate():
	''' animate the displacement in time '''

	ani = matplotlib.animation.FuncAnimation(fig, update, 5000, 
	                               interval=100, blit=False)
	plt.show()

def init():
	return dta

def update(t):
	print(t*10)
	dtx, dty, dtz = get_coords(t*10, True)
	graph._offsets3d = (dtx, dty, dtz)

#====================================#
# MAIN 
#====================================#

#==== LED DATA ====#
data, time, load  = open_led()

#==== plot 3D data ====#
# plot_data(0)
# plot_data(len(data)-1, True)

#==== animate 3D data ====#
# fig = plt.figure(figsize=(8, 8))
# ax = fig.add_subplot(111, projection='3d')
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_zlabel('z')
# dtx, dty, dtz = get_coords(0)
# graph = ax.scatter(dtx, dty, dtz)
# animate()

#==== plot 2D data ====#
# xpts, ypts = get_load_disp(15, data, load) #index 16 (L/2)
# plot_load_disp(xpts, ypts)

# xpts1, ypts = get_load_disp(2, data, load) #index 3  (L/4)
# xpts2, ypts = get_load_disp(10, data, load) #index 11 (L/4)
# xpts = (xpts1+xpts2)/2
# plot_load_disp(xpts, ypts)

# xpts1, ypts = get_load_disp(28, data, load) #index 29  (L/4)
# xpts2, ypts = get_load_disp(32, data, load) #index 33 (L/4)
# xpts = (xpts1+xpts2)/2
# plot_load_disp(xpts, ypts)


#==== TRANSDUCER DATA ====#
open_tr()


