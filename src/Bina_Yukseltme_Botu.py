import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import Global_Degiskenler
import Sabit_Degiskenler
import Veri_Yapilari

class Bina_Yukseltme_Botu_c:
    def __init__(self, driver):
        self.driver                 = driver
        self.bina_ismi_tr           = ["Ana Bina", "Kışla", "Ahır", "Atölye", "Demirci", "İçtima Meydanı", "Heykel",
                                       "Pazar", "Oduncu", "Kil Ocağı", "Demir Madeni", "Çiftlik", "Depo", "Gizli Depo",
                                       "Sur", "Akademi"]
        self.bina_ismi_ing          = ["main", "barracks", "stable", "garage", "smith", "place", "statue", "market",
                                       "wood", "stone", "iron", "farm", "storage", "hide", "wall", "snob"]
        self.bina_listesi           = []
        self.yukseltilecek_binalar  = []
        self.yukseltilmis_binalar   = []

        # Bina listesini olusturalim
        self.Bina_Listesi_Olustur()

    def Ana_Bina_Sayfasini_Ac(self):
        self.driver.get(Sabit_Degiskenler.Sayfa_Linkleri.ANA_BINA)
        Global_Degiskenler.log_yoneticisi_c_o.Log_Yaz("Ana Bina sayfasina gidildi", Veri_Yapilari.Log_Tipi.BILGI)
        time.sleep(1)

    def Bina_Listesi_Olustur(self):
        for i, bina_ismi in enumerate(self.bina_ismi_tr):
            yeni_bina = Bina(driver=self.driver, bina_ismi_tr=bina_ismi, bina_ismi_ing=self.bina_ismi_ing[i])
            self.bina_listesi.append(yeni_bina)
            Global_Degiskenler.log_yoneticisi_c_o.Log_Yaz("{} binasi olusturuldu".format(bina_ismi),
                                                          Veri_Yapilari.Log_Tipi.BILGI)

    def Bina_Bilgileri_Guncelle(self):
        for bina in self.bina_listesi:
            bina.Bina_Bilgileri_Guncelle()

    def Yukseltilecek_Bina_Bilgisi_Al(self):
        # Kullanicidan yukseltmek istedigi binalari almadan once mevcut bina bilgilerini guncelleyelim
        self.Bina_Bilgileri_Guncelle()

        # Kullanciya bina listesini gosterelim ve input alalim
        for i, bina_ismi in enumerate(self.bina_ismi_tr):
            print("{}\t-\t{}".format(i, bina_ismi))

        self.yukseltilecek_binalar = input("Yukseltmek istediginiz binalari sirasiyla yaziniz (ör: 2 3 6): ")
        Global_Degiskenler.log_yoneticisi_c_o.Log_Yaz(
            "Kullanicidan bina yukseltme bilgisi alindi: {}".format(self.yukseltilecek_binalar),
            Veri_Yapilari.Log_Tipi.BILGI)

        # Str to int donusumu yapalim
        self.yukseltilecek_binalar = self.yukseltilecek_binalar.split(" ")
        for i, yukseltilece_bina_id in enumerate(self.yukseltilecek_binalar):
            self.yukseltilecek_binalar[i] = int(yukseltilece_bina_id)


    def Bina_Yukseltme_Baslat(self):
        # Yukseltilecek bina bilgisi alalim
        self.Yukseltilecek_Bina_Bilgisi_Al()

        while len(self.yukseltilecek_binalar) != len(self.yukseltilmis_binalar):
            # Ana bina sayfasini acalim
            self.Ana_Bina_Sayfasini_Ac()

            # Bina bilgilerini guncelleyelim
            self.Bina_Bilgileri_Guncelle()

            for yukseltilecek_bina_id in self.yukseltilecek_binalar:
                # Eger yukseltilebilirse binayi yukseltelim
                if True == self.bina_listesi[yukseltilecek_bina_id].bina_yukseltilebilir_mi:
                    self.bina_listesi[yukseltilecek_bina_id].Bina_Yukselt()
                    self.yukseltilmis_binalar.append(yukseltilecek_bina_id)

            # Kuyruk dolu mu kontrol et
            kuyruk_dolu_mu_b = self.Kuyruk_Dolu_Mu()
            # Kuyruk doluysa kuyrugun bitme suresini hesaplayalim ve ona gore sleep atalim
            if True == kuyruk_dolu_mu_b:
                toplam_sure_sn = self.Kuyruk_Suresi_Hesapla()
                print(toplam_sure_sn)
                time.sleep(toplam_sure_sn + 10)

            # Eger yeterli hammadde yoksa 20 dk bekleyelim
            time.sleep(1200)

        self.driver.quit()

    def Kuyruk_Dolu_Mu(self):
        try:
            self.driver.find_element(By.ID, "buildorder_1")
            return True
        except:
            return False

    def Kuyruk_Suresi_Hesapla(self):
        kuyruk_1_xpath = "//*[@id=\"buildqueue\"]/tr[2]/td[2]/span"
        kuyruk_2_xpath = "//*[@id=\"buildorder_1\"]/td[2]/span"

        time.sleep(10)

        kuyruk_1_sure_str = self.driver.find_element(By.XPATH, kuyruk_1_xpath).text
        kuyruk_2_sure_str = self.driver.find_element(By.XPATH, kuyruk_2_xpath).text

        kuyruk_1_sure_sn = self.Sureyi_Saniyeye_Cevir(kuyruk_1_sure_str)
        kuyruk_2_sure_sn = self.Sureyi_Saniyeye_Cevir(kuyruk_2_sure_str)

        return kuyruk_1_sure_sn + kuyruk_2_sure_sn

    def Sureyi_Saniyeye_Cevir(self, sure_str):
        sure_list   = sure_str.split(":")
        sure        = int(sure_list[0]) * 3600 + int(sure_list[1]) * 60 + int(sure_list[2])
        return sure

