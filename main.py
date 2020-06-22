from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import re
import tkinter
from tkinter import messagebox
import time
from link import Link

# Start with a random Wikipedia article
new_page = 'https://en.wikipedia.org/wiki/Special:Random'
browser = webdriver.Chrome('/Users/georgiamartinez/Downloads/chromedriver')

root = tkinter.Tk()
root.withdraw()

pages_visited = []
search = True
tries = 0

start_time = time.perf_counter()

while search:
    browser.get(new_page)
    source = requests.get(browser.current_url).text
    soup = BeautifulSoup(source, 'lxml')

    # Find the page title
    title = soup.find('h1').text

    if title == 'Philosophy':
        finish_time = time.perf_counter()
        time = round(finish_time - start_time, 3)

        print('\nPhilosophy!!!')
        print(f'It took {tries} links to get from "{pages_visited[0]}" to "Philosophy".')
        tkinter.messagebox.showinfo('Philosophy Program', f'It took {tries} links to get from "{pages_visited[0]}" '
                                                          f'to "Philosophy".\n\nTime: {time}')
        break
    else:
        print(f'\n{title}')
        print(f'Page: {tries}')

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

    print(f'First link: {first_link.name}, {first_link.url}')

    new_page = f'https://en.wikipedia.org{first_link.url}'
    print(f'New page: {new_page}')

browser.quit()
