# Данный скрипт запускается обособленно от основного кода бота

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import psycopg2

current_group = input('Введите номер группы: ')

conn = psycopg2.connect(dbname='',
                        user='',
                        password='',
                        host='')
cursor = conn.cursor()

driver = webdriver.Chrome('./chromedriver')
driver.get('https://ruz.hse.ru/ruz/main')
sleep(1)
group = driver.find_element_by_id('autocomplete-group')
group.send_keys(current_group)
sleep(2)
group.send_keys(Keys.ENTER)

sleep(4)
soup = BeautifulSoup(driver.page_source, 'html.parser')

blocks = soup.find('div', class_='list').find_all('div', class_='media')
week = ''
day = ''
month = ''
for i, block in enumerate(blocks):
    if (i % 2 != 0): continue
    subject = block.find('div', class_='title').find('span').text.strip()
    time = block.find('div', class_='time').text.replace(' ', '')
    teacher_name = ' '.join(block.find('div', class_='lecturer').text.split(' ')[2:4]).strip()
    classroom = block.find('span', class_='auditorium').text.replace('-', '').strip()
    try:
        cursor.execute('SELECT id FROM teachers WHERE name=%s', (teacher_name, ))
        teacher_id = cursor.fetchall()[0][0]
    except IndexError: teacher_id = None
    try: week = block.find('div', class_='week').text
    except AttributeError: pass
    try: day = block.find('div', class_='day').text
    except AttributeError: pass
    try: month = block.find('div', class_='month').text
    except AttributeError: pass
    time = week+'.'+day+'.'+month+'.'+time
    print(teacher_id)
    print(classroom)
    print(time)
    print(subject)
    print(current_group)
    if (teacher_id != None): 
        print(cursor.execute("INSERT INTO schedule(teacher_id, class, time, subject, group_id) VALUES (%s, %s, %s, %s, %s)", (int(teacher_id), classroom, time, subject, current_group)))
    else: cursor.execute('INSERT INTO schedule (class, time, subject, group_id) VALUES (%s, %s, %s, %s)', (classroom, time, subject, current_group))
    conn.commit()

conn.close()
