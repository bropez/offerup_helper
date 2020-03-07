import requests
from bs4 import BeautifulSoup


def get_soup(search_keywords: str) -> BeautifulSoup:
    """Gets the soup with specified keywords

    Args:
        search_keywords (str): The keywords string to search for

    Returns:
        BeautifulSoup: The BeautifulSoup class that holds all of the page's html
    """

    # get the first page of offerup using 'nintendo switch' and ship nationwide
    keywords = search_keywords.replace(" ", "%20")
    url = 'http://offerup.com/search/?delivery_param=s&q=' + keywords
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    result = requests.get(url, headers=headers)

    soup = BeautifulSoup(result.text, 'html.parser')
    return soup


def recent_listings(search_keywords: str) -> list:
    """Gets all of the recent listings with specified keywords

    Args:
        search_keywords (str): The keywords to search for 

    Returns:
        list: a list of objects that hold all of the listing information
    """
    soup = get_soup(search_keywords)

    # grabbing first however many 'cards' because of disabled javascript and their information
    card_info = []
    cards = soup.findAll("a", {"class": "_109rpto _1anrh0x"})
    for card in cards:
        # checking if this an external ad
        if card['href'][0] is not '/':
            continue
        href = 'https://offerup.com' + card['href']
        title = card.findAll("img")[0]["alt"]
        # wittling down to only accept 'switch' stuff
        if 'switch' not in title.lower():
            continue
        image = card.findAll("img")[0]["data-src"]

        title, location = title.split(' for Sale in ')
        price = card.findAll("span", {"class": "_s3g03e4"})[0].text
        # if it is different then it has already been SOLD
        if card.findAll("span", {"class": "_nysliq5"}):
            shipping = card.findAll("span", {"class": "_nysliq5"})[0].text

        item = {
            "title": title,
            "loc": location,
            "price": price,
            "ship": shipping,
            "link": href,
            "img": image,
        }
        card_info.append(item)
        # print(card.prettify())

    return card_info


def price_wittler(listings: list, max_price: int) -> list:
    """Gets the objects with a price that is lower than the price you are willing to pay

    Args:
        listings (list): The list with all of the product's information
        max_price (int): The amount that you would not like to pay more than

    Returns:
        list: a list of objects that are less than the max_price
    """
    card_info = []

    for item in listings:
        if item["price"] == "SOLD":
            continue
        if int(item["price"].split('.')[0].replace('$', '')) < max_price:
            card_info.append(item)

    return card_info


if __name__ == '__main__':
    listings = recent_listings("Nintendo Switch")
    cheapo_listings = price_wittler(listings, 250)
    for item in cheapo_listings:
        print(item['title'])
        print(item['loc'])
        print(item['price'])
        print(item['ship'])
        print(item['link'])
        print(item['img'])
        print()
    