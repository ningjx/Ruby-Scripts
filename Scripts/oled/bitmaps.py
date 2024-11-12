from PIL import Image, ImageDraw
# 位图缩放
def expand_bitmap(bitmap_data, scale):
    size = len(bitmap_data)  # 位图的大小，假设是 13x13
    new_size = size * scale  # 放大后的大小
    new_bitmap = Image.new('1', (new_size, new_size))
    draw = ImageDraw.Draw(new_bitmap)
    for y in range(size):
        for x in range(size):
            if bitmap_data[y] & (1 << (size - 1 - x)):
                # 放大像素，使用 scale 倍
                for i in range(scale):
                    for j in range(scale):
                        draw.point((x * scale + i, y * scale + j), fill=1)
    return new_bitmap
# 绘制位图
def draw_bitmap(draw_obj, bitmap_data, x_offset, y_offset):
    bitmap_size = len(bitmap_data)
    for y in range(bitmap_size):
        for x in range(13):
            if bitmap_data[y] & (1 << (12 - x)):
                draw_obj.point((x + x_offset, y + y_offset), fill=1)
# 定义位图数据
def get_bitmap_Tmp():
    return [
        0b0001001001000,
        0b0001001001000,
        0b0011111111100,
        0b1110000000111,
        0b0010100110100,
        0b0010001000100,
        0b1110001000111,
        0b0010001000100,
        0b0010000110100,
        0b1110000000111,
        0b0011111111100,
        0b0001001001000,
        0b0001001001000
    ]
def get_bitmap_LQ():
    return [
        0b0000000000000,
        0b0000000000000,
        0b0111000000000,
        0b0000110000000,
        0b0000001000000,
        0b0111000100000,
        0b0000100010000,
        0b0000010001000,
        0b0110001001000,
        0b0001000100100,
        0b0000100100100,
        0b0100100100100,
        0b0000000000000
    ]
def get_bitmap_IP():
    return [
        0b0000000000000,
        0b0000111110000,
        0b0001100011000,
        0b0111000001110,
        0b0100000000010,
        0b0101111111010,
        0b0101000001010,
        0b0101000001010,
        0b0101010101010,
        0b0101111111010,
        0b0100000000010,
        0b0111111111110,
        0b0000000000000
    ]