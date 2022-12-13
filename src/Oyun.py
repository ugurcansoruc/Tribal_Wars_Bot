from typing import Optional
from functools import wraps
import time

from selenium.webdriver.common.by import By

class Sayfalar:
    class Genel:
        GIRIS_EKRANI = "https://tr74.klanlar.org/"
        DUNYA_SECIMI = "https://tr74.klanlar.org/page/play/tr74"
    class Ictima_Meydani:
        KOMUTLAR = "https://tr74.klanlar.org/game.php?village=42080&screen=place"
        BIRLIKLER = "https://tr74.klanlar.org/game.php?village=42080&screen=place&mode=units"
        TEMIZLEME = "https://tr74.klanlar.org/game.php?village=42080&screen=place&mode=scavenge"
        SIMULATOR = "https://tr74.klanlar.org/game.php?village=42080&screen=place&mode=sim"
    
class Tribal_Wars:
    def __init__(self, web_driver):
        self.web_driver = web_driver
        pass
    
    def sayfa_getirici(fonksiyon):
        def sureli_sayfa_getirici(self, * args, **kwargs):
            self.web_driver.get(fonksiyon())
            time.sleep(10)
        return sureli_sayfa_getirici

    def event_tetikleyici(fonksiyon):
        def sureli_event_tetikleyici(self, * args, **kwargs):
            fonksiyon().click()
            time.sleep(5)
        return sureli_event_tetikleyici
    
    def sayfa_degistirmeyen_islem(fonksiyon):
        def sureli_sayfa_degistirmeyen_islem(self, * args, **kwargs):
            fonksiyon()
            time.sleep(1)
        return sureli_sayfa_degistirmeyen_islem
    

    @sayfa_getirici
    def git_ana_ekran():
        return Sayfalar.Genel.GIRIS_EKRANI

    @sayfa_getirici
    def sec_dunya():
        return Sayfalar.Genel.DUNYA_SECIMI

    @sayfa_getirici
    def git_ictima_meydani(yer = Sayfalar.Ictima_Meydani.TEMIZLEME, adres: Optional[str] = Sayfalar.Ictima_Meydani.TEMIZLEME):
        for _yer in Sayfalar.Ictima_Meydani:
            if yer == _yer:
                adres = yer
                break
        return adres

    @event_tetikleyici
    def gerceklestir_ictima_meydani_temizle_asker_sec(self):
        return self.web_driver.find_element(By.LINK_TEXT, "Tüm birlikler").click()
    
    @sayfa_degistirmeyen_islem
    def al_ictima_meydani_sure_bilgisi(self):
        return self.web_driver.find_element(By.CLASS_NAME, "duration").text #hangi sureyi aldigimiz onemli degil birini alsak yeter

    @event_tetikleyici
    def baslat_ictima_meydani_temizlik(self):
        # if daha once yapilmamissa
        try:
            self.web_driver.find_elements(By.LINK_TEXT, "Başla")[1].click() #tiklarken ikinciye tiklayacagiz.
        except:
            try:
                self.web_driver.find_element(By.LINK_TEXT, "Başla").click()
            except:
                pass
