import csv
import urllib.request as urllib2
from bs4 import BeautifulSoup


root_url = 'http://books.toscrape.com/';
quote_page = 'http://books.toscrape.com/catalogue/the-great-railway-bazaar_446/index.html';
page = urllib2.urlopen(quote_page);
soup = BeautifulSoup(page, 'html.parser');

img_link = soup.find('img')['src'];
img_link = img_link[6:];
img_link = root_url + img_link;

book_data = {
    'product_page': quote_page,
    'universal_product_code': soup.findAll('td')[0].get_text(),
    'title': soup.find('h1').get_text(),
    'price_including_tax': soup.findAll('td')[2].get_text(),
    'price_excluding_tax': soup.findAll('td')[3].get_text(),
    'number_available':soup.findAll('td')[5].get_text(),
    'product_description':soup.findAll("p")[3].get_text(),
    'category':soup.findAll('a')[3].get_text(),
    'review_rating':soup.findAll('td')[6].get_text(),
    'image_url':img_link,
}

for i,j in book_data.items():
    print(i,': ',j)
with open('book_test.csv', 'w', newline='') as csvfile:
    dict_writer = csv.DictWriter(csvfile,fieldnames=book_data, dialect = csv.excel)
                                 
    dict_writer.writeheader()
    dict_writer.writerow(book_data);
    #dict_writer.writerows(book_data)
    
#print(soup.findAll("p")[3].get_text())
#print(soup.find('h1').get_text())
#print(soup.findAll('a')[3].get_text())
#print(soup.find('img')['src'])
#print(img_link);
#print(book_data);
#for a in soup.findAll('th'):
#    print(a.get_text());
#for a in soup.findAll('td'):
#    print(a.get_text());
#count = 0;