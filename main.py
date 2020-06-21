from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import re
import time
from link import Link

# Start with a random Wikipedia article
new_page = 'https://en.wikipedia.org/wiki/Special:Random'
browser = webdriver.Chrome('/Users/georgiamartinez/Downloads/chromedriver')

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
        print('\n' + title + '!!!')
        print('It took ' + str(tries) + ' links to get from ' + pages_visited[0] + ' to Philosophy.')
        break
    else:
        print('\n' + title)
        print('Page: ' + str(tries))

    print(browser.current_url)

    # Check for loops
    for name in pages_visited:
        if name == title:
            print('Loop')
            search = False
            break

    pages_visited.append(title)

    # Get the paragraph
    paragraph = soup.find(id='mw-content-text')

    # Remove unnecessary tags
    for unwanted in soup.find_all(['span', 'table', 'small']):
        unwanted.replace_with('')

    paragraph = paragraph.find_all('p')
    paragraph = re.sub(r' \(.*?\)', '', str(paragraph))
    paragraph = BeautifulSoup(paragraph, 'lxml')

    # Debugging
    text = ''
    for p in paragraph.find_all('p'):
        text += p.text

    # Get all links
    all_links = []

    for link in paragraph.find_all('a', href=True):
        name = link.text
        url = str(link['href'])

        if url.startswith('/wiki/') and len(name) > 1 and not name == '':
            all_links.append(Link(name, url))

    paragraph = str(paragraph)

    # Find all dialogue tags
    for x in paragraph:
        if x.find('&quot;'):
            paragraph = paragraph.replace('&quot;', '\"')

    # Find the first link
    first_link = Link(all_links[0].name, all_links[0].url)

    # index = len(paragraph)
    # for link in all_links:
    #     name = link.name
    #     url = link.url
    #     new_index = paragraph.index(url)
    #
    #     if paragraph.index(url) > - 1:
    #         print('FOUND: ' + name + ' [' + str(paragraph.index(url)) + ']' + url)
    #
    #         if new_index < index:
    #             print('NEW INDEX: ' + name + ' [' + str(paragraph.index(url)) + '] ' + url)
    #             first_link = link
    #             index = new_index

    tries += 1

    if '(disambiguation)' in first_link.url:
        first_link.url = first_link.url.replace('(disambiguation)', '')

    print('First link: ' + first_link.name + ', ' + first_link.url)

    new_page = ('https://en.wikipedia.org' + first_link.url)
    print('New page: ' + new_page)

time.sleep(5)
browser.close()
