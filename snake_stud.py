from pygame import display, time, draw, QUIT, init, KEYDOWN, K_a, K_s, K_d, K_w
from random import randint
import pygame
import os
from numpy import sqrt
init()

done = False
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

width = 600
height = 600

screen = display.set_mode([width, height])
display.set_caption("snake_self")
clock = time.Clock()

# Center the Game Application
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Text Renderer
def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, 0, textColor)

    return newText

# Game Fonts
font = "C://Users//Ilham Fakhri//Documents//Belajar Phyton//vscode//PressStart2P-Regular.ttf"

# Main Menu
def main_menu():

    menu=True
    selected="start"

    while menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    selected="start"
                elif event.key==pygame.K_DOWN:
                    selected="quit"
                if event.key==pygame.K_RETURN:
                    if selected=="start":
                        menu=False
                    if selected=="quit":
                        pygame.quit()
                        quit()

        # Main Menu UI
        screen.fill(BLACK)
        title1=text_format("si ular", font, 50, WHITE)
        title2=text_format("mandiri", font, 50, WHITE)
        if selected=="start":
            text_start=text_format("START", font, 35, YELLOW)
        else:
            text_start = text_format("START", font, 35, WHITE)
        if selected=="quit":
            text_quit=text_format("QUIT", font, 35, YELLOW)
        else:
            text_quit = text_format("QUIT", font, 35, WHITE)

        title_rect1=title1.get_rect()
        title_rect2=title2.get_rect()
        start_rect=text_start.get_rect()
        quit_rect=text_quit.get_rect()

        # Main Menu Text
        screen.blit(title1, (width/2 - (title_rect1[2]/2), 110))
        screen.blit(title2, (width/2 - (title_rect2[2]/2), 180))
        screen.blit(text_start, (width/2 - (start_rect[2]/2), 340))
        screen.blit(text_quit, (width/2 - (quit_rect[2]/2), 400))
        pygame.display.update()
        clock.tick(30)

current = 15

def make_str(flag):
    global current
    if flag==1:
        current=current+1
    elif flag==0:
        current=current
    elif flag==-1:
        current=current-1
    elif flag==-2:
        return current
    if current<5:
        current=5
    elif current>25:
        current=25
    return "<"+"  "+str(current)+"  "+">"

def draw_ui():
    # Main Menu UI
    screen.fill(BLACK)
    title1=text_format("si ular", font, 50, WHITE)
    title2=text_format("mandiri", font, 50, WHITE)
    text_up=text_format("row and cols", font, 35, WHITE)
    text_down=text_format(make_str(0), font, 35, YELLOW)
    #print(current)

    title_rect1=title1.get_rect()
    title_rect2=title2.get_rect()
    text_rect=text_up.get_rect()
    cols_row_rect=text_down.get_rect()

    # Main Menu Text
    screen.blit(title1, (width/2 - (title_rect1[2]/2), 110))
    screen.blit(title2, (width/2 - (title_rect2[2]/2), 180))
    screen.blit(text_up, (width/2 - (text_rect[2]/2), 340))
    screen.blit(text_down, (width/2 - (cols_row_rect[2]/2), 400))
    pygame.display.update()

# setting row and cols Menu
def setting_menu():
    menu=True
    draw_ui()
    while menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    menu=False
                elif event.key==pygame.K_RIGHT:
                    make_str(1)
                    draw_ui()
                elif event.key==pygame.K_LEFT:
                    make_str(-1)
                    draw_ui()
                #print(current)

        clock.tick(30)

#a-star algorithm
def getpath(food1, snake1):
    food1.camefrom = []
    for s in snake1:
        s.camefrom = []
    openset = [snake1[-1]]
    closedset = []
    dir_array1 = []
    while 1:
        current1 = min(openset, key=lambda x: x.f)
        openset = [openset[i] for i in range(len(openset)) if not openset[i] == current1]
        closedset.append(current1)
        for neighbor in current1.neighbors:
            if neighbor not in closedset and not neighbor.obstrucle and neighbor not in snake1:
                tempg = neighbor.g + 1
                if neighbor in openset:
                    if tempg < neighbor.g:
                        neighbor.g = tempg
                else:
                    neighbor.g = tempg
                    openset.append(neighbor)
                neighbor.h = sqrt((neighbor.x - food1.x) ** 2 + (neighbor.y - food1.y) ** 2)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.camefrom = current1
        if current1 == food1: #exit of infinite loop
            break
    while current1.camefrom: #mencatat direction untuk mendapatkan food dengan flag angka
        if current1.x == current1.camefrom.x and current1.y < current1.camefrom.y:
            dir_array1.append(2)
        elif current1.x == current1.camefrom.x and current1.y > current1.camefrom.y:
            dir_array1.append(0)
        elif current1.x < current1.camefrom.x and current1.y == current1.camefrom.y:
            dir_array1.append(3)
        elif current1.x > current1.camefrom.x and current1.y == current1.camefrom.y:
            dir_array1.append(1)
        current1 = current1.camefrom
    #print(dir_array1)
    for i in range(rows):
        for j in range(cols):
            grid[i][j].camefrom = []
            grid[i][j].f = 0
            grid[i][j].h = 0
            grid[i][j].g = 0
    return dir_array1

