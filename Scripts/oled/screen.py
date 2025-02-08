import threading
import os
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont, ImageChops
import time
import logging
import sysinfos
from usage_graph import UsageGraph
from temperature_graph import TemperatureGraph
from ip_graph import IPGraph
from lq_graph import LinkQGraph

log_dir = "/home/RubyScripts/logs"
log_file = os.path.join(log_dir, "screen.log")
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=log_file,
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

ip = None
# 创建锁对象
lock = threading.Lock()

def init():
    try:
        serial = i2c(port=3, address=0x3D)
        device = ssd1306(serial, width=128, height=64)
        return device
    except Exception as e:
        logging.error(f"Failed to initialize device: {e}")
        return None

def create_image():
    image = Image.new('1', (128, 64))
    draw = ImageDraw.Draw(image)
    return image, draw

def get_infos():
    global ip
    while True:
        try:
            ip = sysinfos.get_local_ip()
            
        except Exception as e:
            logging.error(f"Error updating graphs: {e}")

        time.sleep(5)  # 更新频率

def update_graphs(cpu_graph, ram_graph, temp_graph, ip_graph, lq_graph, draw):
    global ip
    while True:
        try:
            with lock:
                # 获取系统信息
                cpu_usage = sysinfos.get_cpu_usage()
                ram_usage = sysinfos.get_ram_usage()

                # 绘制图表
                cpu_graph.draw_usage_graph(cpu_usage)
                ram_graph.draw_usage_graph(ram_usage)
                # 分隔线
                draw.line((0, 14, 127, 14), fill=255, width=1)
                draw.line((64, 14, 64, 63), fill=255, width=1)

                temperature = sysinfos.get_cpu_temperature()
                temp_graph.draw(temperature)
                ip_graph.draw(ip)
                lq_graph.draw(time.localtime().tm_sec)
        except Exception as e:
            logging.error(f"Error updating graphs: {e}")

        time.sleep(1)  # 更新频率

def update_graphs_fast(cpu_graph, ram_graph, temp_graph, ip_graph, draw):
    global ip
    while True:
        try:
            with lock:
                ip_graph.draw(ip)

        except Exception as e:
            logging.error(f"Error updating graphs: {e}")

        time.sleep(0.3)  # 更新频率

def display_screen(device, image):
    previous_image = None  # 保存上一帧的图像
    while True:
        try:
            with lock:  # 获取锁，确保图像绘制完成后才能显示
                if previous_image is None:
                    # 第一次显示图像
                    device.display(image)
                    previous_image = image.copy()  # 保存当前图像为上一帧
                else:
                    # 比较当前图像与上一帧
                    difference = ImageChops.difference(image, previous_image)

                    # 如果有差异才显示
                    if difference.getbbox():
                        device.display(image)
                        previous_image = image.copy()  # 更新上一帧为当前图像

        except Exception as e:
            logging.error(f"Error displaying image: {e}")

        time.sleep(0.1)  # 调整刷新频率

def main():
    device = init()
    if device is None:
        return
    
    # 创建图像和绘图对象
    image, draw = create_image()

    lq_graph = LinkQGraph(draw)
    temp_graph = TemperatureGraph(draw=draw, x_offset=1, y_offset=0, width=30)
    ip_graph = IPGraph(draw=draw, x_offset=32, y_offset=0)
    cpu_graph = UsageGraph(draw=draw, x_offset=64, y_offset=15, width=64, height=24)
    ram_graph = UsageGraph(draw=draw, x_offset=64, y_offset=40, width=64, height=24)

    # 创建绘制线程
    get_infos_thread = threading.Thread(target=get_infos, daemon=True)
    draw_thread = threading.Thread(target=update_graphs, args=(cpu_graph, ram_graph, temp_graph, ip_graph, lq_graph, draw), daemon=True)
    draw_thread_fast = threading.Thread(target=update_graphs_fast, args=(cpu_graph, ram_graph, temp_graph, ip_graph, draw), daemon=True)
    display_thread = threading.Thread(target=display_screen, args=(device, image), daemon=True)

    # 启动线程
    get_infos_thread.start()
    draw_thread.start()
    draw_thread_fast.start()
    display_thread.start()

    # 保持主线程运行
    get_infos_thread.join()
    draw_thread.join()
    draw_thread_fast.join()
    display_thread.join()

if __name__ == "__main__":
    main()
