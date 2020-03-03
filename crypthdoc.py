import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testdip.settings')
django.setup()

from document.models import Doc
from cypher.models import AES, DES

# # Start Crypth
# if __name__ == '__main__':
#     # получение элементов которые не закончили шифрование
#     finish_item = Doc.objects.filter(finish=0)
#     # не начинать шифрование если очередь не закончена
#     if len(finish_item) == 0:
#         # получение списка файлов для шифрования
#         cl = Doc.objects.filter(active=1, decrypth=0).values('file')
#         print(cl)
#
#         key = 'kos123'
#
#         for item in cl:
#             # установка флага о начале шифрования
#             item.update(finish=0)
#             # зашифровка файла методом AES
#             new_name = AES.init_encrypt(key, item['file'])
#             if new_name:
#                 # устанока флага о зашифровке и установка флага о завершении шифрования
#                 item.update(decrypth=0, file="doc\\crypted\\"+new_name)
#             item.update(finish=1)
#     else:
#         print("Очередь не закончена")

if __name__ == '__main__':
    # получение элементов которые не закончили шифрование
    finish_item = Doc.objects.filter(finish=0)
    # не начинать шифрование если очередь не закончена
    if len(finish_item) == 0:
        # получение списка файлов для шифрования
        cl = Doc.objects.filter(active=1, decrypth=0, run=1).values('id', 'file', 'crypth')
        print(cl)

        key = 'kos123456'

        for item in cl:
            # установка флага о начале шифрования
            Doc.objects.filter(id=item['id']).update(finish=0)
            # зашифровка файла методом AES
            new_name = AES.init_encrypt(key, item['file'])
            if new_name:
                # устанока флага о зашифровке и установка флага о завершении шифрования
                Doc.objects.filter(id=item['id']).update(decrypth=0, file="doc\\crypted\\"+new_name, run=0)
            Doc.objects.filter(id=item['id']).update(finish=1)
    else:
        print("Очередь не закончена")
