from PIL import ImageDraw, ImageFont
import bitmaps

class TemperatureGraph:
    def __init__(self,draw,x_offset,y_offset,width=0,height=0,font_path="Scripts/oled/fonts/Roboto-Light.ttf"):
        self.draw_obj = draw  
        self.width = width
        self.height = height
        self.x_offset = x_offset  
        self.y_offset = y_offset
        self.bitmap_Tmp = bitmaps.get_bitmap_Tmp()
        self.icon_width = max(len(bin(row)) - 2 for row in self.bitmap_Tmp)
        self.icon_height = len(self.bitmap_Tmp)
        if self.width == 0:
            self.width = 127 - x_offset
        if self.height == 0:
            self.height = self.icon_height + 1
        
        if font_path is None:
            self.font_large = ImageFont.load_default(14)
        else:
            self.font_large = ImageFont.truetype(font_path, 14)
    # 绘制温度信息到图像
    def draw(self, temperature):
        self.draw_obj.rectangle((self.x_offset, self.y_offset, self.x_offset + self.width, self.y_offset + self.icon_height), fill=0)
        bitmaps.draw_bitmap(self.draw_obj, self.bitmap_Tmp, self.x_offset, self.y_offset)
        self.draw_obj.text((self.x_offset + self.icon_width + 1, self.y_offset - 3), f"{int(temperature)}", fill=1, font=self.font_large)