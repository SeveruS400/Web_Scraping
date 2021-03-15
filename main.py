import requests
from bs4 import BeautifulSoup
import pandas as pd

url="https://www.migros.com.tr"

def get_data(url):
    r=requests.get(url)
    soup=BeautifulSoup(r.text,"html.parser")
    return soup

def parse(soup):
    productslist=[]
    titles=[]
    nextpage=True

    results=soup.find_all("li",{"class":"category-list-item category-title"})
    for subtitle in results:
        title_att={
            "name":subtitle.find("a").text.strip(),
            "link":subtitle.find("a")["href"].strip(),
        }
        #print(title_att["name"]+"  "+url+title_att["link"])
        titles.append(title_att)

    for m in titles[0:int(len(titles)/2)]:
        count=2
        def getnextpage(itemlink,count):
            page = itemlink.find()
            if not page.find("li", {"class": "pag-next"}):
                return
            else:
                return url + m["link"]+"?sayfa="+str(count)

        itemlink = get_data(url + m["link"])
        item_list = itemlink.find_all("div", {"class": "list"})
        print(m["name"])
        nextItemLink = itemlink
        while True:
            for j in item_list:

                    item={
                        "name":j.find("h5",{"class":"title product-card-title"}).text.strip(),
                        "price":j.find("span",{"class":"value"}).text.strip(),
                        "link":j.find("a")["href"].strip(),
                    }
                    productslist.append(item)

                    print(item["name"]+"  "+item["price"]+"  "+url+item["link"])

            nexturl = getnextpage(nextItemLink,count)
            if nexturl == None:
                break
            else:
                count = count + 1
                print("sayfa"+str(count)+"basıldı")
                nextItemLink2 = get_data(nexturl)
                nextItemLink = nextItemLink2
                item_list2 = nextItemLink2.find_all("div", {"class": "list"})
                item_list=item_list2

    return productslist

def output(productslist):
    # dosya=open("sonuc.txt","w+")
    # dosya.write(str(productslist))
    # dosya.close()
    productsdf=pd.DataFrame(productslist)
    productsdf.to_csv("Migros_Fiyat_Listesi.csv",index=False)
    print("Saved to CSV")
    return

soup = get_data(url)
productslist=parse(soup)
output(productslist)

# nexturl = getnextpage(soup)
# if nexturl == None:
#     nextpage = False
# else:
#     nextItemLink = get_data(nexturl)
#     j = nextItemLink.find_all("div", {"class": "list"})

