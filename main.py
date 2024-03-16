from datetime import datetime, timedelta, timezone
import asyncio
import schedule
import time

import config
import scraping
import visualization
import form_xlsx
import send_email



def run_monthly():
  print('running')
  data = []
  date_max = datetime.now()
  date_min = date_max - timedelta(days=config.period)
  scraping_tg = scraping.Scraping(config.username, config.api_id, config.api_hash)
  data = asyncio.run(scraping_tg.tg_scraping(config.channel, date_max.replace(tzinfo=timezone.utc), date_min.replace(tzinfo=timezone.utc), config.key_search))
  
  # Построение графиков
  vis = visualization.Visualization(data)
  vis.make_posts_graph()
  vis.make_ratio_piechart()
  vis.save_imgs()

  # Формирование Excel документа
  xls = form_xlsx.FormXlsx(data)
  filename = xls.form_xlsx_file(date_max.strftime("%d-%m-%Y"))

  # Отправка на email
  email = send_email.SendEmail(config.smtp_server, config.smtp_username, config.smtp_password)
  email.send(config.sender, config.receiver, filename)
  print('end')


if __name__ == '__main__':

  schedule.every(10).seconds.do(run_monthly)
  while True:
    schedule.run_pending()
    time.sleep(1)
  
  