class Bina:
    def __init__(self, driver, bina_ismi_tr, bina_ismi_ing):
        self.driver                     = driver
        self.bina_ismi_tr               = bina_ismi_tr
        self.bina_ismi_ing              = bina_ismi_ing
        self.ihtiyac_odun               = None
        self.ihtiyac_kil                = None
        self.su_anki_seviye             = None
        self.ihtiyac_demir              = None
        self.bina_yukseltiliyor_mu      = False
        self.bina_yukseltilebilir_mi    = False
        self.yapim_suresi_sn            = None

        # Bina bilgilerini alalim
        self.Bina_Bilgileri_Guncelle()

    def Bina_Bilgileri_Guncelle(self):
        self.Ihtiyac_Odun_Guncelle()
        self.Ihtiyac_Kil_Guncelle()
        self.Ihtiyac_Demir_Guncelle()
        self.Su_Anki_Seviye_Guncelle()
        self.Bina_Yukseltilebilir_Mi_Guncelle()

    def Ihtiyac_Odun_Guncelle(self):
        try:
            ihtiyac_odun_xpath  = "//*[@id=\"main_buildrow_{}\"]/td[2]/span".format(self.bina_ismi_ing)
            self.ihtiyac_odun   = int(self.driver.find_element(By.XPATH, ihtiyac_odun_xpath).text)
        except:
            self.ihtiyac_odun   = None

        Global_Degiskenler.log_yoneticisi_c_o.Log_Yaz(
            "{} binasinin ihtiyac odunu guncellendi".format(self.bina_ismi_tr),
            Veri_Yapilari.Log_Tipi.BILGI)

    def Ihtiyac_Kil_Guncelle(self):
        try:
            ihtiyac_kil_xpath   = "//*[@id=\"main_buildrow_{}\"]/td[3]/span".format(self.bina_ismi_ing)
            self.ihtiyac_kil    = int(self.driver.find_element(By.XPATH, ihtiyac_kil_xpath).text)
        except:
            self.ihtiyac_kil    = None

        Global_Degiskenler.log_yoneticisi_c_o.Log_Yaz(
            "{} binasinin ihtiyac kili guncellendi".format(self.bina_ismi_tr),
            Veri_Yapilari.Log_Tipi.BILGI)

    def Ihtiyac_Demir_Guncelle(self):
        try:
            ihtiyac_demir_xpath = "//*[@id=\"main_buildrow_{}\"]/td[4]/span".format(self.bina_ismi_ing)
            self.ihtiyac_demir  = int(self.driver.find_element(By.XPATH, ihtiyac_demir_xpath).text)
        except:
            self.ihtiyac_demir  = None

        Global_Degiskenler.log_yoneticisi_c_o.Log_Yaz(
            "{} binasinin ihtiyac demiri guncellendi".format(self.bina_ismi_tr),
            Veri_Yapilari.Log_Tipi.BILGI)

    def Su_Anki_Seviye_Guncelle(self):
        try:
            su_anki_seviye_xpath    = "//*[@id=\"main_buildrow_{}\"]/td[1]/span".format(self.bina_ismi_ing)
            self.su_anki_seviye     = int(self.driver.find_element(By.XPATH, su_anki_seviye_xpath).text.split(" ")[1])
        except:
            self.su_anki_seviye     = None

        Global_Degiskenler.log_yoneticisi_c_o.Log_Yaz(
            "{} binasinin su anki seviyesi guncellendi".format(self.bina_ismi_tr),
            Veri_Yapilari.Log_Tipi.BILGI)

    def Yapim_Suresi_Guncelle(self):
        try:
            yapim_suresi_xpath      = "//*[@id=\"main_buildrow_{}\"]/td[5]/span".format(self.bina_ismi_ing)
            yapim_suresi            = self.driver.find_element(By.XPATH, yapim_suresi_xpath).text.split(":")
            self.yapim_suresi_sn    = int(yapim_suresi[0]) * 3600 + int(yapim_suresi[1]) * 60 + int(yapim_suresi[2])
        except:
            self.yapim_suresi_sn    = None

        Global_Degiskenler.log_yoneticisi_c_o.Log_Yaz(
            "{} binasinin yapim suresi guncellendi".format(self.bina_ismi_tr),
            Veri_Yapilari.Log_Tipi.BILGI)

    def Bina_Yukseltilebilir_Mi_Guncelle(self):
        try:
            bina_yukseltememe_uyarisi_xpath = "//*[@id=\"main_buildrow_{}\"]/td[7]/div".format(self.bina_ismi_ing)
            bina_yukseltememe_uyarisi_div   = self.driver.find_element(By.XPATH, bina_yukseltememe_uyarisi_xpath)
            self.bina_yukseltilebilir_mi = False
        except:
            self.bina_yukseltilebilir_mi = True

    def Bina_Yukselt(self):
        try:
            bina_yukseltme_xpath = "//*[@id=\"main_buildlink_{}_{}\"]".format(self.bina_ismi_ing,
                                                                              self.su_anki_seviye + 1)

            bina_yukseltme_linki = self.driver.find_element(By.XPATH, bina_yukseltme_xpath).get_attribute("href")
            self.driver.get(bina_yukseltme_linki)
            time.sleep(10)
            self.bina_yukseltiliyor_mu  = True
            self.su_anki_seviye         = self.su_anki_seviye + 1

            Global_Degiskenler.log_yoneticisi_c_o.Log_Yaz(
                "{} binasi yukseltilmeye baslandi".format(self.bina_ismi_tr),
                Veri_Yapilari.Log_Tipi.BILGI)
            return True
        except:
            Global_Degiskenler.log_yoneticisi_c_o.Log_Yaz(
                "{} binasi yukseltilemedi".format(self.bina_ismi_tr),
                Veri_Yapilari.Log_Tipi.BILGI)
            return False