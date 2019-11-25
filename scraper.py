from bs4 import BeautifulSoup
import sqlite3
import requests

LOCAL = False

con = sqlite3.connect(':memory:')
con.execute('''DROP TABLE IF EXISTS courses;''')
con.execute('''CREATE TABLE courses (
    crn INTEGER PRIMARY KEY,
    course TEXT,
    section INTEGER,
    attr TEXT,
    title TEXT,
    instr TEXT
    );''')
if LOCAL:
    with open('csciCoursePage.html') as page:
        soup = BeautifulSoup(page, 'lxml')
else:
    URL = 'https://courselist.wm.edu/courselist/courseinfo/searchresults?term_code=202020&term_subj=CSCI&attr=0&attr2=0&levl=UG&status=0&ptrm=0&search=Search'
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html5lib')
table = soup.table
table_rows = table.find_all('tr')

'''
courses = list()
for row in table_rows:
    contents = row.find_all('td')
    course = [i.text.strip() for i in contents]
    if len(course) > 0:
        courses.append(course)
'''

courses = [[i.text.strip() for i in row.find_all('td')] for row in table_rows][1:]

dat = [[row[0], row[1][:-3], row[1][-2:]] + row[2:5] for row in courses]

#for course in dat:
#    print(course)

with con:
    con.executemany('''INSERT INTO courses (crn, course, section, attr, title, instr)
        VALUES (?, ?, ?, ?, ?, ?);''', dat)
        
for course in con.execute('''SELECT DISTINCT course FROM courses ORDER BY course;'''):
    cur = con.execute('''SELECT crn FROM courses WHERE course=? ORDER BY section;''', course)
    print(cur.fetchone()[0], course[0])

con.close()
