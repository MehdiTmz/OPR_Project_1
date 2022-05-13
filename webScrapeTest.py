from ast import Num
import csv
from unicodedata import category
import urllib.request as urllib2
from bs4 import BeautifulSoup
import os

# Parameter of the function:
# - url = url of the image (str).
# - name = title of the book.

def download_image(url,name):
    # remove all the character except num and letter
    s = ''.join(ch for ch in name if ch.isalnum())+'.jpg';
    
    # Create a directory image
    if not os.path.exists('image'):
        os.makedirs('image');
        
    # Save the image in the directory image  
    urllib2.urlretrieve(url,'image/'+s);s
    #print('Image Dowloaded succesfully');

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

    download_image(img_link,book_data['title']);
    
    return book_data;
    
def categoryDataRetreiver(quote_page,root_url,quote_page_cat_root):
    page = urllib2.urlopen(quote_page);
    soup = BeautifulSoup(page, 'html.parser');
    page_num = soup.find_all('a')[-1].get_text();
    
    url_book_list = [];
    category_book_data = [];
    temp_cat_list = [];


    for x in soup.find_all('div', class_='image_container'):
        url = x.find('a')['href'][9:];
        url = root_url +'catalogue/'+ url;
        category_book_data.append(bookDataRetrieve(url,root_url));
        url_book_list.append(url);
        
    if(page_num == 'previous'):
        return category_book_data;
    
    if(page_num == 'next'):
            temp_quote = quote_page_cat_root + soup.find_all('a')[-1]['href'];
            temp_cat_list  = categoryDataRetreiver(temp_quote,root_url,quote_page_cat_root);
            category_book_data.extend(temp_cat_list);
    return category_book_data;

def URLcategoryfunction(soup):
    url_cat_list = [];
    root_url_cat_list = [];
    cat_txt =[];

    for x in soup.find('ul', class_='nav nav-list').find_all('li'):
        url_temp1 = x.find('a')['href'];
        cat_txt.append(x.get_text())
        url_cat_list.append(url_temp1);
        url_temp2 = url_temp1.replace('index.html','');
        root_url_cat_list.append(url_temp2)

    del url_cat_list[0]
    del root_url_cat_list[0]
    del cat_txt[0]
    return url_cat_list,root_url_cat_list,cat_txt;

####### Script  ##########

root_url = 'http://books.toscrape.com/';
quote_page = 'http://books.toscrape.com/catalogue/full-moon-over-noahs-ark-an-odyssey-to-mount-ararat-and-beyond_811/index.html';
quote_page2 = 'http://books.toscrape.com/catalogue/category/books/travel_2/index.html';
quote_page_cat_root = 'http://books.toscrape.com/catalogue/category/books/travel_2/';

page = urllib2.urlopen(root_url);
soup = BeautifulSoup(page, 'html.parser');

print('hello')
url_cat_list, root_url_cat_list, cat_txt = URLcategoryfunction(soup);

for x in url_cat_list:
    print('Currently working in the following link : ',root_url + x)
    csv_header = ['product_page','universal_product_code','title','price_including_tax','price_excluding_tax','number_available','product_description','category','review_rating','image_url'];
    cat_name = cat_txt[url_cat_list.index(x)].replace('\n','').replace(' ',"");
    
    with open('book'+ cat_name +'.csv', 'w',encoding="utf-8", newline='') as csvfile:
        dict_writer = csv.DictWriter(csvfile,fieldnames=csv_header, dialect = csv.excel)                         
        dict_writer.writeheader()                
        
        page_book_list = categoryDataRetreiver(root_url + x,root_url,root_url + root_url_cat_list[url_cat_list.index(x)]);
        print('There are '+ str(len(page_book_list))+' books in the '+ cat_name +' category')
        for x in range(len(page_book_list)):
            dict_writer.writerow(page_book_list[x])