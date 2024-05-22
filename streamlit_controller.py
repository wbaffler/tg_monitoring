from datetime import datetime, timedelta, timezone
import asyncio
import schedule
import time

import config
import scraping
import visualization
import form_xlsx
import send_email
import pandas as pd


class Controller(object):

    stopped = True

    def __init__(self, channel, key_word):
        self.channel = channel
        self.key_word = key_word
        
        
        self.data = []

    def get_data(self, period):
        data = []
        date_max = datetime.now()
        date_min = date_max - timedelta(days=int(period))
        scraping_tg = scraping.Scraping(config.username, config.api_id, config.api_hash)
        print(self.channel)
        data = asyncio.run(scraping_tg.tg_scraping(self.channel, date_max.replace(tzinfo=timezone.utc), 
                                                   date_min.replace(tzinfo=timezone.utc), self.key_word))
        self.data = data
        df = pd.DataFrame(data)
        if not df.empty:
            df['emoji_list'] = df['emoji_list'].apply(lambda x: ', '.join([f"{d['emoji']} ({d['count']})" for d in x]))
        return df
    
    def build_charts(self):
        vis = visualization.Visualization(self.data)
        vis.make_ratio_piechart()
        fig1 = vis.make_posts_reactions_graph_sl()
        fig2 = vis.make_posts_views_graph_sl()
        return [fig1, fig2]
    
    def __form_excel(self, period, receiver, key_word, channel, smtp_password, smtp_username, smtp_server):
        data = []
        print(period)
        date_max = datetime.now()
        date_min = date_max - timedelta(days=period)
        scraping_tg = scraping.Scraping(config.username, config.api_id, config.api_hash)
        data = asyncio.run(scraping_tg.tg_scraping(channel, date_max.replace(tzinfo=timezone.utc), date_min.replace(tzinfo=timezone.utc), key_word))
        
        # Построение графиков
        vis = visualization.Visualization(data)
        vis.make_posts_graph()
        vis.make_ratio_piechart()
        fig1 = vis.make_posts_views_graph_sl()
        fig2 = vis.make_posts_reactions_graph_sl()

        vis.save_imgs(fig1, fig2)

        # Формирование Excel документа
        xls = form_xlsx.FormXlsx(data)
        filename = xls.form_xlsx_file(date_max.strftime("%d-%m-%Y"))

        email = send_email.SendEmail(smtp_server, smtp_username, smtp_password)
        email.send(smtp_username, receiver, filename)


    def set_schedule_sendin_email(self, period, receiver, key_word, channel, smtp_password, smtp_username, smtp_server):
        schedule.every(period).days.do(self.__form_excel, period, receiver, key_word, channel, smtp_password, smtp_username, smtp_server)
        while True and not self.stopped:
            schedule.run_pending()
            time.sleep(1)