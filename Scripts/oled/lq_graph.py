from PIL import ImageDraw, ImageFont
import os
import bitmaps

class LinkQGraph:
    def __init__(self,draw,x_offset=0, y_offset=0,font_path="fonts/SanJiLuoLiHei-2.ttf"):
        script_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本目录
        font_path = os.path.join(script_dir, "fonts", "SanJiLuoLiHei-2.ttf")  # 确保字体文件名正确
        print(f"[DEBUG] 字体路径: {font_path}")  # 添加调试输出

        if not os.path.exists(font_path):
            raise FileNotFoundError(f"字体文件不存在: {font_path}")


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