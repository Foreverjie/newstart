from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery as pq
import time


EMAIL = '864129545@qq.com'
PASSWORD = 'zzj1234'

class CrackGeetest():
    def __init__(self):
        self.url = 'https://account.geetest.com/login'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.email = EMAIL
        self.password = PASSWORD

    def get_geetest_button(self):
        '''
        获取初始验证按钮
        :return:： 按钮对象
        '''
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
        return button

    def get_position(self):
        '''
        获取验证码位置
        :return:  验证码位置元组
        '''
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img')))
        time.sleep(2)
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['w0idth']
        return (top, bottom, left, right)

    def get_geetest_image(self, name='captcha.png'):
        '''
        获取验证码图片
        :return: 图片对象
        '''
        top, bottom, left, right = self.get_position()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((top, bottom, left, right))
        return captcha

    def get_slider(self):
        '''
        获取滑块
        :return: 滑块对象
        '''
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        return slider

    def is_pixel_equal(self, image1, image2, x, y):
        '''
        判断两个像素是否相同
        :param image1: 图片1
        :param image2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        '''
        # 取两个图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threhold = 60
        if abs(pixel1[0] - pixel2[0]) < threhold and abs(pixel1[1] -pixel2[1]) < threhold and abs(pixel1[2] - pixel2[2]) < threhold:
            return True
        else:
            return False

    def get_gap(self, image1, image2):
        '''
        获取缺口偏移量
        :param image1: 不带缺口图片
        :param image2: 带缺口图片
        :return:
        '''
        left = 60
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                pass