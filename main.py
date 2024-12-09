from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import subprocess
import re
import os

# 设置Chrome无头模式
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 启用无头模式
options.add_argument('--disable-gpu')  # 禁用GPU加速
options.add_argument("--no-sandbox")  # 禁用沙盒
# 登录校园网
def login_campus_network():
    driver = None
    max_attempts = 5  # 最大尝试次数
    attempts = 0

    while attempts < max_attempts:
        try:
            driver = webdriver.Chrome(options=options)
            driver.get('http://10.10.9.9/')

            # 检查是否已经登录
            try:
                already_logged_in = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, 'toLogOut'))
                )
                print("已经登录校园网，跳过登录步骤。")
                return
            except Exception:
                print("未检测到登录状态，继续执行登录。")

            # 登录流程
            try:
                username_input = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'username'))
                )
                username_input.send_keys('*******')

                pwd_tip = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'pwd_tip'))
                )
                pwd_tip.click()

                password_input = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'pwd'))
                )
                password_input.send_keys('*******')

                login_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'loginLink_div'))
                )
                login_button.click()

                # 确保页面登录完成
                time.sleep(5)
                print("校园网登录成功")
                return
            except Exception as e:
                print(f"登录过程中发生错误: {e}")
                attempts += 1
                print(f"尝试次数: {attempts}/{max_attempts}")

        except Exception as e:
            print(f"校园网连接或其他错误: {e}")
            attempts += 1
            print(f"尝试次数: {attempts}/{max_attempts}")

        finally:
            if driver:
                driver.quit()

        time.sleep(5)  # 等待一段时间后再尝试

    print("达到最大尝试次数，登录失败。")

# 获取本地网络接口的IP地址
def get_internal_ip():
    try:
        result = subprocess.run(['ipconfig'], stdout=subprocess.PIPE)
        output = result.stdout.decode('gbk')
        ip_match = re.findall(r'IPv4 地址[^\d]*(\d+\.\d+\.\d+\.\d+)', output)
        internal_ips = [ip for ip in ip_match if not ip.startswith('127.')]
        return internal_ips[0] if internal_ips else "未找到有效的内网IP"
    except Exception as e:
        return f"获取内网IP时出错: {e}"

# 检查网络是否可以ping通百度
def check_network_connection():
    try:
        result = subprocess.run(['ping', '-c', '1', 'www.baidu.com'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except Exception as e:
        print(f"检查网络连接时出错: {e}")
        return False


print("尝试登录校园网...")
login_campus_network()

