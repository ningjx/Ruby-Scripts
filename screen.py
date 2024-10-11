import psutil
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont
import time
import socket
import logging
import bitmaps
import sysinfos
from usage_graph import UsageGraph
from temperature_graph import TemperatureGraph
from ip_graph import IPGraph

logging.basicConfig(filename='screen.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

font13 = ImageFont.truetype("SourceHanSansSC-Normal-2.otf",13)
font8 = ImageFont.truetype("SourceHanSansSC-Normal-2.otf",8)

def init_i2c(i2c_bus, i2c_address):
    try:
        serial = i2c(port=i2c_bus, address=i2c_address)
        return serial
    except Exception as e:
        logging.error(f"Failed to initialize I2C: {e}")
        return None

def init_oled(serial, width=64, height=48):
    try:
        device = ssd1306(serial, width=width, height=height)
        return device
    except Exception as e:
        logging.error(f"Failed to initialize OLED device: {e}")
        return None

def create_image(width, height):
    image = Image.new('1', (width, height))
    return image, ImageDraw.Draw(image)

def main():
    # I2C 和 OLED 参数
    I2C_BUS = 3
    I2C_ADDRESS = 0x3C
    WIDTH = 128
    HEIGHT = 64
    # 初始化 I2C 和 OLED 显示器
    serial = init_i2c(I2C_BUS, I2C_ADDRESS)
    if serial is None:
        return  # 无法初始化 I2C，停止执行
    device = init_oled(serial, width=WIDTH, height=HEIGHT)
    if device is None:
        return  # 无法初始化 OLED，停止执行
    
    # 创建图像和绘图对象
    image, draw = create_image(WIDTH, HEIGHT)

    #bitmap_LQ = bitmaps.get_bitmap_IP()
    #bitmaps.draw_bitmap(draw, bitmap_LQ, 30, 0)
    draw.line((0, 14, 127, 14), fill=255, width=1)  # 绘制一条线
    ip = sysinfos.get_local_ip()

    temp_graph = TemperatureGraph(draw=draw,x_offset=1, y_offset=0)
    ip_graph = IPGraph(draw=draw,x_offset=32, y_offset=0)
    cpu_graph = UsageGraph(draw=draw,x_offset=64, y_offset=15)
    ram_graph = UsageGraph(draw=draw,x_offset=64, y_offset=40)
    while True:
        temperature = sysinfos.get_cpu_temperature()
        cpu_usage = sysinfos.get_cpu_usage()
        ram_usage = sysinfos.get_ram_usage()
        cpu_graph.draw_usage_graph(cpu_usage)
        ram_graph.draw_usage_graph(ram_usage)
        temp_graph.draw(temperature)
        ip_graph.draw(ip)
        
        draw.line((64, 14, 64, 63), fill=255, width=1)  # 绘制一条线

        device.display(image)
        time.sleep(1)
# 程序入口
if __name__ == "__main__":
    main()

