from PIL import Image, ImageDraw, ImageFont

def get_average_color(image):
    # Calculate the average color of the image
    colors = image.getdata()
    r, g, b = 0, 0, 0
    count = 0

    for color in colors:
        r += color[0]
        g += color[1]
        b += color[2]
        count += 1

    return (r // count, g // count, b // count)

def invert_color(color):
    r, g, b = color
    return (255 - r, 255 - g, 255 - b)

def main():
    text = "Aleo-Bold.otf"
    image_path = "example.jpeg"
    name = "Logo"

    # Open the local image file
    image = Image.open(image_path)

    txt_layer = Image.new('RGBA', image.size, (255, 255, 255, 0))

    # Calculate the average color of the image
    average_color = get_average_color(image)

    # Adjust the font path according to your font file location
    font = ImageFont.truetype("fonts/" + text, 62)

    d = ImageDraw.Draw(txt_layer)

    # Use the inverted color of the average color as the text color
    inverted_color = invert_color(average_color)
    d.text((0, 0), name, fill=inverted_color + (255,), font=font)

    out = Image.alpha_composite(image.convert("RGBA"), txt_layer)
    out.save('out.png')

if __name__ == "__main__":
    main()
