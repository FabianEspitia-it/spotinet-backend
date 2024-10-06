import os
import imaplib
import email
import re

from email.header import decode_header


def get_netflix_code_email(user_email: str, email_subject: str) -> str:

    mail = imaplib.IMAP4_SSL(os.getenv("IMAP_SERVER"))

    mail.login(os.getenv("NETFLIX_EMAIL"), os.getenv("NETFLIX_PASSWORD"))

    mail.select("inbox")

    status, messages = mail.search(
        None, f'(FROM "{user_email}")')

    if status == "OK":

        message_ids: list[str] = messages[0].split()

        if message_ids != []:

            for msg_id in message_ids[::-1]:

                status, message = mail.fetch(msg_id, "(RFC822)")

                if status == "OK":
                    for response in message:
                        if isinstance(response, tuple):
                            email_message = email.message_from_bytes(
                                response[1])

                            subject, encoding = decode_header(
                                email_message["Subject"])[0]
                            if isinstance(subject, bytes):
                                subject = subject.decode(
                                    encoding if encoding else "utf-8")

                            new_subject: str = subject.replace(
                                " ", "").replace("RV:", "").replace("FW:", "").replace("هدایت:", "")

                            if email_subject in new_subject:

                                if email_message.is_multipart():
                                    for part in email_message.walk():
                                        if part.get_content_type() == "text/plain":
                                            body = part.get_payload(decode=True).decode(
                                                "utf-8", errors="ignore")
                                else:
                                    body = email_message.get_payload(
                                        decode=True).decode("utf-8", errors="ignore")

                                pattern = None

                                if email_subject == "Tu código de acceso temporal de Netflix".replace(" ", ""):

                                    pattern = r'https://www\.netflix\.com/account/travel/verify\?nftoken=[\w-]+.*'
                                else:
                                    pattern = r'https://www\.netflix\.com/account/update-primary-location\?nftoken=[\w\+\/-]+.*'

                                match = re.search(pattern, body)

                                if match:

                                    link = match.group(0).replace(">", "")

                                    return link

                                else:
                                    return 'No se encontró ningún link'

                            else:
                                print("No se encontró el asunto del correo")
                                continue
        else:
            status, messages = mail.search(
                None, '(FROM "info@account.netflix.com")')

            counter: int = 0

            if status == "OK":

                message_ids = messages[0].split()

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

                                new_subject: str = subject.replace(
                                    " ", "").replace("RV:", "").replace("FW:", "").replace("هدایت:", "")

                                if email_subject in new_subject:

                                    if email_message.is_multipart():
                                        for part in email_message.walk():
                                            if part.get_content_type() == "text/plain":
                                                body = part.get_payload(decode=True).decode(
                                                    "utf-8", errors="ignore")
                                    else:
                                        body = email_message.get_payload(
                                            decode=True).decode("utf-8", errors="ignore")

                                    pattern = None

                                    if email_subject == "Tu código de acceso temporal de Netflix".replace(" ", ""):

                                        pattern = r'https://www\.netflix\.com/account/travel/verify\?nftoken=[\w-]+.*'
                                    else:
                                        pattern = r'https://www\.netflix\.com/account/update-primary-location\?nftoken=[\w\+\/-]+.*'

                                    match = re.search(pattern, body)

                                    if match:

                                        link = match.group(0).replace(
                                            ">", "").replace("]", "")

                                        return link

                                    else:
                                        return 'No se encontró ningún link'

                                else:
                                    print("No se encontró el asunto del correo")
                                    continue

    mail.close()


def get_netflix_session_code(user_email: str):
    mail = imaplib.IMAP4_SSL(os.getenv("IMAP_SERVER"))

    mail.login(os.getenv("NETFLIX_EMAIL"), os.getenv("NETFLIX_PASSWORD"))

    mail.select("inbox")

    status, messages = mail.search(
        None, f'(FROM "{user_email}")')

    if status == "OK":

        message_ids: list[str] = messages[0].split()

        if message_ids != []:

            for msg_id in message_ids[::-1]:
                status, message = mail.fetch(msg_id, "(RFC822)")

                if status == "OK":
                    for response in message:
                        if isinstance(response, tuple):
                            email_message = email.message_from_bytes(
                                response[1])

                            subject, encoding = decode_header(
                                email_message["Subject"])[0]
                            if isinstance(subject, bytes):
                                subject = subject.decode(
                                    encoding if encoding else "utf-8")

                            new_subject: str = subject.replace(
                                " ", "").replace("RV:", "").replace("FW:", "")

                            if "Tu código de inicio de sesión".replace(" ", "") in new_subject:

                                if email_message.is_multipart():
                                    for part in email_message.walk():
                                        if part.get_content_type() == "text/plain":
                                            body = part.get_payload(decode=True).decode(
                                                "utf-8", errors="ignore")
                                else:
                                    body = email_message.get_payload(
                                        decode=True).decode("utf-8", errors="ignore")

                                code = re.findall(
                                    r'(\d{4})(?:\s|\n|$)', body)

                                if code:
                                    print(code)
                                    return code[1]

                                else:
                                    print("No se encontró el código")

        else:
            status, messages = mail.search(
                None, '(FROM "info@account.netflix.com")')

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

                                new_subject: str = subject.replace(
                                    " ", "").replace("RV:", "").replace("FW:", "")

                                if "Tu código de inicio de sesión".replace(" ", "") in new_subject:

                                    if email_message.is_multipart():
                                        for part in email_message.walk():
                                            if part.get_content_type() == "text/plain":
                                                body = part.get_payload(decode=True).decode(
                                                    "utf-8", errors="ignore")
                                    else:
                                        body = email_message.get_payload(
                                            decode=True).decode("utf-8", errors="ignore")

                                    code = re.findall(
                                        r'(\d{4})(?:\s|\n|$)', body)

                                    if code:
                                        print(code)
                                        return code[0]

                                    else:
                                        print("No se encontró el código")

    mail.close()
