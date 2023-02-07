from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

import random


class PlayGameScreen(Screen):
    def __init__(self, **kwargs):
        self.settings = kwargs.pop("settings")
        super().__init__(**kwargs)

    def on_pre_enter(self):
        self.mine_layout_box = self.ids["mine_layout"]
        self.add_widget(
            MineLayout(
                rows=self.settings["rows"],
                cols=self.settings["cols"],
                settings=self.settings,
            )
        )


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        self.settings = kwargs.pop("settings")
        super().__init__(**kwargs)

    def select_size(self, rows, cols, bomb_number):
        print("select size", rows, cols)
        self.settings["cols"] = cols
        self.settings["rows"] = rows
        self.settings["bomb_number"] = bomb_number

        self.manager.current = "play_game"


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
            self.parent.settings["right_click_count"] += 1
            print(self.parent.parent)
            self.parent.parent.ids["score_number"].text = str(
                self.parent.settings["right_click_count"]
            )
            return

        self.text = "bomb"
        self.source = "images/bomb.png"
        # popup = BombPopup()
        # popup.open()


class MineLayout(GridLayout):
    def __init__(self, **kwargs):
        self.settings = kwargs.pop("settings")
        super().__init__(**kwargs)
        self.mine = self.random_bomb(
            self.settings["rows"], self.settings["cols"], self.settings["bomb_number"]
        )
        self.generate_field(self.settings["rows"], self.settings["cols"])

        print(self.mine)

    def generate_field(self, rows, cols):
        for i in range(rows):
            for j in range(cols):
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
        self.settings = dict(rows=8, cols=8, bomb_number=5, right_click_count=0)
        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name="login", settings=self.settings))
        self.sm.add_widget(PlayGameScreen(name="play_game", settings=self.settings))
        return self.sm


if __name__ == "__main__":
    SimpleMineApp().run()
