import requests
from bs4 import BeautifulSoup


#  testing
def get_soup(search_keywords):
    # get the first page of offerup using 'nintendo switch' and ship nationwide
    # https://offerup.com/search/?delivery_param=s&q=nintendo%20switch
    keywords = search_keywords.replace(" ", "%20")
    url = 'http://offerup.com/search/?delivery_param=s&q=' + keywords
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    result = requests.get(url, headers=headers)
    print(result.status_code)

    soup = BeautifulSoup(result.text, 'html.parser')
    return soup


def recent_switch_listings(search_keywords):
    soup = get_soup(search_keywords)

    # grabbing first however many 'cards' because of disabled javascript and their information
    card_info = []
    counter = 0
    cards = soup.findAll("a", {"class": "_109rpto _1anrh0x"})
    for card in cards:
        # checking if this an external ad
        if card['href'][0] is not '/':
            continue
        # print(card.prettify())
        href = 'https://offerup.com' + card['href']
        title = card.findAll("img")[0]["alt"]
        # wittling down to only accept 'switch' stuff
        if 'switch' not in title.lower():
            continue

        title, location = title.split(' for Sale in ')
        price = card.findAll("span", {"class": "_s3g03e4"})[0].text
        # if it is different then it has already been SOLD
        if card.findAll("span", {"class": "_nysliq5"}):
            shipping = card.findAll("span", {"class": "_nysliq5"})[0].text

        print(counter)
        print(title)
        print(location)
        print(price)
        print(shipping)
        print(href)

        print()
        item = {
            "title": title,
            "loc": location,
            "price": price,
            "ship": shipping,
            "link": href,
        }
        card_info.append(item)
        counter = counter + 1


if __name__ == '__main__':
    recent_switch_listings("Nintendo Switch")
    