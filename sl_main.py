import streamlit as st
import streamlit_controller
import threading
import config

class TrackingThread(threading.Thread):
    def __init__(self, receiver, period, key_word, channel, smtp_password, smtp_username, smtp_server):
        super().__init__()
        self.receiver = receiver
        self.period = period
        self.key_word = key_word
        self.channel = channel
        self.smtp_password = smtp_password
        self.smtp_username = smtp_username
        self.smtp_server = smtp_server
        self.stopped = False

    def run(self):
        controller.stopped = False
        controller.set_schedule_sendin_email(int(self.period), self.receiver, self.key_word, self.channel, self.smtp_password, self.smtp_username, self.smtp_server)

    def stop(self):
        self.stopped = True
        controller.stopped = True

if "tracking_threads" not in st.session_state:
    st.session_state.tracking_threads = []


def display_tracking_info_element(index, thread):
    st.write(f"**Отслеживание {index+1}:**")
    st.write(f"**- Канал:** {thread.channel}")
    st.write(f"**- Ключевое слово:** {thread.key_word}")
    st.write(f"**- Период:** {thread.period}")
    st.write(f"**- Email получателя:** {thread.receiver}")
    if st.button(f"Удалить отслеживание {index+1}"):
        stop_tracking(index)


def display_tracking_info():

    st.write("### Текущие отслеживания:")
    for index, thread in enumerate(st.session_state.tracking_threads):
        display_tracking_info_element(index, thread)
        

def display_data(period):
    data = controller.get_data(period)
    if data.empty:
        st.title("Сообщения по заданному ключевому слову за текущий период не найдены или у канала отключены реакции")
    else:
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.write(data)
        fig = controller.build_charts()
        st.pyplot()
        st.plotly_chart(fig[0], use_container_width=True)
        st.plotly_chart(fig[1], use_container_width=True)

def tracking(receiver, period, key_word, channel, smtp_password, smtp_username, smtp_server):
    controller.set_schedule_sendin_email(int(period), receiver, key_word, channel, smtp_password, smtp_username, smtp_server)
    

def start_tracking():
    
    smtp_server = st.sidebar.text_input("SMTP Server", config.smtp_server)
    smtp_username = st.sidebar.text_input("SMTP Username", config.smtp_username)
    smtp_password = st.sidebar.text_input("SMTP Password", config.smtp_password, type="password")
    receiver = st.sidebar.text_input("Receiver Email", config.receiver)
    period_options = [7, 14, 30]
    period = st.sidebar.selectbox("Выберите периодичность формирование отчета (в днях):", period_options)

    if st.sidebar.button("Старт"):
        print('in')
        thread = TrackingThread(receiver, period, key_word, channel, smtp_password, smtp_username, smtp_server)
        print(thread, 'start')
        thread.start()

        st.session_state.tracking_threads.append(thread)

        index = len(st.session_state.tracking_threads) - 1
        display_tracking_info_element(index, thread)

        # st.experimental_rerun()

def stop_tracking(index):
    thread = st.session_state.tracking_threads.pop(index)
    print(thread, 'stop')
    thread.stop()
    st.rerun()

def one_time_analysis():
    period = st.sidebar.text_input("Выберите период мониторинга (в днях):", 10)

    if st.sidebar.button("Старт"):
        display_data(period)



st.title("Сервис по мониторингу Telegram-каналов")
channel = st.sidebar.text_input("Telegram-канал", "@tass_agency")
key_word = st.sidebar.text_input("Ключевое слово", "Яндекс")
controller = streamlit_controller.Controller(channel, key_word)


option = st.sidebar.radio("Выберите действие:", ("Автоотправка отчетов", "Мониторинг"))

if option == "Автоотправка отчетов":
    display_tracking_info()
    start_tracking()
elif option == "Мониторинг":
    one_time_analysis()

