#!/usr/bin/env python
from getpass import getpass
from os import environ
import pickle

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import SearchRequest
from telethon.tl.types import InputMessagesFilterEmpty

if __name__ == '__main__':
    session_name = environ.get('TG_SESSION', 'session')
    user_phone = environ['TG_PHONE']
    client = TelegramClient(
        session_name, int(environ['TG_API_ID']), environ['TG_API_HASH'],
        proxy=None, update_workers=4
    )
    try:
        print('INFO: Connecting to Telegram Servers...', end='', flush=True)
        client.connect()
        print('Done!')

        if not client.is_user_authorized():
            print('INFO: Unauthorized user')
            client.send_code_request(user_phone)
            code_ok = False
            while not code_ok:
                code = input('Enter the auth code: ')
                try:
                    code_ok = client.sign_in(user_phone, code)
                except SessionPasswordNeededError:
                    password = getpass('Two step verification enabled. '
                                       'Please enter your password: ')
                    code_ok = client.sign_in(password=password)
        print('INFO: Client initialized successfully!')

        target_user = client.get_entity(environ['TGDUMP_USER'])
        target_chat = client.get_entity(environ['TGDUMP_CHAT'])

        offset = 0
        all_msgs = []
        limit = 100

        while True:
            result = client(SearchRequest(
              target_chat,
              '',  # query
              InputMessagesFilterEmpty(),  # msg_filter
              None, None,  # min_date, max_date
              0,  # offset_id
              offset,  # add_offset
              limit,  # limit
              0,  # max_id
              0,  # min_id
              target_user
            ))
            all_msgs.extend(result.messages)
            offset += limit
            if not result.messages:
                break

        all_msgs = [m.to_dict() for m in all_msgs]
        filename = 'data/' + target_chat.title + '.dump'
        with open(filename, 'wb') as f:
            pickle.dump(all_msgs, f, pickle.HIGHEST_PROTOCOL)
            print(str(len(all_msgs)) + ' messages are saved to ' + filename)

        # input('Press Enter to stop this!\n')
    except KeyboardInterrupt:
        pass
    finally:
        client.disconnect()

