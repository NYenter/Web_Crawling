from urllib.request import urlopen as uReq
from urllib.request import Request
from bs4 import BeautifulSoup as soup 
my_url = 'https://bakugan.wiki/wiki/Battle_Brawlers_(Card_set)'

#Way to get past forbidden websites that catch bots
req = Request(my_url, headers={'User-Agent': 'Mozilla/5.0'})

html_info = uReq(req).read()
webpage = html_info.decode('utf-8')

page_soup = soup(html_info,'html.parser')

container = page_soup.find("div",{"class":"mw-parser-output"})
container.findAll('table')
table = container.find_all('table',limit = 2)
info_table = table[1]
tr_info = info_table.tbody.find_all("tr")

#test_tr = tr_info[1]
#signle_tr replace test.tr
#td = test_tr.find_all('td')
#card_set_number = td[0]
#image_url_info = td[1].a['href']
#card_name = td[2].a['title']
#card_type = td[3].a['title']
#faction_type = td[4].a['title']

#remove the first index since we don't need it
del tr_info[0]

f = open('Bakugan_Info.csv','w')
headers = "Card Set Number, Card Name, Card Type, Faction Type \n"
f.write(headers)

for single_tr in tr_info:
    td = single_tr.find_all('td')
    card_type = td[3].a['title']
    
    if 'Evo' in card_type or 'Character' in card_type:
        image_url_info = td[1].a['href']
        if '%3F%3F%3F' not in image_url_info:
            card_set_number = td[0]
            card_name = td[2].a['title']
            faction_type = td[4].a['title']
            print(card_set_number)
            print(image_url_info)
            print(card_name)
            print(card_type)
            print(faction_type)
            f.write(str(card_set_number) + ',' + card_name + ',' + card_type + ',' + faction_type + '\n')

f.close()






#do logic to select need info
