import arcade
import PIL


class SpriteCache:
    _sprites: dict[str, list[arcade.Texture]] = {}

    @staticmethod
    def load_spritesheet(
        file_path: str,
        sprite_width: int,
        sprite_height: int,
        columns: int,
        count: int,
        flip: bool = False,
    ) -> list[arcade.Texture]:
        textures = arcade.load_spritesheet(
            file_name=file_path,
            sprite_width=sprite_width,
            sprite_height=sprite_height,
            columns=columns,
            count=count,
        )

        if flip:
            file_path = f"{file_path}_flipped"
            textures = [
                arcade.Texture(
                    f"{texture.name}_flipped",
                    image=texture.image.transpose(PIL.Image.FLIP_LEFT_RIGHT),
                )
                for texture in textures
            ]

        SpriteCache._sprites[file_path] = textures
        return textures

    @staticmethod
    def get_sprite(file_path: str, flip: bool = False) -> list[arcade.Texture]:
        if flip:
            file_path += "_flipped"

        return SpriteCache._sprites[file_path]
