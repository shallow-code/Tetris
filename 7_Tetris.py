import pyglet
import pyglet.clock
import random
from pyglet.window import key


#start
check_gameON = True
points_score = 0
main_batch = pyglet.graphics.Batch()
delta = 30
n_celle_x_game = 10
n_celle_x_inizio = n_celle_x_game // 2 -1
n_celle_x_info = 5
n_celle_x = n_celle_x_game + n_celle_x_info
n_celle_y = 20

window_height = n_celle_y * delta
window_width = n_celle_x * delta

# order of images
background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)
forestrings = pyglet.graphics.OrderedGroup(2)
#create game window
game_window = pyglet.window.Window(window_width, window_height)
line1 = pyglet.shapes.Line(n_celle_x_game*delta+1, 0, n_celle_x_game*delta+1, window_height, 1, color = (255, 255, 255), batch = main_batch, group=foreground)
line2 = pyglet.shapes.Line(n_celle_x_game*delta+3, 0, n_celle_x_game*delta+3, window_height, 1, color = (255, 255, 255), batch = main_batch, group=foreground)
label_info_NEXT_piece = pyglet.text.Label('Next Piece:',
                                          font_name='Impact',
                                          font_size=20/5 * n_celle_x_info,
                                          x=n_celle_x_game*delta+(n_celle_x_info*delta)//2, y=(n_celle_y - 3) * delta,
                                          anchor_x='center', anchor_y='bottom',batch = main_batch, group=foreground)
label_info_Score = pyglet.text.Label('Score:',
                                          font_name='Impact',
                                          font_size=20/5 * n_celle_x_info,
                                          x=n_celle_x_game*delta+(n_celle_x_info*delta)//2, y=85,
                                          anchor_x='center', anchor_y='bottom',batch = main_batch, group=foreground)
label_Score = pyglet.text.Label(str(points_score),
                                          font_name='Impact',
                                          font_size=40/5 * n_celle_x_info,
                                          x=n_celle_x_game*delta+(n_celle_x_info*delta)//2, y=20,
                                          anchor_x='center', anchor_y='bottom',batch = main_batch, group=foreground)


#path
pyglet.resource.path=['./resources']
pyglet.resource.reindex()
#load img
blue_p_imm = pyglet.resource.image("blue_p.png")
green_p_imm = pyglet.resource.image("green_p.png")
red_p_imm = pyglet.resource.image("red_p.png")
orange_p_imm = pyglet.resource.image("orange_p.png")
purple_p_imm = pyglet.resource.image("purple_p.png")
background_imm = pyglet.resource.image("background_pattern_2.jpg")
background_info_imm = pyglet.resource.image("background_info1.png")
#load music
GameOver_music = pyglet.media.load('C:/Users/Antonio/Desktop/Python/Pyglet/Tetris/resources/GameOver.wav', streaming=True)
Fall_music = pyglet.media.load('C:/Users/Antonio/Desktop/Python/Pyglet/Tetris/resources/Fall_quieter.wav', streaming=True)
Line_music = pyglet.media.load('C:/Users/Antonio/Desktop/Python/Pyglet/Tetris/resources/Line.wav', streaming=False)
player=pyglet.media.Player()
player.volume=0.2
#create dictonary
dict_color = {0:blue_p_imm ,1:green_p_imm ,2:red_p_imm ,3:orange_p_imm ,4:purple_p_imm}




def random_color():
    n_color = random.randint(0,4)
    return dict_color[n_color]

def random_piece(type_piece, color_img):
    global foreground
    piece = []
    c = [0 ,0 ,0 ,0]
    
    #I
    if type_piece==0:
        c[0] = [0 ,2]
        c[1] = [0 ,1]
        c[2] = [0 ,0]
        c[3] = [0 ,-1]

    #J
    if type_piece==1:
        c[0] = [0 ,1]
        c[1] = [0 ,0]
        c[2] = [0 ,-1]
        c[3] = [-1 ,-1]

    #L
    if type_piece==2:
        c[0] = [0 ,1]
        c[1] = [0 ,0]
        c[2] = [0 ,-1]
        c[3] = [1 ,-1]

    #O
    if type_piece==3:
        c[0] = [0 ,1]
        c[1] = [1 ,1]
        c[2] = [1 ,0]
        c[3] = [0 ,0]

    #S
    if type_piece==4:
        c[0] = [-1 ,1]
        c[1] = [0 ,1]
        c[2] = [0 ,0]
        c[3] = [1 ,0]

    #Z
    if type_piece==5:
        c[0] = [1 ,1]
        c[1] = [0 ,1]
        c[2] = [0 ,0]
        c[3] = [-1 ,0]

    #T
    if type_piece==6:
        c[0] = [0 ,1]
        c[1] = [-1 ,0]
        c[2] = [0 ,0]
        c[3] = [1 ,0]

    for i in range(4):
        block = moving_block(img=color_img ,x=c[i][0]*delta ,y=c[i][1]*delta, batch = main_batch, group=foreground)
        piece.append(block)

    return piece




