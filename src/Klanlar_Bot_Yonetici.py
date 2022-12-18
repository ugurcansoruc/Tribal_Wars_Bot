import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

import Global_Degiskenler
import Sabit_Degiskenler
import Veri_Yapilari
from Bina_Yukseltme_Botu import Bina_Yukseltme_Botu_c

class Klanlar_Bot_Yonetici_c:
    def __init__(self, profil_klasoru_yolu, geckodriver_yolu = r"geckodriver.exe",
                 firefox_yolu = r"C:\Program Files\Mozilla Firefox\firefox.exe"):
        if profil_klasoru_yolu == "":
            raise Exception("Profil klasörü yolu boş bırakılamaz.")

        self.profil_klasoru_yolu        = profil_klasoru_yolu
        self.geckodriver_yolu           = geckodriver_yolu
        self.firefox_yolu               = firefox_yolu
        self.driver                     = None
        self.driver_ayarlari            = None

        # Baslangic ayarlarini yapalim
        self.Baslangic_Ayarlarini_Yap()

        self.bina_yukseltme_botu_c_o    = Bina_Yukseltme_Botu_c(driver=self.driver)

    def Baslangic_Ayarlarini_Yap(self):
        # Driver ayarlarini yapalim
        self.Driver_Ayarlarini_Yap()
        # Oyunu acalim
        self.Oyunu_Ac()

    def Driver_Ayarlarini_Yap(self):
        try:
            ayarlar                 = Options()
            ayarlar.binary_location = self.firefox_yolu
            ayarlar.profile         = self.profil_klasoru_yolu
            self.driver_ayarlari     = ayarlar
            self.driver             = webdriver.Firefox(executable_path=self.geckodriver_yolu,
                                                        options=self.driver_ayarlari)
        except e as Exception:
            Global_Degiskenler.log_yoneticisi_c_o.Log_Yaz("Driver ayarlari yapilirken hata",
                                                          Veri_Yapilari.Log_Tipi.HATA)

        Global_Degiskenler.log_yoneticisi_c_o.Log_Yaz("Driver icin baslangic ayarlari yapildi",
                                                      Veri_Yapilari.Log_Tipi.BILGI)

    def Oyunu_Ac(self):
        self.driver.get(Sabit_Degiskenler.Sayfa_Linkleri.GIRIS_EKRANI)
        time.sleep(1)
        Global_Degiskenler.log_yoneticisi_c_o.Log_Yaz("Giris ekrani sayfasi acildi", Veri_Yapilari.Log_Tipi.BILGI)

        self.driver.get(Sabit_Degiskenler.Sayfa_Linkleri.DUNYA_SECIMI)
        time.sleep(1)
        Global_Degiskenler.log_yoneticisi_c_o.Log_Yaz("Dunya secimi sayfasi acildi", Veri_Yapilari.Log_Tipi.BILGI)

        self.driver.get(Sabit_Degiskenler.Sayfa_Linkleri.GENEL_BAKİS)
        time.sleep(1)
        Global_Degiskenler.log_yoneticisi_c_o.Log_Yaz("Genel bakis sayfasi acildi", Veri_Yapilari.Log_Tipi.BILGI)

    def Temizleme_Botu_Baslat(self):
        Global_Degiskenler.log_yoneticisi_c_o.Log_Yaz("Temizleme botu baslatiliyor",
                                                      Veri_Yapilari.Log_Tipi.BILGI)
        while True:
            # Temizleme sayfasini acalim
            self.driver.get(Sabit_Degiskenler.Sayfa_Linkleri.Ictima_Meydani.TEMIZLEME)
            Global_Degiskenler.log_yoneticisi_c_o.Log_Yaz("Ictima meydanindan Temizleme sayfasi acildi",
                                                          Veri_Yapilari.Log_Tipi.BILGI)
            time.sleep(1)

            # Tum askerleri secelim
            self.driver.find_element(By.XPATH,
                                     "//*[@id=\"scavenge_screen\"]/div/div[1]/table/tbody/tr[2]/td[7]/a").click()
            Global_Degiskenler.log_yoneticisi_c_o.Log_Yaz("Tum askerleri sec butonuna basildi",
                                                          Veri_Yapilari.Log_Tipi.BILGI)
            time.sleep(1)

            # Hangi sureyi aldigimiz onemli degil birini alsak yeter
            zaman_bilgisi = self.driver.find_element(By.CLASS_NAME, "duration").text

            if "" != zaman_bilgisi:
                # If daha once yapilmamissa
                try:
                    # Tiklarken ikinciye tiklayacagiz.
                    baslat_butonu_2 = self.driver.find_elements(By.XPATH,
                                         "//*[@id=\"scavenge_screen\"]/div/div[2]/div[2]/div[3]/div/div[2]/a[1]")
                    baslat_butonu_2.click()
                    Global_Degiskenler.log_yoneticisi_c_o.Log_Yaz("2. Baslat tusuna basildi",
                                                                  Veri_Yapilari.Log_Tipi.BILGI)
                except:
                    try:
                        # Ikıncı temizleme açik degilse ilkine tiklayalim
                        baslat_butonu_1 = self.driver.find_element(By.XPATH,
                                            "//*[@id=\"scavenge_screen\"]/div/div[2]/div[1]/div[3]/div/div[2]/a[1]")
                        baslat_butonu_1.click()
                        Global_Degiskenler.log_yoneticisi_c_o.Log_Yaz("1. Baslat tusuna basildi",
                                                                      Veri_Yapilari.Log_Tipi.BILGI)
                    except:
                        Global_Degiskenler.log_yoneticisi_c_o.Log_Yaz("Harhangi bir yagma baslat aktif degil",
                                                                      Veri_Yapilari.Log_Tipi.UYARI)
                        pass
                time.sleep(10)

                # Sayfayi kapatalim
                self.driver.quit()
                time.sleep(10)

                # Driver ayarlarini bastan yapalim
                self.Driver_Ayarlarini_Yap()
                time.sleep(5)

                # Sayfalari tekrar acalim
                self.driver.get(Sabit_Degiskenler.Sayfa_Linkleri.DUNYA_SECIMI)
                time.sleep(1)

                self.driver.get(Sabit_Degiskenler.Sayfa_Linkleri.Ictima_Meydani.TEMIZLEME)
                time.sleep(1)

            time.sleep(10)

    def Bina_Yukseltme_Botu_Baslat(self):
        Global_Degiskenler.log_yoneticisi_c_o.Log_Yaz("Bina Yukseltme botu baslatiliyor",
                                                      Veri_Yapilari.Log_Tipi.BILGI)

        self.bina_yukseltme_botu_c_o.Bina_Yukseltme_Baslat()


