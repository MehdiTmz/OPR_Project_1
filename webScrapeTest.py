import csv
from unicodedata import category
import urllib.request as urllib2
from bs4 import BeautifulSoup

count = 1;
def bookDataRetrieve(quote_page,root_url):
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
    #for i,j in book_data.items():
        #print(i,': ',j)
    return book_data;
    
root_url = 'http://books.toscrape.com/';
quote_page = 'http://books.toscrape.com/catalogue/full-moon-over-noahs-ark-an-odyssey-to-mount-ararat-and-beyond_811/index.html';
#bookDataRetrieve(quote_page);
quote_page2 = 'http://books.toscrape.com/catalogue/category/books/travel_2/index.html';
quote_page_cat_root = 'http://books.toscrape.com/catalogue/category/books/travel_2/';
def categoryDataRetreiver(quote_page,root_url,quote_page_cat_root):
    page = urllib2.urlopen(quote_page);
    soup = BeautifulSoup(page, 'html.parser');
    count = 1;
    page_num = soup.find_all('a')[-1].get_text();
    print(page_num);
    
    url_book_list = [];
    category_book_data = [];
    temp_cat_list = [];
    #dict_writer.writerow(book_data);
    for x in soup.find_all('div', class_='image_container'):
        url = x.find('a')['href'][9:];
        url = root_url +'catalogue/'+ url;
        #print(url);
        #print(count);
        category_book_data.append(bookDataRetrieve(url,root_url));
        count = count +1;
        url_book_list.append(url);
    if(page_num == 'previous'):
        #print( 'HHAHHAHHAHAHAH')
        return category_book_data;
    if(page_num == 'next'):
            
            #print('hello');
            #print(page_num,1);
            temp_quote = quote_page_cat_root + soup.find_all('a')[-1]['href'];
            temp_cat_list  = categoryDataRetreiver(temp_quote,root_url);
            category_book_data.extend(temp_cat_list);
            #print(page_num,2);
    return category_book_data;
                    
csv_header = ['product_page','universal_product_code','title','price_including_tax','price_excluding_tax','number_available','product_description','category','review_rating','image_url'];
with open('book_test2.csv', 'w',encoding="utf-8", newline='') as csvfile:
        dict_writer = csv.DictWriter(csvfile,fieldnames=csv_header, dialect = csv.excel)
                                    
        dict_writer.writeheader()                
        
        page_book_list = categoryDataRetreiver(quote_page2,root_url,quote_page_cat_root);
        print(len(page_book_list))
        for x in range(len(page_book_list)):
            dict_writer.writerow(page_book_list[x])

