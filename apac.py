# https://api.arcade.academy/en/latest/example_code/sprite_tiled_map.html

import arcade
from arcade.types import Color

width = 1280
height = 720

scale = 0.2
tile_scaling = 0.5
pixel_size = 128
grid_pixel_size = pixel_size * tile_scaling

player_speed = 5
gravity = 1
player_jump_speed = 20

camera_follow_decay = 0.3  # get within 1% of the target position within 2 seconds


class Player(arcade.Sprite):
    def __init__(self, texture, scale):
        self.right_texture = arcade.load_texture(texture)
        self.left_texture = self.right_texture.flip_left_right()

        super().__init__(self.right_texture, scale)

        self.textures.append(self.left_texture)

    def update(self, delta_time = 1/60):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.change_x < 0:
            self.texture = self.textures[1]
        elif self.change_x > 0:
            self.texture = self.textures[0]


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.camera_sprites = arcade.camera.Camera2D()
        self.camera_bounds = self.window.rect
        self.camera_gui = arcade.camera.Camera2D()

        self.scene = self.create_scene()

        self.player_sprite = Player(
            "assets/luchador.png",
            scale
        )

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=gravity, walls=self.scene["Platforms"]
        )

        self.left_key_down = False
        self.right_key_down = False

        self.victory_display = arcade.Text(
            "",
            x=30,
            y=600,
            color=arcade.csscolor.BLACK,
            font_size=50,
        )

        self.reset()

    def create_scene(self) -> arcade.Scene:
        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            },
        }
        tile_map = arcade.load_tilemap(
            "pycon-stage.json",
            scaling=tile_scaling,
            layer_options=layer_options,
        )

        if tile_map.background_color:
            self.window.background_color = Color.from_iterable(tile_map.background_color)

        self.camera_bounds = arcade.LRBT(
            self.window.width / 2.0,
            tile_map.width * grid_pixel_size - self.window.width / 2.0,
            self.window.height / 2.0,
            tile_map.height * grid_pixel_size
        )

        return arcade.Scene.from_tilemap(tile_map)

    def reset(self):
        self.victory = False
        self.scene = self.create_scene()

        self.player_sprite.position = (128, 128)
        self.scene.add_sprite("Player", self.player_sprite)

    def on_draw(self):
        self.clear()

        with self.camera_sprites.activate():
            # Note, if you a want pixelated look, add pixelated=True to the parameters
            self.scene.draw()

        with self.camera_gui.activate():
            if self.victory:
                self.victory_display.text = f"WINNER WINNER\nCHICKEN DINNER"
                self.victory_display.draw()

    def update_player_speed(self):
        self.player_sprite.change_x = 0

        if self.left_key_down and not self.right_key_down:
            self.player_sprite.change_x = -player_speed
        elif self.right_key_down and not self.left_key_down:
            self.player_sprite.change_x = player_speed

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = player_jump_speed
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_key_down = True
            self.update_player_speed()
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_key_down = True
            self.update_player_speed()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_key_down = False
            self.update_player_speed()
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_key_down = False
            self.update_player_speed()

    def center_camera_to_player(self):
        self.camera_sprites.position = arcade.math.smerp_2d(
            self.camera_sprites.position,
            self.player_sprite.position,
            self.window.delta_time,
            camera_follow_decay,
        )

        self.camera_sprites.view_data.position = arcade.camera.grips.constrain_xy(
            self.camera_sprites.view_data, self.camera_bounds
        )

    def on_update(self, delta_time: float):
        self.player_sprite.update()
        self.physics_engine.update()
        self.center_camera_to_player()

        exit_hit = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Exit"]
        )

        if exit_hit:
            self.victory = True

    def __on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self.camera_sprites.match_window()
        self.camera_gui.match_window(position=True)


def main():
    window = arcade.Window(width, height, "PyCon APAC 2025")
    game = GameView()

    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()
