import time
import os
from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
import requests
import shutil

class App:
    def __init__(self,username='YOUR_USERNAME_HERE', password='YOUR_PASSWORD_HERE', target_username='TARGET_PROFILE_HERE', path='WHERE_YOU_WANT_TO_STORE_DOWNLOADED_IMAGES'):
        
        if not os.path.exists(path):
            os.mkdir(path)
        
        self.username = username
        self.password = password
        self.target_username =  target_username
        self.path = path
        self.driver = webdriver.Chrome()
        self.main_url = 'https://www.instagram.com'
        #multiple of 4,5, only
        self.pics = int(24)
        self.count = int(0)
    
    
    #openBrowser
    def open_Browser(self,):
            self.driver.get(self.main_url)
            self.driver.maximize_window()
            time.sleep(3)
    
    
    #write Log_In fucntion
    def log_In(self,):
        try:
            try:
                uname = self.driver.find_element_by_xpath("/html//div[@id='react-root']/section/main[@role='main']/article[@class='_4_yKc']//form[@method='post']//input[@name='username']")
                uname.click()
                uname.send_keys(self.username)
                time.sleep(3)

                password = self.driver.find_element_by_xpath("/html//div[@id='react-root']/section/main[@role='main']/article[@class='_4_yKc']//form[@method='post']//input[@name='password']")
                password.click()
                password.send_keys(self.password)
                time.sleep(3)
            except Exception:
                print("some error occured while finding username and password boxes")
            try:
                logIn = self.driver.find_element_by_xpath("//div[@id='react-root']/section/main[@role='main']/article[@class='_4_yKc']//form[@method='post']//button[@type='submit']/div[.='Log In']")
                logIn.click()
            except Exception:
                print("notification button not found")
        except Exception:
            print("Some error occured while logging in")
    
    
    #Turn_On notification handler    
    def close_noti(self,):
        try:
            not_now = self.driver.find_element_by_xpath('/html[1]/body[1]/div[4]/div[1]/div[1]/div[3]/button[2]')
            not_now.click()
            time.sleep(1)
        except Exception:
            pass
    
    
    #goto the profile
    def goto_Profile(self,):
        profile = self.main_url + '/' + self.target_username + '/'
        self.driver.get(profile)  
    
                
    def save_img(self,img,i,j):
        if(j>1):
            try:
                filename = self.target_username+str(i*j)+'.jpg'
                response = requests.get(img,stream=True)
                image_path = os.path.join(self.path, filename)
                with open(image_path, 'wb') as file:
                    shutil.copyfileobj(response.raw, file)
            except Exception:
                pass       
        if(j==1):
            try:
                filename = self.target_username+str(self.count)+'.jpg'
                response = requests.get(img,stream=True)
                image_path = os.path.join(self.path, filename)
                with open(image_path, 'wb') as file:
                    shutil.copyfileobj(response.raw, file)
            except Exception:
                pass  
        
    def downloading_Images(self,):
        
        if self.pics <= 24 and self.pics >5:        
            for j in range(1,int(self.pics/3)+1):
                for i in range(1,4):
                    imgurl = self.driver.find_element_by_xpath('//div//div//div//div//div//div['+str(j)+']//div['+str(i)+']//a[1]//div[1]//div[1]//img[1]').get_attribute("src")
                    self.save_img(imgurl,i,j)
        
        elif self.pics >24:
            for j in range(1,int(self.pics/3)+1):
                if j % 9 == 0:
                    self.jump()
                    time.sleep(2)
                    for i in range(1,4):
                        imgurl = self.driver.find_element_by_xpath('//div//div//div//div//div//div['+str(j)+']//div['+str(i)+']//a[1]//div[1]//div[1]//img[1]').get_attribute("src")
                        self.count+=1
                        self.save_img(imgurl,self.count,1)
                else:
                        for i in range(1,4):
                            imgurl = self.driver.find_element_by_xpath('//div//div//div//div//div//div['+str(j)+']//div['+str(i)+']//a[1]//div[1]//div[1]//img[1]').get_attribute("src")
                            self.count+=1
                            self.save_img(imgurl,self.count,1)
    def jump(self,):
        time.sleep(2)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight*(0.25));")
    
    
if __name__ == '__main__':
    app = App()
    
app.open_Browser()
app.log_In()
time.sleep(3)
app.close_noti()
time.sleep(3)
app.goto_Profile()
time.sleep(5)
app.downloading_Images()
input('')
time.sleep(2)
app.driver.close()