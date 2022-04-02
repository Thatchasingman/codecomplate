from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from image_match import distance
from image_match import get_tracks
from image_match import getSlideInstance

class Dacard(object):
    def __init__(self, url, prt='', time2wait=10):
        self.browser = webdriver.Firefox()
        # self.browser.set_window_size(500,800)
        self.browser.implicitly_wait(10)
        self.browser.get(url)
        self.wait = WebDriverWait(self.browser, time2wait)
        print('注意：请打卡期间请勿进行电脑操作！！')

    def __clickVerifyBtn(self):
        verify_btn = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "yidun_slider")))
        verify_btn.click()

    def __slideVerifyCode(self):
        self.browser.execute_script("document.querySelector('.yidun_panel').style.display='block'")
        slider = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'yidun_slider')))
        ActionChains(self.browser).click_and_hold(slider).perform()
        slider_loc_x = slider.location["x"]
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "yidun_bg-img")))
        icon = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "yidun_jigsaw")))
        pic_width = img.size['width']
        icon_width = icon.size['width']
        img_tags = self.browser.find_elements_by_tag_name("img")
        img_url = img_tags[1].get_attribute("src")
        # print(img_url)
        icon_url = img_tags[2].get_attribute("src")
        # print(icon_url)
        match_x = distance(img_url, icon_url, pic_width)
        if match_x == -1:
            raise Exception()

        slider_instance = getSlideInstance(pic_width, icon_width, match_x)
        tracks = get_tracks(slider_instance)

        for track in tracks:
            ActionChains(self.browser).move_by_offset(xoffset=track, yoffset=0).perform()
        else:
            ActionChains(self.browser).move_by_offset(xoffset=3, yoffset=0).perform()
            ActionChains(self.browser).move_by_offset(xoffset=-3, yoffset=0).perform()
            time.sleep(0.5)
            ActionChains(self.browser).release().perform()
        time.sleep(3)
        cur_loc_x = slider.location["x"]
        if cur_loc_x > slider_loc_x:
            print("success")
            return True
        else:
            return False

    def verifySlideCode(self,attempt_times=10):
        #尝试attempt_times次滑动验证，返回是否验证通过
        self.wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME,"yidun_tips__text"), r"向右拖动滑块填充拼图"))
        for attempt in range(attempt_times):
            try:
                if self.__slideVerifyCode():
                    return True
            except Exception as e:
                print(e)
                ActionChains(self.browser).release().perform()
                refresh = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "yidun_refresh")))
                refresh.click()
                time.sleep(0.6)
        return False
    def dacard(self, user, psd):
        username = self.browser.find_element_by_id('zh')
        password = self.browser.find_element_by_id('passw')
        btn = self.browser.find_element_by_class_name('btn')
        username.clear()
        password.clear()
        username.send_keys(user)
        password.send_keys(psd)
        if(self.verifySlideCode()):
            btn.click()
            time.sleep(0.5)
            print('登录成功！')
            print('注意：在自动打卡期间，请勿使用电脑，否则打卡将失败……')
            self.fill()
    def fill(self):
        try:
            self.browser.execute_script("window.scrollTo(200,0)")
            print('我滚动了200px')
            # 晨检
            tar = self.browser.find_element_by_id('cjtw').send_keys("36.5")
            self.browser.find_element_by_id('twyjcrq').click()
            self.browser.find_element_by_class_name('today').click()
            time.sleep(0.5)
            print("您晨检温度设置为：36，5")
            # 午检
            self.browser.find_element_by_id('wujtw').send_keys("36.7") #更改温度
            self.browser.find_element_by_id('twejcrq').click()
            self.browser.find_element_by_class_name('today').click()
            time.sleep(0.5)
            print("您午检温度设置为：36，7")
            # 晚检
            self.browser.find_element_by_id('wajtw').send_keys("36.6")
            self.browser.find_element_by_id('twsjcrq').click()
            self.browser.find_element_by_class_name('today').click()
            time.sleep(0.5)
            print("您晨检温度设置为：36，6")

            self.browser.execute_script("window.scrollTo(0, 800)")
            print("滚动了800px")
            confirm = self.browser.find_element_by_id('10000')
            confirm.click()
            print("点击了确认按钮")
            time.sleep(1)
            self.browser.find_element_by_id('tj').click()
            print('打卡成功，1秒后关闭浏览器……')
            time.sleep(1)
            self.browser.quit()
        except Exception as e:
            print(e)
            print("发生错误了耶，您可能已打卡……")
if __name__=="__main__":
    Dacard = Dacard('https://stuhealth.jnu.edu.cn/#/login')
    Dacard.dacard('username', 'password') 
    #username = > 打卡账号
    #password = > 密码
