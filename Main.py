# Zombie Pew
# By Neslie Fernandez

# This program contains sprites. 

# Module that allows you to make games
import pygame

# initialize pygame
pygame.init()

# Create a window
win = pygame.display.set_mode((800,480))

pygame.display.set_caption("Zombie Pew")

# Code to load images

# Code for walking right and left
walkRight = [pygame.image.load('Player/0.png'), pygame.image.load('Player/1.png'), pygame.image.load('Player/2.png'), pygame.image.load('Player/3.png'), pygame.image.load('Player/4.png'), pygame.image.load('Player/5.png'), pygame.image.load('Player/6.png'), pygame.image.load('Player/7.png'), pygame.image.load('Player/8.png')]
walkLeft = [pygame.image.load('Player/10.png'), pygame.image.load('Player/11.png'), pygame.image.load('Player/12.png'), pygame.image.load('Player/13.png'), pygame.image.load('Player/14.png'), pygame.image.load('Player/15.png'), pygame.image.load('Player/16.png'), pygame.image.load('Player/17.png'), pygame.image.load('Player/18.png')]
fireRight = [pygame.image.load('Player/FireRight.png')]
fireLeft = [pygame.image.load('Player/FireLeft.png')]

'''
Optimal Solution 

walkRight = [pygame.image.load('Player/%s.png' % frame) for frame in range(1, 10)]
walkLeft = [pygame.image.load('Player/%s.png' % frame) for frame in range(10, 18)]

'''

bg = pygame.image.load('Background/background.jpg')
char = pygame.image.load('Player/standing.png')

clock = pygame.time.Clock()


score = 0

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = True
        self.right = False
        self.walkCount = 0
        # tracks character standing
        self.standing = True

        # hitbox
        # x,y,width, height
        self.hitbox = (self.x - 4, self.y, 36, 50)
        self.health = 10
        self.visible = True


    def draw(self,win):
        # Draw image
        if self.walkCount + 1 >= 27:
            self.walkCount = 0


        # See whether he is standing still or moving
        if not(self.standing):
            if self.left:
                # integer divided by 3 so it takes out decimals
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
        # if we are not moving right or left we are standing still
        else:
            ''' # character looking front
            win.blit(char, [self.x,self.y])
            '''
            # If he is standing still he is either looking to the right or left
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))



        # Everytime we draw the character we move the hit box with it
        self.hitbox = (self.x - 4, self.y, 36, 50)
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)
                
class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

        


class enemy(object):

    '''
    walkLeft = [pygame.image.load('Enemy/0.png'), pygame.image.load('Enemy/1.png'), pygame.image.load('Enemy/2.png'), pygame.image.load('Enemy/3.png'), pygame.image.load('Enemy/4.png'), pygame.image.load('Enemy/5.png'), pygame.image.load('Enemy/6.png'), pygame.image.load('Enemy/7.png'), pygame.image.load('Enemy/8.png')]
    walkRight = [pygame.image.load('Enemy/10.png'), pygame.image.load('Enemy/11.png'), pygame.image.load('Enemy/12.png'), pygame.image.load('Enemy/13.png'), pygame.image.load('Enemy/14.png'), pygame.image.load('Enemy/15.png'), pygame.image.load('Enemy/16.png'), pygame.image.load('Enemy/17.png'), pygame.image.load('Enemy/18.png')]
    '''

    # Optimize version to load images
    walkLeft = [pygame.image.load('Enemy/L%s.png' % frame) for frame in range(0,12)]
    walkRight = [pygame.image.load('Enemy/R%s.png' % frame) for frame in range(0,12)]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end] # Where we start and Where we end
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x - 4, self.y, 36, 50)
        self.health = 10
        self.visible  = True
        
    def draw(self, win):
        # everytime we draw we move 
        self.move()
        # if character is visible we draw him on the screen
        # along with his hitbox
        if self.visible:
            # Greater than so enemy moves
            if self.walkCount + 1 >= 33:
                self.walkCount = 0
            # Check whether they are moving left or right
            # If it's greater than 0 we are moving right
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            # Else if we are not moving right we are moving left
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1


            # Draw healthbar
            pygame.draw.rect(win,(255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            # health bar, 10 hits 
            pygame.draw.rect(win,(0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))

            # move the hitbox along with the enemy
            self.hitbox = (self.x - 4, self.y, 36, 50)
            #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
                

    # Enemy will move in one dimension
    # We only be moving x values
    def move(self):
        if self.vel > 0: # moving right
            # If the character is less than the end
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            # switch directions
            else:
                # changing it to -1 to flip it 180 degrees
                self.vel = self.vel * -1
                self.walkCount = 0
        # If our velocity is negative, which is not greater than 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

                
    # Collision
    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print("Hit")
        

# Game window, this is where we update the screen
def redrawGameWindow():
    # We will fill the screen with the background image
    win.blit(bg, (0,0))

    # To show the score
    text = font.render('Score: ' + str(score), 1, (0,0,0))
    # Top right corner
    win.blit(text, (390,10))
    man.draw(win)
    # We draw the enemy 
    bad.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    
    # To show something
    pygame.display.update()


# font type, size, bold, italic
font = pygame.font.SysFont('comicsans', 30, True, True)


# create instance of our character
man = player(300, 410, 64, 64)

# Create instance of enemy
# We end at 450 path
bad = enemy(100, 410, 64, 64, 450)
# Create bullets list
bullets = []

shootLoop = 0

# Main loop
run = True
while run:

    # 27 FPS in game
    clock.tick(27)


    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0
    
    # Check for events from user
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    for bullet in bullets:
        # check if bullets are in same y coordinate
        # If we are above the bottom of our rectangle and below the top layer
        if bullet.y - bullet.radius < bad.hitbox[1] + bad.hitbox[3] and bullet.y + bullet.radius > bad.hitbox[1]:
            # Check left side and right side
            if bullet.x + bullet.radius > bad.hitbox[0] and bullet.x - bullet.radius < bad.hitbox[0] + bad.hitbox[2]:
                bad.hit()
                # When we hit the goblin we increment score
                score += 1
                bullets.pop(bullets.index(bullet))
                
        # if bullet.x is not going out of the screen
        if bullet.x < 500 and bullet.x > 0:
            # this means our bullet moves to the direction we set to
            bullet.x += bullet.vel
        else:
            # if it's not greater than 500 or less than 0
            bullets.remove(bullet)
            

    # To move the rectangle
    # Check if the key is press
    # If you hold down a key it should continue moving character
    keys = pygame.key.get_pressed()

    # User can shoot a bullet if bullet cool down is max
    if keys[pygame.K_SPACE] and shootLoop == 0:
        if man.left:
            # if we are looking left our bullet is moving left negative direction
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            # create a new bullet object
            # round so we don't mess up the number
            bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height //2), 6, (250,0,0), facing))

        shootLoop = 1
            
    # to prevent going out of boundaries we add an and
    # it's greater than 5
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False

    # x is less than the screen
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        ''' # We remove this because we won't see which way he is looking
        man.right = False
        man.left = False
        '''
        # this way we know if he is looking right or left
        man.standing = True
        man.walkCount = 0
        

    if not(man.isJump):
              # Our jump key
        if keys[pygame.K_UP]:
            man.isJump = True
            man.walkCount = 0

    else:
        if man.jumpCount >= -10:
            neg = 1
            # If we are in negative side we set neg to -1
            if man.jumpCount < 0:
                neg = -1
            # We also multiple all these to -1 to go downwards
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
                
    # draw Game Window function
    redrawGameWindow()
    
# ends and closes windows for us
pygame.quit()
    

