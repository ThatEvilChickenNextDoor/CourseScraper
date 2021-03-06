from bs4 import BeautifulSoup
import sqlite3
import requests

import prereqScraper as ps

LOCAL = False
SCRAPE = True

def findCourses(soup, con, semester):
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

    dat = [[row[0], row[1][:-3]] + row[2:4] + [semester] for row in courses]

    with con:
        con.executemany('''INSERT OR IGNORE INTO courses (crn, course, attr, title, semester)
            VALUES (?, ?, ?, ?, ?);''', dat)

if __name__ == '__main__':

    if SCRAPE:
        con = sqlite3.connect('store.db')
    else:
        con = sqlite3.connect(':memory:')
        
    con.execute('''DROP TABLE IF EXISTS courses;''')
    con.execute('''CREATE TABLE courses (
        crn INTEGER PRIMARY KEY,
        course TEXT UNIQUE,
        attr TEXT,
        title TEXT,
        semester TEXT,
        prereqs TEXT DEFAULT '?',
        coreqs TEXT DEFAULT '?',
        require TEXT DEFAULT '?'
        );''')

    if LOCAL:
        with open('csciCoursePage.html') as page:
            soup = BeautifulSoup(page, 'html5lib')
    else:
        URLf = 'https://courselist.wm.edu/courselist/courseinfo/searchresults?term_code=202010&term_subj=PHYS&attr=0&attr2=0&levl=UG&status=0&ptrm=0&search=Search'
        r = requests.get(URLf)
        soupf = BeautifulSoup(r.text, 'html5lib')
        URLs = 'https://courselist.wm.edu/courselist/courseinfo/searchresults?term_code=202020&term_subj=PHYS&attr=0&attr2=0&levl=UG&status=0&ptrm=0&search=Search'
        r = requests.get(URLs)
        soups = BeautifulSoup(r.text, 'html5lib')

    findCourses(soupf, con, 'Fall')
    findCourses(soups, con, 'Spring')

    if SCRAPE:    
        cur = con.execute('''SELECT crn, semester FROM courses ORDER BY course;''')
        q = cur.fetchall()
        
        res = ps.reqStack(q)

        with con:
            con.executemany('''UPDATE courses SET prereqs=?, coreqs=?, require=? WHERE crn=?;''', res)

    for row in con.execute('''SELECT * FROM courses ORDER BY course;'''):
        print(row, '\n')

    con.close()