#CLASS
#piece
class moving_block(pyglet.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_x = 0
        self.old_y = 0


def add_mass(mass, new_piece, img_color_block):
    global foreground
    for block in new_piece:
        mass_block = moving_block(img=img_color_block ,x=block.x ,y=block.y, batch = main_batch, group=foreground)
        mass.append(mass_block)

# control hit of the piece
def hit_control():
    global piece, mass
    check = False
    # hit mass of blocks
    for block in piece:
        for mass_block in mass:
            if (block.x==mass_block.x) and (block.y==mass_block.y):
                check = True
    # hit bottom line
    for block in piece:
        if block.y < 0:
            check = True
    return check
        

# hit managmet
def hit_managment(axis):
    global piece, mass, color_img, check_gameON, foreground, NEXT_type_piece, NEXT_color_img, type_piece, NEXT_piece
    if hit_control():
        for block in piece: #reset position
            block.x = block.old_x
            block.y = block.old_y
            
        # erase line
        if axis=='y':
            add_mass(mass, piece, color_img)
            y_test = set()
            for block in piece:
                y_test.add(block.y)
                block.delete()
            check_erase_line(y_test)

            #create piece
            type_piece = NEXT_type_piece
            color_img = NEXT_color_img
            #create info per next piece
            NEXT_type_piece = random.randint(0,6)
            NEXT_color_img = random_color() #immagine di colore casuale            
            piece = create_piece(type_piece, color_img)

            #display next piece
            NEXT_piece = random_piece(NEXT_type_piece, NEXT_color_img)
            center_x = (n_celle_x_game + n_celle_x_info//2) * delta
            center_y = (n_celle_y - 7) * delta
            if NEXT_type_piece == 3:
                center_x -= delta//2
            for block in NEXT_piece:
                block.x += center_x
                block.y += center_y

            #check if game over
            if hit_control():
                check_gameON = False
                x_0 = (n_celle_x_game*delta)//2
                y_0 = game_window.height//2
                f_0 = 45/10*min(n_celle_x_game,n_celle_y)

                # black written and white border
                label_GO_border1 = pyglet.text.Label('GAME OVER',font_name='Impact',font_size=f_0, x=x_0 + 2, y=y_0 + 2,
                                             anchor_x='center', anchor_y='center',batch = main_batch, group=forestrings)
                label_GO_border2 = pyglet.text.Label('GAME OVER',font_name='Impact',font_size=f_0, x=x_0 + 2, y=y_0 - 2,
                                             anchor_x='center', anchor_y='center',batch = main_batch, group=forestrings)
                label_GO_border3 = pyglet.text.Label('GAME OVER',font_name='Impact',font_size=f_0, x=x_0 - 2, y=y_0 + 2,
                                             anchor_x='center', anchor_y='center',batch = main_batch, group=forestrings)
                label_GO_border4 = pyglet.text.Label('GAME OVER',font_name='Impact',font_size=f_0, x=x_0 - 2, y=y_0 - 2,
                                             anchor_x='center', anchor_y='center',batch = main_batch, group=forestrings)
                label_GO_border1.color = (255,255,255,255)
                label_GO_border2.color = (255,255,255,255)
                label_GO_border3.color = (255,255,255,255)
                label_GO_border4.color = (255,255,255,255)
                label_GO = pyglet.text.Label('GAME OVER',font_name='Impact',font_size=f_0, x=x_0, y=y_0,
                                             anchor_x='center', anchor_y='center',batch = main_batch, group=forestrings)
                label_GO.color = (0,0,0,255)
                player.queue(GameOver_music)
                player.play()



# erase line
def check_erase_line(y_test):
    global mass, points_score
    y_erase = set()

    #check line to erase
    for y in y_test:
        k = 0
        for block in mass:
            if block.y == y:
                k += 1
            if k == n_celle_x_game:
                y_erase.add(y)
                points_score += 1 #increase score
                break

    #erase the lines
    y_erase = list(y_erase)
    y_erase.sort(reverse=True)
    block_erase = []
    for y in y_erase:
        for block in mass:
            if block.y == y:
                block_erase.append(block)
            elif block.y > y:
                block.y -= delta
    #erase blocks
    for block in block_erase:
        block.delete()  #elimino dal batch
        mass.remove(block) # elimino dal ìl' array della massa sul fondo
    if y_erase != []:
        player.queue(Line_music)
        player.play()


                


# create piece
def create_piece(type_piece, color_img):
    global I_orientation, center_x, center_y, check_gameON
    if check_gameON:
        piece = random_piece(type_piece, color_img)
        I_orientation = 1
        center_x = n_celle_x_inizio * delta
        center_y = n_celle_y * delta
        for block in piece:
            block.x += center_x
            block.y += center_y
        return piece

#inzialiation
#create bottom mass
mass = []
#create random piece
type_piece = random.randint(0,6)
color_img = random_color() #immagine di colore casuale
piece = create_piece(type_piece, color_img)
#create info per next piece
NEXT_type_piece = random.randint(0,6)
NEXT_color_img = random_color() #immagine di colore casuale
#
background_game = pyglet.sprite.Sprite(img=background_imm ,x=0 ,y=0, batch = main_batch, group=background)
background_info = pyglet.sprite.Sprite(img=background_info_imm ,x=n_celle_x_game*delta ,y=0, batch = main_batch, group=background)




@game_window.event #############################################################################################
def on_key_press(symbol, modifiers): # movement piece
    global I_orientation, center_x, center_y, check_gameON

    if check_gameON:
        # rotation piece, no rotation for square and only 2 mod for string
        if symbol == key.UP:
            if (type_piece == 0) or (type_piece == 4) or (type_piece == 5):
                #chech boundries
                check_ok = True
                for block in piece:
                    x_new = (block.y - center_y) * I_orientation + center_x
                    if (x_new<0) or (x_new==n_celle_x_game*delta):
                        check_ok = False
                #rotation
                if check_ok:
                    for block in piece:
                        block.old_x=block.x
                        block.old_y=block.y
                        x_coord = block.x - center_x
                        y_coord = block.y - center_y
                        block.x = y_coord * I_orientation + center_x
                        block.y = -x_coord * I_orientation + center_y
                    I_orientation *= -1
                    # hit control and managment
                    hit_managment('x')
                    
            elif type_piece != 3:
                #chech boundries
                check_ok = True
                for block in piece:
                    x_new = (block.y - center_y) + center_x
                    if (x_new<0) or (x_new==n_celle_x_game*delta):
                        check_ok = False
                #rotation
                if check_ok:
                    for block in piece:
                        block.old_x=block.x
                        block.old_y=block.y
                        x_coord = block.x - center_x
                        y_coord = block.y - center_y
                        block.x = y_coord + center_x
                        block.y = -x_coord + center_y
                    # hit control and managment

                    hit_managment('x')

        # left traslation
        if symbol == key.LEFT:
            #check boundries
            check_ok = True
            for block in piece:
                if block.x == 0:
                    check_ok = False
            if check_ok:
                center_x -= delta
                for block in piece:
                    block.old_x=block.x
                    block.old_y=block.y
                    block.x -= delta
            # hit control and managment
            hit_managment('x')

        # right traslation
        if symbol == key.RIGHT:
            #chech boundries
            check_ok = True
            for block in piece:
                if block.x == (n_celle_x_game-1)*delta:
                    check_ok = False
            if check_ok:
                center_x += delta
                for block in piece:
                    block.old_x=block.x
                    block.old_y=block.y
                    block.x += delta
            # hit control and managment
            hit_managment('x')

        # down traslation
        if symbol == key.DOWN:
            center_y -= delta
            for block in piece:
                block.old_x=block.x
                block.old_y=block.y
                block.y -= delta
            # hit control and managment
            hit_managment('y')

        # FAST down traslation
        if symbol == key.SPACE:
            check = True
            while check:
                center_y -= delta
                for block in piece:
                    block.old_x=block.x
                    block.old_y=block.y
                    block.y -= delta
                # hit control and managment
                check = not hit_control()
                hit_managment('y')
            #sound fall
            player.queue(Fall_music)
            player.play()
  
    
    
@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()


def update(dt):
    #movement piece
    global center_y, check_gameON, points_score, label_Score, foreground

    if check_gameON:
        center_y -= delta
        for block in piece:
            block.old_x=block.x
            block.old_y=block.y
            block.y -= delta

        #score update
        label_Score.delete()
        label_Score = pyglet.text.Label(str(points_score),
                                          font_name='Impact',
                                          font_size=40/5 * n_celle_x_info,
                                          x=n_celle_x_game*delta+(n_celle_x_info*delta)//2, y=20,
                                          anchor_x='center', anchor_y='bottom',batch = main_batch, group=foreground)

        # hit control and managment
        hit_managment('y')


if __name__=='__main__':
    pyglet.clock.schedule_interval(update, 1/5.0)
    pyglet.app.run()
