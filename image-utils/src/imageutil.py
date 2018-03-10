from PIL import Image, ImageDraw, ImageChops, ImageEnhance, ImageFont
import aggdraw


# --------------------------------

# 批量处理照片的函数

# --------------------------------



# 将照片变成圆角边

def roundCorner(image, radius):
    """

    Generate the rounded corner image for orgimage.

    """

    image = image.convert('RGBA')

    # generate the mask image

    mask = Image.new('RGBA', image.size, (0, 0, 0, 0))

    draw = aggdraw.Draw(mask)

    brush = aggdraw.Brush('black')

    width, height = mask.size

    draw.rectangle((0, 0, mask.size[0], mask.size[1]), aggdraw.Brush('white'))

    # north-west corner

    draw.pieslice((0, 0, radius * 2, radius * 2), 90, 180, None, brush)

    # north-east corner

    draw.pieslice((width - radius * 2, 0, width, radius * 2), 0, 90, None, brush)

    # south-west corner

    draw.pieslice((0, height - radius * 2, radius * 2, height), 180, 270, None, brush)

    # south-east corner

    draw.pieslice((width - radius * 2, height - radius * 2, width, height), 270, 360, None, brush)

    # center rectangle

    draw.rectangle((radius, radius, width - radius, height - radius), brush)

    # four edge rectangle

    draw.rectangle((radius, 0, width - radius, radius), brush)

    draw.rectangle((0, radius, radius, height - radius), brush)

    draw.rectangle((radius, height - radius, width - radius, height), brush)

    draw.rectangle((width - radius, radius, width, height - radius), brush)

    draw.flush()

    del draw

    return ImageChops.add(mask, image)


# 加圆角线条边框

def roundCornerFrame(image, radius, line_width, line_color, opacity=1.0):
    width, height = image.size

    draw = aggdraw.Draw(image)

    pen = aggdraw.Pen(line_color, line_width, int(255 * opacity))

    # 注意: aggdraw对角度的解释与PIL有区别！

    # aggdraw画线的位置是线的中线，因此，需要减除半条线宽

    halfwidth = int(line_width / 2)

    # north-west corner

    draw.arc((halfwidth, halfwidth, radius * 2 - halfwidth, radius * 2 - halfwidth), 90, 180, pen)

    # north-east corner

    draw.arc((width - radius * 2 + halfwidth, halfwidth, width - halfwidth, radius * 2 - halfwidth), 0, 90, pen)

    # south-west corner

    draw.arc((halfwidth, height - radius * 2 + halfwidth, radius * 2 - halfwidth, height - halfwidth), 180, 270, pen)

    # south-east corner

    draw.arc((width - radius * 2 + halfwidth, height - radius * 2 + halfwidth, width - halfwidth, height - halfwidth),
             270, 360, pen)

    # four edge line

    draw.line((halfwidth, radius, halfwidth, height - radius), pen)

    draw.line((radius, halfwidth, width - radius, halfwidth), pen)

    draw.line((width - halfwidth, radius, width - halfwidth, height - radius), pen)

    draw.line((radius, height - halfwidth, width - radius, height - halfwidth), pen)

    draw.flush()

    del draw

    return image


def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""

    assert opacity >= 0 and opacity <= 1

    if im.mode != 'RGBA':

        im = im.convert('RGBA')

    else:

        im = im.copy()

    alpha = im.split()[3]

    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)

    im.putalpha(alpha)

    return im


# 为照片加水印

def watermark(image, markimage, position, opacity=1):
    """Adds a watermark to an image."""

    im = image

    mark = markimage

    if opacity < 1:
        mark = reduce_opacity(mark, opacity)

    if im.mode != 'RGBA':
        im = im.convert('RGBA')

    # create a transparent layer the size of the image and draw the

    # watermark in that layer.

    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))

    if position == 'tile':

        for y in range(0, im.size[1], mark.size[1]):

            for x in range(0, im.size[0], mark.size[0]):
                layer.paste(mark, (x, y))

    elif position == 'scale':

        # scale, but preserve the aspect ratio

        ratio = min(

            float(im.size[0]) / mark.size[0], float(im.size[1]) / mark.size[1])

        w = int(mark.size[0] * ratio)

        h = int(mark.size[1] * ratio)

        mark = mark.resize((w, h))

        layer.paste(mark, ((im.size[0] - w) / 2, (im.size[1] - h) / 2))

    else:

        layer.paste(mark, position)

    # composite the watermark with the layer

    return Image.composite(layer, im, layer)


# 为照片增加文字

def signature(image, text, position, font=None, color=(255, 0, 0)):
    """

    imprints a PIL image with the indicated text in lower-right corner

    """

    if image.mode != "RGBA":
        image = image.convert("RGBA")

    textdraw = ImageDraw.Draw(image)

    textsize = textdraw.textsize(text, font=font)

    textpos = [image.size[i] - textsize[i] - position[i] for i in [0, 1]]

    textdraw.text(textpos, text, font=font, fill=color)

    del textdraw

    return image

