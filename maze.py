
from pygame import *
import random
import math
init()
font.init()
mixer.init()




FONT = 'PressStart2P-Regular.ttf'

FPS = 60
TILE_SIZE = 40
MAP_WIDTH, MAP_HEIGHT = 40, 35
scr_info= display.Info()


WIDTH, HEIGHT = scr_info.current_w, scr_info.current_h

#створи вікно гри
window = display.set_mode((WIDTH,HEIGHT), flags=FULLSCREEN)
display.set_caption("Hotline Kiev")
clock = time.Clock()



#задай фон сцени
bg = image.load("using images/Bg.png")
bg = transform.scale(bg, (WIDTH, HEIGHT))
player_img = image.load("using images/y1y-ThQx (1) 1 (1).png")
enemy_img = image.load("using images/enemy_img (1).png")
floor1_img = image.load("using images/floor_1.png")
floor2_img = image.load("using images/floor_2.png")
floor3_img = image.load("using images/floor_3 (3).png")
floor4_img = image.load("using images/floor_4.png")
floor5_img = image.load("using images/floor_5.png")
floor6_img = image.load("using images/floor_6.png")
left_wall_img = image.load("using images/left_wall.png")
right_wall_img = image.load("using images/right_wall.png")
top_wall_img = image.load("using images/top_wall.png")
bottom_wall_img = image.load("using images/bottom_wall.png")






 
#enemy_img = image.load("cyborg.png")
treasure_img = image.load("treasure.png")

all_labels = sprite.Group()
all_sprites = sprite.Group()
#створи 2 спрайти та розмісти їх на сцені
class BaseSprite(sprite.Sprite):
    def __init__(self,image, x, y, width, height):
        super().__init__()
        self.image = transform.scale(image, (width, height))
        self.rect = Rect(x,y, width, height)
        self.mask = mask.from_surface(self.image)
        all_sprites.add(self)
    def draw(self, window):
        window.blit(self.image, self.rect)


class Label(sprite.Sprite):
    def __init__(self,text, x, y, fontsize = 30,color = (255, 255, 255),font_name = FONT):
        super().__init__()
        self.color = color
        self.font = font.Font(FONT, fontsize)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        all_labels.add(self)

    def set_text(self, new_text, color = (255, 255, 255)):
        self.image = self.font.render(new_text, True, color)

def move_map(shift_x= 0, shift_y=0):

    for s in all_sprites:
        s.rect.x += shift_x
        s.rect.y += shift_y
    coll_list = sprite.spritecollide(player1, walls, False, sprite.collide_mask)
    if len (coll_list)>0:
        for s in all_sprites:
            s.rect.x -= shift_x
            s.rect.y -= shift_y


class Player(BaseSprite):
    def __init__(self, image, x, y, width, height):
        super().__init__(image, x, y, width, height)
        self.right_image = self.image
        self.left_image = transform.flip(self.image,True, False)
        self.damage_timer = time.get_ticks()       
        self.speed = 15
        self.original_image = self.image
        self.hp = 100
        self.coins_counter = 0



    


    def update(self):
        shift_x, shift_y = 0, 0
        keys = key.get_pressed()

        if keys[K_a]:
            if self.rect.x <= WIDTH / 2:
                shift_x += self.speed 
            else:
                self.rect.x -= self.speed
        if keys[K_d]:
            if self.rect.x >= WIDTH / 2:
                shift_x -= self.speed
            else:
                self.rect.x += self.speed
        if keys[K_w]:
            if self.rect.y <= HEIGHT / 3:
                shift_y += self.speed
            else:
                self.rect.y -= self.speed
        if keys[K_s]:
            if self.rect.y >= HEIGHT / 3:
                shift_y -= self.speed
            else:
                self.rect.y += self.speed
        move_map(shift_x, shift_y)

        coll_list = sprite.spritecollide(player1, walls, False, sprite.collide_mask)
 


        self.rotate()
    


    def rotate(self):
        mouse_x, mouse_y = mouse.get_pos()
        player_x = self.rect.centerx
        player_y = self.rect.centery
        angle = math.atan2(mouse_y-player_y, mouse_x-player_x)
        self.image = transform.rotate(self.original_image, -math.degrees(angle))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = mask.from_surface(self.image)


        
            


