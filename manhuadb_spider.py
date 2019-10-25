"""漫画DB爬虫"""

import os
import requests
import json
from bs4 import BeautifulSoup


FILE_PATH = 'F:/01_Comic/昆虫末日/'
WEB_URL = 'https://www.manhuadb.com/'
COMIC_URL = 'https://www.manhuadb.com/manhua/8615'

def get_count(url):
    first_page = requests.get(url).text
    soup = BeautifulSoup(first_page, 'html.parser')
    return int(soup.find_all(class_='vg-r-data')[0].attrs['data-total'])

def get_comic_list():
    """get all comic list"""

    respont = requests.get(COMIC_URL)
    respont.raise_for_status()
    soup = BeautifulSoup(respont.text, "html.parser")
    comics = []
    section_name = []

    for tag in soup.find_all(class_='fixed-a-es'):
        comics.append(tag.attrs["href"])
        section_name.append(tag.string)

    return comics, section_name

def set_comic_list_need(comics, section_name):
    if not os.path.exists(FILE_PATH + 'data.txt'):
        os.makedirs(FILE_PATH)
        with open(FILE_PATH + 'data', 'w+') as file:
            data = {'max_section', section_name[-1]}
            file.write(data)
    else:
        with open(FILE_PATH + 'data', 'w+') as file:
            max_section_download = json.load(file.read)['max_section']
            index_of_section_download = section_name.index(max_section_download)
            if index_of_section_download + 1 == len(section_name):
                comics = []
                section_name = []
            else:
                comics = comics[index_of_section_download:]
                section_name = section_name[index_of_section_download:]
                max_section_download['max_section'] = section_name[-1]
                file.write(max_section_download)

def get_html(url):
    """aq"""

    respont = requests.get(url)
    respont.raise_for_status()
    return respont.text

def parse_html(html):
    """parse html"""

    soup = BeautifulSoup(html, "html.parser")
    img = soup.img
    return img.attrs['src']

def write_to_file(file_info, file_path, file_name):
    """write to file"""

    with open(file_path + str(file_name) + '.jpg', "wb") as img:
        img.write(requests.get(file_info).content)


def main():
    """master"""
    comic_list, section_name = get_comic_list()
    set_comic_list_need(comic_list, section_name)

    if len(comic_list) == 0:
        print('没有更新')
        return

    for comic in comic_list:
        count = get_count(WEB_URL + comic)
        url = (WEB_URL + comic).replace(r'.html', '_p{}.html')
        file_path = FILE_PATH + section_name[comic_list.index(comic)] + "/"

        number = 1
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        while 1:
            if number > count:
                break

            htmls = get_html(url.format(number))
            file_info = parse_html(htmls)
            write_to_file(file_info, file_path, number)
            print('\r进度 : {:.2f}%'.format(number * 100 / count), end='')
            number += 1

if __name__ == '__main__':
    main()
