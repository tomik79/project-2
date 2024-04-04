from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.image import Image
from random import randint
from kivy.core.window import Window


class LoadingScreen(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #self.label = Label(text="", font_size=50, size_hint=(None, None), size=(300, 150), pos=(Window.width / 2 - 150, Window.height / 2 - 75))
        #self.add_widget(self.label)

        # Adding the snake image
        snake_image = Image(source="blue-snake.png", size=(796, 866), size_hint=(None, None), pos=(Window.width / 2 - 398, Window.height / 2 - 550))
        self.add_widget(snake_image)

        #Clock.schedule_once(self.remove_loading_screen, 5)

    def remove_loading_screen(self, dt):
        self.remove_widget(self.label)


class SnakePart(Widget):
    pass


class GameScreen(Widget):
    step_size = 80
    movement_x = 0
    movement_y = 0
    snake_parts = []
    score = 0
    score_label = None

    def new_game(self):
        to_be_removed = []
        for child in self.children:
            if isinstance(child, SnakePart):
                to_be_removed.append(child)
        for child in to_be_removed:
            self.remove_widget(child)

        self.snake_parts = []
        self.movement_x = 0
        self.movement_y = 0
        head = SnakePart()
        head.pos = (0, 0)
        self.snake_parts.append(head)
        self.add_widget(head)

        self.score = 0
        self.update_score()

    def update_score(self):
        if not self.score_label:
            self.score_label = Label(text=f"Score: {self.score}", color='yellow', font_size=50, size_hint=(None, None), size=(150, 50), pos=(40, Window.height - 70))
            self.add_widget(self.score_label)
        else:
            self.score_label.text = f"Score: {self.score}"

    def on_touch_up(self, touch):
        dx = touch.x - touch.opos[0]
        dy = touch.y - touch.opos[1]
        if abs(dx) > abs(dy):
            # Moving left or right
            self.movement_y = 0
            if dx > 0:
                self.movement_x = self.step_size
            else:
                self.movement_x = - self.step_size
        else:
            # Moving up or down
            self.movement_x = 0
            if dy > 0:
                self.movement_y = self.step_size
            else:
                self.movement_y = - self.step_size

    def collides_widget(self, wid1, wid2):
        if wid1.right <= wid2.x:
            return False
        if wid1.x >= wid2.right:
            return False
        if wid1.top <= wid2.y:
            return False
        if wid1.y >= wid2.top:
            return False
        return True

    def next_frame(self, *args):
        # Move the snake
        if not self.snake_parts:
            return  # Return if there are no snake parts
        head = self.snake_parts[0]
        food = self.ids.food
        last_x = self.snake_parts[-1].x
        last_y = self.snake_parts[-1].y

        # Move the body
        for i, part in enumerate(self.snake_parts):
            if i == 0:
                continue
            part.new_y = self.snake_parts[i - 1].y
            part.new_x = self.snake_parts[i - 1].x
        for part in self.snake_parts[1:]:
            part.y = part.new_y
            part.x = part.new_x

        # Move the head
        head.x += self.movement_x
        head.y += self.movement_y

        # Check for snake colliding with food
        if self.collides_widget(head, food):
            food.x = randint(0, Window.width - food.width)
            food.y = randint(0, Window.height - food.height)
            new_part = SnakePart()
            new_part.x = last_x
            new_part.y = last_y
            self.snake_parts.append(new_part)
            self.add_widget(new_part)
            self.score += 1
            self.update_score()

        # Check for snake colliding with snake
        for part in self.snake_parts[1:]:
            if self.collides_widget(part, head):
                self.new_game()

        # Check for snake colliding with wall
        if not self.collides_widget(self, head):
            self.new_game()


class MainApp(App):
    def on_start(self):
        loading_screen = LoadingScreen()
        self.root.add_widget(loading_screen)
        Clock.schedule_once(self.start_game, 5)

    def start_game(self, dt):
        self.root.remove_widget(self.root.children[0])
        self.root.new_game()
        Clock.schedule_interval(self.root.next_frame, .25)


MainApp().run()
