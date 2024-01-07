from genericpath import exists
from filter import filter_phones
from sender import send_message
from converterVCFtoCSV import convert_vcf_to_csv
import configparser
import time
from os import path, walk
path_to_config_text_for_send = path.abspath(path.join(path.dirname(__file__), 'config_text_for_send.ini'))
path_to_config_whatsapp_sender = path.abspath(path.join(path.dirname(__file__), 'config_whatsapp_sender.ini'))

if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read(path_to_config_whatsapp_sender)
    if config['turne']['last_phone'] == '0':    # Проверяем первый ли запуск текущей базы
   
        

        data_for_send = input('Если у вас есть готовая база контактов\
в формате csv, напишите название файла. Усли нет, напишите "NO": ')
        
        
        if data_for_send.lower() == 'no':
            vcf_file = input('Введите название файла vcf: ')

            path_to_vcf_file = path.abspath(path.join(path.dirname(__file__), '..', vcf_file))
            if not exists(path_to_vcf_file): # проверка наличия необходимого файла
                # list_paths = [path.join(dirpath, f)\
                #               for dirpath, dirnames, filenames in walk(path.abspath(path.join(path.dirname(__file__), '..')))\
                #                                                                     for f in filenames]
                list_filenames = next(walk(path.abspath(path.join(path.dirname(__file__), '..'))), (None, None, []))[2]
                for i, v in enumerate(list_filenames):
                    print(f'{i+1} - {v}')
                n = int(input(f'Файл {vcf_file} не найден!\n\
Выберите номер файла из списка: '))
                vcf_file = list_filenames[n-1]

            csv_file = input('Введите название cоздаваемого файла без фильтра в формате csv: ')
            convert_vcf_to_csv(vcf_file, csv_file)   # создаем файл csv со всеми контактами

            data_csv = csv_file
            data_for_send = input('Введите название создаваемого отфильтрованного файла для рассылки (формат csv): ')
            filter_word = input('Введите критерий фильтра в названии контакта: ')

            filter_phones(data_csv, data_for_send, filter_word)     # фильтруем контакты по ключевому значению в имени контакта

            print(f'Имя файла: {data_for_send}')
            time.sleep(5)

        path_to_data_for_send = path.abspath(path.join(path.dirname(__file__), '..', data_for_send))
        if not exists(path_to_data_for_send): # проверка наличия необходимого файла

            list_filenames = next(walk(path.abspath(path.join(path.dirname(__file__), '..'))), (None, None, []))[2]
            for i, v in enumerate(list_filenames):
                print(f'{i+1} - {v}')
            n = int(input(f'Файл {data_for_send} не найден!\n\
Выберите номер файла из списка: '))
            data_for_send = list_filenames[n-1]

        config_message = configparser.ConfigParser()
        config_message.read(path_to_config_text_for_send, encoding='utf-8')
        topics = list(config_message.sections())    # выводим список назаваний текстов для рассылки
        for i, v in enumerate(topics):
            print(f'{i+1} - {v}')
        number_topic = int(input('Выберите название сообщения из списка: '))

        print('Сообщения отправляются. Для принудительной остановки нажмите CTRL+C.\n\
При повторном запуске, рассылка продолжится с того же места!')
        time.sleep(10)
        send_message(config_message[topics[number_topic-1]]['message'], data_for_send)

    else:
        
        # блок для продолжения рассылки со следующего контакта
        config_message = configparser.ConfigParser()
        config_message.read(path_to_config_text_for_send, encoding='utf-8')
        topics = list(config_message.sections())
        for i, v in enumerate(topics):
            print(f'{i+1} - {v}')
        
        number_topic = int(input('Выберите название сообщения из списка: '))

        print('Сообщения отправляются. Для принудительной остановки нажмите CTRL+C.\n\
При повторном запуске, рассылка продолжится с того же места!')
        time.sleep(10)
        send_message(config_message[topics[number_topic-1]]['message'], config['turne']['filename'])
        

        
        

    

