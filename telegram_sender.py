import time
from random import randint
from os import path, walk
from pyrogram.client import Client
from pyrogram.enums import ChatAction, ParseMode
from my_functions import write_to_config, check_config, list_contacts, list_contacts, write_config

path_to_config_tg = path.abspath(path.join(path.dirname(__file__), 'config_tg.json'))

async def send_to_telegram(user: str, text: str, filename: str, photo: str | bool=False):
    async with Client('9298383864_pyrogram', api_id = 27336265, api_hash = 'a88448786618495285ff9898ab10f43c') as client:
        # user, filename, flag, counter = check_config(res='tg')
        contacts = list_contacts(filename)
        counter = 0
        flag = False
        for contact in contacts:
            if user == '0' or flag == True:
                if counter <= 20:
                    if photo:
                        await client.send_chat_action(contact, ChatAction.UPLOAD_PHOTO)
                        time.sleep(5)
                        await client.send_photo(contact, photo=photo, caption=text, parse_mode=ParseMode.HTML)
                    else:
                        await client.send_chat_action(contact, ChatAction.TYPING)
                        time.sleep(5)
                        await client.send_message(contact, text, parse_mode=ParseMode.HTML)
                else:
                    print('Рассылка остановлена по лимиту!\n')
                    break
                user = contact
                flag = True
                counter += 1    # считаем количество отправлений
                write_to_config(user, filename, flag, counter, res='tg')
                time.sleep(randint(10, 60))
            elif contact==user:
                flag = not flag
        write_config(filename, res='tg')

    
#     '''Определяем всю ли базу прошли
#         и записываем в конфиг файл
#     '''
#     if contacts[-1][0] == user:
#         print(f'За сессию отправлено: {counter} сообщений\n\
# Всего отправлено: {contacts.index([user])+1} сообщений\n\
# Осталось отправить: {len(contacts)-(contacts.index([user])+1)} сообщений')
#         input('Чтобы закрыть намите Enter')
#         user = '0'
#         write_to_config(user)
#     elif user != '0':
#         write_to_config(user, filename)
#         print(f'За сессию отправлено: {counter} сообщений\n\
# Всего отправлено: {contacts.index([user])+1} сообщений\n\
# Осталось отправить: {len(contacts)-(contacts.index([user])+1)} сообщений')
#         input('Чтобы закрыть намите Enter')
#     else:
#         print('УПС! Рассылка прервалась не начавшись!')
#         input('Чтобы закрыть намите Enter')
    

# if __name__ == '__main__':
#     text = 'Здравствуйте, меня зовут Оксана.✨\n\
# Я ваш @ok_karmaterapy, хочу подарить Вам <b>бесплатную</b> дистанционную консультацию 🎁\n\
# На которой <b>ОСОЗНАЕТЕ</b> для себя конкретное решение Вашей самой насущной проблемы.\n\n\
# <b>Порядок действий такой:</b>\n\
# Вы озвучиваете что вас волнует!\n\
# Я с помощью ясновидения смотрю причину происходящего и даю рекомендации...\n\
# Это займёт 15 минут.\n\n\
# Желаете согласовать  дату и время общения?\n\n\
# P.S. На консультации не будет продаж'
    
    # asyncio.run(send_to_telegram('79898198015', photo ='photo_Krasovskaya.jpg', text = text))