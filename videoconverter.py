import os
import subprocess
import logging
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 设置日志配置
logging.basicConfig(
    filename='/home/ning/scripts/videoconverter.log',  # 日志文件路径
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class H265Handler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        
        # 处理 .h265 文件
        if event.src_path.endswith('.h265'):
            self.wait_for_file_ready(event.src_path)

    def wait_for_file_ready(self, h265_file):
        while True:
            try:
                # 尝试以独占模式打开文件
                with open(h265_file, 'rb') as f:
                    f.read()  # 读取文件内容
                break  # 如果成功打开，退出循环
            except IOError:
                logging.info(f"文件 {h265_file} 被占用，一秒后重试...")
                time.sleep(1)  # 等待一秒后重试

        self.convert_h265_to_mp4(h265_file)

    def convert_h265_to_mp4(self, h265_file):
        mp4_file = h265_file.rsplit('.', 1)[0] + '.mp4'

        # 检查转换后的文件是否已存在
        if not os.path.exists(mp4_file):
            logging.info(f"准备将 {h265_file} 转换为 {mp4_file}...")
            try:
                #subprocess.run(['ffmpeg -r 30', '-i', h265_file, '-c:v', 'copy', mp4_file], check=True)
                subprocess.run(['ffmpeg', '-r', '30', '-fflags', '+genpts', '-i', h265_file, '-c:v', 'copy', mp4_file], check=True)
                logging.info(f"已将 {h265_file} 转换为 {mp4_file}。")
            except subprocess.CalledProcessError as e:
                logging.error(f"转换 {h265_file} 失败，失败原因: {e}")
        else:
            logging.info(f"文件 {mp4_file} 已存在，跳过该转换。")

def initial_conversion(path):
    for filename in os.listdir(path):
        if filename.endswith('.h265'):
            h265_file = os.path.join(path, filename)
            handler.wait_for_file_ready(h265_file)

if __name__ == "__main__":
    path = '/home/radxa/ruby/media'
    handler = H265Handler()
    
    # 初始转换未转换的文件
    initial_conversion(path)
    
    observer = Observer()
    observer.schedule(handler, path, recursive=False)

    logging.info(f"正在监控目录 {path} 下的新 .h265 文件...")
    observer.start()

    try:
        while True:
            time.sleep(1)  # 每秒检查一次
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
