import pandas as pd
from requests_html import HTMLSession, user_agent
import logging
from scrapper_class import Scrap

FIXED_DIV = 2
ITEMS_PER_PAGE = 15


class ShoppingScrapper(Scrap):
    def __init__(self, df, func, to_cont, nums=25) -> None:
        self.rank = [None] * FIXED_DIV * ITEMS_PER_PAGE * self.nums

    def add_csv(self):
        if self.count == FIXED_DIV * self.nums * ITEMS_PER_PAGE:
            print("")
            temp = pd.DataFrame(
                {
                    "names": self.names,
                    "places": self.places,
                    "popularity": self.popularities,
                    "scores": self.scores,
                    "links": self.links,
                    "imgs": self.imgs,
                }
            )
            temp.to_csv(f"../csv/sight_data_{self.index}.csv", index=False)
            self.count = 0
            self.index += 1


df = pd.read_csv(r"csv\cities_n_links.csv")
a = ShoppingScrapper(df, "shoppinglist", 0, 1)
print(a.total_data)
