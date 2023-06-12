from scrapper_class import Scrap
import pandas as pd

FIXED_DIV = 20
ITEMS_PER_PAGE = 15


class RestScrapper(Scrap):
    def __init__(self, df, func, to_cont, nums=25) -> None:
        super().__init__(df, func, to_cont, nums)
        self.total_data = self.nums * FIXED_DIV * ITEMS_PER_PAGE
        self.scores = [None] * self.total_data
        self.prices = [None] * self.total_data
        self.addresses[None] * self.total_data

    def create_csv(self):
        temp = pd.DataFrame(
            {
                "names": self.names,
                "places": self.places,
                "prices": self.prices,
                "scores": self.scores,
                "address": self.addresses,
                "links": self.links,
                "imgs": self.imgs,
            }
        )
        return temp

    def get_standard_items(self, item):
        pass
