from scrapper_class import Scrap
import pandas as pd


class SightScrapper(Scrap):
    def __init__(self, df, func, to_cont, nums=1, render=False) -> None:
        super().__init__(df, func, to_cont, nums, render)
        self.total_data = 20
        self.popularity = [None] * self.total_data
        self.scores = [None] * self.total_data
        self.addresses = [None] * self.total_data
        self.index = 25

        self.data_df["popularity"] = self.popularity
        self.data_df["scores"] = self.scores
        self.data_df["addresses"] = self.addresses

    def get_pop(self, item):
        pop = item.find("a .hot_score_number", first=True)
        return pop.text if pop else None

    def get_score(self, item):
        score = item.find(".score strong", first=True)
        return score.text if score else None

    def get_address(self, item):
        addr = item.find("dl .ellipsis", first=True)
        return addr.text if addr else None

    def get_standard_items(self, item):
        super().get_standard_items(item)

        popularity = self.get_pop(item)
        score = self.get_score(item)
        address = self.get_address(item)

        self.popularity[self.count] = popularity
        self.scores[self.count] = score
        self.addresses[self.count] = address


if __name__ == "__main__":
    df = pd.read_csv(r"/home/jun/travelWeb/csv/cities_n_links.csv")
    ss = SightScrapper(df, "sight", 503, 5)
    ss.scrap_info()
