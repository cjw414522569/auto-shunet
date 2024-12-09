# 使用官方 Python 镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 将当前目录下的所有文件复制到容器中的工作目录
COPY . /app

# 安装系统依赖
RUN apt-get update && \
    apt-get install -y \
    wget \
    curl \
    unzip \
    libx11-dev \
    libgconf-2-4 \
    libnss3 \
    libxss1 \
    libgdk-pixbuf2.0-0 \
    libasound2 \
    libxtst6 \
    libdrm2 \
    libgbm1 \
    libvulkan1 \
    xdg-utils \
    iputils-ping \
    cron \
    fonts-liberation \
    libappindicator3-1 \
    libnspr4 \
    libnss3-dev \
    libxcomposite1 \
    libxrandr2 \
    libgtk-3-0 \
    libdbus-1-3 \
    libatspi2.0-0 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*


# 安装 Google Chrome
RUN dpkg -i google-chrome-stable_current_amd64.deb || apt-get install -f -y

# 安装 chromedriver
COPY chromedriver /usr/local/bin/chromedriver
RUN chmod +x /usr/local/bin/chromedriver

# 删除本地文件
RUN rm -f google-chrome-stable_current_amd64.deb chromedriver

# 安装 selenium
RUN pip install selenium

# 设置环境变量
ENV CHROME_BIN=/usr/bin/google-chrome-stable
ENV CHROMEDRIVER=/usr/local/bin/chromedriver

# 设置定时任务
RUN echo "*/5 * * * * python /app/main.py >> /var/log/cron.log 2>&1" > /etc/cron.d/my-cron \
    && chmod 0644 /etc/cron.d/my-cron \
    && crontab /etc/cron.d/my-cron

# 创建日志文件
RUN touch /var/log/cron.log

# 启动 cron 服务并运行主服务
CMD ["sh", "-c", "cron && tail -f /var/log/cron.log"]