import os
import telebot
import numpy as np
# Это мои собственные модули
# API - содержит token бота
from API import token
# ANS - хранит в себе тексты ответов бота 
from ANS import start_message, help_message, positive_res, negative_res, not_found, incorrect
# backbone - так называемый "бекенд" с моделью
from backbone import check_user_id_folder, get_files, get_prediction, update_folder, identifity_object

tb = telebot.TeleBot(token)


@tb.message_handler(commands=['start'])
def send_start(message):
    tb.send_message(message.chat.id, start_message, parse_mode='html')


@tb.message_handler(commands=['help'])
def send_help(message):
    tb.send_message(message.chat.id, help_message)


# get_photo отвечает за сохранение полученного фото
# отправленное пользователем
@tb.message_handler(content_types=['photo'])
def get_photo(message):
    raw = message.photo[-1].file_id
    user_id = str(message.from_user.id)
    new_path = 'downloads/' + user_id + '/'
    os.makedirs(new_path, exist_ok=True)
    path = new_path + raw + ".jpg"
    file_info = tb.get_file(raw)
    downloaded_file = tb.download_file(file_info.file_path)
    with open(path,'wb') as new_file:
        new_file.write(downloaded_file)
        

# send_predictions отвечает за прогноз
# в теле функции ипользованы функции модуля backbone
@tb.message_handler(commands=['go'])
def send_predictions(message):
    user_id = str(message.from_user.id)
    if check_user_id_folder(user_id):
        obj_id = identifity_object(user_id)
        counter = 0
        
        for i in range(len(obj_id)):
            if obj_id[i] == 1:
                counter += 1
            else:
                counter = 0

        answer = counter / len(obj_id)
        to_user = ''
        if answer < .5:
            to_user = incorrect
        else:
            counter = 0
            prediction = get_prediction(user_id)
    
            for i in range(len(prediction)):
                if prediction[i] == 1:
                    counter += 1
                else:
                    counter = 0
    
            answer = counter / len(prediction)
            to_user = ''
        
            if answer >= .45:
                to_user = positive_res[np.random.randint(len(positive_res))]
            else:
                to_user = negative_res[np.random.randint(len(negative_res))]
        
        tb.send_message(message.chat.id, to_user)
        update_folder(user_id)
    else:
        tb.send_message(message.chat.id, not_found[np.random.randint(len(not_found))])
    

tb.polling(none_stop=True)
