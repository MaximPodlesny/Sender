import csv


def filter_phones(data_csv, data_for_send, filter_word):
    # функция для фильтрации контактов по ключевому значению

    with open(data_csv, 'r', encoding='utf-8') as data, open(data_for_send, 'w', encoding='utf-8', newline='') as file:
        reader = list(csv.DictReader(data))
        writer = csv.writer(file)
        counter = 0
        counter_c = 0
        for row in reader:
            if filter_word.lower() in row['name'].lower():  # если в имени контакта есть ключевое значение
                counter_c += 1
                s = ''
                for i in row['phone']:  #  собираем строку из цифр всех телефонов контакта
                    if i.isdigit():
                        s += i
                        
                # преобразование строки из телефонов и запись в файл
                if len(s)>11 and s[1:11] != s[12:22]:   # если есть два телефона у кортакта
                    phone1 = ['{}{}'.format('+7', s[1:11])]
                    phone2 = ['{}{}'.format('+7', s[12:22])]
                    writer.writerow(phone1)
                    writer.writerow(phone2)
                    counter += 2
                if len(s)>11 and s[1:11] == s[12:22]:   # для исключения дубликата
                    phone1 = ['{}{}'.format('+7', s[1:11])]
                    writer.writerow(phone1)
                    counter += 1
                elif len(s)==11:
                    phone = ['{}{}'.format('+7', s[1:])]
                    writer.writerow(phone)
                    counter += 1

        print(f'Из {counter_c} контактов собрано по фильтру {counter} телефонных номеров.')
        

