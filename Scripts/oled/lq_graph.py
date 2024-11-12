from PIL import ImageDraw, ImageFont
import bitmaps

class LinkQGraph:
    def __init__(self,draw,x_offset=0, y_offset=0,font_path="/home/ning/scripts/SanJiLuoLiHei-Cu-2.ttf"):
        self.draw_obj = draw  
        #self.width = width
        #self.height = height
        self.x_offset = x_offset  
        self.y_offset = y_offset
        
        #font = ImageFont.truetype("SanJiLuoLiHei-Cu-2.ttf",50)
        #
        #draw.text((5,11), "99", fill=0, font=font)
        self.bitmap_Tmp = bitmaps.get_bitmap_LQ()
        
        if font_path is None:
            self.font_large = ImageFont.load_default(50)
        else:
            self.font_large = ImageFont.truetype(font_path, 50)
    # 绘制温度信息到图像
    def draw(self, lq):
        self.draw_obj.rectangle((0,15,63,63),fill=0)
        self.draw_obj.text((5,11), f"{(lq)}", fill=255, font=self.font_large)