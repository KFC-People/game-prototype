import arcade


class Robot(arcade.Sprite):
    def __init__(self):
        super().__init__()

        main_path = ":resources:images/animated_characters/robot/robot"

        self.idle_texture = arcade.load_texture(f"{main_path}_idle.png")
        self.jump_texture = arcade.load_texture(f"{main_path}_jump.png")
        self.fall_texture = arcade.load_texture(f"{main_path}_fall.png")

        self.walk_textures = []

        for i in range(8):
            texture = arcade.load_texture(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

        self.texture = self.idle_texture
        self.current_texture_index = 0

    def update_animation(self, *_):
        if self.change_y > 0:
            self.texture = self.jump_texture
            return

        if self.change_y < 0:
            self.texture = self.fall_texture
            return

        if self.change_x == 0:
            self.texture = self.idle_texture
            return

        self.current_texture_index += 1
        self.current_texture_index %= len(self.walk_textures)

        self.texture = self.walk_textures[self.current_texture_index]
