import requests
from bs4 import BeautifulSoup
import re
import base64


class Spider:
    session = requests.session()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0'
    host = 'https://www.mirdvornikov.ru'

    @classmethod
    def get_html(cls, url, func_name):
        print(func_name + " -> " + url)
        response = cls.session.get(url=url, headers={'User-Agent': cls.user_agent})

        return response.text

    @classmethod
    def get_categories_links(cls):
        html = cls.get_html(url=cls.host + '/catalog/', func_name='get_categories_links')
        soup = BeautifulSoup(html, "html.parser")
        a_list = soup.find_all('a', class_='cat_top_img_wrap')
        links = [i.attrs['href'] for i in a_list]

        return links

    @staticmethod
    def pages_quantity(soup):

        parent_tag = soup.find('div', class_='nav-pages')
        if parent_tag:
            a_list = parent_tag.find_all('a')
            last_link = a_list[len(a_list) - 1].attrs['href']
            sub_string = re.findall(r'PAGEN_\d=\d{0,}', last_link)[0]
            pages_quantity = re.split(r'=', sub_string)[1]

            return int(pages_quantity)
        else:
            return None
    @classmethod
    def get_products_links(cls, category_url):
        # get links from first page
        html = cls.get_html(url=cls.host + category_url, func_name='get_products_links')
        soup = BeautifulSoup(html, "html.parser")
        div_list = soup.find_all('div', class_='sitem-head')
        links = [a.find('a').attrs['href'] for a in div_list]
        # get quantity pages
        pages_quantity = cls.pages_quantity(soup)
        # iteration for pages
        if pages_quantity:
            for page_num in range(2, pages_quantity + 1):
                page = f'?PAGEN_1={page_num}'
                url = category_url + page
                html = cls.get_html(url=cls.host + url, func_name='get_products_links')
                soup = BeautifulSoup(html, "html.parser")
                div_list = soup.find_all('div', class_='sitem-head')
                links.extend([a.find('a').attrs['href'] for a in div_list])
        else:
            html = cls.get_html(url=cls.host + category_url, func_name='get_products_links')
            soup = BeautifulSoup(html, "html.parser")
            div_list = soup.find_all('div', class_='sitem-head')
            links.extend([a.find('a').attrs['href'] for a in div_list])

        return links

    @staticmethod
    def replace_sep(string):
        # support foo
        for _ in range(len(string)):
            string = string.replace('\n', '')
            string = string.replace('\t', '')
            string = string.replace('\xa0', '')
        return string

    @classmethod
    def get_product_content(cls, product_url):
        result = {
            "brand": '',
            "name": '',
            "article": '',
            "group": 'Щетки стеклоочистителя',
            'params': []
        }

        html = cls.get_html(url=cls.host + product_url, func_name='get_product_content')
        soup = BeautifulSoup(html, "html.parser")

        dl = soup.find('dl', class_='sitem-props')
        dt_list = [i.text for i in dl.find_all('dt')]  # left colum
        dd_list = [cls.replace_sep(i.text) for i in dl.find_all('dd')]  # right colum

        #  PARAMS OF PRODUCT
        result["name"] = soup.find('h1', class_='sitem-head').text
        for left_co_item, right_co_item in zip(dt_list, dd_list):
            if left_co_item == 'Рейтинг':
                continue
            if left_co_item == 'Производитель':
                result['brand'] = right_co_item
            elif left_co_item == 'Артикул':
                result['article'] = right_co_item
            else:
                if right_co_item != '':
                    result['params'].append({"name": left_co_item, "value": right_co_item})
                else:
                    continue

        #  DESCRIPTION
        description = soup.find('div', id='DESCRIPTION')
        if description:
            description = description.text
            result["text"] = description

        # RELATION CARS
        cars_parent_block = soup.find('div', 'app_links')
        if cars_parent_block:
            relation_cars_url = [i.attrs['href'] for i in cars_parent_block.find_all('a')]
            if relation_cars_url:
                relation_cars_content = [cls.get_relation_car(url) for url in relation_cars_url]
                if relation_cars_content:
                    result["models"] = relation_cars_content

        #  IMAGES
        images_parent_block = soup.find('div', class_='sitem-pics')
        images_url = [i.attrs['href'] for i in images_parent_block.find_all('a')]
        files = []
        for image_url in images_url:
            if image_url:
                files.append(cls.get_img_convert_base64(cls.host + image_url))
        if files:
            result["files"] = files

        return result

    @classmethod
    def get_relation_car(cls, car_url):
        html = cls.get_html(url=cls.host + car_url, func_name='get_relation_car')
        soup = BeautifulSoup(html, "html.parser")
        parent_block = soup.find('div', id='filter-content-auto')
        #  manufacturer
        option_list = parent_block.find('select', id='select-mfa').find_all('option')
        manufact = ''
        for elem in option_list:
            if elem.get('selected', False) == '':
                if elem.text == 'Выберите марку':
                    continue
                else:
                    manufact = elem.text
                    break
        #  model
        option_list = parent_block.find('select', id='select-mod').find_all('option')
        model = ''
        for elem in option_list:
            if elem.get('selected', False) == '':
                if elem.text == 'Выберите модель':
                    continue
                else:
                    model = elem.text
                    break
        #  modification
        option_list = parent_block.find('select', id='select-type').find_all('option')
        modfic = ''
        for elem in option_list:
            if elem.get('selected', False) == '':
                if elem.text == 'Выберите модификацию':
                    continue
                else:
                    modfic = elem.text
                    break
        modific_range = re.findall(r'\d{2}.\d{4}->|\d{2}.\d{4}-\d{2}.\d{4}', modfic)[0]
        modfic = modfic.replace(modific_range, '')
        modific_range = modific_range.replace('>', '')
        return {"manufacturer": manufact, "name": model, "modifications": [{"name": modfic, "range": modific_range}]}

    @staticmethod
    def get_img_convert_base64(url):
        r = requests.get(url)
        if r.status_code == 200:
            encoded_string = base64.b64encode(r.content)
            return str(encoded_string).lstrip("b'").rstrip("'")
