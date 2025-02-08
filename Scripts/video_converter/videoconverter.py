import os
import subprocess
import logging
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

log_dir = "/home/RubyScripts/logs"
log_file = os.path.join(log_dir, "videoconverter.log")
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
class H265Handler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        
        # 处理 .h265 和 .h264 文件
        if event.src_path.endswith(('.h265', '.h264')):
            self.wait_for_file_ready(event.src_path)

    def wait_for_file_ready(self, video_file, retries=10):
        attempt = 0
        while attempt < retries:
            try:
                # 尝试以独占模式打开文件
                with open(video_file, 'rb') as f:
                    f.read()  # 读取文件内容
                break  # 如果成功打开，退出循环
            except IOError:
                attempt += 1
                logging.info(f"文件 {video_file} 被占用，等待一秒后重试（第 {attempt}/{retries} 次）...")
                time.sleep(1)  # 等待一秒后重试
        else:
            logging.error(f"文件 {video_file} 在多次重试后仍被占用，放弃转换。")
            return

        self.convert_to_mp4(video_file)

    def convert_to_mp4(self, video_file):
        mp4_file = video_file.rsplit('.', 1)[0] + '.mp4'

        # 检查转换后的文件是否已存在
        if not os.path.exists(mp4_file):
            logging.info(f"准备将 {video_file} 转换为 {mp4_file}...")
            try:
                #subprocess.run(['ffmpeg', '-r', '30', '-fflags', '+genpts', '-i', video_file, '-c:v', 'copy', mp4_file], check=True)
                subprocess.run(['ffmpeg','-i', video_file, '-c:v', 'copy', mp4_file], check=True)
                logging.info(f"已将 {video_file} 转换为 {mp4_file}。")
            except subprocess.CalledProcessError as e:
                logging.error(f"转换 {video_file} 失败，失败原因: {e}")
        else:
            logging.info(f"文件 {mp4_file} 已存在，跳过该转换。")

def initial_conversion(path):
    try:
        for filename in os.listdir(path):
            if filename.endswith(('.h265', '.h264')):
                video_file = os.path.join(path, filename)
                handler.wait_for_file_ready(video_file)
    except Exception as e:
        logging.error(f"无法列出目录 {path}，错误原因: {e}")

if __name__ == "__main__":
    path = '/home/radxa/ruby/media'
    handler = H265Handler()
    
    # 初始转换未转换的文件
    initial_conversion(path)
    
    observer = Observer()
    observer.schedule(handler, path, recursive=False)

    logging.info(f"服务已启动，正在监控目录 {path} 下新创建的 .h265 和 .h264 文件...")
    observer.start()
    observer.join()
