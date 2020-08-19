import requests
from bs4 import BeautifulSoup as BS 
from six.moves.urllib import parse


class telegram_page_download_scroll:

    def __init__(self):
        self.QUEUE = []
        self.post_messages = []

        self.page_counter = 0


    def parse_list_page(self, url):
        #print("page_counter:", self.page_counter)
        if self.page_counter == 3:
            return self.QUEUE

        resp = requests.get(url)
        if resp.status_code == 200:
            soup = BS(resp.text, 'html.parser')
            text= [d.text for d in soup.find_all('div',{'class':'tgme_widget_message_text js-message_text'})] 
        #print(text)
        self.post_messages.append(text)

        r = requests.get(url)
        soup = BS(r.text, "lxml")

        links = soup.select('a[class="tme_messages_more js-messages_more"]')    
        #print(links)

        if links:
            next_link = links[0].attrs['href'] 
            #print("next_link", next_link)

            next_link = "https://telegram.me"+ next_link 
            self.QUEUE.append(
                (self.parse_list_page, next_link)
            )
            self.page_counter = self.page_counter + 1

    def main(self, user):
        self.QUEUE.append(
            (self.parse_list_page, user)
        )

        while len(self.QUEUE):
            call_back, url = self.QUEUE.pop(0)
            call_back(url)

        return self.post_messages


    def teleg_page_info(self, url):
        source = requests.get(url).text
        soup = BS(source, 'lxml')
        output = {}
        counters = [d.text for d in soup.find_all('span', {'class':'counter_value'})]
        output['title'] = [d.text for d in soup.find_all('div', {'class':'tgme_channel_info_header_title'})]
        output['members'] = counters[0]
        output['photos'] = counters[1]
        output['videos'] = counters[2]
        output['files'] = counters[3]

        return output

