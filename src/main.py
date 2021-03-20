#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://t.me/KoyomiNaoBot
import io
import os
import time
import json
import config
import shutil
import logging
import sqlite3
import requests
from PIL import Image
from datetime import datetime
from telebot import TeleBot, types, apihelper


print('\n\n',
      ' /$$   /$$                                             /$$\n',
      '| $$  /$$/                                            |__/\n',
      '| $$ /$$/   /$$$$$$  /$$   /$$  /$$$$$$  /$$$$$$/$$$$  /$$\n',
      '| $$$$$/   /$$__  $$| $$  | $$ /$$__  $$| $$_  $$_  $$| $$\n',
      '| $$  $$  | $$  \ $$| $$  | $$| $$  \ $$| $$ \ $$ \ $$| $$\n',
      '| $$\  $$ | $$  | $$| $$  | $$| $$  | $$| $$ | $$ | $$| $$\n',
      '| $$ \  $$|  $$$$$$/|  $$$$$$$|  $$$$$$/| $$ | $$ | $$| $$\n',
      '|__/  \__/ \______/  \____  $$ \______/ |__/ |__/ |__/|__/\n',
      '                     /$$  | $$     @Eilaluth - v1.1       \n',
      '                    |  $$$$$$/                            \n',
      '                     \______/                             \n')


bot = TeleBot(config.tgBotToken)


@bot.message_handler(commands=['start'])
def cmd_start(message):
    def SendMessages():
        try:
            bot.send_message(message.chat.id,
                             'Halo Kak! Koyomi Adalah Bot Yang Di Buat Oleh Papah @Eilaluth Untuk Mempermudah Kakak Kakak Dalam Mencari Sauce, Mau Itu Anime Atau Manga, Bahkan Ilustrasi 2d Koyomi Juga Bisa Cariin Sauce Nya!' +
                             "\n\nBTC : bc1q6p56r9x4neqaw3ukaj30u9tar64cqumwhk4gjp",
                             parse_mode='HTML',
                             disable_web_page_preview=True)
            bot.send_message(message.chat.id, "<b>Langsung Kirim Aja Gambar Nya Ke Aku Nanti Aku Cariin!</b>", parse_mode='HTML')
            addLog('i', f'Welcome new user [id:{message.chat.id}]')
        except Exception as ex:
            if type(ex).__name__ == 'ConnectionError':
                addLog('w', f'{type(ex).__name__} ada yang salah di cmd_start() --> SendMessages() [id:{message.chat.id}]: {str(ex)}')
                addLog('i', 'Koyomi coba kirim ulang pesannya')
                time.sleep(3)
                SendMessages()
            addLog('e', f'Keknya [{type(ex).__name__}] ada yang salah di cmd_start() --> SendMessages() [id:{message.chat.id}]: {str(ex)}')
            
    def SetState():
        try:
            config.set_state(
                message.chat.id, config.States.S_REQUEST_Media.value)
        except Exception as ex:
            addLog('e', f'Keknya [{type(ex).__name__}] ada yang salah di cmd_start() --> SetState() [id:{message.chat.id}]: {str(ex)}')

    SendMessages()
    SetState()


@bot.message_handler(commands=['reset'])
def cmd_reset(message):
    def SendMessages():
        try:
            bot.send_message(message.chat.id,
                             'Halo Kak! Koyomi Adalah Bot Yang Buat Oleh Papah @Eilaluth Untuk Mempermudah Kakak Kakak Dalam Mencari Sauce, Mau Itu Anime Atau Manga, Bahkan Ilustrasi 2d Koyomi Juga Bisa Cariin Sauce Nya!' +
                             "\n\nBTC : bc1q6p56r9x4neqaw3ukaj30u9tar64cqumwhk4gjp",
                             parse_mode='HTML',
                             disable_web_page_preview=True)
            bot.send_message(message.chat.id, "<b>Langsung Kirim Aja Gambar Nya Ke Aku Nanti Aku Cariin!</b>", parse_mode='HTML')
            addLog('i', f'User restarted bot [id:{message.chat.id}]')
        except Exception as ex:
            if type(ex).__name__ == 'ConnectionError':
                addLog('w', f'{type(ex).__name__} ada yang salah di cmd_reset() --> SendMessages() [id:{message.chat.id}]: {str(ex)}')
                addLog('i', 'Koyomi coba kirim ulang pesannya')
                time.sleep(3)
                SendMessages()
            addLog('e', f'Keknya [{type(ex).__name__}] ada yang salah di cmd_reset() --> SendMessages() [id:{message.chat.id}]: {str(ex)}')

    def SetState():
        try:
            config.set_state(
                message.chat.id, config.States.S_REQUEST_Media.value)
        except Exception as ex:
            addLog('e', f'Keknya [{type(ex).__name__}] ada yang salah di cmd_reset() --> SetState() [id:{message.chat.id}]: {str(ex)}')

    SendMessages()
    SetState()


