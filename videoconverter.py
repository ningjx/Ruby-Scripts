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
            self.convert_h265_to_mp4(event.src_path)

    def convert_h265_to_mp4(self, h265_file):
        mp4_file = h265_file.rsplit('.', 1)[0] + '.mp4'

        # 检查转换后的文件是否已存在
        if not os.path.exists(mp4_file):
            logging.info(f"Converting {h265_file} to {mp4_file}...")
            try:
                subprocess.run(['ffmpeg', '-i', h265_file, '-c:v', 'copy', mp4_file], check=True)
                logging.info(f"Converted {h265_file} to {mp4_file}.")
            except subprocess.CalledProcessError as e:
                logging.error(f"Error converting {h265_file}: {e}")
        else:
            logging.info(f"{mp4_file} already exists. Skipping conversion.")

def initial_conversion(path):
    for filename in os.listdir(path):
        if filename.endswith('.h265'):
            h265_file = os.path.join(path, filename)
            handler.convert_h265_to_mp4(h265_file)

if __name__ == "__main__":
    path = '/home/radxa/ruby/media'
    handler = H265Handler()
    
    # 初始转换未转换的文件
    initial_conversion(path)
    
    observer = Observer()
    observer.schedule(handler, path, recursive=False)

    logging.info(f"Monitoring {path} for new .h265 files...")
    observer.start()

    try:
        while True:
            time.sleep(1)  # 每秒检查一次
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
