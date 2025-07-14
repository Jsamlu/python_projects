import pygame as pg
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


pg.init()

width, height = 800, 600 
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Particle simulation")

particles =[]
max_particles = 100

BLACK = (0,0,0)
RED = (255,0,0)

clock = pg.time.Clock()


fig, ax = plt.subplots(figsize=(6, 4))
ax.set_xlim(0, width)        
ax.set_ylim(height, 0)        
ax.set_title("Average Particle Position")
line, = ax.plot([], [], 'ro-')
average_positions = []


def add_particles(pos):
    if len(particles) < max_particles:
        particles.append(
            {
                'pos' : np.array(pos, dtype=float),
                'vel' : np.random.rand(2) * 2
            }
        )
def update_particles():
    for p in particles:
        p['pos'] += p['vel']

        # for bounce of walls
        if  p['pos'][0] <= 0 or p['pos'][0] >= width:
            p['vel'][0] *= -1
        if p['pos'][1] <= 0 or p['pos'][1] >= height:
            p['vel'][1] *= -1

def update_plot(frame):
    if particles:
        avg_pos = np.mean([p['pos'] for p in particles], axis = 0)
        average_positions.append(avg_pos)
        x_data = [pos[0] for pos in average_positions]
        y_data = [pos[1] for pos in average_positions]
        line.set_data(x_data, y_data)
        ax.relim()
        ax.autoscale_view()
    return line,


#set up animations

anim = FuncAnimation(fig, update_plot, frames=8, interval=10, blit=True)
plt.show(block=False)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            add_particles(pg.mouse.get_pos())
        
    update_particles()

    screen.fill(BLACK)

    #draw particles

    for p in particles:
        pg.draw.circle(screen, RED, p['pos'].astype(int), 5)
    pg.display.flip()
    clock.tick(60)

    #update Matplot 
    
    plt.pause(0.001)

pg.quit()

plt.close(fig)