import pandas as pd
from requests_html import HTMLSession


class Scrap:
    def __init__(self, df, func) -> None:
        # select the functionality
        self.func = func
        # transform the dataframe (change the http links to retrieve functional information)
        self.df = self.transform(df.copy())
        # initialize arrays to store scrapped data (for each city/province)
        self.data = [None] * len(self.df)

    # This function helps to change the html page to prefered site e.g sight/restaurant/shopping
    def transform(self, df):
        df["links"] = df["links"].replace({"/place/": f"/{self.func}/"}, regex=True)
        return df

    # The looping function that retrives all info given a target city/province across all pages
    def scrap_info(self):
        # start session
        session = HTMLSession()

        # loop through each city/province,e.g. shanghai,beijing etc
        for i in range(len(self.df)):
            # establish link to the target city/province
            r = session.get(self.df.links[i])

            # initialize temporary array to store values from each city/province
            names, hot_scores, ratings, links, imgs = [], [], [], [], []

            # check if the next page is available
            next_page = list(r.html.find(".nextpage", first=True).absolute_links)[0]

            # retrieve all information for a target city/province across all pages
            while next_page:
                # find and add all tourist attractions on the current page
                self._add_info(r, names, hot_scores, ratings, links, imgs)

                # reassign the next page value
                r = session.get(next_page)
                next_page = list(r.html.find(".nextpage", first=True).absolute_links)[0]
                print(next_page)
                break

            # add the temp arrays to the overall data array
            self.data[i] = [names, hot_scores, ratings, links, imgs]

            if i == 2:
                break

    # the main function that retrives information by scrapping the relevant html tags
    # and add the data to memory
    def _add_info(self, r, names, hot_scores, ratings, links, imgs):
        # the class tag amounting up to 10 items, each item contains the main information of the tourist attraction
        items = r.html.find(".list_mod2")

        # loop through all the tourist attraction on the page
        for item in items:
            # the secondary/temporary holder tag
            temp = item.find("dt", first=True)

            hot_score = temp.find(".hot_score_number", first=True)

            name = temp.find("a", first=True)

            link = temp.find("a", first=True).absolute_links

            img = item.find(".leftimg img", first=True)

            rating = item.find(".score", first=True)
            rating = rating.find("strong", first=True)
            if rating:
                rating = rating.text

            img = str(img.html).split('"')[1]
            print(name.text, hot_score.text, rating, list(link)[0], img)

            # if else statements to make sure scrapping goes through even if certain variables are not found
            names.append(name.text)
            hot_scores.append(hot_score.text)
            ratings.append(rating)
            links.append(list(link)[0])
            imgs.append(img)
