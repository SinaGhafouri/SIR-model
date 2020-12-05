"""Edit: removed is a better description that recovered, so change it!"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anime
from matplotlib.widgets import Slider
import time

n = 500 #population.
w = 5 #width of area.
x, y = np.random.rand(n)*w, np.random.rand(n)*w
v0 = 5 #velocity coeficient.
vx, vy = (np.random.rand(n)-.5)*v0, (np.random.rand(n)-.5)*v0 #velocities.

infected = {np.random.randint(n)} #first item is the index of the patient-zero.
total_inf = [len(infected)] #number of infected people.

inf_day = np.zeros(n) #number of days passed after infection.
recovered = set() #once upon a time were infected but now they're good.
total_rec = [len(recovered)] #number of recovered people.

dead = set() #they didn't make it.
total_dead = [len(dead)]

dt = .01 #time steps.

"""Animation"""
fig = plt.figure(figsize=(12,6)) #facecolor='black', 

ax1 = fig.add_subplot(121, frameon=True, xlim=(0,w), ylim=(0,w))
ax2 = fig.add_subplot(122, frameon=True, xlim=(0,n), ylim=(0,n))

################## This part is just for the guidance.
lll= []
lll.append(ax1.plot([], [], 'ro',label='Infectious'))
lll.append(ax1.plot([], [], 'go',label='Susceptible'))
lll.append(ax1.plot([], [], 'ko',label='Dead'))
lll.append(ax1.plot([], [], 'bo',label='Recovered'))
ax1.legend(loc='upper left',bbox_to_anchor=(-.38, 1))
##################
lines = []
for i in range(n):
    if i in infected:
        lines.append(ax1.plot([], [], 'ro',label='Infectiuos')[0])
    else:
        lines.append(ax1.plot([], [], 'go',label='Susceptible')[0])

line1, = ax2.plot([],[],'r-',label='Infectious') #for the infected people
line2, = ax2.plot([],[],'b-',label='Removed = \nRecovered + Dead') #for the recovered people
line3, = ax2.plot([],[],'k-',label='Dead') #for the dead people
ax2.legend(loc='upper right',bbox_to_anchor=(1.3,1))
    
days = []
this_inf = []
def animate(i):
    global x,y,j,cx,cy,vx,vy,con,dr
    v = 5 #velocity coefficient.
    dr = .25 #infection radius.
    ic = .5 #infection chance min = 0, max = 1.
    dc = .05 #death chance.
    rc = 1-dc #recover chance.
    tresh_day = 14 #number of days the people are infected.
    
    if i%(int(np.random.random()*50)+1)==0:
        ri = np.random.randint(n,size=np.random.randint(n+1)) #random index
        for i in ri:
            vx[i]=(np.random.rand()-.5)*v
            vy[i]=(np.random.rand()-.5)*v

    '''outbreak of the disease'''
    infcopy = infected.copy() #temporary variable.
    '''infectiong near people'''
    for i in infcopy: 
        con = ((x<x[i]+dr) & (x>x[i]-dr) & (y<y[i]+dr) & (y>y[i]-dr))#it indicates if there is someone near or not

        for j in np.where(con==True)[0]:
            if np.random.random() < ic and j not in recovered and j not in dead: infected.add(j)

    '''to see the destiny of the infected people'''
    infcopy = infected.copy() #temporary variable.
    for i in infcopy:
        inf_day[i] += 1
        if inf_day[i]>=tresh_day:
            if np.random.random()>dc:
                recovered.add(i)
                infected.remove(i)
            else: 
                dead.add(i)
                infected.remove(i)
    x = (x+vx*dt)%w
    y = (y+vy*dt)%w

    for lnum,line in enumerate(lines):
        line.set_data(x[lnum], y[lnum])
        if lnum not in infected  and lnum not in recovered and lnum not in dead:
            line.set_color('green')
        if lnum in infected:
            line.set_color('red')
        if lnum in recovered:
            line.set_color('blue')
        if lnum in dead:
            line.set_color('black')

    """ax2"""
    total_inf.append(len(infected))
    total_rec.append(len(recovered))
    total_dead.append(len(dead))

    days = range(len(total_inf))
    line1.set_data([days, total_inf])
    line2.set_data([days, n-np.array(total_rec)-total_dead])
    line3.set_data([days, total_dead])
    ax2.set_xlim(0,days[-1])

    return lines, line1, line2, line3

anim = anime.FuncAnimation(fig, animate, interval=1)
plt.show()
