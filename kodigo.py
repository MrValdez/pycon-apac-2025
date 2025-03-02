import arcade
import random

width = 800
height = 600
coin_count = 10


class Game(arcade.Window):
    def __init__(self):
        super().__init__(width, height, "PyCon APAC 2025")
        arcade.set_background_color(arcade.color.AMAZON)

        self.sprites_layer1 = arcade.SpriteList()
        self.sprites_layer2 = arcade.SpriteList()

        img = ":resources:images/animated_characters/female_person/femalePerson_idle.png"
        img = "python.png"
        scale = .5
        self.hero = arcade.Sprite(img, scale)
        self.hero.center_x = width / 2
        self.hero.center_y = height / 2
        self.sprites_layer1.append(self.hero)

        for i in range(coin_count):
            coin = arcade.Sprite(":resources:images/items/coinGold.png")
            coin.center_x = random.randint(0, width)
            coin.center_y = random.randint(0, height)
            self.sprites_layer2.append(coin)

        self.set_mouse_visible(False)

    def on_draw(self):
        self.clear()

        self.sprites_layer2.draw()
        self.sprites_layer1.draw()

    def on_update(self, dt):
        collisions = arcade.check_for_collision_with_list(self.hero, self.sprites_layer2)
        for collision in collisions:
            collision.remove_from_sprite_lists()

    def on_mouse_motion(self, x, y, dx, dy):
        self.hero.center_x = x
        self.hero.center_y = y


game = Game()
arcade.run()
