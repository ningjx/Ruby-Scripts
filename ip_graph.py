from PIL import ImageDraw, ImageFont, Image
import bitmaps

class IPGraph:
    def __init__(self,draw,x_offset, y_offset,width, height,font_path="SourceHanSansSC-Normal-2.otf"):
        self.draw_obj = draw  
        self.width = width
        self.height = height
        self.x_offset = x_offset  
        self.y_offset = y_offset
        self.font_large = ImageFont.truetype(font_path, 14)
        self.bitmap_Tmp = bitmaps.get_bitmap_IP()

        self.scroll_offset = 0  # 初始偏移量
        self.scroll_speed = 1  # 滚动速度


    def draw(self, ip):
        bitmaps.draw_bitmap(self.draw_obj, self.bitmap_Tmp, self.x_offset, self.y_offset)
        buffer_image = Image.new('1', (self.width, self.height))
        buffer_draw = ImageDraw.Draw(buffer_image)

        max_usage_box = self.draw_obj.textbbox((0, 0), ip, font=self.font_large)
        text_width = max_usage_box[2]
        # 如果文本宽度超出屏幕宽度，开始滚动
        if text_width > 128 - (self.x_offset + 14):
            # 更新滚动偏移量
            self.scroll_offset -= self.scroll_speed
            if self.scroll_offset <  128 - (self.x_offset + 14) - text_width:  # 如果偏移量超过文本宽度，则重置
                self.scroll_offset = 0  # 从右侧重新开始滚动
        #self.draw_obj.text((self.x_offset + 14, self.y_offset - 5), ip, fill=1, font=self.font_large)
        buffer_draw.text((self.scroll_offset, - 5), ip, fill=1, font=self.font_large)
        self.draw_obj.bitmap((self.x_offset + 14, self.y_offset), buffer_image, fill=1)