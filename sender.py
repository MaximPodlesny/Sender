import pywhatkit.whats as pk
import csv
import time
import configparser
from os import path, walk
from my_functions import write_to_config, check_config, list_contacts, list_contacts, write_config

path_to_config_text_for_send = path.abspath(path.join(path.dirname(__file__), 'config_text_for_send.ini'))
path_to_config_whatsapp_sender = path.abspath(path.join(path.dirname(__file__), 'config_whatsapp_sender.ini'))


def send_message(user, message, filename):
    '''Определение функии для отправки сообщений
        которая принимает текст сообщения и 
        имя файла базы телефонов
    '''
    
    # with open(filename, 'r', encoding='utf-8') as data:
    #     contacts = list(csv.reader(data))

    #     config = configparser.ConfigParser()        # открываем файл с сохраненными данными пересылки 
    #     config.read(path_to_config_whatsapp_sender)
    #     if config['turne']['last_phone'] == '0':    # определяем первый ли запуск телущей базы или нет
    #         last_phone = '0'
    #     else:
    #         last_phone = config['turne']['last_phone']

    # user, flag, counter = check_config(res='tg')
    contacts = list_contacts(filename)
    counter = 0
    flag = False
    for contact in contacts:
        if last_phone == '0' or flag == True:
            pk.sendwhatmsg_instantly(phone_no=contact, message=message,\
                                            wait_time=60, tab_close=True)
            last_phone = contact
            flag = True
            counter += 1    # считаем количество отправлений
        elif contact==last_phone:
            flag = not flag
        write_to_config(user, filename, flag, counter, res='wa')

    write_config(filename, res='wa')   
        # os.remove('config_whatsapp_sender.ini')
#         with open(path_to_config_whatsapp_sender, 'w', encoding='utf-8') as conf:
#             '''Определяем всю ли базу прошли
#                 и записываем в конфиг файл
#             '''
#             if contacts[-1][0] == last_phone:
#                 config['turne'] = {'last_phone': '0'}
#                 config.write(conf)
#                 print(f'За сессию отправлено: {counter} сообщений\n\
# Всего отправлено: {contacts.index([last_phone])+1} сообщений\n\
# Осталось отправить: {len(contacts)-(contacts.index([last_phone])+1)} сообщений')
#                 input('Чтобы закрыть намите Enter')
#             elif last_phone != '0':
#                 config['turne'] = {'last_phone': last_phone,
#                                    'filename': filename}
#                 config.write(conf)
#                 print(f'За сессию отправлено: {counter} сообщений\n\
# Всего отправлено: {contacts.index([last_phone])+1} сообщений\n\
# Осталось отправить: {len(contacts)-(contacts.index([last_phone])+1)} сообщений')
#                 input('Чтобы закрыть намите Enter')
#             else:
#                 print('УПС! Рассылка прервалась не начавшись!')
#                 input('Чтобы закрыть намите Enter')
            

# if __name__ == '__main__':

#     config_message = configparser.ConfigParser()
#     config_message.read('config_text_for_send.ini', encoding='utf-8')

#     config = configparser.ConfigParser()
#     config.read('config_whatsapp_sender.ini')

#     topics = list(config_message.sections())
#     for i, v in enumerate(topics):
#         print(f'{i+1} - {v}')
#     number_topic = int(input('Выберите название сообщения из списка: '))

#     send_message(config_message[topics[number_topic-1]]['message'], config['turne']['filename'])

            