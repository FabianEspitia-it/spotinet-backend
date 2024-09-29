import os
import imaplib
import email
import re

import time

from email.header import decode_header

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_netflix_code_email(user_email: str, netflix_password: str, email_subject: str) -> str:

    mail = imaplib.IMAP4_SSL(os.getenv("IMAP_SERVER"))

    mail.login(os.getenv("NETFLIX_EMAIL"), os.getenv("NETFLIX_PASSWORD"))

    mail.select("inbox")

    status, messages = mail.search(
        None, f'(FROM "{user_email}")')

    if status == "OK":
        message_ids = messages[0].split()

        for msg_id in message_ids:
            status, mensaje = mail.fetch(msg_id, "(RFC822)")

            if status == "OK":
                for respuesta in mensaje:
                    if isinstance(respuesta, tuple):
                        mensaje_correo = email.message_from_bytes(respuesta[1])

                        subject, encoding = decode_header(
                            mensaje_correo["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(
                                encoding if encoding else "utf-8")

                        new_subject: str = subject.replace(
                            " ", "").replace("RV:", "").replace("FW:", "")

                        if email_subject in new_subject:

                            if mensaje_correo.is_multipart():
                                for part in mensaje_correo.walk():
                                    if part.get_content_type() == "text/plain":
                                        body = part.get_payload(decode=True).decode(
                                            "utf-8", errors="ignore")
                            else:
                                body = mensaje_correo.get_payload(
                                    decode=True).decode("utf-8", errors="ignore")

                            print(body)

                            pattern = None

                            if email_subject == "Tu código de acceso temporal de Netflix".replace(" ", ""):

                                pattern = r'https://www\.netflix\.com/account/travel/verify\?nftoken=[\w-]+.*'
                            else:
                                pattern = r'https://www.netflix.com/account/update-primary-location[\w-]+.*'

                            match = re.search(pattern, body)

                            if match:
                                link = match.group(0).replace(">", "")

                                driver = webdriver.Chrome()

                                driver.get(link)

                                time.sleep(2)

                                email_element = WebDriverWait(driver, 5).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH, "//*[@id=':r0:']"))
                                )

                                email_element.send_keys(user_email)

                                password_element = WebDriverWait(driver, 5).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH, "//*[@id=':r3:']"))
                                )

                                password_element.send_keys(netflix_password)

                                submit_button = WebDriverWait(driver, 5).until(
                                    EC.element_to_be_clickable(
                                        (By.CSS_SELECTOR, 'button[data-uia="login-submit-button"]'))
                                )

                                submit_button.click()

                                time.sleep(2)

                                if email_subject == "Tu código de acceso temporal de Netflix".replace(" ", ""):

                                    code = WebDriverWait(driver, 5).until(
                                        EC.presence_of_element_located(
                                            (By.CSS_SELECTOR, '[data-uia="travel-verification-otp"]'))
                                    )

                                    return code.text

                                else:
                                    button = WebDriverWait(driver, 5).until(
                                        EC.element_to_be_clickable(
                                            (By.CSS_SELECTOR, 'button[data-uia="set-primary-location-action"]'))
                                    )

                                    button.click()

                                    time.sleep(2)

                                    return "Process completed"

                            else:
                                return 'No se encontró ningún link'

                        else:
                            return "No se encontró el asunto del correo"

    mail.close()


def get_netflix_session_code(user_email: str):
    mail = imaplib.IMAP4_SSL(os.getenv("IMAP_SERVER"))

    mail.login(os.getenv("NETFLIX_EMAIL"), os.getenv("NETFLIX_PASSWORD"))

    mail.select("inbox")

    status, messages = mail.search(
        None, f'(FROM "{user_email}")')

    if status == "OK":
        message_ids = messages[0].split()

        for msg_id in message_ids[::-1]:
            status, mensaje = mail.fetch(msg_id, "(RFC822)")

            if status == "OK":
                for respuesta in mensaje:
                    if isinstance(respuesta, tuple):
                        mensaje_correo = email.message_from_bytes(
                            respuesta[1])

                        subject, encoding = decode_header(
                            mensaje_correo["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(
                                encoding if encoding else "utf-8")

                        new_subject: str = subject.replace(
                            " ", "").replace("RV:", "").replace("FW:", "")

                        if "Tu código de inicio de sesión".replace(" ", "") in new_subject:

                            if mensaje_correo.is_multipart():
                                for part in mensaje_correo.walk():
                                    if part.get_content_type() == "text/plain":
                                        body = part.get_payload(decode=True).decode(
                                            "utf-8", errors="ignore")
                            else:
                                body = mensaje_correo.get_payload(
                                    decode=True).decode("utf-8", errors="ignore")

                            print(body)

                            code = re.findall(
                                r'(\d{4})(?:\s|\n|$)', body)

                            if code:
                                print(code[-1])
                                return code[-1]

                            else:
                                return "No se encontró el código"

    mail.close()