@bot.message_handler(content_types=['photo'])
def work_with_photo(message):
    def getPhoto():
        try:
            fileID = message.photo[-1].file_id
            file_info = bot.get_file(fileID)
            downloaded_file = bot.download_file(file_info.file_path)

            if not os.path.isdir('media'):
                os.mkdir('media')

            if not os.path.isdir(f'media/{message.chat.id}'):
                os.mkdir(f'media/{message.chat.id}')

            with open(f"media/{message.chat.id}/image.jpg", 'wb') as new_file:
                new_file.write(downloaded_file)
            addLog('i', f'Media dah di download [id:{message.chat.id}]')
            getData()
        except Exception as ex:
            if type(ex).__name__ == 'ConnectionError':
                addLog('w', f'{type(ex).__name__} ada yang salah di work_with_photo() --> getPhoto() [id:{message.chat.id}]: {str(ex)}')
                addLog('i', 'Koyomi coba kirim ulang pesannya')
                time.sleep(3)
                getPhoto()
            addLog('e', f'Keknya [{type(ex).__name__}] ada yang salah di work_with_photo() --> getPhoto() [id:{message.chat.id}]: {str(ex)}')
    
    def getData():
        try:
            extensions = {".jpg", ".jpeg", ".png"}
            thumbSize = (250, 250)

            for root, _, files in os.walk(f'./media/{message.chat.id}', topdown=False):
                for f in files:
                    fname = os.path.join(root, f)
                    for ext in extensions:
                        if fname.lower().endswith(ext):
                            addLog('i', f'Media di simpen di [{fname}]')
                            image = Image.open(fname)
                            image = image.convert('RGB')
                            image.thumbnail(thumbSize, resample=Image.ANTIALIAS)
                            imageData = io.BytesIO()
                            image.save(imageData, format='PNG')

                            url = f'http://saucenao.com/search.php?output_type={config.output_type}&numres={config.numres}&minsim={config.minsim}&dbmask={str(getBitmask())}&api_key={config.api_key}'
                            files = {'file': ("image.png", imageData.getvalue())}
                            imageData.close()

                            processResults = True
                            r = requests.post(url, files=files)
                            addLog('i', f'[id:{message.chat.id}] dapet result')
                            sendResults(message, r.json())
        except Exception as ex:
            addLog('e', f'Keknya [{type(ex).__name__}] ada yang salah di getData() [id:{message.chat.id}]: {str(ex)}')

    def sendResults(message, result):
        try:
            '''
            i = 1
            while i <= config.numres:
            result_case = result['results'][i - 1]
            result_name = result['results'][i - 1]['data']['title']
            result_picture = result['results'][i - 1]['header']['thumbnail']
            result_similarity = result['results'][i - 1]['header']['similarity']

            bot.send_message(message.chat.id, f'<a href="{result_picture}"> </a>Result ({i} of {config.numres}): {result_name}\n' +
                             f'Similarity = {result_similarity}%', parse_mode='HTML')
            i = i + 1
            '''
            i = 1
            while i <= config.numres:
                try:
                    result_case = result['results'][i - 1]
                except:
                    result_case = ''
                    
                try:
                    result_name = result['results'][i - 1]['data']['source']
                except:
                    try:
                        result_name = result['results'][i - 1]['data']['title']
                    except:
                        result_name = ''
                    
                try:
                    result_part = result['results'][i - 1]['data']['part']
                except:
                    result_part = ''
                    
                try:
                    result_year = result['results'][i - 1]['data']['year']
                except:
                    result_year = ''
                    
                try:
                    result_time = result['results'][i - 1]['data']['est_time']
                except:
                    result_time = ''
                    
                try:
                    result_url = result['results'][i - 1]['data']['ext_urls'][0]
                except:
                    result_url = ''
                    
                try:
                    result_picture = result['results'][i - 1]['header']['thumbnail']
                except:
                    result_picture = ''
                    
                try:
                    result_similarity = result['results'][i - 1]['header']['similarity']
                except:
                    result_similarity = ''
                
                try:
                    message_text = ''
                    if result_name != '':
                        message_text = message_text + f"<b>Title:</b> <a href='{result_url}'>{result_name}</a>\n"
                    if result_part != '':
                        message_text = message_text + f'<b>Part:</b> {result_part}\n'
                    if result_year != '':
                        message_text = message_text + f'<b>Year:</b> {result_year}\n'
                    if result_time != '':
                        message_text = message_text + f'<b>Time:</b> {result_time}\n'
                    if result_similarity != '':
                        message_text = message_text + f'<b>Similarity:</b> {result_similarity}%\n\n'
                    if result_similarity < '{config.minsim}':
                        message_text = 'Maaf Kak, Koyomi Ngak Tau Sauce Nya Apa...\nPastiin Yang Di Kirim Itu Gambar 2d Dan Ngak Di Crop Ya Kak!'
                except:
                    x = 0
                
                def send_result():
                    try:
                        bot.send_message(message.chat.id, message_text, parse_mode='HTML')
                        addLog('i', f'Result dah dikirim ke [id:{message.chat.id}] Similarity: {result_similarity}%"')
                    except Exception as ex:
                        if type(ex).__name__ == 'ConnectionError':
                            addLog('w', f'{type(ex).__name__} ada yang salah di sendResults() --> send_result() [id:{message.chat.id}]: {str(ex)}')
                            addLog('i', 'Koyomi coba kirim ulang pesannya')
                            time.sleep(3)
                            send_result()
                        addLog('e', f'User ngak dapet result karna keknya [{type(ex).__name__}] ada yang salah di sendResults() --> send_result(): {ex}')
                
                send_result()
                i = i + 1
            clearTemp()
        except Exception as ex:
            addLog('e', f'Keknya [{type(ex).__name__}] ada yang salah di sendResults() [id:{message.chat.id}]: {str(ex)}')

    def clearTemp():
        try:
            if os.path.isdir(f'media/{message.chat.id}'):
                shutil.rmtree(f'media/{message.chat.id}')
                addLog('i', f'[./media/{message.chat.id}/] folder dah di apus')
        except Exception as ex:
            addLog('e', f'keknya [{type(ex).__name__}] ada yang salah di clearTemp() [id:{message.chat.id}]: {str(ex)}')
    
    getPhoto()


