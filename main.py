from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import re
import tkinter
from tkinter import messagebox
import time
from link import Link

browser = webdriver.Chrome('/Users/georgiamartinez/Downloads/chromedriver')

root = tkinter.Tk()
root.withdraw()


# Find all wiki links
def find_link(paragraph):
    for link in paragraph.find_all('a', href=True):
        name = link.text
        url = str(link['href'])

        if url.startswith('/wiki/') and len(name) > 1 and not name == '':
            # print(f'{name}, {url}')
            return Link(name, url)
            break


# Display message
def show_message(message):
    print(message)
    input = tkinter.messagebox.askquestion('Philosophy Program', message + '\n\nWould you like to run the program again?')

    if input == 'yes':
        print('\nNEW RUN: ')
        search()
    else:
        browser.quit()

# Random page to Philosophy
def search():
    new_page = 'https://en.wikipedia.org/wiki/Special:Random'
    pages_visited = []
    tries = 0

    start_time = time.perf_counter()

    while True:
        browser.get(new_page)
        source = requests.get(browser.current_url).text
        soup = BeautifulSoup(source, 'lxml')

        # Find the page title
        title = soup.find('h1').text

        if title == 'Philosophy':
            finish_time = time.perf_counter()
            total_time = round(finish_time - start_time, 3)

            print('Philosophy!!!')

            message = f'It took {tries} links to get from "{pages_visited[0]}" to "Philosophy".\n\nTime: {total_time} seconds'
            show_message(message)

        else:
            print(title)
            # print(f'\n{title}')
            # print(f'Page: {tries}')
            # print(browser.current_url)

        # Check for loops
        if title in pages_visited:
            message = 'A loop was found so the program is stopping.'
            show_message(message)

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
        if find_link(paragraph):
            first_link = find_link(paragraph)
        else:
            # Checking links outside of p tags
            paragraph = soup.find(id='mw-content-text')

            if find_link(paragraph):
                first_link = find_link(paragraph)
            else:
                message = 'The program couldn\'t find a link so is stopped.'
                show_message(message)

        if '(disambiguation)' in first_link.url:
            first_link.url = first_link.url.replace('(disambiguation)', '')

        tries += 1

        # print(f'First link: {first_link.name}, {first_link.url}')

        new_page = f'https://en.wikipedia.org{first_link.url}'
        # print(f'New page: {new_page}')


# Run the program
search()