def game_over():
    screen.fill(BLACK)
    title=text_format("Game Over", font, 50, WHITE)
    title_rect=title.get_rect()
    screen.blit(title, (width/2 - (title_rect[2]/2), 280))
    pygame.display.flip()

def draw_score():
    title=text_format(score_it(2), font, 10, YELLOW)
    title_rect=title.get_rect()
    screen.blit(title, (540 - (title_rect[2]/2), 15))
    #pygame.display.flip()

def score_it(flag):
    global score
    if flag==1:
        score=score+1
        return score
    elif flag==2:
        return "Score : "+str(score)

#inisialisasi kebutuhan pada pencarian a-starnya 
class Spot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.camefrom = []
        self.obstrucle = False
        if randint(1, 101) < 3:
            self.obstrucle = True

    #function untuk merealisasikan dengan gambaran dengan panggilan warna untuk display-kan ke layar
    def show(self, color):
        draw.rect(screen, color, [self.x*hr+2, self.y*wr+2, hr-4, wr-4])

    #Function untuk menginisialisasi neighbor daripada grid-nya
    def add_neighbors(self):
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.x < rows - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y < cols - 1:
            self.neighbors.append(grid[self.x][self.y + 1])

main_menu()
setting_menu()

cols = current
rows = current
wr = width/cols
hr = height/rows
direction = 1
score = 0

#inisialisasi grid berdasarkan kolom dan baris yang akan dipakai untuk arena ular
grid = [[Spot(i, j) for j in range(cols)] for i in range(rows)]

#inisialisasi masing-masing neighbor dari setiap grid nya
for i in range(rows):
    for j in range(cols):
        grid[i][j].add_neighbors()

snake = [grid[round(rows/2)][round(cols/2)]] #Inisialisasi awal mulai snake dari tengah-tengah layar
food = grid[randint(0, rows-1)][randint(0, cols-1)] #Food selalu diinisialisasi secara acak dengan syntax radint dengan interval 0 hingga (kolom atau baris)
current = snake[-1] #Posisi current merupakan posisi kepala daripada si ular
dir_array = getpath(food, snake) #dir_array yaitu array untuk mendapatkan direction flag daripada pergerakan ular tersebut
food_array = [food] #array yang mencatat riwayat daripada food yang pernah dipakai sebelumnya.

while not done:
    clock.tick(12)
    screen.fill(BLACK)
    #Inisialisasi direction dengan mengambil nilai terbelakang daripada dir_array dan append si snake tersebut ke arah sesuai nilai flag tersebut.
    direction = dir_array.pop(-1)
    if direction == 0:    # down
        snake.append(grid[current.x][current.y + 1])
    elif direction == 1:  # right
        snake.append(grid[current.x + 1][current.y])
    elif direction == 2:  # up
        snake.append(grid[current.x][current.y - 1])
    elif direction == 3:  # left
        snake.append(grid[current.x - 1][current.y])
    current = snake[-1]

    #saat kepala ular menenui makanannya, tambahkan scorenya dan buat food baru dengan posisi acak dan cari path kembali
    if current.x == food.x and current.y == food.y:
        score_it(1)
        while 1:
            food = grid[randint(0, rows - 1)][randint(0, cols - 1)]
            if not (food.obstrucle or food in snake):
                break
        food_array.append(food)
        dir_array = getpath(food, snake)
    else: #jika ular belum bertemu makanan, maka hapus bagian ekor ter-belakang ular
        snake.pop(0)

    #beri warna badan ular dengan warna putih
    for spot in snake:
        spot.show(WHITE)
    #beri warna obstruclenya dengan warna merah
    for i in range(rows):
        for j in range(cols):
            if grid[i][j].obstrucle:
                grid[i][j].show(RED)

    food.show(GREEN) #beri warna makanan dengan warna hijau
    snake[-1].show(BLUE) #beri warna kepala ular dengan warna biru
    draw_score() #menampilkan score
    display.flip()
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == KEYDOWN:
            if event.key==pygame.K_ESCAPE:          
                game_over()
                time.wait(1000)
                done = True
