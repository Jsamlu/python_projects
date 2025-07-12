import pygame as pg

pg.init()

WIDTH = 900
HEIGHT = 700
screen = pg.display.set_mode([WIDTH, HEIGHT])

fps = 60
timer = pg.time.Clock()

#game variables

wall_thickness = 10
gravity = 1
bounce_stop = 0.3

#track pos i mouse movement vector
mouse_trajectory = []


class Ball:
    def __init__(self, x_pos, y_pos, radius, color, mass, retention, x_speed, y_speed, id, friction):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.mass = mass
        self.retention = retention
        self.color = color
        self.id = id
        self.circle = ''
        self.selected = False
        self.friction = friction

    def draw(self):
        self.circle = pg.draw.circle(screen, self.color, (self.x_pos, self.y_pos), self.radius)

    def check_gravity(self):
        if not self.selected:
            if self.y_pos < HEIGHT - self.radius - (wall_thickness/2):
                self.y_speed += gravity
            else:
                if self.y_speed > bounce_stop:
                    self.y_speed = self.y_speed * -1 * self.retention
                else:
                    if abs(self.y_speed) <= bounce_stop:
                        self.y_speed = 0
            
            if (self.x_pos < self.radius+ (wall_thickness/2) and self.x_speed < 0) or (self.x_pos > WIDTH - self.radius - (wall_thickness/2) and self.x_speed > 0):
                self.x_speed *= -1 * self.retention
                if abs(self.x_speed) < bounce_stop:
                    self.x_speed = 0
            if self.y_speed == 0 and self.x_speed != 0:
                if self.x_speed > 0:
                    self.x_speed -= self.friction 
                elif self.x_speed < 0:
                    self.x_speed += self.friction
        else:
            self.x_speed = x_push
            self.y_speed = y_push

        return self.y_speed        

    def update_pos(self, mouse):
        if not self.selected:
            self.y_pos += self.y_speed
            self.x_pos += self.x_speed
        else:
            self.x_pos = mouse[0]
            self.y_pos = mouse[1]

    def check_select(self, pos):
        self.selected = False
        if self.circle.collidepoint(pos):
            self.selected = True
        return self.selected



def draw_walls():
    left = pg.draw.line(screen, 'white', (0,0), (0, HEIGHT), wall_thickness)
    
    right = pg.draw.line(screen, 'white', (WIDTH,0), (WIDTH, HEIGHT), wall_thickness)
    
    top = pg.draw.line(screen, 'white', (0,0), (WIDTH,0), wall_thickness)

    bottom = pg.draw.line(screen, 'white', (0,HEIGHT), (WIDTH, HEIGHT), wall_thickness)

    wall_list= [left, right, top, bottom]

    return wall_list

def calc_motion_vector():
    x_speed = 0 
    y_speed = 0

    if len(mouse_trajectory) > 19:
        x_speed = (mouse_trajectory[-1][0] - mouse_trajectory[0][0]) / len(mouse_trajectory)
        y_speed = (mouse_trajectory[-1][1] - mouse_trajectory[0][1]) / len(mouse_trajectory)
    return x_speed, y_speed 

ball1 = Ball(50,50,30,"red", 100, 0.9, 0, 0, 1, .02) 
ball2 = Ball(500,120,90,"green", 100, 0.6, 0, 0, 1, .03) 
ball3 = Ball(150,300,50,"blue", 100, 0.8, 0, 0, 1, .02) 


balls= [ball1, ball2, ball3]
#main game loop
run = True
while run:
    timer.tick(fps)
    screen.fill("black")
    mouse_coords = pg.mouse.get_pos() 
    mouse_trajectory.append(mouse_coords)

    if len(mouse_trajectory) > 20:
        mouse_trajectory.pop(0)
    x_push, y_push = calc_motion_vector()

    walls = draw_walls()
    ball1.draw()
    ball1.update_pos(mouse_coords)
    ball1.y_speed = ball1.check_gravity()

    ball2.draw()
    ball2.update_pos(mouse_coords)
    ball2.y_speed = ball2.check_gravity()

    ball3.draw()
    ball3.update_pos(mouse_coords)
    ball3.y_speed = ball3.check_gravity()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if ball1.check_select(event.pos) or ball2.check_select(event.pos) or ball3.check_select(event.pos):
                    active_select = True
        
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                active_select = False
                for i in range(len(balls)):
                    balls[i].check_select((-1000, -1000))

    pg.display.flip()
pg.quit()