class Enemy(BaseSprite):
    def __init__(self, image, x, y, width, height, dir_list):
        super().__init__(image, x, y, width, height)
        self.right_image = self.image
        self.left_image = transform.flip(self.image,True, False)
        self.speed = 2
        self.dir_list = dir_list
        self.dir = random.choice(self.dir_list)
    def update(self):
        old_pos = self.rect.x, self.rect.y
        if self.dir == 'left':
            self.rect.x -=self.speed
            self.image = self.left_image
        elif self.dir == 'right':
           self.rect.x +=self.speed
           self.image = self.right_image
        elif self.dir == 'up':
            self.rect.y -=self.speed
        elif self.dir == 'down':
            self.rect.y +=self.speed
        
        coll_list = sprite.spritecollide(self, walls, False, sprite.collide_mask)
        if len(coll_list)>0:
            self.rect.x, self.rect.y = old_pos
            self.dir = random.choice(self.dir_list)
        

player1 = Player(player_img,200,300, 60, 60)
all_sprites.remove(player1)

result = Label("", 300, 300, fontsize=60)
restart_text = Label("Press R to restart", 350, 350, fontsize=20 )
all_labels.remove(restart_text)
hp_label = Label(f"HP:{player1.hp}", 10, 10, fontsize=20)
floors = sprite.Group()
enemys = sprite.Group()
walls = sprite.Group()
def game_start():
    global treasure, run, finish
    for floor1 in floors:
        floor1.kill()
    for e in enemys:
        e.kill()
    
    
    run = True
    finish = False
    player1.hp = 100
    hp_label.set_text(f"HP:{player1.hp}")
    result.set_text('')
    all_labels.remove(restart_text)
    with open("map.txt", "r") as file:
        map = file.readlines()
        x, y = 0,0
        for row in map:
            for symbol in row:

                

                if symbol=='F':
                    floors.add(BaseSprite(floor1_img, x, y, TILE_SIZE, TILE_SIZE))

                if symbol=='V':
                    floors.add(BaseSprite(floor2_img, x, y, TILE_SIZE, TILE_SIZE))
                
                if symbol=='1':
                    floors.add(BaseSprite(floor3_img, x, y, TILE_SIZE, TILE_SIZE))                
                
                if symbol=='2':
                    floors.add(BaseSprite(floor4_img, x, y, TILE_SIZE, TILE_SIZE))
                              
                if symbol=='3':
                    floors.add(BaseSprite(floor5_img, x, y, TILE_SIZE, TILE_SIZE))

                if symbol=='4':
                    floors.add(BaseSprite(floor6_img, x, y, TILE_SIZE, TILE_SIZE))

                if symbol == 'P':
                    player1.rect.x = x
                    player1.rect.y = y
                

                
                

                


                x+=TILE_SIZE
            x = 0    
            y+= TILE_SIZE


    with open("map2.txt", "r") as file:
        map = file.readlines()
        x, y = 0,0
        for row in map:
            for symbol in row:

                if symbol=='1':
                    walls.add(BaseSprite(top_wall_img, x, y, TILE_SIZE, TILE_SIZE))
                
                if symbol=='2':
                    walls.add(BaseSprite(left_wall_img, x, y, TILE_SIZE, TILE_SIZE))

                if symbol=='3':
                    walls.add(BaseSprite(bottom_wall_img, x, y, TILE_SIZE, TILE_SIZE))
                
                if symbol=='4':
                    walls.add(BaseSprite(right_wall_img, x, y, TILE_SIZE, TILE_SIZE))
                if symbol=='E':
                    enemys.add(Enemy(enemy_img, x, y, 55, 55, ['left', 'right', 'top','bottom']))
                
                x+=TILE_SIZE
            x = 0    
            y+= TILE_SIZE
    move_map(0,-500)
    player1.rect.y -= 500
game_start()
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_r and finish:
                game_start()


    if player1.hp<=0:
        finish = True
        result.set_text("You lose!")
        result.rect.x = WIDTH/2 - result.image.get_width()/2

        result.rect.y = HEIGHT/2 - result.image.get_height()/2
        all_labels.add(restart_text)
        restart_text.rect.x = WIDTH/2 - result.image.get_width()/2


    if not finish:
        player1.update()

        enemys.update()


    window.blit(bg, (0,0))
    
    all_sprites.draw(window)
    player1.draw(window)
    all_labels.draw(window)



    display.update()
    clock.tick(FPS)