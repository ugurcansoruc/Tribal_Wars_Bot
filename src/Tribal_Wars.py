from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time

ffOptions = Options()
ffOptions.add_argument("-profile")
ffOptions.add_argument('/home/ugurcan/snap/firefox/common/.mozilla/firefox/j4p1uupc.default')

# Tarayıcının kullanılacağı sürücüyü yükleyin
driver = webdriver.Firefox(options=ffOptions)

# Tarayıcıyı açın ve bir web sitesine gidin
driver.get("https://tr74.klanlar.org/")
time.sleep(3)

driver.get("https://tr74.klanlar.org/page/play/tr74")
time.sleep(1)

driver.get("https://tr74.klanlar.org/game.php?village=42080&screen=place&mode=scavenge")
time.sleep(1)

while True:
    try:
        #time.sleep(driver.find_element(By.CLASS_NAME, "return-countdown").text.split(":")[1] * 60)
        driver.get("https://tr74.klanlar.org/page/play/tr74")
        time.sleep(1)   
        driver.get("https://tr74.klanlar.org/game.php?village=42080&screen=place&mode=scavenge")
        time.sleep(1)

        driver.find_element(By.LINK_TEXT, "Tüm birlikler").click()
        time.sleep(1)

        value = driver.find_element(By.CLASS_NAME, "duration").text #hangi sureyi aldigimiz onemli degil birini alsak yeter
        time.sleep(1)
        if value != "":
            # if daha once yapilmamissa
            try:
                driver.find_elements(By.LINK_TEXT, "Başla")[1].click() #tiklarken ikinciye tiklayacagiz.
            except:
                try:
                    driver.find_element(By.LINK_TEXT, "Başla").click()
                except:
                    pass
            time.sleep(10)

            driver.quit()
            time.sleep(3000)

            driver = webdriver.Firefox(options=ffOptions)
            time.sleep(5)

            #time.sleep(driver.find_element(By.CLASS_NAME, "return-countdown").text.split(":")[1] * 60)
            driver.get("https://tr74.klanlar.org/page/play/tr74")
            time.sleep(1)

            driver.get("https://tr74.klanlar.org/game.php?village=42080&screen=place&mode=scavenge")
            time.sleep(1)
    except:
        time.sleep(1)
    time.sleep(100)


# Tarayıcıyı kapatın
time.sleep(5)
driver.quit()
