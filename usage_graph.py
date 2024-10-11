from PIL import ImageDraw, ImageFont
import logging

class UsageGraph:
    def __init__(self,draw,x_offset,y_offset,width=64,height=24,font_path="Roboto-Light.ttf"):
        self.draw_obj = draw  
        self.width = width  # 折线图的宽度
        self.height = height  # 折线图的高度
        self.x_offset = x_offset  
        self.y_offset = y_offset  
        self.cpu_usage_list = [0] * self.width  # 初始化 CPU 使用率数据列表
        
        if font_path is None:
            self.font = ImageFont.truetype(8)
            self.font_large = ImageFont.load_default(13)
        else:
            self.font = ImageFont.truetype(font_path, 8)
            self.font_large = ImageFont.truetype(font_path, 13)

    def update_cpu_usage(self, usage):
        self.cpu_usage_list.pop(0)
        self.cpu_usage_list.append(usage)

    def draw_usage_graph(self, usage):
        self.update_cpu_usage(usage)
        # 清除之前的图像
        self.draw_obj.rectangle((self.x_offset, self.y_offset, self.x_offset + self.width, self.y_offset + self.height), outline=0, fill=0)
        points = []
        auto_scale = 5  # 自动调整y轴最大值的间隔
        max_usage = (max(self.cpu_usage_list) + auto_scale) // auto_scale * auto_scale
        for i in range(self.width):
            x = self.x_offset + i
            y = self.y_offset + self.height - int(self.cpu_usage_list[i] / max_usage * self.height)
            if y < self.y_offset:
                y = self.y_offset
            points.append((x, y))

        # 添加底部两个点，形成封闭的区域
        points.append((self.x_offset + self.width - 1, self.y_offset + self.height))
        points.append((self.x_offset, self.y_offset + self.height))

        # 填充区域
        self.draw_obj.polygon(points, fill=255)

        # 绘制最大最小值
        max_usage_text = f"{int(max_usage)}"
        max_usage_box = self.draw_obj.textbbox((0, 0), max_usage_text, font=self.font)
        self.draw_obj.rectangle((self.x_offset + self.width - max_usage_box[2] - 2, self.y_offset, self.x_offset + self.width, self.y_offset + 7), outline=0, fill=0)
        self.draw_obj.rectangle((self.x_offset + self.width - 6, self.y_offset + self.height - 8, self.x_offset + self.width, self.y_offset + self.height - 1), outline=0, fill=0)

        self.draw_obj.text((self.x_offset + self.width - max_usage_box[2] - 0, self.y_offset - 2), max_usage_text, fill=1, font=self.font)
        self.draw_obj.text((self.x_offset + self.width - 4, self.y_offset + self.height - 10), "0", fill=1, font=self.font)

        # 绘制 CPU 使用率数字
        cpu_usage_text = f"{int(self.cpu_usage_list[-1])}%"
        cpu_usage_box = self.draw_obj.textbbox((0, 0), cpu_usage_text, font=self.font_large)
        self.draw_obj.rectangle((self.x_offset + 1, self.y_offset + 1, self.x_offset + 2 + cpu_usage_box[2], self.y_offset - 3 + cpu_usage_box[3]), outline=0, fill=0)
        self.draw_obj.text((self.x_offset + 2, self.y_offset - 4), cpu_usage_text, fill=1, font=self.font_large)
