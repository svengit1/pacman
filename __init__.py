import pyglet

from pyglet.window import key

#constants
pc_chew_speed = 0.1
pc_pixel_step = 100
pc_move_direction = 0

window = pyglet.window.Window(width=672, height=744)

#Genral graphics
graphic_grid = pyglet.image.load('./resources/spritemap-384.png')
graphic_sequence = pyglet.image.ImageGrid(graphic_grid, 10, 16)

#PacMan graphics
pc_l = [graphic_sequence[32], graphic_sequence[98], graphic_sequence[96]]
pc_r = [graphic_sequence[32], graphic_sequence[102], graphic_sequence[100]]
pc_d = [graphic_sequence[32], graphic_sequence[103], graphic_sequence[101]]
pc_u = [graphic_sequence[32], graphic_sequence[99], graphic_sequence[97]]

pc_anim_l = pyglet.image.Animation.from_image_sequence(pc_l, pc_chew_speed, True)
pc_anim_r = pyglet.image.Animation.from_image_sequence(pc_r, pc_chew_speed, True)
pc_anim_d = pyglet.image.Animation.from_image_sequence(pc_d, pc_chew_speed, True)
pc_anim_u = pyglet.image.Animation.from_image_sequence(pc_u, pc_chew_speed, True)

#PacMan died animation
pc_died = [graphic_sequence[i] for i in range(37, 48)]
pc_anim_died = pyglet.image.Animation.from_image_sequence(pc_died, pc_chew_speed, True)


sp_pc_died = pyglet.sprite.Sprite(pc_anim_died)

batch = pyglet.graphics.Batch()
background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)

sp_pc = pyglet.sprite.Sprite(pc_anim_r)
sp_pc.batch = batch
sp_pc.group = foreground


#Draw maze
sp_walls = []

valid_x_coords = []
valid_y_coords = []

def init_sprite(img,x,y,batch,group):
    s = pyglet.sprite.Sprite(img)
    s.x = x
    s.y = y
    s.batch = batch
    s.group = group
    return s


def load_world_def():
    global sp_walls
    walls_definition = []
    with open('resources/phase_1.txt', 'r') as f:
        for l in f:
            walls_definition.append(list(l))
    y = window.height-24
    for r in walls_definition:
        x = 0
        for c in r:
            if c == '\u250F':
                sp_walls.append(init_sprite(graphic_sequence[84], x, y, batch, background))
            if c == '\u2501':
                sp_walls.append(init_sprite(graphic_sequence[80], x, y, batch, background))
            if c == '\u2513':
                sp_walls.append(init_sprite(graphic_sequence[85], x, y, batch, background))
            if c == '\u2517':
                sp_walls.append(init_sprite(graphic_sequence[82], x, y, batch, background))
            if c == '\u251B':
                sp_walls.append(init_sprite(graphic_sequence[83], x, y, batch, background))
            if c == '\u2503':
                sp_walls.append(init_sprite(graphic_sequence[81], x, y, batch, background))
            x += 24
        y -= 24


@window.event
def on_draw():
    window.clear()
    batch.draw()
    sp_pc_died.draw()

def update(dt):
    if pc_move_direction == 0:
        sp_pc.x += dt * pc_pixel_step
    if pc_move_direction == 90:
        sp_pc.y += dt * pc_pixel_step
    if pc_move_direction == 180:
        sp_pc.x -= dt * pc_pixel_step
    if pc_move_direction == 270:
        sp_pc.y -= dt * pc_pixel_step

@window.event
def on_key_press(symbol, modifiers):
    global pc_move_direction
    if symbol == key.RIGHT:
        pc_move_direction = 0
        sp_pc.image = pc_anim_r

    if symbol == key.LEFT:
        pc_move_direction = 180
        sp_pc.image = pc_anim_l

    if symbol == key.DOWN:
        pc_move_direction = 270
        sp_pc.image = pc_anim_d

    if symbol == key.UP:
        pc_move_direction = 90
        sp_pc.image = pc_anim_u



def main():
    load_world_def()
    pyglet.clock.schedule_interval(update, 1 / 100.)
    pyglet.app.run()


if __name__ == "__main__":
    # execute only if run as a script
    main()

