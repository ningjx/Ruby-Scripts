from PIL import ImageDraw, ImageFont, Image
import bitmaps

class IPGraph:
    def __init__(self,draw,x_offset, y_offset,width, height,font_path="SourceHanSansSC-Normal-2.otf"):
        self.draw_obj = draw  
        self.width = width
        self.height = height
        self.x_offset = x_offset  
        self.y_offset = y_offset
        
        if font_path is None:
            self.font_large = ImageFont.load_default(14)
        else:
            self.font_large = ImageFont.truetype(font_path, 14)

        self.bitmap_Tmp = bitmaps.get_bitmap_IP()
        self.buffer_image = Image.new('1', (width, height))
        self.buffer_draw = ImageDraw.Draw(self.buffer_image)
        self.scroll_offset = 0  # 初始偏移量
        self.scroll_speed = 1  # 滚动速度
        self.pre_ip = "ip"
        self.static_offset = 0
        self.direction = False

    def draw(self, ip):
        self.draw_obj.rectangle((self.x_offset, self.y_offset, self.x_offset + self.width, self.y_offset + self.height - 1), fill=0)
        bitmaps.draw_bitmap(self.draw_obj, self.bitmap_Tmp, self.x_offset, self.y_offset)
        self.buffer_draw.rectangle((0,0,self.width,self.height),fill=0)
        if ip != self.pre_ip:
            self.pre_ip = ip
            max_usage_box = self.draw_obj.textbbox((0, 0), ip, font=self.font_large)
            text_width = max_usage_box[2]
            self.static_offset = text_width - (127 - (self.x_offset + 14))
        
        if self.static_offset > 0:
            if self.static_offset < - self.scroll_offset or self.scroll_offset > 0:
                self.direction = not self.direction
            if self.direction:
                self.scroll_offset -= self.scroll_speed
            else:
                self.scroll_offset += self.scroll_speed

        self.buffer_draw.text((self.scroll_offset, - 5), ip, fill=1, font=self.font_large)

        self.draw_obj.bitmap((self.x_offset + 14, self.y_offset), self.buffer_image, fill=1)