import pandas as pd
from requests_html import HTMLSession, user_agent
from scrapper_class import Scrap

FIXED_DIV = 20
ITEMS_PER_PAGE = 15


class ShoppingScrapper(Scrap):
    def __init__(self, df, func, to_cont, nums=25) -> None:
        super().__init__(df, func, to_cont, nums)
        self.total_data = FIXED_DIV * self.nums * ITEMS_PER_PAGE
        self.ranks = [None] * self.total_data
        self.scores = [None] * self.total_data
        self.address = [None] * self.total_data
        self.rank_count = 1

    def create_csv(self):
        temp = pd.DataFrame(
            {
                "names": self.names,
                "places": self.places,
                "ranks": self.ranks,
                "scores": self.scores,
                "address": self.address,
                "links": self.links,
                "imgs": self.imgs,
            }
        )
        return temp

    def page_loop(self, session, next_page, r, p, i):
        super().page_loop(session, next_page, r, p, i)
        # reset the rank count to 1 for after every city/province is visited
        self.rank_count = 1

    def get_standard_items(self, item):
        # the secondary/temporary holder tag
        temp = item.find("dt", first=True)

        name = temp.find("a", first=True)
        if name:
            name = name.text

        link = temp.find("a", first=True)
        if link:
            link = list(link.absolute_links)[0]

        img = item.find("a img", first=True)
        if img:
            img = str(img.html).split('"')[1]

        score = item.find(".score", first=True)
        score = score.find("strong", first=True)
        if score:
            score = score.text

        addr = item.find("dl .ellipsis", first=True)
        if addr:
            addr = addr.text

        self.scores[self.count] = score
        self.address[self.count] = addr
        self.ranks[self.count] = self.rank_count
        self.rank_count += 1

        return name, link, img


if __name__ == "__main__":
    df = pd.read_csv(r"csv\cities_n_links.csv")
    a = ShoppingScrapper(df, "shoppinglist", 0, 3)
    a.scrap_info()
