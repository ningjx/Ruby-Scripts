import socket
import logging
import psutil

def get_cpu_temperature():
    try:
        with open('/sys/class/hwmon/hwmon0/temp1_input', 'r') as f:
            temp_str = f.readline().strip()
            # 将温度值转换为摄氏度
            temp_c = float(temp_str) / 1000.0
            return temp_c
    except Exception as e:
        logging.error(f"Error reading CPU temperature: {e}")
        return None
    
def get_local_ip():
    addresses = psutil.net_if_addrs()
    for interfaces,addr_list in addresses.items():
        for addr in addr_list:
            if addr.family == socket.AF_INET and addr.address != "127.0.0.1":
                return addr.address
    return None

# 获取 CPU 使用率
def get_cpu_usage():
    try:
        return psutil.cpu_percent()#interval=1
    except Exception as e:
        logging.error(f"Error getting CPU usage: {e}")
        return 0
def get_ram_usage():
    try:
        memory_info = psutil.virtual_memory()
        return memory_info.percent
    except Exception as e:
        logging.error(f"Error getting CPU usage: {e}")
        return 0