import logging

from email_validator import EmailNotValidError, validate_email
from itemadapter.adapter import ItemAdapter

MESSAGE1 = "(メールを送信される場合は●を@に変換してください)"
MESSAGE2 = "(メールを送信する場合は●を@に変換してください)"
MESSAGE3 = "(・を@に置き換えてください)"


class EmailPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get("メールアドレス"):
            email = str(adapter.get("メールアドレス"))
            if email.endswith(MESSAGE1):
                email = email[: -len(MESSAGE1)].replace("●", "@").strip()
            elif email.endswith(MESSAGE2):
                email = email[: -len(MESSAGE2)].replace("●", "@").strip()
            elif email.endswith(MESSAGE3):
                email = email[: -len(MESSAGE3)].replace("・", "@").strip()
            else:
                email = email.replace("(アットマーク)", "@")
                email = email.replace("_at_", "@")
                email = email.replace("(at)", "@")
                email = email.replace(" [at] ", "@")
                email = email.replace("[at]", "@")
                email = email.replace("(@)", "@")
                email = email.replace(" at ", "@")
                email = email.replace("●", "@")
                email = email.replace("ア", "@")
                email = email.replace("・", "@")
                email = email.replace("★", "@")
                email = email.strip()
            try:
                emailinfo = validate_email(email, check_deliverability=False)
                adapter["メールアドレス"] = emailinfo.normalized
            except EmailNotValidError as e:
                logging.critical(f"{e}: {email}")
        return item
