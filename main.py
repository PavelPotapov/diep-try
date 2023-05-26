import play
from random import randint


objects = []
for e in range(5120):
    r=randint(3,7)
    dot = play.new_circle(color='black', x=randint(-10000, 10000), y=randint(-10000, 10000), radius=r, border_color=play.random_color(),border_width=r, transparency=100)
    objects.append(dot)

class Player():
    def __init__(self, x, y, radius, color='black', border_color=play.random_color(), border_width=10, transparency=100, speed=1):
        self.barrel = play.new_box( color='gray', x=x, y=y, width=50, height=150, border_color="light blue", border_width=1)
        self.circle = play.new_circle(color=color, x=x, y=y, radius=radius, border_color=border_color,border_width=border_width, transparency=transparency)
        self.speed = speed
        self.prad = self.circle.radius
        self.bullets = []
    def move(self):
        self.barrel.point_towards(play.mouse)
        self.barrel.angle += 90
        self.barrel.height = self.prad + 100

        if play.key_is_pressed('up', 'w'):
            for obj in objects:
                obj.y -= 5
            for enemy in enemies:
                enemy.circle.y -= 5
                enemy.y1 -=5
            for bullet in self.bullets:
                bullet.y -= 5
        if play.key_is_pressed('down', 's'):
            for obj in objects:
                obj.y += 5
            for enemy in enemies:
                enemy.circle.y += 5
                enemy.y1 +=5
            for bullet in self.bullets:
                bullet.y += 5
        if play.key_is_pressed('left', 'a'):
            for obj in objects:
                obj.x += 5
            for enemy in enemies:
                enemy.circle.x += 5
                enemy.x1 +=5
            for bullet in self.bullets:
                bullet.x += 5
        if play.key_is_pressed('left', 'd'):
            for obj in objects:
                obj.x -= 5
            for enemy in enemies:
                enemy.circle.x -= 5
                enemy.x1 -=5
            for bullet in self.bullets:
                bullet.x -= 5
        #кушаю еду
        for obj in objects:
            if self.circle.is_touching(obj):
                if obj.radius < self.circle.radius:
                    self.prad+=obj.radius / (self.circle.radius ** (1./2.)) / 5
                    self.circle.radius = int(self.prad)
                    obj.hide()
                    objects.remove(obj)

        #кушаю врагов
        for enemy in enemies:
            if self.circle.is_touching(enemy.circle):
                if enemy.circle.radius < self.circle.radius:
                    self.prad+=enemy.circle.radius / (self.circle.radius ** (1./2.)) / 5
                    self.circle.radius = int(self.prad)
                    enemy.circle.hide()
                    enemies.remove(enemy)

    def fire(self):
        ball = play.new_circle(color='black', x=self.circle.x, y=self.circle.y,  radius=20, border_color="light blue", border_width=1, transparency=100)
        ball2 = play.new_circle(color='black', x=self.circle.x, y=self.circle.y,  radius=20, border_color="light blue", border_width=1, transparency=100)
        ball.point_towards(play.mouse)
        ball2.point_towards(play.mouse)
        ball2.angle += 180
        self.bullets.append(ball)
        self.bullets.append(ball2)
class Enemy():
    def __init__(self, x, y, radius, color='black', border_color=play.random_color(), border_width=10, transparency=100, speed=1):
        self.circle = play.new_circle(color=color, x=x, y=y, radius=radius, border_color=border_color,border_width=border_width, transparency=transparency)
        self.is_move = False
        self.x1 = 0
        self.y1 = 0
        self.speed = speed
        self.prad = self.circle.radius
        self.health = randint(3,5)
    
    def move(self):
        if not self.is_move:
            self.x1 = randint(-10000,10000)
            self.y1 = randint(-10000,10000)
            print('Новая точка:', self.x1, self.y1)
            self.circle.point_towards(self.x1, self.y1)
            self.is_move = True
        else:
            self.circle.move(self.speed)
            if self.circle.distance_to(self.x1, self.y1) <= 10:
                self.is_move = False

        for obj in objects:
            if self.circle.is_touching(obj):
                if obj.radius < self.circle.radius:
                    self.prad += obj.radius / (self.circle.radius ** (1./2.)) / 5
                    self.circle.radius = int(self.prad)
                    obj.hide()
                    objects.remove(obj)

        #кушают героя
        if self.circle.is_touching(player.circle):
            if player.circle.radius < self.circle.radius:
                self.prad+=player.circle.radius / (self.circle.radius ** (1./2.)) / 5
                self.circle.radius = int(self.prad)
                player.circle.hide()
                print('СЪЕЛИ ГЛАВНОГО ГЕРОЯ')

        #кушаю врагов
        for enemy in enemies:
            if enemy != self:
                if self.circle.is_touching(enemy.circle):
                    if enemy.circle.radius < self.circle.radius:
                        self.prad+=enemy.circle.radius / (self.circle.radius ** (1./2.)) / 5
                        self.circle.radius = int(self.prad)
                        enemy.circle.hide()
                        enemies.remove(enemy)

enemy1 = Enemy(color='black', x=200, y=0, radius=randint(30,70), border_color=play.random_color(),border_width=10, transparency=100, speed=5)
enemy2 = Enemy(color='black', x=200, y=200, radius=randint(30,70), border_color=play.random_color(),border_width=10, transparency=100, speed=5)
enemy3 = Enemy(color='black', x=200, y=-200, radius=randint(30,70), border_color=play.random_color(),border_width=10, transparency=100, speed=5)
enemies = [enemy1, enemy2, enemy3]

player = Player(color='black', x=0, y=0, radius=50, border_color=play.random_color(),border_width=10, transparency=100)

@play.repeat_forever
def do():
    for enemy in enemies:
        enemy.move()
    player.move()
    for bullet in player.bullets:
        bullet.move(10)
        for enemy in enemies:
            if bullet.is_touching(enemy.circle):
                print('КАСАЕТСЯ')
                enemy.health -= 1
                if enemy.health <= 0:
                    enemy.circle.hide()
                    enemies.remove(enemy)
                    enemy.circle.remove()
                bullet.hide()
                player.bullets.remove(bullet)
                bullet.remove()

@play.repeat_forever
async def do2():
    if play.mouse.is_clicked:
        player.fire()
        await play.timer(seconds=1)
       
@play.repeat_forever
async def do3():
    if len(player.bullets) > 0:
        await play.timer(seconds=3)
        try:
            player.bullets[0].hide()
            player.bullets.remove(player.bullets[0])
            player.bullets[0].remove()
        except:
            pass

play.start_program()