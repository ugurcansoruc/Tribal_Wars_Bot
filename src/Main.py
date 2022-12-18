import configparser

import Global_Degiskenler
import Sabit_Degiskenler
import Veri_Yapilari
import Log_Yoneticisi
from Klanlar_Bot_Yonetici import Klanlar_Bot_Yonetici_c



def main():
    # Botumuzu baslatmak icin baslangic ayarlarini alalim
    firefox_yolu, geckodriver_yolu, profil_klasoru_yolu = Config_Dosyasi_Oku()
    Global_Degiskenler.log_yoneticisi_c_o.Log_Yaz("Config.ini dosyasi basariyla okundu", Veri_Yapilari.Log_Tipi.BILGI)

    # Config ayarlarini kontrol edelim
    if "" == firefox_yolu:
        Global_Degiskenler.log_yoneticisi_c_o.Log_Yaz("Firefox.exe yolu bos birakilamaz",
                                                      Veri_Yapilari.Log_Tipi.HATA)
        raise Exception("Firefox.exe yolu boş bırakılamaz")
    elif "" == geckodriver_yolu:
        Global_Degiskenler.log_yoneticisi_c_o.Log_Yaz("Geckodriver.exe yolu bos birakilamaz",
                                                      Veri_Yapilari.Log_Tipi.HATA)
        raise Exception("Geckodriver.exe yolu boş bırakılamaz")
    elif "" == profil_klasoru_yolu:
        Global_Degiskenler.log_yoneticisi_c_o.Log_Yaz("Profil klasoru yolu bos birakilamaz",
                                                      Veri_Yapilari.Log_Tipi.HATA)
        raise Exception("Profil klasörü yolu boş bırakılama.")


    # Bot yöneticisi objemizi olusturalim
    klanlar_bot_yoneticisi_c_o = Klanlar_Bot_Yonetici_c(profil_klasoru_yolu=profil_klasoru_yolu,
                                                        geckodriver_yolu=geckodriver_yolu,
                                                        firefox_yolu=firefox_yolu)

    # Temizleme botunu baslatalim
    #klanlar_bot_yoneticisi_c_o.Temizleme_Botu_Baslat()

    # Bina yukseltme botunu baslatalim
    klanlar_bot_yoneticisi_c_o.Bina_Yukseltme_Botu_Baslat()

def Config_Dosyasi_Oku():
    config = configparser.ConfigParser()
    config.read(Sabit_Degiskenler.Klasor_Yollari.CONFIG_YOLU)

    firefox_yolu        = ""
    geckodriver_yolu    = ""
    profil_klasoru_yolu  = ""
    for section in config.sections():
        for key in config[section]:
            if "firefox_yolu" == key:
                firefox_yolu = config[section][key]
            elif "geckodriver_yolu" == key:
                geckodriver_yolu = config[section][key]
            elif "profil_klasoru_yolu" == key:
                profil_klasoru_yolu = config[section][key]

    return firefox_yolu, geckodriver_yolu, profil_klasoru_yolu

if __name__ == "__main__":
    main()