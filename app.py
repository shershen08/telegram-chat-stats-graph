import configparser
import json

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

from datetime import timedelta, datetime

import draw

# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

dialog_id = config['Telegram']['dialog']

api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)

## TODO
# get messages per user
# draw dates nicer

msg_list = []

async def main():
    await client.start()
    print("Client Created")

    # Ensure you're authorized
    if not await client.is_user_authorized():
        #client.send_code_request(phone)
        try:
            client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            client.sign_in(password=input('Password: '))

    async for dialog in client.iter_dialogs():
        if dialog.id == int(dialog_id):
            print('dialog found: ', dialog.name)
            async for message in client.iter_messages(dialog):
                # print(message.date)
                add_msg(message)

    if len(msg_list) == 0:
        raise Exception('no messages was retrieved')
    #sort
    dates_sorted = sort_dates(msg_list[::-1])
    #save
    draw.draw_graph(dates_sorted, dialog_id)

def add_msg(message):
    msg_list.append(str(message.date))

def sort_dates(dates):
    one_day = timedelta(days=1)
    d = {}
    for i, date in enumerate(dates, start=0):
        if i < len(dates) - 1:
            cur_date = date.split()[0]
            if datetime.fromisoformat(dates[i+1]) - datetime.fromisoformat(date) < one_day: 
                
                if cur_date in d: 
                    d[cur_date] = d[cur_date] + 1
                else:
                    d[cur_date] = 1 
            
    return d

with client:
    client.loop.run_until_complete(main())
