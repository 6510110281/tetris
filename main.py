from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.graphics.vertex_instructions import Rectangle


class TetrisApp(App):
    pass


class GridButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.background_color = (0.25, 0.25, 0.25, 1)
        self.disabled = True
        self.background_disabled_normal = ""


class TetrisWidget(GridLayout):
    shapes = []
    game_speed = 0.5
    time = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        for box in range(200):
            obj = GridButton()
            self.add_widget(obj)

        self.new_shape()

    def update_game(self, window_width, dt):
        self.fall(dt)
        self.size_change(window_width)
        self.collisions_bottom()

    def fall(self, dt):
        self.time += dt
        if self.time >= self.game_speed:
            self.time = 0
            for i in self.shapes[-1]:
                i.position_y -= 1

    def size_change(self, window_width):
        self.unit = window_width / 10
        for i in self.shapes:
            for j in i:
                j.pos = (j.position_x * self.unit, j.position_y * self.unit)
                j.size = (self.unit, self.unit)

    def new_shape(self):
        shape = []
        with self.canvas:
            shape.append(Shape(4, 20, size=(0, 0)))
        self.shapes.append(shape)

    def collisions_bottom(self):
        for i in self.shapes[0:-1]:
            for j in i:
                for k in self.shapes[-1]:
                    if j.position_y + 1 == k.position_y and j.position_x == k.position_x:
                        for j in self.shapes[-1]:
                            j.active = False
        for i in self.shapes[-1]:
            if i.active == True:                        
                if i.position_y == 0:
                    for j in self.shapes[-1]:
                        j.active = False                 
            else:
                self.new_shape()
                return True             

class Shape(Rectangle):
    position_x = 0
    position_y = 0
    active = True

    def __init__(self, position_x, position_y, **kwargs):
        super().__init__(**kwargs)
        self.position_x = position_x
        self.position_y = position_y


class App(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'horizontal'

        self.tetris = TetrisWidget()
        self.add_widget(self.tetris)

        Clock.schedule_interval(self.update, 1/120)

    def update(self, dt):
        self.tetris.update_game(self.tetris.width, dt)


if __name__ == "__main__":
    TetrisApp().run()
