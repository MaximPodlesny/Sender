import asyncio
from my_functions import write_config, choise_file, choise_topic, check_config
from telegram_sender import send_to_telegram
from genericpath import exists
from filter import filter_phones
from sender import send_message
from converterVCFtoCSV import convert_vcf_to_csv
import time
from os import path, walk
path_to_config_text_for_send = path.abspath(path.join(path.dirname(__file__), 'config_text_for_send.ini'))
path_to_config_whatsapp_sender = path.abspath(path.join(path.dirname(__file__), 'config_whatsapp_sender.ini'))
path_to_config = path.abspath(path.join(path.dirname(__file__), 'config_of_sender.json'))

def main():
    try:
        print('Выберите ресурс для рассылки:\n1 - Telegram\n2 - Whatsapp')
        res = ['tg', 'wa'][int(input())-1]
        user, filename, flag, counter = check_config(res=res)
        path_to_data_for_send = filename

        if (user == '0' and res == 'wa')\
            or (user == '0' and res == 'tg'):    # Проверяем первый ли запуск текущей базы
            data_for_send = input('Если у вас есть готовая база контактов\
    в формате csv, напишите название файла. Усли нет, напишите "NO": ')   
            
            if data_for_send.lower() == 'no':
                vcf_file = input('Введите название файла vcf: ')

                path_to_vcf_file = path.abspath(path.join(path.dirname(__file__), '..', vcf_file))
                if not exists(path_to_vcf_file): # проверка наличия необходимого файла
                    # list_paths = [path.join(dirpath, f)\
                    #               for dirpath, dirnames, filenames in walk(path.abspath(path.join(path.dirname(__file__), '..')))\
                    #                                                                     for f in filenames]
                    
                    path_to_vcf_file = choise_file(vcf_file)

                csv_file = input('Введите название cоздаваемого файла без фильтра в формате csv: ')
                convert_vcf_to_csv(path_to_vcf_file, csv_file)   # создаем файл csv со всеми контактами

                data_csv = csv_file
                data_for_send = input('Введите название создаваемого отфильтрованного файла для рассылки (формат csv): ')
                filter_word = input('Введите критерий фильтра в названии контакта. Или введите "NO": ')

                if filter_word.lower() != 'no':
                    filter_phones(data_csv, data_for_send, filter_word)     # фильтруем контакты по ключевому значению в имени контакта
                else:
                    data_for_send = data_csv

                print(f'Имя файла: {data_for_send}')
                time.sleep(5)

            path_to_data_for_send = path.abspath(path.join(path.dirname(__file__), '..', data_for_send))

            if not exists(path_to_data_for_send): # проверка наличия необходимого файла
                path_to_data_for_send = choise_file(data_for_send)

            text_topic = choise_topic()

            print('Сообщения отправляются. Для принудительной остановки нажмите CTRL+C.\n\
При повторном запуске, рассылка продолжится с того же места!')
            time.sleep(10)
            if res == 'tg':
                asyncio.run(send_to_telegram(user=user, filename=path_to_data_for_send, photo ='photo_Krasovskaya.jpg', text = text_topic))
            elif res == 'wa':
                send_message(user, text_topic, path_to_data_for_send)

        else:
            
            # блок для продолжения рассылки со следующего контакта
            text_topic = choise_topic()

            print('Сообщения отправляются. Для принудительной остановки нажмите CTRL+C.\n\
При повторном запуске, рассылка продолжится с того же места!')
            time.sleep(10)
            if res == 'tg':
                asyncio.run(send_to_telegram(user=user, filename=path_to_data_for_send, photo ='photo_Krasovskaya.jpg', text = text_topic))
            elif res == 'wa':
                send_message(user, text_topic, filename)
    
    except KeyboardInterrupt:
        print('Программа остановлена принудительно!')
        write_config(path_to_data_for_send, res)
        
if __name__ == '__main__':
    main()
    
        
        

        
        

    

