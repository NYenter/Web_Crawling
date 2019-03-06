from urllib.request import urlopen as uReq
from urllib.request import Request
import urllib.request as Retrieve
from bs4 import BeautifulSoup as soup 

#Global Variables
wiki_url = 'https://bakugan.wiki'


def DownloadImages(url, name):
    from stat import S_IWUSR, S_IRUSR
    import os, re, shutil, requests
    
    # Set file path and permissions
    save_path = 'C:/Bakugan_Images/'
    os.chmod(file_destination, S_IWUSR | S_IRUSR)

    # Use index to keep track of name
    index = 0

    for image_url in url:     
        #name_of_file = 'test3'
        completeName = os.path.join(save_path + name[index] + ".png")         
        #test = 'https://bakugan.wiki/wiki/File:Pegatrix_(Ventus_Card)_369_CC_BB.png'
        image_req = Request(test, headers={'User-Agent': 'Mozilla/5.0'})
        image_html_info = uReq(image_req).read()
        #image_webpage = image_html_info.decode('utf-8')
        image_page_soup = soup(image_html_info, 'html.parser')
        image_container = image_page_soup.find('div', {'class':'fullImageLink'})
        image_src = wiki_url + image_container.find('a').find('img')['src']

        # Way to get past 403 Error
        r = requests.get(image_src, stream=True, headers={'User-agent': 'Mozilla/5.0'})
        if r.status_code == 200:
            with open(completeName, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

        #f.write(image)
        index +=1
    f.close()


def MainHtmlParser():
    my_url = 'https://bakugan.wiki/wiki/Battle_Brawlers_(Card_set)'
    req = Request(my_url, headers={'User-Agent': 'Mozilla/5.0'})
    html_info = uReq(req).read()
    webpage = html_info.decode('utf-8')
    page_soup = soup(html_info,'html.parser')
    container = page_soup.find("div",{"class":"mw-parser-output"})
    container.findAll('table')
    table = container.find_all('table',limit = 2)
    info_table = table[1]
    tr_info = info_table.tbody.find_all("tr")

    #remove the first index since we don't need it for the report
    del tr_info[0]

    f = open('Bakugan_Info.csv','w')
    headers = "Card Set Number, Card Name, Card Type, Faction Type, Image URL \n"
    f.write(headers)
    image_url_list = []
    image_save_name = []
    
    for single_tr in tr_info:
        td = single_tr.find_all('td')
        card_type = td[3].a['title']
    
        if 'Evo' in card_type or 'Character' in card_type:
            image_url_info = td[1].a['href']
            if '%3F%3F%3F' not in image_url_info:
                card_set_number = td[0]
                offical_image_url = wiki_url + image_url_info
                image_url_list.append(offical_image_url)
                card_name = td[2].a['title']
                faction_type = td[4].a['title']
                save_name = card_name + faction_type
                image_save_name.append(save_name)
                print(card_set_number)
                print('https://bakugan.wiki' + image_url_info)
                print(card_name)
                print(card_type)
                print(faction_type)

                f.write(str(card_set_number) + ',' + card_name + ',' + card_type + ',' + faction_type + ',' + offical_image_url + '\n')
    f.close()

    print(image_url_list)
    #Processing
    #DownloadImages(image_url_list, image_save_name)

#Processing
MainHtmlParser()
