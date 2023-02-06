from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

import random

ROWS = 5
COLS = 5


class PlayGameScreen(Screen):
    pass


class LoginScreen(Screen):
    pass


class BombPopup(Popup):
    pass


class Field(Button):
    def __init__(self, **kwargs):
        self.row_id = kwargs.pop("row_id")
        self.col_id = kwargs.pop("col_id")
        super().__init__(**kwargs)

    def on_press(self):
        print(self.row_id, self.col_id)
        print(self.parent.mine[self.row_id][self.col_id])
        self.disabled = True
        if self.parent.mine[self.row_id][self.col_id] == 0:
            self.text = ""
            return

        self.text = "bomb"
        popup = BombPopup()
        popup.open()


class MineLayout(GridLayout):
    rows = ROWS
    cols = COLS

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mine = self.random_bomb(ROWS, COLS, 10)
        self.generate_field()

        print(self.mine)

    def generate_field(self):
        for i in range(ROWS):
            for j in range(COLS):
                self.add_widget(Field(text=f"{i} {j}", row_id=i, col_id=j))

    def random_bomb(self, rows: int, cols: int, bomb_number: int) -> list:

        mine = [[0] * cols for i in range(rows)]

        counter = min(bomb_number, rows * cols)

        while counter > 0:
            r = random.randint(0, rows - 1)
            c = random.randint(0, cols - 1)

            if mine[r][c] == -1:
                continue

            mine[r][c] = -1
            counter -= 1

        return mine


class SimpleMineApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(PlayGameScreen(name="play_game"))
        return self.sm


if __name__ == "__main__":
    SimpleMineApp().run()
