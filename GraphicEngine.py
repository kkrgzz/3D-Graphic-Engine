import pygame
import sys
import math

green = (34, 139, 34)


def rotate2d(pos, rad): x, y = pos; s, c = math.sin(rad), math.cos(rad); return x * c - y * s, y * c + x * s


class Cam:
    def __int__(self, pos=(0, 0, 0), rot=(0, 0)):
        self.pos = list(pos)
        self.rot = list(rot)

    def events(self, event):
        if event.type == pygame.MOUSEMOTION:
            x, y = event.rel
            x /= 200
            y /= 200
            self.rot[0] += y
            self.rot[1] += x

    def update(self, dt, key):
        s = dt * 10

        if key[pygame.K_q]: self.pos[1] += s
        if key[pygame.K_e]: self.pos[1] -= s

        x, y = s * math.sin(self.rot[1]), s * math.cos(self.rot[1])

        if key[pygame.K_w]: self.pos[0] += x; self.pos[2] += y
        if key[pygame.K_s]: self.pos[0] -= x; self.pos[2] -= y

        if key[pygame.K_a]: self.pos[0] -= y; self.pos[2] += x
        if key[pygame.K_d]: self.pos[0] += y; self.pos[2] -= x


class Cube:
    vertices = (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)
    edges = (0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (3, 7), (2, 6), (1, 5)
    faces = (0, 1, 2, 3), (4, 5, 6, 7), (1, 2, 6, 5), (0, 3, 7, 4), (0, 1, 5, 4), (2, 3, 7, 6)
    colors = (255, 0, 0), (255, 128, 0), (255, 255, 0), (255, 255, 255), green, (0, 255, 0)

    def __init__(self, pos=(0, 0, 0)):
        x, y, z = pos
        self.verts = [(x + X / 2, y + Y / 2, z + Z / 2) for X, Y, Z in self.vertices]


pygame.init()
w, h = 1000, 800
pygame.display.set_caption("3D Graphics Engine")
font = pygame.font.Font(pygame.font.get_default_font(), 12)
cx, cy = w // 2, h // 2
screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

cam = Cam()
cam.__int__((0, 0, 0))

pygame.event.get()
pygame.mouse.get_rel()
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

cubes = [Cube((0, 0, 0)), Cube((2, 0, 0)), Cube((5, 4, 0))]


i, k = (0, 0)
x, y, z = (10, 10, 10)
cubes  = []
# Print X values to the ground
while i < 10:  # Length of the X axis that in block unit
    k=0
    while k < 10:  # Length of the Z axis that in block unit
        cubes.extend([Cube((x-i, y, z-k))])
        k += 1
    i+=1



while True:
    dt = clock.tick() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
        cam.events(event)
    screen.fill((0, 192, 255))

    # X, Y, Z  ve FPS de??erleri ekrana yazd??r??l??yor.
    xValue = font.render('X: ' + str(cam.pos[0]), True, (253, 84, 99))
    yValue = font.render('Y: ' + str(cam.pos[1]), True, (227, 140, 89))
    zValue = font.render('Z: ' + str(cam.pos[2]), True, (250, 227, 98))
    fpsValue = font.render('FPS: ' + str(clock.get_fps()), True, (255, 255, 255))
    screen.blit(xValue, dest=(0, 0))
    screen.blit(yValue, dest=(0, 15))
    screen.blit(zValue, dest=(0, 30))
    screen.blit(fpsValue, dest=(0, 45))

    face_color = []
    depth = []
    face_list = []

    for obj in cubes:

        vert_list = []
        screen_coords = []
        for x, y, z in obj.verts:
            x -= cam.pos[0]
            y -= cam.pos[1]
            z -= cam.pos[2]

            x, z = rotate2d((x, z), cam.rot[1])
            y, z = rotate2d((y, z), cam.rot[0])

            vert_list += [(x, y, z)]

            f = 200 / z
            x, y = x * f, y * f
            screen_coords += [(cx + int(x), cy + int(y))]

        for f in range(len(obj.faces)):
            face = obj.faces[f]
            on_screen = False
            for i in face:
                x, y = screen_coords[i]
                if vert_list[i][2] > 0 and 0 < x < w and 0 < y < h: on_screen = True; break

            if on_screen:
                coords = [screen_coords[i] for i in face]
                face_list += [coords]
                face_color += [obj.colors[f]]
                depth += [sum(sum(vert_list[j][i] for j in face) ** 2 for i in range(3))]

    # Final drawing part, all faces from all objects
    order = sorted(range(len(face_list)), key=lambda i: depth[i], reverse=True)
    for i in order:
        try:
            pygame.draw.polygon(screen, face_color[i], face_list[i])
        except:
            pass
    pygame.display.flip()

    key = pygame.key.get_pressed()
    cam.update(dt, key)
