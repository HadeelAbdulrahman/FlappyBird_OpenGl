from math import cos, sin
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.fonts import GLUT_BITMAP_HELVETICA_18
import random
import os

# === Initialize ===
pygame.init()
pygame.mixer.init()
glutInit()

screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Flappy Bird")
gluOrtho2D(0, 800, 0, 600)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# === Load Bird Texture ===
def load_texture(image_path):
    try:
        surface = pygame.image.load(image_path).convert_alpha()
        texture_data = pygame.image.tostring(surface, "RGBA", True)
        width, height = surface.get_size()
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        return tex_id, width, height
    except Exception as e:
        print("Failed to load texture:", e)
        return None, 0, 0

# === Drawing Helpers ===
def draw_sprite(texture, x, y, width, height):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)
    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x, y)
    glTexCoord2f(1, 0); glVertex2f(x + width, y)
    glTexCoord2f(1, 1); glVertex2f(x + width, y + height)
    glTexCoord2f(0, 1); glVertex2f(x, y + height)
    glEnd()
    glDisable(GL_TEXTURE_2D)

def draw_pipe(x, y, width, height, day_mode=True):
    if day_mode:
        base_color = (0.0, 0.8, 0.0)
        side_color = (0.0, 0.6, 0.0)
        top_color = (0.2, 0.9, 0.2)
    else:
        base_color = (0.0, 0.4, 0.0)
        side_color = (0.0, 0.3, 0.0)
        top_color = (0.2, 0.5, 0.2)

    glColor3f(*base_color)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()

    depth = 10
    glColor3f(*side_color)
    glBegin(GL_QUADS)
    glVertex2f(x + width, y)
    glVertex2f(x + width + depth, y - depth)
    glVertex2f(x + width + depth, y + height - depth)
    glVertex2f(x + width, y + height)
    glEnd()

    glColor3f(*top_color)
    glBegin(GL_QUADS)
    glVertex2f(x, y + height)
    glVertex2f(x + width, y + height)
    glVertex2f(x + width + depth, y + height - depth)
    glVertex2f(x + depth, y + height - depth)
    glEnd()

def draw_grass_3d(day_mode=True):
    if day_mode:
        front = (0.0, 0.6, 0.0)
        side = (0.0, 0.4, 0.0)
    else:
        front = (0.0, 0.3, 0.0)
        side = (0.0, 0.2, 0.0)

    w = 40
    depth = 5
    for i in range(0, 800, w):
        glColor3f(*front)
        glBegin(GL_TRIANGLES)
        glVertex2f(i, 0)
        glVertex2f(i + w // 2, 30)
        glVertex2f(i + w, 0)
        glEnd()

        glColor3f(*side)
        glBegin(GL_TRIANGLES)
        glVertex2f(i + w, 0)
        glVertex2f(i + w + depth, -depth)
        glVertex2f(i + w // 2 + depth, 30 - depth)
        glEnd()

def draw_bird_with_shadow(texture, x, y, width, height, day_mode=True):
    shadow_color = (0, 0, 0, 0.2) if day_mode else (0.1, 0.1, 0.1, 0.4)
    offset = 4

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)
    glColor4f(*shadow_color)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x + offset, y - offset)
    glTexCoord2f(1, 0); glVertex2f(x + width + offset, y - offset)
    glTexCoord2f(1, 1); glVertex2f(x + width + offset, y + height - offset)
    glTexCoord2f(0, 1); glVertex2f(x + offset, y + height - offset)
    glEnd()

    draw_sprite(texture, x, y, width, height)

def draw_gradient_background(day_mode=True):
    glBegin(GL_QUADS)
    if day_mode:
        glColor3f(0.5, 0.8, 1.0)
        glVertex2f(0, 600)
        glVertex2f(800, 600)
        glColor3f(0.1, 0.6, 0.9)
    else:
        glColor3f(0.05, 0.05, 0.2)
        glVertex2f(0, 600)
        glVertex2f(800, 600)
        glColor3f(0.0, 0.0, 0.1)
    glVertex2f(800, 0)
    glVertex2f(0, 0)
    glEnd()

    if day_mode:
        glColor3f(1.0, 0.5, 0.0)
        radius = 150
    else:
        glColor3f(0.9, 0.9, 1.0)
        radius = 100

    cx, cy = 800, 600
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(cx, cy)
    for i in range(101):
        angle = 2 * 3.14159 * i / 100
        glVertex2f(cx + radius * cos(angle), cy + radius * sin(angle))
    glEnd()

def circle_rect_collision(cx, cy, radius, rect):
    nx = max(rect.left, min(cx, rect.right))
    ny = max(rect.top,  min(cy, rect.bottom))
    dx, dy = cx - nx, cy - ny
    return dx*dx + dy*dy < radius*radius

