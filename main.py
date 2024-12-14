import pygame
import random
pygame.init()

#display screen
W=1150
H=650
win=pygame.display.set_mode((W,H)) 
pygame.display.set_caption("FRUIT CATCHER") 

#fonts to display the text
FONT = pygame.font.Font(None, 47)

# loading of images

bg=pygame.image.load('pics\\bback.jpg') 
bgm= pygame.image.load('pics\\FBG.jpg')
bgf= pygame.image.load('pics\\fin.jpg') 
basket = pygame.image.load("pics\\fruit.png")
basket= pygame.transform.scale(basket, (120, 120))
bomb= pygame.image.load("pics\\bomb.png")
bomb= pygame.transform.scale(bomb, (85, 85))
fruits = {
    "apple": pygame.image.load("pics\\apple (1).png"),
    "banana": pygame.image.load("pics\\banana (1).png"),
    "strawberry": pygame.image.load("pics\\strawberry (1).png"),
}
for i in fruits:
    fruits[i] = pygame.transform.scale(fruits[i], (85, 85))

#basket details
x = W // 2 # dividing window into 2 part placing basket at center
y = H - 120 #basket is 120 px from bottom of screen
bas_speed = 7# speed of basket 

# Clock
clock = pygame.time.Clock()
FPS = 60

#empty basket 
empty = [] 
fru_speed = 3


#score details
score = 0
timer = 60 
target = "apple"
high_score = 0

def display_text(text, color, x, y):
    label = FONT.render(text, True, color)
    win.blit(label, (x, y)) # used to display rendered text or an image

#reseting of game
def reset():
    global empty, score, timer, fr_speed
    empty = []
    score = 0
    timer = 60
    fr_speed = 3

#to create a new fruit or bomb to fall from top of screen
def new_fruit():
    new = random.choice(["fruit", "bomb"])
    if new == "fruit":
        fruit_type = random.choice(list(fruits.keys()))#loop of fruits only keys are called here 
        #Converts the dictionary keys into a list, to make random.choice() function to work on it.
        return {
            "type": "fruit",
            "fruit": fruit_type,
            "img": fruits[fruit_type],
            "x": random.randint(0, W - 40),
            "y": -40, #the fruit starts "falling" from above.
        }
    else:
        return {
            "type": "bomb",
            "img": bomb,
            "x": random.randint(0, W - 40),
            "y": -40,
        }
        
def info():
    global high_score
    run = True
    while run:
        win.blit(bg,(0,0))
        display_text("Fruit Catcher", (0, 45, 20), W // 2 - 100, H // 2 - 50)#blue
        display_text("Press SPACE to Start", (75, 175, 10), W // 2 - 150, H // 2)#green
        display_text(f"High Score: {high_score}", (255, 0, 0), W // 2 - 100, H // 2 + 50)#red

        for event in pygame.event.get():
            if event.type == pygame.QUIT:# checks whether user closes the game window 
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # Checks if the pressed key is the Spacebar
                run = False

        pygame.display.flip()# Makes all rendering updates visible on the screen.
        clock.tick(FPS)# Limits the frame rate



def game(level):
    global x, score, timer, fr_speed, high_score
    
    x = W // 2 #basket position
    if level == 1 :
        fr_speed = 3
    else:
        fr_speed = 5

    ticking = pygame.time.get_ticks()
    run = True

    while run:
        win.blit(bgm,(0,0))
        
        #display of level 
        display_text(f"LEVEL: {level}", (0,0,0), W // 2 - 50, 10) #black

        # display of timer 
        seconds = (pygame.time.get_ticks() - ticking) // 1000
        timer = 60 - seconds
        if timer <= 0:
            break

        # creating fruits to fall down 
        if random.randint(1, 30) == 1:
            empty.append(new_fruit())

        # event to quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
        # movement of basket
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            x -= bas_speed  
            
        if keys[pygame.K_RIGHT]:
            x += bas_speed  

        # to keep basket within bounds
        
        x = max(0, min(W - 100, x))

        # Update objects
        for obj in empty[:]:
            obj["y"] += fr_speed #move the fruits vertically down

            # Collision detection
            if (
                x < obj["x"] + 40
                and x + 100 > obj["x"]
                and y < obj["y"] + 40
                and y + 50 > obj["y"]
            ):
                if obj["type"] == "fruit":
                    if level == 1 and obj.get("fruit") == target:
                        score += 10
                    else:
                        score += 5
                elif obj["type"] == "bomb":
                    score -= 5 if level == 1 else 10
                empty.remove(obj)
                
                # Checks if the object has fallen off the screen 
            if obj["y"] > H:
                empty.remove(obj)

        # Draw objects
        for obj in empty:
            win.blit(obj["img"], (obj["x"], obj["y"]))

        # Draw basket
        win.blit(basket, (x,y))

        # Display score and timer
        display_text(f"Score: {score}", (0,0,0), 10, 40)
        display_text(f"Time: {timer}s", (0,0,0), W - 150, 40)

        pygame.display.flip()
        clock.tick(FPS)

    if score > high_score:
        high_score = score
        
def score_screen():
    global score
    run = True
    while run:
        win.blit(bgf,(0,0))
        display_text("Game Over", (255, 0, 0), W // 2 - 70, H // 2 - 50)
        display_text(f"Your Score: {score}", (0, 45, 20), W // 2 - 100, H // 2)
        display_text(f"High Score: {high_score}", (0, 0 ,145), W // 2 - 100, H // 2 + 50)
        display_text("Press R to Restart or Q to Quit", (0, 0, 0), W // 2 - 200, H // 2 + 100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset()
                    return
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

        pygame.display.flip()
        clock.tick(FPS)

# Game flow
while True:
    info()
    game(1)  # Level 1
    game(2)  # Level 2
    score_screen()
