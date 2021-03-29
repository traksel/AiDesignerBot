from os import walk
from os.path import exists
import numpy as np
from shutil import rmtree

from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model

PATH = 'downloads/'
OTHER_CLF = 'other_clf_model'
INTERIORS_CLF = 'interiors_clf_model'


# check_user_id_folder проверяет, существует ли каталог пользователя
# если каталога нет, пользователь получит сообщение с просьбой отправить фото
def check_user_id_folder(id=None):
    if exists(PATH + str(id)):
        return True
    else: 
        return False


# get_files получает название файлов в каталоге пользователя
def get_files(id=None):
    _, _, filenames = next(walk(PATH + str(id)))
    input_arr = []
    for i in range(len(filenames)):
        img = load_img(PATH + str(id) + '/' + filenames[i], target_size=(225, 225))
        img = img_to_array(img)
        img = img / 255
        input_arr.append(img)
    return np.array(input_arr)


# identifity_object идентефицирует полученное изображение.
# при положительном ответе пользователь получит прогноз касаемо
# дизайна интерьера, при отрицательном - получит ответ с просьбой
# отправить фото с дизайном интерьера
def identifity_object(id=None):
    arr = get_files(id)
    model = load_model(OTHER_CLF)
    predictions = model.predict_classes(arr)
    return predictions


# get_predictions - отвечает за прогноз полученного изображения
def get_prediction(id=None):
    arr = get_files(id)
    model = load_model(INTERIORS_CLF)
    predictions = model.predict_classes(arr)
    return predictions


# update_folder удаляет каталог с id пользователя после того,
# как пользователь получит прогноз
def update_folder(id=None):
    rmtree(PATH + str(id))
    

if __name__ == '__main__':
    check_user_id_folder()
    get_files()
    identifity_object()
    get_prediction()
    update_folder()
