import pygame as p
import Text as t

class FancyClickButton(p.sprite.Sprite):
    super.__init__()
    def __init__(self,Pos:tuple,Images:tuple):
        self.images = Images
        self.rect = Images[0].get_rect()
        if len(Pos) != 2:
            raise ValueError("This Is NOT a 3D Game")
        if len(Images) != 2:
            raise ValueError("Too many images")
        self.rect.center = Pos
        self.state = 0

    def update(self,Mpos:tuple,**MouseButtonStatus): 
        if self.rect.collidepoint(Mpos[0],Mpos[1]):
            for ButtonName,ButtonState in MouseButtonStatus.items:
                if ButtonState:
                    if ButtonName == "left":
                        return True
                    else:
                        raise ValueError("This Mouse Button isn't supported by the package")
        self.image = self.images[self.state]


class FancyToggleButton(p.sprite.Sprite):
    super.__init__()
    def __init__(self,Pos:tuple,Images:tuple):
        self.statescount = len(Images)
        self.images = Images
        self.rect = Images[0].get_rect()
        if len(Pos) != 2:
            raise ValueError("This Is NOT a 3D Game")
        self.rect.center = Pos
        self.state = 0

    def update(self,Mpos:tuple,**MouseButtonStatus): 
        if self.rect.collidepoint(Mpos[0],Mpos[1]):
            for ButtonName,ButtonState in MouseButtonStatus.items:
                if ButtonState:
                    if ButtonName == "left":
                        self.next_state()
                    if ButtonName == "right":
                        self.previous_state()
                    else:
                        raise ValueError("This Mouse Button isn't supported by the package")
        self.image = self.images[self.state]

    def next_state(self):
        if self.state == self.statescount - 1:
            self.state = 0
        else:
            self.state+=1

    def previous_state(self):
        if self.state == 1:
            self.state = self.statescount - 1
        else:
            self.state -= 1
