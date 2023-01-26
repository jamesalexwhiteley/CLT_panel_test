import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation

def get_coords(t, scale=False):
	dt = data[int(t),:]

	dtx = dt[::3]
	dty = np.roll(dt,-1)[::3]
	dtz = np.roll(dt,-2)[::3]

	if scale == True: 
		sfactor = 50

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

	dtx, dty, dtz = get_coords(t, scale)
	fig = plt.figure(figsize=(8, 8))
	ax = fig.add_subplot(projection='3d')
	label = np.linspace(0,len(dtx)-1,len(dtx))+1

	for i in range(len(dtx)):
		if abs(dtx[i]) < 20:
			ax.scatter(dtx[i], dty[i], dtz[i])
			label = ax.text(dtx[i], dty[i], dtz[i], '%s' % (i), size=8, zorder=1, color='k')
			label.set_alpha(.5)

		ax.set_xlabel('x')
		ax.set_ylabel('y')
		ax.set_zlabel('z')
		ax.set_xlim(-5e2,5e2)
		ax.set_zlim(-4e2,5e2)

	plt.show()

def init():
	return dta

def update(t):
	print(t*10)
	dtx, dty, dtz = get_coords(t*10, True)
	graph._offsets3d = (dtx, dty, dtz)

#====================================#
# extract data
#====================================#

led = open("led.txt", "r")
led = led.read()
led = led.split()

start = 437
nmarker = 48
led = np.array(led[start:],dtype=float)
numcol = 146
numrow = 5439

led = led.reshape((numrow, numcol))
time = led[:,0]
totload = led[:,-1]
data = led[:,1:numcol-1]

#====================================#
# plot data 
#====================================#

# plot_data(0)
# plot_data(5000, True)

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
# ax.set_xlim(-5e2,5e2)
# ax.set_zlim(-4e2,5e2)

dtx, dty, dtz = get_coords(0)
graph = ax.scatter(dtx, dty, dtz)

ani = matplotlib.animation.FuncAnimation(fig, update, 5000, 
                               interval=100, blit=False)
plt.show()






