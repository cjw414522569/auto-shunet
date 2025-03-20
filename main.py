import logging
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

class CampusNetworkLogin:
    def __init__(self) -> None:
        logging.info("启动 Selenium")

        # 设置 Chrome 无头模式
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # 查找 chromedriver 的路径
        chromedriver_path = shutil.which("chromedriver")
        if not chromedriver_path:
            logging.error("chromedriver 未找到，请确保已安装并配置正确的路径。")
            exit(1)

        # 创建 WebDriver 实例
        self.driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)

    # 登录校园网
    def login_campus_network(self):
        driver = self.driver
        max_attempts = 5  # 最大尝试次数
        attempts = 0

        while attempts < max_attempts:
            try:
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
                    username_input.send_keys('24721481')

                    pwd_tip = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, 'pwd_tip'))
                    )
                    pwd_tip.click()

                    password_input = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.ID, 'pwd'))
                    )
                    password_input.send_keys('Glh544664')

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

            time.sleep(5)  # 等待一段时间后再尝试

        print("达到最大尝试次数，登录失败。")

    # 检查网络是否可以 ping 通百度
    def check_network_connection(self):
        try:
            result = subprocess.run(['ping', '-c', '1', 'www.baidu.com'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return result.returncode == 0
        except Exception as e:
            print(f"检查网络连接时出错: {e}")
            return False

    # 检查网络连接状态
    def check_and_login(self):
        if self.check_network_connection():
            print("网络连接正常，无需登录。")
        else:
            print("网络无法连接，尝试登录校园网...")
            self.login_campus_network()

# 创建 CampusNetworkLogin 实例并调用 check_and_login 函数
campus_network = CampusNetworkLogin()
campus_network.check_and_login()
