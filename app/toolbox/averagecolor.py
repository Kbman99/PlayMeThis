from io import BytesIO

import requests
from PIL import Image


def average_color(url):
    image_url = url

    # Here we get the image from the web, but we could as easily load
    # from the local filesystem. See Pillow docs on how to open images.
    resp = requests.get(image_url)
    assert resp.ok
    img = Image.open(BytesIO(resp.content))

    img2 = img.resize((1, 1))

    color = img2.getpixel((0, 0))
    return '#{:02x}{:02x}{:02x}'.format(*color).upper()
