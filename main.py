from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import re
import tkinter
from tkinter import messagebox
from link import Link

# Start with a random Wikipedia article
new_page = 'https://en.wikipedia.org/wiki/Special:Random'
browser = webdriver.Chrome('/Users/georgiamartinez/Downloads/chromedriver')

root = tkinter.Tk()
root.withdraw()

pages_visited = []
search = True
tries = 0

while search:
    browser.get(new_page)
    source = requests.get(browser.current_url).text
    soup = BeautifulSoup(source, 'lxml')

    # Find the page title
    title = soup.find('h1').text

    if title == 'Philosophy':
        search = False
        print('\n' + title + '!!!')
        print('It took ' + str(tries) + ' links to get from ' + pages_visited[0] + ' to Philosophy.')
        tkinter.messagebox.showinfo('Philosophy Program', 'It took ' + str(tries) + ' links to get from ' + pages_visited[0] + ' to Philosophy.')
        break
    else:
        print('\n' + title)
        print('Page: ' + str(tries))

    print(browser.current_url)

    # Check for loops
    if title in pages_visited:
        print('LOOP FOUND: Stopping program')
        tkinter.messagebox.showinfo('Philosophy Program', 'LOOP FOUND: Stopping program')
        break

    pages_visited.append(title)

    # Get the paragraph
    paragraph = soup.find(id='mw-content-text')

    # Remove unnecessary tags
    for unwanted in soup.find_all(['span', 'table', 'small']):
        unwanted.replace_with('')

    # Find all paragraph tags and remove ( )
    paragraph = paragraph.find_all('p')
    paragraph = re.sub(r' \(.*?\)', '', str(paragraph))
    paragraph = BeautifulSoup(paragraph, 'lxml')

    # Debugging
    text = ''
    for p in paragraph.find_all('p'):
        text += p.text

    # Get the first link
    all_links = []

    for link in paragraph.find_all('a', href=True):
        name = link.text
        url = str(link['href'])

        if url.startswith('/wiki/') and len(name) > 1 and not name == '':
            all_links.append(Link(name, url))
            break

    if len(all_links):
        first_link = Link(all_links[0].name, all_links[0].url)
    else:
        print('Could not find a link')
        tkinter.messagebox.showinfo('Philosophy', 'COULD NOT FIND LINK: Stopping program')
        break

    if '(disambiguation)' in first_link.url:
        first_link.url = first_link.url.replace('(disambiguation)', '')

    tries += 1

    print('First link: ' + first_link.name + ', ' + first_link.url)

    new_page = ('https://en.wikipedia.org' + first_link.url)
    print('New page: ' + new_page)

browser.quit()
