from scrapper_class import Scrap
import pandas as pd


class RestScrapper(Scrap):
    def __init__(self, df, func, to_cont, nums=25) -> None:
        super().__init__(df, func, to_cont, nums)
        self.scores = [None] * self.total_data
        self.prices = [None] * self.total_data
        self.address = [None] * self.total_data

        self.data_df["scores"] = self.scores
        self.data_df["address"] = self.address

    def get_addr(self, item):
        pass

    def get_score(self, item):
        pass

    def get_price(self, item):
        pass

    def get_standard_items(self, item):
        super().get_standard_items(item)

        addr = self.get_addr(item)
        score = self.get_score(item)
        price = self.get_price(item)

        self.scores[self.count] = score
        self.address[self.count] = addr
        self.prices[self.count] = price


if __name__ == "__main__":
    df = pd.read_csv(r"csv\cities_n_links.csv")
    a = RestScrapper(df, "shoppinglist", 0, 3)
    a.scrap_info()
