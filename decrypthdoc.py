import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testdip.settings')
django.setup()

from document.models import Doc
from client.models import Client
from cypher.models import AES, DES

from smtplib import SMTP_SSL
from email.mime.multipart import MIMEMultipart, MIMEBase
import email.encoders as encoders

def sendFileSMTP(filepath, address):
    basename = os.path.basename(filepath)
    #print(basename)
    # Compose attachment
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(filepath, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % basename)

    # Compose message
    msg = MIMEMultipart()
    msg['From'] = "kostyarach40@gmail.com"
    msg['To'] = address
    msg['Subject'] = "Пришел файл"
    msg.attach(part)
    #print(msg)

    # Send mail
    smtp = SMTP_SSL()
    smtp.connect('smtp.gmail.com')
    smtp.login(msg['From'], 'Kos#021098kos')
    smtp.sendmail(address, address, msg.as_string())
    smtp.quit()

# Start Decrypth
if __name__ == '__main__':
    # получение элементов которые не закончили шифрование
    finish_item = Doc.objects.filter(finish=0, decrypth=1)
    # не начинать шифрование если очередь не закончена
    if len(finish_item) == 0:
        # получение списка файлов для шифрования
        cl = Doc.objects.filter(active=1, decrypth=1).values('id', 'file', 'client_id')
        print(cl)

        key = 'kos123'

        for item in cl:
            # установка флага о начале шифрования
            Doc.objects.filter(id=item['id']).update(finish=0)

            new_name = AES.init_decrypt(key, item['file'])
            # зашифровка файла методом AES
            if new_name:
                # устанока флага о зашифровке и установка флага о завершении шифрования
                Doc.objects.filter(id=item['id']).update(decrypth=0)
                kl = Client.objects.get(id=item['client_id']).email
                sendFileSMTP("media/doc/"+new_name, kl)
                os.remove(os.path.abspath("media\\doc\\" + os.path.basename(new_name)))
            Doc.objects.filter(id=item['id']).update(finish=1)
            print("end")
    else:
        print("Очередь не закончена")