def load_high_score():
    try:
        with open("highscore.dat", "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    with open("highscore.dat", "w") as f:
        f.write(str(score))

def update_high_score(current_score):
    hs = load_high_score()
    if current_score > hs:
        save_high_score(current_score)
        return current_score
    return hs

def draw_high_score_display(x, y, high_score, current_score):
    glColor3f(0.9, 0.9, 0.2)
    glWindowPos2d(x, y)
    for ch in f"High Score: {high_score}":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
    glColor3f(1, 1, 1)
    glWindowPos2d(x, y - 20)
    for ch in f"Score: {current_score}":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

# === Particle System ===
class Particle:
    def __init__(self, x, y, dx, dy, size, color, lifespan):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.size = size
        self.color = color
        self.lifespan = lifespan

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.lifespan -= 1

    def draw(self):
        glColor4f(*self.color)
        glBegin(GL_QUADS)
        glVertex2f(self.x - self.size, self.y - self.size)
        glVertex2f(self.x + self.size, self.y - self.size)
        glVertex2f(self.x + self.size, self.y + self.size)
        glVertex2f(self.x - self.size, self.y + self.size)
        glEnd()

particles = []

def spawn_particles(x, y, count=10):
    for _ in range(count):
        dx = random.uniform(-1.5, 1.5)
        dy = random.uniform(1, 3)
        size = random.uniform(2, 5)
        color = (random.uniform(0.8, 1.0), random.uniform(0.8, 1.0), random.uniform(0.1, 0.3), 1.0)
        lifespan = random.randint(20, 40)
        particles.append(Particle(x, y, dx, dy, size, color, lifespan))

# === Load Assets ===
bird_texture, bird_w, bird_h = load_texture("bird.png")
jump_sound = pygame.mixer.Sound("jump.wav")
fall_sound = pygame.mixer.Sound("fall.wav")

# === Game Variables ===
bird_x, bird_y = 100, 300
velocity, gravity = 0, -0.5
jump_strength = 8
game_over = False
score = 0
high_score = load_high_score()

pipes = []
pipe_gap = 200
pipe_freq = 1500
last_pipe = pygame.time.get_ticks()
pipe_speed = 2

clock = pygame.time.Clock()
running = True

# === Main Game Loop ===
while running:
    glClear(GL_COLOR_BUFFER_BIT)
    day_mode = (score // 5) % 2 == 0
    draw_gradient_background(day_mode)
    draw_grass_3d(day_mode)

    now = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_q:
                running = False
            if event.key == K_SPACE and not game_over:
                velocity = jump_strength
                jump_sound.play()
                spawn_particles(bird_x + bird_w // 2, bird_y)  # Spawn particles when the bird jumps
            if event.key == K_r and game_over:
                bird_y, velocity = 300, 0
                pipes.clear()
                score = 0
                game_over = False

    if not game_over:
        velocity += gravity
        bird_y += velocity
        if bird_y <= 0:
            bird_y, velocity = 0, 0
            fall_sound.play()
            game_over = True

        if now - last_pipe > pipe_freq:
            pipes.append([800, random.randint(100,400), False])
            last_pipe = now

        for pipe in pipes[:]:
            pipe[0] -= pipe_speed
            if not pipe[2] and pipe[0] + 80 < bird_x:
                score += 1
                pipe[2] = True
                high_score = update_high_score(score)
            draw_pipe(pipe[0], pipe[1] + pipe_gap, 80, 400, day_mode)
            draw_pipe(pipe[0], pipe[1] - 400, 80, 400, day_mode)
            cx, cy = bird_x + bird_w/2, bird_y + bird_h/2
            r = min(bird_w, bird_h)/2 - 5
            top = pygame.Rect(pipe[0], pipe[1] + pipe_gap, 80, 400)
            bot = pygame.Rect(pipe[0], pipe[1] - 400, 80, 400)
            if circle_rect_collision(cx, cy, r, top) or circle_rect_collision(cx, cy, r, bot):
                fall_sound.play()
                game_over = True
            if pipe[0] < -80:
                pipes.remove(pipe)

    for particle in particles[:]:
        particle.update()
        particle.draw()
        if particle.lifespan <= 0:
            particles.remove(particle)

    draw_bird_with_shadow(bird_texture, bird_x, bird_y, bird_w, bird_h, day_mode)
    draw_high_score_display(10, 580, high_score, score)

    if game_over:
        glColor3f(1, 0, 0)
        glWindowPos2d(250, 300)
        for ch in "GAME OVER - Press R to restart":
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()