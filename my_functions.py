import csv
import json
from os import path, walk
import configparser
path_to_config_text_for_send = path.abspath(path.join(path.dirname(__file__), 'config_text_for_send.ini'))
path_to_config = path.abspath(path.join(path.dirname(__file__), 'config_of_sender.json'))


def write_config(path_to_data_for_send, res):
    with open(path_to_config, encoding='utf-8') as file:
        data = json.load(file)
        user = data[f'turne_{res}']['user']
        filename = data[f'turne_{res}']['filename']
        flag = data[f'turne_{res}']['flag']
        counter = data[f'turne_{res}']['counter']
        '''Определяем всю ли базу прошли
            и записываем в конфиг файл
        '''
        contacts = list_contacts(path_to_data_for_send)

        if contacts[-1] == user:
            print(f'За сессию отправлено: {counter} сообщений\n\
    Всего отправлено: {contacts.index(user)+1} сообщений\n\
    Осталось отправить: {len(contacts)-(contacts.index(user)+1)} сообщений')
            input('Чтобы закрыть намите Enter')
            
            write_to_config(user='0', filename=None, flag=False, counter=0, res=res)
        elif user != '0':
            write_to_config(user=user, filename=filename, flag=False, counter=0, res=res)
            print(f'За сессию отправлено: {counter} сообщений\n\
    Всего отправлено: {contacts.index(user)+1} сообщений\n\
    Осталось отправить: {len(contacts)-(contacts.index(user)+1)} сообщений')
            input('Чтобы закрыть намите Enter')
        else:
            print('УПС! Рассылка прервалась не начавшись!')
            input('Чтобы закрыть намите Enter')

def choise_file(data_for_send):
    list_filenames = next(walk(path.abspath(path.join(path.dirname(__file__), '..'))), (None, None, []))[2]
    for i, v in enumerate(list_filenames):
        print(f'{i+1} - {v}')
    n = int(input(f'Файл {data_for_send} не найден!\n\
Выберите номер файла из списка: '))
    return path.abspath(path.join(path.dirname(__file__), '..', list_filenames[n-1]))

def choise_topic():
    config_message = configparser.ConfigParser()
    config_message.read(path_to_config_text_for_send, encoding='utf-8')
    topics = list(config_message.sections())    # выводим список назаваний текстов для рассылки
    for i, v in enumerate(topics):
        print(f'{i+1} - {v}')
    number_topic = int(input('Выберите название сообщения из списка: '))
    return config_message[topics[number_topic-1]]['message']


def write_to_config(user, filename, flag, counter, res):
    with open(path_to_config, encoding='utf-8') as file:
        data = json.load(file)
        # if user != '0':
        data[f'turne_{res}'] = {'user': user,
                        'filename': filename,
                        'flag': flag,
                        'counter': counter}
        # else:
        #     data[f'turne_{res}']['user'] = user
        with open(path_to_config, 'w', encoding='utf-8') as conf:
            json.dump(data, conf, indent=4, ensure_ascii=True)

def check_config(res):
    with open(path_to_config, encoding='utf-8') as file:
        data = json.load(file)
        return data[f'turne_{res}']['user'], data[f'turne_{res}']['filename'],\
            data[f'turne_{res}']['flag'], data[f'turne_{res}']['counter']
    
def list_contacts(filename):
    with open(filename, 'r', encoding='utf-8') as data:
        return [i[0] for i in list(csv.reader(data))[1:]]