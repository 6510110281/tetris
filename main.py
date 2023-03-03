from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color
import random


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

        self.r = random.randint(1, 7)
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
            colors = [
                (1, 0, 0),    # red
                (1, 0.5, 0),  # orange
                (1, 1, 0),    # yellow
                (0, 1, 0),    # green
                (0, 1, 1),    # cyan
                (0, 0, 1),    # blue
                (0.5, 0, 1),  # purple
            ]

            color = random.choice(colors)
            Color(*color)
            if self.r == 1:

                shape.append(Shape(4, 20, "I", size=(0, 0)))
                shape.append(Shape(4, 21, "I", size=(0, 0)))
                shape.append(Shape(4, 22, "I", size=(0, 0)))
                shape.append(Shape(4, 23, "I", size=(0, 0)))
            elif self.r == 2:

                shape.append(Shape(4, 20, "O", size=(0, 0)))
                shape.append(Shape(5, 20, "O", size=(0, 0)))
                shape.append(Shape(4, 21, "O", size=(0, 0)))
                shape.append(Shape(5, 21, "O", size=(0, 0)))
            elif self.r == 3:

                shape.append(Shape(4, 20, "L", size=(0, 0)))
                shape.append(Shape(4, 21, "L", size=(0, 0)))
                shape.append(Shape(4, 22, "L", size=(0, 0)))
                shape.append(Shape(5, 20, "L", size=(0, 0)))
            elif self.r == 4:

                shape.append(Shape(4, 20, "J", size=(0, 0)))
                shape.append(Shape(5, 20, "J", size=(0, 0)))
                shape.append(Shape(5, 21, "J", size=(0, 0)))
                shape.append(Shape(5, 22, "J", size=(0, 0)))
            elif self.r == 5:

                shape.append(Shape(4, 20, "Z", size=(0, 0)))
                shape.append(Shape(5, 20, "Z", size=(0, 0)))
                shape.append(Shape(5, 21, "Z", size=(0, 0)))
                shape.append(Shape(6, 21, "Z", size=(0, 0)))
            elif self.r == 6:

                shape.append(Shape(4, 20, "S", size=(0, 0)))
                shape.append(Shape(4, 21, "S", size=(0, 0)))
                shape.append(Shape(5, 21, "S", size=(0, 0)))
                shape.append(Shape(5, 22, "S", size=(0, 0)))
            else:

                shape.append(Shape(4, 20, "E", size=(0, 0)))
                shape.append(Shape(4, 21, "E", size=(0, 0)))
                shape.append(Shape(4, 22, "E", size=(0, 0)))
                shape.append(Shape(5, 21, "E", size=(0, 0)))

        self.shapes.append(shape)

        self.r = random.randint(1, 7)

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

    def collisions_right(self):
        for i in self.shapes[-1]:
            if i.position_x == 9:
                return True
            for j in self.shapes[0:-1]:
                for k in j:
                    if i.position_x + 1 == k.position_x and i.position_y == k.position_y:
                        return True
        return False

    def collisions_left(self):
        for i in self.shapes[-1]:
            if i.position_x == 0:
                return True
            for j in self.shapes[0:-1]:
                for k in j:
                    if i.position_x - 1 == k.position_x and i.position_y == k.position_y:
                        return True
        return False

    def move_right(self):
        if not self.collisions_right():
            for i in self.shapes[-1]:
                i.position_x += 1

    def move_left(self):
        if not self.collisions_left():
            for i in self.shapes[-1]:
                i.position_x -= 1


class Shape(Rectangle):
    position_x = 0
    position_y = 0
    active = True
    brick = ""

    def __init__(self, position_x, position_y, brick, **kwargs):
        super().__init__(**kwargs)

        self.position_x = position_x
        self.position_y = position_y
        self.brick = brick


class App(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'horizontal'

        self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_key_down)
        self._keyboard.bind(on_key_up=self.on_key_up)

        self.tetris = TetrisWidget()
        self.add_widget(self.tetris)

        Clock.schedule_interval(self.update, 1/120)

    def on_key_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == "left":
            self.tetris.move_left()
        if keycode[1] == "right":
            self.tetris.move_right()
        if keycode[1] == "down":
            self.tetris.game_speed = 0.1
        return True

    def on_key_up(self, keyboard, keycode):
        if keycode[1] == "down":
            self.tetris.game_speed = 0.5
        return True

    def keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_key_down)
        self._keyboard.unbind(on_key_up=self.on_key_up)
        self._keyboard = None

    def update(self, dt):
        self.tetris.update_game(self.tetris.width, dt)


if __name__ == "__main__":
    TetrisApp().run()
