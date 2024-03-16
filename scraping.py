import time
from telethon.sync import TelegramClient
from emoji_rating import emoji_ratings


class Scraping(object):

    def __init__(self, username, api_id, api_hash):
        self.username = username
        self.api_id = api_id
        self.api_hash = api_hash

    def __estimating_reactions(self, emoji_list):
        negative_count = 0
        neutral_count = 0
        positive_count = 0

        for emoji in emoji_list:
            for rating_el in emoji_ratings:
                if rating_el['emoji'] == emoji['emoji']:
                    if rating_el['measure'] == -1:
                        negative_count += emoji['count']
                    elif rating_el['measure'] == 0:
                        neutral_count += emoji['count']
                    elif rating_el['measure'] == 1:
                        positive_count +=  emoji['count']
        vals = [negative_count, neutral_count, positive_count]
        return vals
        

    
    async def tg_scraping(self, channel, date_max, date_min, key_search):
        index = 1
        data_list = []
        async with TelegramClient(self.username, self.api_id, self.api_hash) as client:
            async for message in client.iter_messages(channel, search=key_search):
                if message.date < date_max and message.date > date_min:
                    
                    url = f'https://t.me/{channel}/{message.id}'.replace('@', '')
                    if message.reactions == None:
                        pass
                    else:
                        emoji_list = []
                    if message.reactions is None:
                        continue
                    for reaction_count in message.reactions.results:
                        emoji = reaction_count.reaction.emoticon
                        count = int(reaction_count.count)
                        emoji_list.append({
                        'emoji': emoji,
                        'count': count
                        })

                    vals = self.__estimating_reactions(emoji_list)

                    content = {
                        'index': index,
                        'channel': channel, 
                        'text': message.text, 
                        'date': message.date.strftime('%Y-%m-%d %H:%M:%S'), 
                        'message_views': message.views,
                        'url': url, 
                        'negative_emotion': vals[0],
                        'neutral_emotion': vals[1],
                        'positive_emotion': vals[2],
                        'emoji_list': emoji_list

                    }
                    data_list.append(content)

                    print(f'Item {index:05} completed!')
                    print(f'Id: {message.id:05}.\n')

                    index = index + 1

                    
                    time.sleep(1)
                elif message.date < date_min:
                    return data_list

        return data_list