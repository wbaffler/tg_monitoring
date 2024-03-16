import matplotlib, mplcairo
matplotlib.use("module://mplcairo.macosx")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.font_manager import FontProperties
import numpy as np
import plotly.graph_objects as go
import pandas as pd





from emoji_rating import emoji_ratings

class Visualization(object):

    def __init__(self, data_list):
        self.data_list = data_list
        
        # Изменяем шрифт для корректного отображения Эмодзи
        self.prop = FontProperties(fname='/System/Library/Fonts/Apple Color Emoji.ttc')
        # Задаем параметры отображаемого окна
        self.fig = plt.figure(figsize=(12, 8))

        emojies_lists = [d['emoji_list'] for d in self.data_list]
        self.result_dict = self.__convert_emoji_list(emojies_lists)

        self.subplot_i = 0 
        self.subplots_rows = 2 # количество строк с графиками
        self.subplots_cols = 1 # количество столбцов с графиками


    def __convert_emoji_list(self, emojies_lists):
        result_dict = {}
        for dict_list in emojies_lists:
            for d in dict_list:
                if d['emoji'] not in result_dict:
                    result_dict[d['emoji']] = []

        for dict_list in emojies_lists:
            prev_result_dict_lens = [len(v) for v in result_dict.values()]
            for d in dict_list:
                result_dict[d['emoji']].append(d['count'])
            for prev in prev_result_dict_lens:
                for k, v in result_dict.items():
                    if prev == len(v):
                        result_dict[k].append(0)  

        return result_dict
    
    

    def __sum_estimating_reactions(self):

        negative_count = 0
        neutral_count = 0
        positive_count = 0
        for element in self.data_list:
            negative_count += element['negative_emotion']
            neutral_count += element['neutral_emotion']
            positive_count += element['positive_emotion']
        
        vals = [negative_count, neutral_count, positive_count]
        return vals


    def make_ratio_piechart(self):
        self.subplot_i = self.subplot_i + 1

        vals = self.__sum_estimating_reactions()

        labels = [f"Негативная реакция ({vals[0]})", f"Нейтральная реакция ({vals[1]})", 
                  f"Позитивная реакция ({vals[2]})"]
        ax = self.fig.add_subplot(self.subplots_rows, self.subplots_cols, self.subplot_i)
        ax.pie(vals, labels=labels, autopct='%1.1f%%')
        ax.axis("equal")
        ax.set_title('Соотношение реакций')
    

    def make_posts_graph(self):
        self.subplot_i = self.subplot_i + 1

        date_list = [d['date'] for d in self.data_list]
        x_values = np.linspace(0, 1, len(date_list))
      
        ax = self.fig.add_subplot(self.subplots_rows, self.subplots_cols, self.subplot_i)
        ax.set_title('График реакций')
        ax.xaxis.set_major_locator(ticker.FixedLocator(x_values))
        ax.xaxis.set_major_formatter(ticker.FixedFormatter(list(range(1, len(x_values)))))
        ax.set_xlabel('Номер публикации')
        ax.set_ylabel('Количество реакций')

        # count_of_emojies = 
        values = np.asarray(list(self.result_dict.values()))
        ratio_values = values / np.sum(values, axis=0) * 100

        for emoji_key, ratio_v in zip(self.result_dict.keys(), ratio_values.tolist()):
            ax.plot(x_values, ratio_v, label=emoji_key)
        
        self.fig.legend(prop=self.prop)
        plt.savefig(f'temp/posts_graf.png')


    def make_posts_reactions_graph_sl(self):

        df = pd.DataFrame(self.data_list)
        links = ['<a href="' + link + '">' + str(index+1) + '</a>' for index, link in enumerate(df['url'])]
        values_neg = df['negative_emotion']
        values_neut = df['neutral_emotion']
        values_pos = df['positive_emotion']


        # Создание линейных графиков с кликабельными ссылками
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=links, y=values_neg, mode='lines+markers', name='Негативные реакции'))
        fig.add_trace(go.Scatter(x=links, y=values_neut, mode='lines+markers', name='Нейтральные реакции'))
        fig.add_trace(go.Scatter(x=links, y=values_pos, mode='lines+markers', name='Позитивные реакции'))

        # Настройка внешнего вида
        fig.update_layout(
            title='Количество реакций',
            xaxis_title='Ссылки',
            yaxis_title='Количество реакций',
        )
        
        return fig
    

    def make_posts_views_graph_sl(self):

        df = pd.DataFrame(self.data_list)
        links = ['<a href="' + link + '">' + str(index+1) + '</a>' for index, link in enumerate(df['url'])]
        views = df['message_views']
        values_neg = df['negative_emotion']
        values_neut = df['neutral_emotion']
        values_pos = df['positive_emotion']

        sum_values = [sum(x) for x in zip(values_neg, values_neut, values_pos)]

        # Создание линейных графиков с кликабельными ссылками
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=links, y=views, mode='lines+markers', name='Количество просмотров'))
        fig.add_trace(go.Scatter(x=links, y=sum_values, mode='lines+markers', name='Количество реакций'))

        # Настройка внешнего вида
        fig.update_layout(
            title='Количество просмотров',
            xaxis_title='Ссылки',
            yaxis_title='Количество',
        )

        return fig


    def save_imgs(self, fig1, fig2):
        plt.savefig(f'temp/visualisations.png')
        print(fig1, fig2)
        # fig1.write_image(f"temp/fig1.png")
        # fig2.write_image(f"temp/fig2.png")





