from Tribal_Wars import Tribal_Wars_Bot
import time

def main():
    tribal_wars_bot = Tribal_Wars_Bot()
    tribal_wars_bot.oto_temizlik_yagmasi_baslat()

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()