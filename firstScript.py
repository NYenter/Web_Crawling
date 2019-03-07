from urllib.request import urlopen as uReq
from urllib.request import Request
import urllib.request as Retrieve
from bs4 import BeautifulSoup as soup 

#Global Variables
wiki_url = 'https://bakugan.wiki'

def DownloadImages(image_urls, save_names):
    from stat import S_IWUSR, S_IRUSR
    import os, re, shutil, requests
    
    # Set file path and permissions
    folder_path = 'C:/Bakugan_Images/'
    os.chmod(folder_path, S_IWUSR | S_IRUSR)

    # Use cur_name_index to keep track of name
    cur_name_index = 0

    for image_url in image_urls:     
        # Concatenate together file destination, name of the file, and type of file extension
        completeName = os.path.join(folder_path + save_names[cur_name_index] + ".png")         
        image_req = Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        image_html_info = uReq(image_req).read()
        image_page_soup = soup(image_html_info, 'html.parser')
        image_container = image_page_soup.find('div', {'class':'fullImageLink'})
        image_src = wiki_url + image_container.find('a').find('img')['src']

        # Way to get past 403 Error
        r = requests.get(image_src, stream=True, headers={'User-agent': 'Mozilla/5.0'})

        # Save image using completeName with write, binary permissions ('wb')
        if r.status_code == 200:
            with open(completeName, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

        cur_name_index +=1

def MainHtmlParser():
    website_url = 'https://bakugan.wiki/wiki/Battle_Brawlers_(Card_set)'
    req = Request(website_url, headers={'User-Agent': 'Mozilla/5.0'})
    html_info = uReq(req).read()
    page_soup = soup(html_info,'html.parser')
    container = page_soup.find("div",{"class":"mw-parser-output"})
    table = container.find_all('table',limit = 2)
    info_table = table[1]
    tr_info = info_table.tbody.find_all("tr")

    #remove the first index since we don't need it for the report
    del tr_info[0]

    # Open a new file to write to 
    f = open('Bakugan_Info.csv','w')
    column_headers = "Card Set Number, Card Name, Card Type, Faction Type, Image URL \n"
    f.write(column_headers)

    # Create lists to hold info that will be passed to a function
    image_urls = []
    image_save_names = []
    
    for single_tr in tr_info:
        td = single_tr.find_all('td')
        card_type = td[3].a['title']
    
        if 'Evo' in card_type or 'Character' in card_type:
            # Grab image url
            image_url_info = td[1].a['href']
            # skip all blank images
            if '%3F%3F%3F' not in image_url_info:
                card_set_number = td[0]
                offical_image_url = wiki_url + image_url_info
                # Add to list to be used when dl the image
                image_url_list.append(offical_image_url)
                card_name = td[2].a['title']
                faction_type = td[4].a['title']
                save_name = card_name + faction_type
                # Add to list to be used when saving the dl image
                image_save_name.append(save_name)

                f.write(str(card_set_number) + ',' + card_name + ',' + card_type + ',' + faction_type + ',' + offical_image_url + '\n')
    f.close()

    # Call func to dl images
    DownloadImages(image_urls, image_save_names)

#Processing
MainHtmlParser()
