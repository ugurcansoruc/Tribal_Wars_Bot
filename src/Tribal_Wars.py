from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

from Oyun import Tribal_Wars, Sayfalar
from threading import Thread

import time

class Tribal_Wars_Bot:
    def __init__(self):
        self.web_driver = self.browser_baslat(self.browser_ayarlarini_gerceklestir()) 
        self.tribal_wars = Tribal_Wars(self.web_driver)
        pass

    def browser_islem_limitle(fonksiyon):
        def sureli_browser_islem_limitle(self, * args, ** kwargs):
            fonksiyon()
            time.sleep(10)
            pass
        return sureli_browser_islem_limitle

    @browser_islem_limitle
    def browser_baslat(_options):
        return webdriver.Firefox(options = _options)

    @browser_islem_limitle
    def browser_durdur(self):
        self.web_driver.quit()
        pass

    def browser_ayarlarini_gerceklestir(self):
        self.web_driver_options = Options()
        self.web_driver_options.add_argument("-profile")
        self.web_driver_options.add_argument('/home/ugurcan/snap/firefox/common/.mozilla/firefox/j4p1uupc.default')        
        return self.web_driver_options
    
    def oto_temizlik_yagmasi_baslat(self):
        self.oto_temizlik_thread = Thread(target = self.oto_temizlik_yagmasi_gerceklestir, daemon=True)
        self.oto_temizlik_thread.start()
        pass

    def oto_temizlik_yagmasi_durdur(self):
        self.oto_temizlik_thread.kill()
        pass

    def oto_temizlik_yagmasi_gerceklestir(self):
        while True:
            self.tribal_wars.git_ana_ekran()
            self.tribal_wars.sec_dunya()
            self.tribal_wars.git_ictima_meydani(Sayfalar.Ictima_Meydani.TEMIZLEME)
            self.tribal_wars.git_ictima_meydani()
            if "" != self.tribal_wars.al_ictima_meydani_sure_bilgisi():
                self.tribal_wars.baslat_ictima_meydani_temizlik()
                self.browser_durdur()
                time.sleep(3000) # ortalama temizlik suresi -> bu oyun icerisinden cekilmeli.
                self.browser_baslat()
            time.sleep(10)