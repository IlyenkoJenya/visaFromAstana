import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import LOGIN, PASSWORD, CHECK_PAGE, BOT_TOKEN, CHAT_ID_SERVICE, CHAT_ID
import telebot

login = LOGIN
password = PASSWORD
checkPage = CHECK_PAGE


bot = telebot.TeleBot(BOT_TOKEN)
chatId_service = CHAT_ID_SERVICE
chatId = CHAT_ID
def mainFunc():
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")
    options.add_argument("--headless=new")  # новый headless
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # реальный user-agent
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/140.0.7339.133 Safari/537.36")

    driver = webdriver.Chrome(options=options)

    # убрать webdriver-след
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"}
    )
    driver.maximize_window()


    driver.get(checkPage)

    ok_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='OK']"))
    )
    ok_button.click()
    time.sleep(2)


    input_imail = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'user_email'))
    )

    input_imail.send_keys(login)
    input_password = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'user_password'))
    )
    input_password.send_keys(password)


    checkbox = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "policy_confirmed"))
    )
    driver.execute_script("arguments[0].click();", checkbox)

    driver.find_element(By.NAME, "commit").click()

    print('я тут')
    # Ждём появления строки с Astana
    astana_row = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//tr[td[contains(., 'Astana')]]"))
    )

    # Взять текст второй ячейки (status)
    status_text = astana_row.find_element(By.XPATH, "./td[@class='text-right']").text.strip()

    if status_text != "В данный момент запись невозможна.":
        bot.send_message(chatId, 'Запись есть ✅', parse_mode='html')
    else:
        bot.send_message(chatId_service, 'Записи нет ❌', parse_mode='html')
    time.sleep(120)

if __name__ == '__main__':
    while True:
        try:
            mainFunc()
        except Exception as e:
            bot.send_message(chatId_service, f'ошибка {e}', parse_mode='html')
            print(f"ошибка: {str(e)}")
            time.sleep(10)