def getBitmask():
    # enable or disable indexes
    index_hmags = '1'
    index_reserved = '1'
    index_hcg = '1'
    index_ddbobjects = '1'
    index_ddbsamples = '1'
    index_pixiv = '1'
    index_pixivhistorical = '1'
    index_reserved = '1'
    index_seigaillust = '1'
    index_danbooru = '1'
    index_drawr = '1'
    index_nijie = '1'
    index_yandere = '1'
    index_animeop = '1'
    index_reserved = '1'
    index_shutterstock = '1'
    index_fakku = '1'
    index_hmisc = '1'
    index_2dmarket = '1'
    index_medibang = '1'
    index_anime = '1'
    index_hanime = '1'
    index_movies = '1'
    index_shows = '1'
    index_gelbooru = '1'
    index_konachan = '1'
    index_sankaku = '1'
    index_animepictures = '1'
    index_e621 = '1'
    index_idolcomplex = '1'
    index_bcyillust = '1'
    index_bcycosplay = '1'
    index_portalgraphics = '1'
    index_da = '1'
    index_pawoo = '1'
    index_madokami = '1'
    index_mangadex = '1'

    db_bitmask = int(index_mangadex+index_madokami+index_pawoo+index_da+index_portalgraphics+index_bcycosplay+index_bcyillust+index_idolcomplex+index_e621+index_animepictures+index_sankaku+index_konachan+index_gelbooru+index_shows+index_movies+index_hanime+index_anime+index_medibang +
                     index_2dmarket+index_hmisc+index_fakku+index_shutterstock+index_reserved+index_animeop+index_yandere+index_nijie+index_drawr+index_danbooru+index_seigaillust+index_anime+index_pixivhistorical+index_pixiv+index_ddbsamples+index_ddbobjects+index_hcg+index_hanime+index_hmags, 2)
    return db_bitmask


def addLog(type, text):
    log_message = ''
    if type == 'w':  # WARNING
        log_message = f'[WARNING] {text}'
        print(datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
              '| ' + log_message)
        logging.warning(log_message)
    elif type == 'i':  # INFO
        log_message = f'[Koyomi] [Info] {text}'
        print(datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
              '| ' + log_message)
        logging.info(log_message)
    elif type == 'e':  # ERROR
        log_message = f'[ERROR] {text}'
        print(datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
              '| ' + log_message)
        logging.error(log_message)


def infinity_polling_start():
    bot.infinity_polling()


def create_table(type_of_table):
    def create_table_states():
        try:
            conn = sqlite3.connect('states.db')
            cursor = conn.cursor()
            conn.execute(
                '''CREATE TABLE IF NOT EXISTS states (user_id INTEGER, state INTEGER)''')
            conn.commit()
            conn.close()
        except Exception as ex:
                addLog('e', f'Keknya [{type(ex).__name__}] ada yang salah di create_table(): {str(ex)}')

    if type_of_table == 'states':
        create_table_states()


if __name__ == '__main__':
    logging.getLogger('requests').setLevel(logging.CRITICAL)
    logging.basicConfig(format='[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - %(message)s',
                        level=logging.INFO, filename='bot.log', datefmt='%d.%m.%Y %H:%M:%S')
    while True:
        if not os.path.isfile('states.db'):
            create_table('states')
        try:
            bot.polling(none_stop=True)
        except Exception as ex:
            addLog('e', f'Keknya [{type(ex).__name__}] ada yang salah di bot.polling(): {str(ex)}')
            time.sleep(5)
