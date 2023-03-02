from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout


class TetrisApp(App):
    pass


class GridButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.background_color = (0.25, 0.25, 0.25, 1)
        self.disabled = True
        self.background_disabled_normal = ""


class TetrisWidget(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        for box in range(200):
            obj = GridButton()
            self.add_widget(obj)


class App(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'horizontal'

        self.tetris = TetrisWidget()
        self.add_widget(self.tetris)


if __name__ == "__main__":
    TetrisApp().run()
