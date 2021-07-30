import pygame
import os
import math
import enemy

TOWER_IMAGE = pygame.image.load(os.path.join("images", "rapid_test.png"))


class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def collide(self, enemy):
        """
        Q2.2)check whether the enemy is in the circle (attack range), if the enemy is in range return True
        :param enemy: Enemy() object
        :return: Bool
        """

        """
        Hint:
        x1, y1 = enemy.get_pos()
        ...
        """
        #回傳bool判斷物件是否在塔範圍內
        x1, y1 = enemy.get_pos()    #取得物件座標
        x_pos,y_pos=self.center     #取得塔座標
        distance=math.sqrt((x1-x_pos)**2+(y1-y_pos)**2) #計算兩個距離
        return True if distance <= self.radius else False





    def draw_transparent(self, win):
        """
        Q1) draw the tower effect range, which is a transparent circle.
        :param win: window surface
        :return: None
        """
        #取得物件座標
        x_pos,y_pos=self.center

        transparent_surface = pygame.Surface((self.radius*2,self.radius*2), pygame.SRCALPHA)
        transparency = 180  # define transparency: 0~255, 0 is fully transparent
        # draw the circle on the transparent surface
        #在transparent_surface上座圓
        pygame.draw.circle(transparent_surface, (128,128,128,transparency), (self.radius,self.radius),self.radius)
        win.blit(transparent_surface, (x_pos-self.radius, y_pos-self.radius))#在win上 blit transparent_surface


class Tower:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(TOWER_IMAGE, (70, 70))  # image of the tower
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # center of the tower
        self.range = 150  # tower attack range
        self.damage = 2   # tower damage
        self.range_circle = Circle(self.rect.center, self.range)  # attack range circle (class Circle())
        self.cd_count = 0  # used in self.is_cool_down()
        self.cd_max_count = 60  # used in self.is_cool_down()
        self.is_selected = True  # the state of whether the tower is selected
        self.type = "tower"

    def is_cool_down(self):
        """
        Q2.1) Return whether the tower is cooling down
        (1) Use a counter to computer whether the tower is cooling down (( self.cd_count
        :return: Bool
        """

        """
        Hint:
        let counter be 0
        if the counter < max counter then
            set counter to counter + 1
        else 
            counter return to zero
        end if
        """
        #判斷frame是否有到max_count，回傳bool
        if self.cd_count <= self.cd_max_count:
            self.cd_count+=1 
            return False
        else:
            self.cd_count=0
            return True


    def attack(self, enemy_group):
        """
        Q2.3) Attack the enemy.
        (1) check the the tower is cool down ((self.is_cool_down()
        (2) if the enemy is in attack range, then enemy get hurt. ((Circle.collide(), enemy.get_hurt()
        :param enemy_group: EnemyGroup()
        :return: None
        """
        #引用is_cool_down函式判斷是否能夠攻擊
        if self.is_cool_down() == True:
            for en in enemy_group.get():#取得串列裡物件的值
                if self.range_circle.collide(en):#判斷是否處在攻擊圈內
                    en.get_hurt(self.damage)#扣血
                    return
        else:
            return
            

    def is_clicked(self, x, y):
        """
        Bonus) Return whether the tower is clicked
        (1) If the mouse position is on the tower image, return True
        :param x: mouse pos x
        :param y: mouse pos y
        :return: Bool
        """
        #用bool判斷是否塔的圖片被點擊
        x_tow,y_tow = self.rect.center
        if (x_tow - self.rect.width<= x <= x_tow +self.rect.width 
        and y_tow - self.rect.height<= y <= y_tow +self.rect.height):
            return True
        return False 

    def get_selected(self, is_selected):
        """
        Bonus) Change the attribute self.is_selected
        :param is_selected: Bool
        :return: None
        """
        
        self.is_selected = is_selected

    def draw(self, win):
        """
        Draw the tower and the range circle
        :param win:
        :return:
        """
        # draw range circle
        if self.is_selected:
            self.range_circle.draw_transparent(win)
        # draw tower
        win.blit(self.image, self.rect)


class TowerGroup:
    def __init__(self):
        self.constructed_tower = [Tower(250, 380), Tower(420, 400), Tower(600, 400)]

    def get(self):
        return self.constructed_tower

