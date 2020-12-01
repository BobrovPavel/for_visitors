from src.framework.logger import logger
import imaplib

logger = logger.get_logger()


imap_host = ""
imap_user = "x"
imap_pass = ""
box = imaplib.IMAP4_SSL(imap_host)


class IMapMail:

    @staticmethod
    def get_mail():
        try:
            box.login(imap_user, imap_pass)
            box.list()
            box.select("inbox")
            rv, data = box.search(None, "All")
            for num in data[0].split():
                rv, data = box.fetch(num, '(RFC822)')
            return data[0][1]
        except Exception as e:
            logger.error(str(e))

    @staticmethod
    def remove_all_emails():
        logger.info("Remove all emails")
        box.login(imap_user, imap_pass)
        box.select("Inbox")
        typ, data = box.search(None, "ALL")
        for num in data[0].split():
            box.store(num, "+FLAGS", "\\Deleted")
        box.expunge()
        box.close()
        box.logout()
