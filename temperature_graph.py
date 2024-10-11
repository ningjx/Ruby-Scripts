from PIL import ImageDraw, ImageFont
import bitmaps

class TemperatureGraph:
    def __init__(self,draw,x_offset, y_offset,font_path="SourceHanSansSC-Normal-2.otf"):
        self.draw_obj = draw  
        #self.width = width
        #self.height = height
        self.x_offset = x_offset  
        self.y_offset = y_offset
        self.font_large = ImageFont.truetype(font_path, 14)
        self.bitmap_Tmp = bitmaps.get_bitmap_Tmp()
    # 绘制温度信息到图像
    def draw(self, temperature):
        bitmaps.draw_bitmap(self.draw_obj, self.bitmap_Tmp, self.x_offset, self.y_offset)
        self.draw_obj.text((self.x_offset + 14, self.y_offset - 5), f"{int(temperature)}", fill=1, font=self.font_large)