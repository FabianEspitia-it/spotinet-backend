import imaplib
import email
import re
import os

from email.header import decode_header


def get_code_email(user_email: str) -> str:

    mail = imaplib.IMAP4_SSL(os.getenv("IMAP_SERVER"), port=993)

    mail.login(os.getenv("DISNEY_EMAIL"), os.getenv("DISNEY_PASSWORD"))

    mail.select("inbox")

    status, messages = mail.search(
        None, f'(FROM "{user_email}")')

    if status == "OK":

        message_ids: list[str] = messages[0].split()

        if message_ids != []:

            status, message = mail.fetch(message_ids[-1], "(RFC822)")

            for response in message:

                if isinstance(response, tuple):

                    email_message = email.message_from_bytes(response[1])

                    subject, encoding = decode_header(
                        email_message["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(
                            encoding if encoding else "utf-8")

                    new_subject: str = subject.replace(" ", "").replace(
                        "FW:", "").replace("RV:", "").replace("هدایت:", "")

                    if ("Tu código de acceso único para Disney+".replace(" ", "") in new_subject) or ("Your one-time passcode for Disney+".replace(" ", "") in new_subject) or ("Votre code d'accès à usage unique pour Disney+".replace(" ", "") in new_subject) or ("Jednorazowy kod dostępu do Disney+".replace(" ", "") in new_subject) or ("Il tuo codice d'accesso temporaneo per Disney+".replace(" ", "") in new_subject) or ("Din engångskod till Disney+".replace(" ", "") in new_subject) or ("Seu código de acesso único para o Disney+".replace(" ", "") in new_subject) or ("Dein einmaliger Passcode für Disney+".replace(" ", "") in new_subject):

                        if email_message.is_multipart():
                            for part in email_message.walk():
                                if part.get_content_type() == "text/plain":
                                    body = part.get_payload(decode=True).decode(
                                        "utf-8", errors="ignore")
                        else:
                            body = email_message.get_payload(
                                decode=True).decode("utf-8", errors="ignore")

                        code = re.findall(r'(\d{6})(?:\s|\n|$)', body)

                        if code:
                            print(f"Código: {code[-1]}")
                            return code[-1]

        else:
            status, messages = mail.search(
                None, '(HEADER From "Disney+")')

            counter: int = 0

            if status == "OK":

                message_ids: list[str] = messages[0].split()

                for msg_id in message_ids[::-1]:

                    status, message = mail.fetch(msg_id, "(RFC822)")

                    if status == "OK":

                        for response in message:

                            if isinstance(response, tuple):

                                email_message = email.message_from_bytes(
                                    response[1])

                                to_email: str = email_message.get("To").lower(
                                ).strip().replace("<", "").replace(">", "")

                                if to_email != user_email.lower().strip():
                                    counter += 1

                                    if counter == 10:
                                        return None
                                    continue

                                subject, encoding = decode_header(
                                    email_message["Subject"])[0]
                                if isinstance(subject, bytes):
                                    subject = subject.decode(
                                        encoding if encoding else "utf-8")

                                new_subject: str = subject.replace(" ", "").replace(
                                    "FW:", "").replace("RV:", "").replace("هدایت:", "")

                                if ("Tu código de acceso único para Disney+".replace(" ", "") in new_subject) or ("Your one-time passcode for Disney+".replace(" ", "") in new_subject) or ("Votre code d'accès à usage unique pour Disney+".replace(" ", "") in new_subject) or ("Jednorazowy kod dostępu do Disney+".replace(" ", "") in new_subject) or ("Il tuo codice d'accesso temporaneo per Disney+".replace(" ", "") in new_subject) or ("Din engångskod till Disney+".replace(" ", "") in new_subject) or ("Seu código de acesso único para o Disney+".replace(" ", "") in new_subject) or ("Dein einmaliger Passcode für Disney+".replace(" ", "") in new_subject):

                                    if email_message.is_multipart():
                                        for part in email_message.walk():
                                            if part.get_content_type() == "text/plain":
                                                body = part.get_payload(decode=True).decode(
                                                    "utf-8", errors="ignore")
                                    else:
                                        body = email_message.get_payload(
                                            decode=True).decode("utf-8", errors="ignore")

                                    code = re.findall(
                                        r'(\d{6})(?:\s|\n|$)', body)

                                    if code:
                                        print(f"Código: {code[-1]}")
                                        return code[-1]

    mail.close()


"""
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

        print("entramos")

        wait = WebDriverWait(driver, 4)
        first_input_box = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div.passcode-key')))

        time.sleep(18)

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

        driver.get("https://www.disneyplus.com/identity/login/enter-passcode")

        time.sleep(18)

        wait = WebDriverWait(driver, 4)
        second_input_box = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div.passcode-key')))

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

    time.sleep(18)

    code = get_code_email(user_email=user_email)

    pyperclip.copy(code)

    wait = WebDriverWait(driver, 4)
    third_input_box = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'div.passcode-key')))

    third_input_box.click()

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
"""
