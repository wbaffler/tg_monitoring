import streamlit as st
import streamlit_controller


def display_data(period):
    data = controller.get_data(period)
    print(data)
    if data.empty:
        st.title("Сообщения по заданному ключевому слову за текущий период не найдены или у канала отключены реакции")
    else:
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.write(data)
        fig = controller.build_charts()
        st.pyplot()
        st.plotly_chart(fig[0], use_container_width=True)
        st.plotly_chart(fig[1], use_container_width=True)

def start_tracking():
    
    smtp_server = st.sidebar.text_input("SMTP Server")
    smtp_username = st.sidebar.text_input("SMTP Username")
    smtp_password = st.sidebar.text_input("SMTP Password", type="password")
    receiver = st.sidebar.text_input("Receiver Email")
    period_options = [3, 7, 14, 30]
    period = st.sidebar.selectbox("Выберите периодичность (в днях):", period_options)

    if st.sidebar.button("Старт"):
        pass # Ваш код для отображения таблицы, графиков и функции send_email

def one_time_analysis():
    period = st.sidebar.text_input("Выберите период анализа (в днях):", 10)

    if st.sidebar.button("Старт"):
        display_data(period)



st.sidebar.title("Мониторинг Telegram-канала")
channel = st.sidebar.text_input("Telegram-канал", "@tass_agency")
key_word = st.sidebar.text_input("Ключевое слово", "Яндекс")
controller = streamlit_controller.Controller(channel, key_word)


option = st.sidebar.radio("Выберите действие:", ("Мониторинг", "Единоразовый анализ"))

if option == "Мониторинг":
    start_tracking()
elif option == "Единоразовый анализ":
    one_time_analysis()

