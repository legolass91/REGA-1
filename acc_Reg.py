import os
import time
import random
import csv
import subprocess
import logging
from datetime import datetime
from pytz import timezone
from selenium.common import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from generate_data import generate_login, generate_password, generate_last_name, generate_first_name
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from fake_useragent import UserAgent
from db import DB

cwd = os.getcwd()
extension_path = cwd + '/capsolver_extension'

file_log = logging.FileHandler('journal.log', mode='w')
console_out = logging.StreamHandler()
logging.basicConfig(handlers=(file_log, console_out), level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s',
                    datefmt=datetime.now().astimezone(timezone('Europe/Minsk')).strftime('%H:%M:%S'), encoding='utf-8')


def use_vpn():
    logging.info('Выключаем ВПН')
    subprocess.call('taskkill /F /IM Windscribe.exe', shell=True)  # Выключаем VPN
    logging.info('Включаем ВПН')
    subprocess.call('vpnwinscribe.bat', shell=True)
    time.sleep(5)


def get_chromedriver():
    logging.info('Запуск функции get_chromedriver')
    user_agent = UserAgent()
    random_user_agent = user_agent.random
    chrome_options = webdriver.ChromeOptions()
    logging.info('Присваиваем фейковый user-agent')
    chrome_options.add_argument(f'user-agent={random_user_agent}')
    chrome_options.add_argument("--load-extension={0}".format(extension_path))
    logging.info('Отключаем в браузере режим автоматизации')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(options=chrome_options)
    logging.info(f'Установлен следующий user-agent:{random_user_agent}')
    return driver


def writer_csv(data):
    logging.info('Запуск функции для создания файла accounts.csv в режиме "append" ')
    file_name = 'accounts.csv'
    with open(file_name, 'a', newline='') as csv_file:
        write = csv.writer(csv_file)
        write.writerow(data.values())


