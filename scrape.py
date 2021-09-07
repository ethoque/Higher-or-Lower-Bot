import requests
import numpy
import time
from bs4 import BeautifulSoup
from ItemList import list
import csv


class PriceFetcher:
  def fetch_price(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    prices = soup.find_all("span",{"class": "infobox-quantity-replace"})
    if not prices:
      return [URL, 0]
    number = 0
    for i in reversed(range(len(URL))):
      if URL[i].isdigit() and number == 0:
        number = int(URL[i])
      if URL[i] == "#":
        break

    URL = URL.replace("%2B","+")
    if URL.count('Poison') != 0:
      number = 2
      number += URL.count('+')
    if number>len(prices)-1:
      number = len(prices)-1
    price_as_int = prices[number].get_text(strip=True)
    price_as_int = int(price_as_int.replace(',', ''))
    return price_as_int  

  def fetch_item(dict_of_item):
    item = dict_of_item['name']
    return PriceFetcher.fetch_price((URLBuilder.build_url(item)))


class URLBuilder:
  def build_url(input_item):
    URL = "https://oldschool.runescape.wiki/w/"
    item_url = input_item.replace(" ","_")

    if "potion(" in input_item:
      number = input_item[-2]
      input_item = input_item[:-3] + "#" + number + "_dose"

    if "(p" in input_item:
      input_item = input_item.replace("(p","#Poison")
      input_item = input_item.replace(")","")

    input_item = input_item.replace("+","%2B")
    item_url = input_item.replace(" ","_")  
    URL = URL + item_url
    return URL



#Creating new data with sorted prices
class list_data:
  def fetch_list_prices_with_range(start,end,filename):

    new_list = []
    for i in range(start,end):
      new_list.append(PriceFetcher.fetch_item(list[i]))
      time.sleep(1.3)

    sorted_list = sorted(new_list,key = lambda x: x[1])

    numpy_list = numpy.array(sorted_list)
    print(numpy_list)
    numpy.save(filename,numpy_list)

#Hosting on repl.it, overall load has to be light.
  def build_list():
    list_prices1 = numpy.load('SortedData 0-499.npy')
    list_prices2 = numpy.load('SortedData 500-999.npy')
    list_prices3 = numpy.load('SortedData 1000-1499.npy')
    list_prices4 = numpy.load('SortedData 2000-2499.npy')
    list_prices5 = numpy.load('SortedData 2500-end.npy')

    list_test = numpy.concatenate((list_prices1,list_prices2,list_prices3,list_prices4,list_prices5))
    list_test = list_test.tolist()
    for x in list_test:
      x[1] = int(x[1])
    list_test = sorted(list_test,key = lambda x: x[1])
    numpy_list = numpy.array(list_test)
    numpy.set_printoptions(threshold=numpy.inf)

    numpy.save('SortedData Full',numpy_list)



class pic_scraper:
  def build_url(input_item):
    URL = "https://oldschool.runescape.wiki/w/File:"
    item_url = input_item.replace(" ","_")

    if not '(p' in input_item:
      input_item = input_item.replace("+","%2B")
    if '(p+)' or '(p++)' in input_item:
      input_item = input_item.replace("(p+)",'(p)')
      input_item = input_item.replace("(p++)",'(p)')
    item_url = input_item.replace(" ","_")  
    URL = URL + item_url + '_detail.png'
    return URL

  def fetch_pic(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    pic = soup.find_all("img")
    if not pic:
      return 'ERROR ' + URL

    pic_url = pic[0]
    pic_url = pic_url.attrs['src']
    pic_url = 'https://oldschool.runescape.wiki' + pic_url
    return pic_url

  def fetch_item(dict_of_item):
    item = dict_of_item['name']
    return PriceFetcher.fetch_price((URLBuilder.build_url(item)))



#with open('data_items.csv', 'a', newline='') as file:
#  writer = csv.writer(file)
#  for i in list[2500:len(list)]:
#    info = []
#    item = i['name']
#    info.append(item)
#    info.append(PriceFetcher.fetch_price(URLBuilder.build_url(item)))
#    info.append(pic_scraper.fetch_pic(pic_scraper.build_url(item)))
#    writer.writerow(info)


#print(PriceFetcher.fetch_price(URLBuilder.build_url(item)))
#print(pic_scraper.fetch_pic(pic_scraper.build_url(item)))
with open(("data_items.csv")) as file:
  reader = csv.reader(file)
  sortedlist = sorted(reader, key=lambda row: int(row[1]))
  with open('sorted_data_items.csv','w') as file:
    writer = csv.writer(file)
    writer.writerow(['Item','Price','Picture'])
    for i in sortedlist:
      writer.writerow(i)




#sortedlist = sorted(reader, key=lambda row: row[1], reverse=True)

