#!/bin/bash

# 创建目录并设置权限
sudo mkdir -p /home/RubyScripts
sudo chown radxa /home/RubyScripts

# 克隆代码仓库到临时文件夹
git clone https://github.com/ningjx/Ruby-Scripts /home/RubyScripts/temp

# 复制文件到目标目录
sudo cp -a /home/RubyScripts/temp/. /home/RubyScripts/ && sudo rm -f /home/RubyScripts/install.sh

# 安装所需软件包
sudo apt update
sudo apt install -y ffmpeg python3-venv python3-dev

# 创建并激活 Python 虚拟环境
python3 -m venv /home/RubyScripts/venv/
source /home/RubyScripts/venv/bin/activate

# 安装 Python 库
pip install psutil luma.oled Pillow watchdog
deactivate

# 复制 .service 文件到 systemd 目录
sudo find /home/RubyScripts/Scripts/ -type f -name "*.service" -exec cp {} /etc/systemd/system/ \;

# 重新加载 systemd
sudo systemctl daemon-reload

# 检查并更新 /etc/fstab
if ! grep -q "/dev/mmcblk1p1" /etc/fstab; then
    echo "/dev/mmcblk1p1 /home/radxa/ruby/media exfat defaults,nofail 0 0" | sudo tee -a /etc/fstab
fi

# 删除临时目录
rm -rf /home/RubyScripts/temp

# 输出安装完成信息
echo "安装完成"