def main():
    logging.info('Запуск функции main для регистрации аккаунта')
    while True:
        try:
            use_vpn()
        except NoSuchElementException:
            logging.exception('NoSuchElementException')
            pass
        logging.info('Запуск браузера!')
        driver = get_chromedriver()
        logging.info('Задаем полноэкранный режим')
        driver.maximize_window()
        wait = WebDriverWait(driver, timeout=100)
        logging.info('Переходим на сайт регистрации')
        driver.get(url='https://www.bing.com/')
        time.sleep(6)
        logging.info('Нажимаем на кнопку "Войти"')
        driver.find_element(By.CSS_SELECTOR, '#id_s').click()
        time.sleep(2)
        logging.info('Нажимаем войти с личной учетной записью')
        driver.find_element(By.CSS_SELECTOR, '#b_idProviders > li:nth-child(1) > a > span').click()
        time.sleep(2)
        logging.info('Нажимаем создать ее')
        driver.find_element(By.CSS_SELECTOR, '#signup').click()
        time.sleep(2)
        logging.info('Нажимаем на поле ввода')
        driver.find_element(By.CSS_SELECTOR, '#liveSwitch').click()
        time.sleep(2)
        while True:
            logging.info('Генерируем Имя')
            first_name = generate_first_name()
            logging.info('Генерируем username')
            username = first_name + generate_login()
            logging.info('Генерируем пароль')
            password = generate_password()
            logging.info('Генерируем Фамилию')
            last_name = generate_last_name()
            logging.info('Находим поле ввода')
            login_input = driver.find_element(By.CSS_SELECTOR, '#MemberName')
            logging.info('Очищаем поле ввода')
            login_input.clear()
            logging.info('Вводим логин')
            login_input.send_keys(username)
            time.sleep(3)
            logging.info('Выбор рандомного домена')
            domain = driver.find_element(By.XPATH, "//select[@id='LiveDomainBoxList']")
            select = Select(domain)
            random_choice = random.randint(0, 1)
            desired_option = 'hotmail.com' if random_choice == 0 else 'outlook.com'
            logging.info('Подставляем домен')
            select.select_by_value(desired_option)
            logging.info('Нажимаем далее')
            driver.find_element(By.CSS_SELECTOR, '#iSignupAction').click()
            time.sleep(3)
            try:
                logging.warning('Проверяем - если мы перешли в поле для ввода пароля, то мы прошли проверку логина!')
                password_input = driver.find_element(By.CSS_SELECTOR, '#PasswordInput')
                logging.info('Вводим пароль')
                password_input.send_keys(password)
                time.sleep(2)
                break
            except NoSuchElementException:
                logging.exception('NoSuchElementException')
                logging.warning('Епана врот, токой логин уже есть!')
                continue
        logging.info('Нажимаем далее')
        driver.find_element(By.CSS_SELECTOR, '#iSignupAction').click()
        time.sleep(2)
        logging.info('Ввод фамилии')
        driver.find_element(By.CSS_SELECTOR, '#LastName').send_keys(last_name)
        time.sleep(1)
        logging.info('Ввод имени')
        driver.find_element(By.CSS_SELECTOR, '#FirstName').send_keys(first_name)
        time.sleep(1)
        logging.info('Нажимаем далее')
        driver.find_element(By.CSS_SELECTOR, '#iSignupAction').click()
        time.sleep(3)
        logging.info('Берем самый пиздатый регион')
        country = Select(wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#Country'))))
        country.select_by_value('NL')  # выбор региона
        # country = country.first_selected_option.text
        time.sleep(2)
        logging.warning('Переходим к вводу дня рождения')
        birth_day = Select(wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#BirthDay'))))
        birth_day.select_by_index(random.randint(1, 28))  # выбор дня
        # birth_day = birth_day.first_selected_option.text
        time.sleep(2)
        logging.warning('Находим барменю с выбором месяца')
        birt_month = Select(wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#BirthMonth'))))
        birt_month.select_by_index(random.randint(1, 12))
        # birt_month = birt_month.first_selected_option.text
        time.sleep(2)
        logging.warning('Находим и выбираем год рождения')
        birt_year = driver.find_element(By.CSS_SELECTOR, '#BirthYear')
        birt_year.send_keys(str(random.randint(1970, 2001)))
        time.sleep(2)
        logging.info('Нажимаем далее')
        driver.find_element(By.CSS_SELECTOR, '#iSignupAction').click()
        time.sleep(5)

        try:
            driver.find_element(By.CSS_SELECTOR, '#HipPaneForm')
            logging.info('Если выпал ввод номера - иди нахуй!')
            driver.quit()
            continue
        except NoSuchElementException:
            logging.exception('NoSuchElementException')
            logging.info('Епта номер вводить не нужно, погнали дальше!')
            pass

        wait_time = 10
        try:
            logging.info('Решаем супер капчу')
            captcha_solution = driver.find_element(By.CSS_SELECTOR, '#pageControlHost')
            while captcha_solution.is_displayed():
                time.sleep(wait_time)
                wait_time += 10
                logging.info('Если нашли еще одну капчу, то делаем ее!')
                captcha_solution = driver.find_element(By.CSS_SELECTOR, '#pageControlHost')
        except NoSuchElementException:
            logging.exception('NoSuchElementException')
            pass
        logging.info('Нажимаем на rewords')
        driver.find_element(By.XPATH, "//a[@id='id_rh']").click()
        time.sleep(5)
        logging.info('Переходим к цели "Получить 200 баллов"')
        driver.get(url='''https://www.bing.com/rewards/panelflyout?&partnerId=BingRewards&date=
                   '04/27/2024&ru=https%3A%2F%2Fwww.bing.com%2F%3Fwlexpsignin%3D1%26wlexpsignin'
                   '%3D1%26wlexpsignin%3D1&requestedLayout=onboarding&form=rwfobc''')
        time.sleep(5)
        logging.info('Выбираем цель')
        driver.find_element(By.CSS_SELECTOR, '#Card_2 > div.ms-StackItem.ellipsis.root-141').click()
        time.sleep(3)
        logging.info('Нажимаем подтвердить')
        driver.find_element(By.CSS_SELECTOR, '#slideshow_nb > span > span').click()
        time.sleep(3)
        logging.info('Возвращаемся на предыдущую страницу')
        driver.back()
        time.sleep(3)
        logging.info('Вуаля, 200 баллов в кармане!')
        logging.info('Записываем куки')
        cookies = driver.get_cookies()
        time.sleep(10)
        logging.info('Записываем все данные в БД')
        data = {
            "account_id": None,
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "password": password,
            "email": username + desired_option,
            "region": country,
            "birth_day": birth_day,
            "birth_month": birt_month,
            "birth_year": birt_year,
            "score": 0,
            "active": True,
            "cookies": cookies,
        }
        writer_csv(data)
        db: DB
        with DB() as db:
            db.create_new_account(
                account_id=None,
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=password,
                email=username + desired_option,
                region=country,
                birth_day=birth_day,
                birth_month=birt_month,
                birth_year=birt_year,
                score=0,
                active=None,
                cookies=cookies
            )
            logging.info('Съебываем')
            driver.quit()


if __name__ == '__main__':
    filename = 'accounts.csv'
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ['account_id', 'first_name', 'last_name', 'username', 'password', 'email', 'region', 'birth_day',
             'birth_month', 'birth_year', 'score', 'active', 'cookies'])
    with DB() as db:
        db.create_schema()
    main()
