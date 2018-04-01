# Data-Processing-and-Scraping

Web scraping(bookstore) project

use web scraping to scrap the html file data from the bookstore website. 
Website: http://search.books.com.tw/search/query/key/python/cat/all

*** Target ***
Try to create a detailed csv dataset including author,price,publisher,table of content...from the website.
The csv file would include top 20 books' content with when searching "Python" on this bookstore website.

*** Step ***
Below are the steps of this pytharm file:
1. scrap the html local file and store the file as bookstore.html. 
2. Open the html file, then use lxml tree to extract the title of these books first. 
3. Extract the html page of each book.
4. Download those html files and rename them with the title we got from step 2. 
5. Read the file from the html file
6. Use Xpath to extract the element from the website and store the value in an empty dictionary.
7. Do some data cleaning and examination job, because some of the book website may have different Xpath. 
8. Export the file and store as python_book.csv file. 
