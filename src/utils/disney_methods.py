import imaplib
import email
import re
import os

import time
import pyperclip

from email.header import decode_header

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def get_code_email(user_email: str) -> str:

    mail = imaplib.IMAP4_SSL(os.getenv("IMAP_SERVER"), port=993)

    mail.login(os.getenv("DISNEY_EMAIL"), os.getenv("DISNEY_PASSWORD"))

    mail.select("inbox")

    status, messages = mail.search(
        None, f'(FROM "{user_email}")')

    if status == "OK":

        print("Enter")

        message_ids = messages[0].split()

        status, mensaje = mail.fetch(message_ids[-1], "(RFC822)")

        for respuesta in mensaje:

            if isinstance(respuesta, tuple):

                mensaje_correo = email.message_from_bytes(respuesta[1])

                subject, encoding = decode_header(
                    mensaje_correo["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(
                        encoding if encoding else "utf-8")

                new_subject = subject.replace(" ", "").replace(
                    "FW:", "").replace("RV:", "").replace("هدایت:", "")

                if "Tu código de acceso único para Disney+".replace(" ", "") in new_subject:

                    if mensaje_correo.is_multipart():
                        for part in mensaje_correo.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode(
                                    "utf-8", errors="ignore")
                    else:
                        body = mensaje_correo.get_payload(
                            decode=True).decode("utf-8", errors="ignore")

                    code = re.findall(r'(\d{6})(?:\s|\n|$)', body)

                    if code:
                        print(f"Código: {code[-1]}")
                        return code[-1]

    mail.close()


def introduce_credentials(user_email: str, new_password: str):
    driver = webdriver.Chrome()

    driver.get("https://www.disneyplus.com/identity/login/enter-email")

    email_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='email']"))
    )

    email_element.send_keys(user_email)

    submit_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[data-testid="continue-btn"]'))
    )
    submit_button.click()

    try:

        first_input_box = driver.find_element(
            By.CSS_SELECTOR, 'div.passcode-key')

        time.sleep(15)

        code_one = get_code_email(
            user_email=user_email)

        pyperclip.copy(code_one)

        first_input_box.click()

        action = ActionChains(driver)
        action.key_down(Keys.CONTROL).send_keys(
            'v').key_up(Keys.CONTROL).perform()

        continue_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[data-testid="continue-btn"]'))
        )

        time.sleep(2)

        continue_button.click()

    except:
        password_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="password"]'))
        )

        driver.get("https://www.disneyplus.com/identity/login/enter-passcode")

        time.sleep(15)

        second_input_box = driver.find_element(
            By.CSS_SELECTOR, 'div.passcode-key')

        code_two = get_code_email(
            user_email=user_email)

        pyperclip.copy(code_two)

        second_input_box.click()

        action = ActionChains(driver)
        action.key_down(Keys.CONTROL).send_keys(
            'v').key_up(Keys.CONTROL).perform()

        continue_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[data-testid="continue-btn"]'))
        )

        time.sleep(2)

        continue_button.click()

        time.sleep(2)

    time.sleep(10)

    driver.get(
        "https://www.disneyplus.com/es-419/commerce/account?pinned=true")

    time.sleep(2)

    user_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[data-testid="selected-avatar-image"]'))
    )

    user_element.click()

    time.sleep(2)

    driver.get(
        "https://www.disneyplus.com/identity/update-credentials?updateType=ChangePassword")

    time.sleep(22)

    code = get_code_email(user_email=user_email)

    pyperclip.copy(code)

    div_element = driver.find_element(By.CSS_SELECTOR, 'div.passcode-key')

    div_element.click()

    action = ActionChains(driver)
    action.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

    continue_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[data-testid="continue-btn"]'))
    )

    continue_button.click()

    time.sleep(1)

    password_input = driver.find_element(By.ID, "password")

    password_input.send_keys(new_password)

    submit_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[data-testid="continue-btn"]'))
    )

    submit_button.click()

    time.sleep(2)

    driver.quit()
