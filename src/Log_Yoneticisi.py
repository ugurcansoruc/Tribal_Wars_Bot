import os
import datetime
import logging
import Sabit_Degiskenler
import Veri_Yapilari

class Log_Yoneticisi_c:
    def __init__(self):
        # Log klasoru yolu var mi yok mu kontrol edelim
        if not os.path.exists(Sabit_Degiskenler.Klasor_Yollari.LOG_KLASORU_YOLU):
            # Yoksa yeni olusturalim
            os.makedirs(Sabit_Degiskenler.Klasor_Yollari.LOG_KLASORU_YOLU)

        # Log dosyamizi olusturalim
        guncel_zaman = datetime.datetime.now()
        formatlanmis_guncel_zaman = guncel_zaman.strftime("%Y-%m-%d_%H-%M-%S")
        self.log_dosyasi_yolu = "{}/{}.log".format(Sabit_Degiskenler.Klasor_Yollari.LOG_KLASORU_YOLU,
                                                   "Log_{}".format(formatlanmis_guncel_zaman))
        open(self.log_dosyasi_yolu, "x")

        # Loggerimizi ayarlayalim
        self.logger = self.Logger_Olustur()
        self.logger.setLevel(logging.DEBUG)


    def Logger_Olustur(self):
        logging.basicConfig(filename=self.log_dosyasi_yolu,
                            format='%(asctime)s %(message)s',
                            filemode='w')
        return logging.getLogger()

    def Log_Yaz(self, mesaj, log_tipi):
        if log_tipi == Veri_Yapilari.Log_Tipi.HATA:
            self.logger.error("HATA: " + mesaj)
        elif log_tipi == Veri_Yapilari.Log_Tipi.UYARI:
            self.logger.warn("UYARI: " + mesaj)
        elif log_tipi == Veri_Yapilari.Log_Tipi.BILGI:
            self.logger.info("BILGI: " + mesaj)
