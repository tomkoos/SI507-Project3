# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import unittest
import requests
import csv


######### PART 0 #########

def getHTML(link, filename=None):
    if filename == None:
        return requests.get(link).text
    else:
        try:
            with open(filename,'r', encoding='utf8') as f:
                data = f.read()
        except:
            data = requests.get(link).text
            with open(filename, 'w', encoding='utf8') as f:
                f.write(data)
        return data

gallery_data = getHTML('http://newmantaylor.com/gallery.html')
soup = BeautifulSoup(gallery_data, 'html.parser')
for img in soup.find_all('img'):
    print(img.get('alt', 'No alternative text provided!'))


######### PART 1 #########

def getHTML_states(state, filename):
    soup = BeautifulSoup(main_page_data, 'html.parser')
    suffix = soup.find('a', href=True, text=state)['href']
    state_url = 'https://www.nps.gov' + suffix
    return getHTML(state_url, filename)

main_page_data = getHTML('https://www.nps.gov/index.htm', 'nps_gov_data.html')
arkansas_data = getHTML_states('Arkansas', 'arkansas_data.html')
california_data = getHTML_states('California', 'california_data.html')
michigan_data = getHTML_states('Michigan', 'michigan_data.html')


######### PART 2 #########

class NationalSite:
    def __init__(self, soup):
        self.soup = soup
        self.type = soup.find('h2').text if soup.find('h2').text else None    
        self.name = soup.find('h3').text if soup.find('h3').text else None  
        self.location = soup.find('h4').text if soup.find('h4').text else None  
        self.description = soup.find('p').text.strip() if soup.find('p').text else None  

    def __str__(self):
        return '{} | {}'.format(self.name, self.location)

    def __contains__(self, inp):
        return inp in self.name

    def get_mailing_address(self):
        link = self.soup.find_all('a', href=True)[2]['href']
        park_html = getHTML(link)
        park_soup = BeautifulSoup(park_html, 'html.parser')
        address = park_soup.find('div', itemprop = 'address')
        return ' / '.join([item.strip() for item in address.text.replace(',','\n').split('\n') if item])


######### PART 3 #########

def getNatlSites(html):
    state_soup = BeautifulSoup(html, 'html.parser')
    parks_soup = state_soup.find('ul', id='list_parks') \
                           .find_all('li', {'class': 'clearfix'})
    return [NationalSite(soup) for soup in parks_soup]

arkansas_natl_sites = getNatlSites(arkansas_data)
california_natl_sites = getNatlSites(california_data)
michigan_natl_sites = getNatlSites(michigan_data)


######### PART 4 #########

def writeCSV(name, natl_sites):
    with open('{}.csv'.format(name), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Location', 'Type', 'Address', 'Description'])
        for item in natl_sites:
            writer.writerow([item.name,
                             item.location,
                             item.type,
                             item.get_mailing_address(),
                             item.description])

writeCSV('arkansas', arkansas_natl_sites)
writeCSV('california', california_natl_sites)
writeCSV('michigan', michigan_natl_sites)