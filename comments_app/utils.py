from PIL import Image, ImageDraw, ImageFont
import random
import string
import io

captcha_store = {}


def generate_captcha_text(length=5):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def generate_captcha_image(text, font_size=22, letter_spacing=5, max_angle=30):
    width, height = 180, 60
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    total_width = sum(draw.textbbox((0, 0), char, font=font)[2] - draw.textbbox((0, 0), char, font=font)[0] for char in
                      text) + letter_spacing * (len(text) - 1)
    offset = 30
    text_position = ((width - total_width) // 2 - offset, (height - font_size) // 2)

    current_x = text_position[0]
    for char in text:
        char_image = Image.new('RGBA', (font_size, font_size), (0, 0, 0, 0))
        char_draw = ImageDraw.Draw(char_image)
        char_draw.text((0, 0), char, font=font, fill='black')

        angle = random.uniform(-max_angle, max_angle)
        rotated_char_image = char_image.rotate(angle, expand=1)

        image.paste(rotated_char_image, (int(current_x), int(text_position[1])), rotated_char_image)

        char_width, char_height = rotated_char_image.size
        current_x += char_width + letter_spacing

    return image


def get_captcha_image(text):
    image = generate_captcha_image(text)
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer
