import pygame, random
from math import sqrt
from numpy import array

pygame.init()

screen = pygame.display.set_mode((640, 480))

class Circle(pygame.sprite.Sprite):
    def __init__(self,r,c):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((2*r, 2*r))
        self.image.set_colorkey((255, 255, 255))
        self.image.fill((255, 255, 255,0))
        pygame.draw.circle(self.image, c, (r, r), r, 0)

        self.rect = self.image.get_rect()
        self.r = r

class Tree(Circle):
    def __init__(self, r):
        Circle.__init__(self, r,(30, 150, 0))

class Mower(Circle):
    def __init__(self,r):
        Circle.__init__(self,r,(0, 0, 255))

        self.dx = 0.5
        self.dy = 0.7

        self.x = self.r
        self.y = self.r


    def update(self):
        trail = 3*self.r//4
        #pygame.draw.circle(screen, (0, 220, 0), (self.rect.x+self.r, self.rect.y+self.r), self.r)

        self.x += self.dx
        self.y += self.dy

        self.rect.center = (self.x,self.y)
        #self.rect.move_ip(self.dx, self.dy)
        #self.rect.move_ip(self.dx, self.dy)

        if self.rect.x < 0 or self.rect.x + 2*self.r > 640:
            self.dx *= -1
        if self.rect.y < 0 or self.rect.y + 2*self.r > 480:
            self.dy *= -1

    def turn(self,direction=None):
        if direction is not None:
            self.dx = direction[0]
            self.dy = direction[1]
        else:
            self.dx = random.uniform(1, 3)*random.randrange(-1, 2, 2)
            self.dy = random.uniform(1, 3)*random.randrange(-1, 2, 2)

        norm = sqrt(self.dx*self.dx + self.dy*self.dy)
        self.dx = self.dx/norm
        self.dy = self.dy/norm

def main():
    pygame.display.set_caption("iMow")

    background = pygame.Surface(screen.get_size())
    background.fill((240, 240, 240))
    screen.blit(background, (0, 0))

    allSprites = pygame.sprite.Group()
    trees = pygame.sprite.Group()

    mower = Mower(10)
    allSprites.add(mower)

    TREEWIDTH = 15


    for i in range(15):
        x = random.uniform(TREEWIDTH, 640-TREEWIDTH)
        y = random.uniform(TREEWIDTH, 480-TREEWIDTH)
        tree = Tree(TREEWIDTH)

        tree.rect.x = x
        tree.rect.y = y

        allSprites.add(tree)
        trees.add(tree)

    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        #clock.tick(50) # lze odkomentovat a snizit rychlost sekacky nastavenim parametru
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

        for block in trees:
            hitList = pygame.sprite.collide_mask(mower, block)
            if hitList:
                away = array([mower.rect.x-block.rect.x,mower.rect.y-block.rect.y])
                perpen = array([away[1],-away[0]])
                alpha = random.uniform(0, 1)

                direct = alpha*away + (1-alpha)*random.randrange(-1, 2, 2)*perpen
                mower.turn(direct)

        pygame.draw.circle(screen, (0, 220, 0), (mower.rect.x + 10, mower.rect.y + 10), 10)

        allSprites.update()
        allSprites.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()