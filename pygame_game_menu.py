from typing import Any
import pygame
import os
import subprocess as sub


#初始化pygame
pygame.init()

#設定視窗大小
FPS = 60
WIDTH = 800
HEIGHT = 480

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Game Menu")
clock = pygame.time.Clock()

#顏色設定
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)

#字體設定
font = pygame.font.SysFont("arialblack",12)
TEXT_COL = (BLACK)

# 滾動速度
scroll_speed = 5
offset = 0
stopScroll = False

RealHeight = 240
#載入圖片
background_path = r'D:\Projects\python_project\game_menu\img\background.png'
game_icon_path = r'D:\Projects\python_project\game_menu\img\pong_game_icon.png'
null_icon_path = r'D:\Projects\python_project\game_menu\img\null_icon.png'


background_icon = pygame.image.load(background_path).convert_alpha()
game_icon = pygame.image.load(game_icon_path).convert_alpha()
null_icon = pygame.image.load(null_icon_path).convert_alpha()
#遊戲路徑
Game_script_path = r'D:\Projects\python_project\pong-game\pygame-pong-game.py'

#開啟遊戲
isOpenGame = False

# function
def open_game_file():
        global isOpenGame
        isOpenGame=True
        sub.Popen(["python",Game_script_path])
        
        pygame.quit()

def draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))

class Mouse(pygame.sprite.Sprite):
    
    def __init__(self, x_pos, y_pos, enabled):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((20,20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.speed = 5
        
        self.enabled = enabled
        

    def update(self):       

        #滑鼠移動到按鈕上時
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speed
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speed

        #滑鼠脫屏
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT

class Button(pygame.sprite.Sprite):
    
    def __init__(self, text, x_pos, y_pos, enabled, icon):
        pygame.sprite.Sprite.__init__(self)

        #self.image = pygame.Surface((160,80))
        self.image = icon
        self.ori_image = pygame.transform.scale(self.image, (190,108))
        self.bigger_img = pygame.transform.scale(self.image, (228,130))
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

        self.text = text
        self.enabled = enabled

     
   

    def update(self):       
        global offset, RealHeight,stopScroll,isOpenGame
        #滑鼠移動到按鈕上時
        key_pressed = pygame.key.get_pressed()
        if pygame.sprite.collide_rect(self,mouse_contr):
            #self.image.fill(RED)
            
            self.image = self.bigger_img
            if key_pressed[pygame.K_j]:
                #self.image.fill(GREEN)
                if(self.text == 'D:\Projects\python_project\pong-game\pygame-pong-game.py' and isOpenGame == False):
                    open_game_file()
           
        else:
            #self.image.fill(WHITE)
            self.image = self.ori_image

        #滑動畫面時
       
        self.rect.y += offset

        #button_text = font.render(self.text, True, BLACK)
        #self.image.blit(button_text, (20,30))
        
      
     

#建構sprite
all_sprites = pygame.sprite.Group()
mouse_contr = Mouse(0,0,True)
button_01 = Button(Game_script_path,10,0,True, game_icon)
button_02 = Button("2",10,150,True, null_icon)
button_03 = Button("3",10,300,True, null_icon)
all_sprites.add(mouse_contr,button_01,button_02,button_03)


#鼠標鎖定 和 隱藏
#pygame.event.set_grab(True)
#pygame.mouse.set_visible(False)

running = True

#遊戲迴圈
while running:



    clock.tick(FPS)
    #取得輸入
    for event in pygame.event.get():
       
        if event.type == pygame.QUIT:
            running = False

    #更新遊戲
    mouse = pygame.mouse.get_pos() 
    key_pressed = pygame.key.get_pressed()
    
          
    
    if key_pressed[pygame.K_UP]:
        offset = scroll_speed
        if  button_03.rect.bottom >= 400:
            offset = 0
    elif key_pressed[pygame.K_DOWN]:
        offset = -scroll_speed
        if button_01.rect.top <= -100 :
            offset = 0
    else:
        offset = 0
    
            
    
    all_sprites.update()

   

    #更新畫面
    screen.blit(background_icon,(0,0))
    all_sprites.draw(screen)
    pygame.display.update()
    

#遊戲結束
pygame.quit()