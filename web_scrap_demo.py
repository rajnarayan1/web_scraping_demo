import json
import bs4
from selenium import webdriver


class scrap_amazon_data:

    def __init__(self, product_name):
        self.product_name = product_name

    '''This function will provide required url for searching a product in Amazon'''

    def make_url_for_amazon_search(self):
        url = 'https://www.amazon.in/s?k={}&ref=nb_sb_noss_2'
        '''Replacing spaces with + sign to make a proper url'''
        search_term = self.product_name.replace(' ', '+')
        return url.format(search_term)

    def write_product_to_file(self, product_dict):
        try:
            with open('convert.txt', 'w') as convert_file:
                convert_file.write(json.dumps(product_dict))
        except:
            print('Something went wrong. Can not write to file')

    '''opening web browser, fetching required details and adding them to file in json format'''
    def open_browser_and_fetch_data(self):
        product_dict = {}
        url = self.make_url_for_amazon_search()
        driver = webdriver.Chrome(executable_path='/home/necs/PycharmProjects/pythonProject/web_scraping/chromedriver')
        driver.get(url)
        soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'class': 's-include-content-margin s-border-bottom s-latency-cf-section'})

        for i in results:
            atag = i.h2.a
            description = atag.text.strip()
            price_elm = i.find('span', 'a-price')
            current_price = price_elm.find('span', 'a-offscreen').text.strip()
            product_dict[description] = current_price
        driver.close()

        self.write_product_to_file(product_dict)



calling_amazon_scrap = scrap_amazon_data('mobile')

calling_amazon_scrap.open_browser_and_fetch_data()

