from PIL import Image, ImageDraw, ImageFont
from dataclasses import dataclass
import base64
from io import BytesIO


@dataclass(frozen=True)
class Padding:
    x: int
    y: int


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int


class Map:
    PADDING = Padding(x=120, y=120)
    RECT_WIDTH = 170
    RECT_HEIGHT = 100
    GRID_GAP = 30
    FILL_COLOR = "#ffffff"
    TEXT_COLOR = "#000000"
    BASE_IMAGE_PATH = "./map.png"

    def __init__(self, north, south, east, west, central):
        self.data_values = {
            'north': north,
            'south': south,
            'east': east,
            'west': west,
            'central': central
        }

    @staticmethod
    def font(font_size):
        return ImageFont.truetype("arial.ttf", font_size)

    def generate_bounding_boxes(self):
        with Image.open(self.BASE_IMAGE_PATH) as im:
            map_width, map_height = im.size
        north_box_1 = Coordinate(map_width / 2 - self.RECT_WIDTH / 2, self.PADDING.y)
        north_box_2 = Coordinate(north_box_1.x + self.RECT_WIDTH, north_box_1.y + self.RECT_HEIGHT)

        central_box_1 = Coordinate(north_box_1.x, north_box_2.y + self.GRID_GAP)
        central_box_2 = Coordinate(central_box_1.x + self.RECT_WIDTH, central_box_1.y + self.RECT_HEIGHT)

        south_box_1 = Coordinate(central_box_1.x, central_box_2.y + self.GRID_GAP)
        south_box_2 = Coordinate(south_box_1.x + self.RECT_WIDTH, south_box_1.y + self.RECT_HEIGHT)

        west_box_1 = Coordinate(north_box_1.x - self.GRID_GAP - self.RECT_WIDTH, central_box_1.y)
        west_box_2 = Coordinate(west_box_1.x + self.RECT_WIDTH, west_box_1.y + self.RECT_HEIGHT)

        east_box_1 = Coordinate(north_box_2.x + self.GRID_GAP, central_box_1.y)
        east_box_2 = Coordinate(east_box_1.x + self.RECT_WIDTH, east_box_1.y + self.RECT_HEIGHT)

        return {
            'north': [north_box_1, north_box_2],
            'south': [south_box_1, south_box_2],
            'east': [east_box_1, east_box_2],
            'west': [west_box_1, west_box_2],
            'central': [central_box_1, central_box_2]
        }

    def generate_image(self):
        im = Image.open(self.BASE_IMAGE_PATH)
        draw = ImageDraw.Draw(im)

        bounding_coors = self.generate_bounding_boxes()
        for box in ['north', 'central', 'south', 'east', 'west']:
            first = bounding_coors[box][0]
            second = bounding_coors[box][1]
            val = self.data_values[box]
            draw.rectangle([(first.x, first.y), (second.x, second.y)], fill=self.FILL_COLOR)
            draw.text((first.x + self.RECT_WIDTH / 2, first.y + 35), anchor="mm", font=self.font(35), text=str(val),
                      fill=self.TEXT_COLOR)
            draw.text((first.x + self.RECT_WIDTH / 2, first.y + 70), anchor="mm", font=self.font(25), text=box.upper(),
                      fill=self.TEXT_COLOR)
        return im

    def generate_base64_string(self):
        im = self.generate_image()
        im = im.convert("RGB")
        im_file = BytesIO()
        im.save(im_file, format="JPEG")
        im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
        return base64.b64encode(im_bytes).decode("utf-8")

    def show(self):
        im = self.generate_image()
        im.show()


def lambda_handler(event, context):
    params = event["queryStringParameters"]
    print(f'params {params}')

    im = Map(north=params.get('north', '-'),
             south=params.get('south', '-'),
             east=params.get('east', '-'),
             west=params.get('west', '-'),
             central=params.get('central', '-')
             )
    return {
        'statusCode': 200,
        'body': im.generate_base64_string(),
        'headers': {'Content-Type': 'image/jpeg'},
        'isBase64Encoded': True
    }
