from telethon import TelegramClient, sync
import pandas as pd
import csv
import asyncio

class telegram_API:

    def __init__(self):
        self.api_id = YOUR_API_ID
        self.api_hash = 'YOUR_API_HASH'


    def teleg_ch_infos(self, username):
        #chanel info
        self.client = TelegramClient('session', self.api_id, self.api_hash).start()
        entity = self.client.get_entity(username)
        ch_info ={'id':entity.id, 'title':entity.title, 'username':entity.username, 'created_date':entity.date}
        return ch_info


    def teleg_ch_photo(self, username):
        #chanel image
        self.client = TelegramClient('session', self.api_id, self.api_hash).start()
        path = self.client.download_profile_photo(username)
        print (path)


    def teleg_ch_posts(self, username):
        #posts info
        self.client = TelegramClient('session', self.api_id, self.api_hash).start()
        chats = self.client.get_messages(username, 100)
        message_id =[]
        message =[]
        sender =[]
        reply_to =[]
        time = []
        if len(chats):
            for chat in chats:
                message_id.append(chat.id)
                message.append(chat.message)
                sender.append(chat.from_id)
                reply_to.append(chat.reply_to_msg_id)
                time.append(chat.date)
        data ={'message_id':message_id, 'message': message, 'sender_ID':sender, 'reply_to_msg_id':reply_to, 'time':time}
        pd.DataFrame(data).to_csv('farsna_messages.csv')
        return data


    #def teleg_ch_posts(self, username):
        ##members info
        # self.client = TelegramClient('session', self.api_id, self.api_hash).start()
        #participants = self.client.get_participants(group_username)
        #firstname =[]
        #lastname = []
        #username = []
        #if len(participants):
        #    for x in participants:
        #        firstname.append(x.first_name)
        #        lastname.append(x.last_name)
        #        username.append(x.username)

        #data ={'first_name' :firstname, 'last_name':lastname, 'user_name':username}
        #pd.DataFrame(data).to_csv('userdetails.csv')

        #return data
