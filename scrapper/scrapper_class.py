import pandas as pd
from requests_html import HTMLSession, user_agent
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(message)s")

file_handler = logging.FileHandler("../logging/scrapper.log")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)


logger.addHandler(file_handler)

# total data to be scrapped is around 740 cities/provinces, so a dividen of 20 is enough to split the dataset into 30 sets
FIXED_DIV = 20
# the standard numbers of item on a single page is 10
ITEMS_PER_PAGE = 10


class Scrap:
    def __init__(self, df, func, nums=25) -> None:
        self.nums = nums
        # a count variable inplace to keep track of the last item added
        self.count = 0
        # select the functionality
        self.func = func
        # transform the dataframe (change the http links to retrieve functional information)
        self.df = self.transform(df.copy())
        # initialize arrays to store scrapped data (20 * the targeted page number * number of items per page
        # we store the data in a new csv everytime the limit is reached and reset the arrays
        self.total_data = FIXED_DIV * self.nums * ITEMS_PER_PAGE

        (
            self.names,
            self.popularities,
            self.scores,
            self.links,
            self.imgs,
        ) = self.set_empty_arrays()

    def set_empty_arrays(self):
        return (
            self.total_data * [None],
            self.total_data * [None],
            self.total_data * [None],
            self.total_data * [None],
            self.total_data * [None],
        )

    # This function helps to change the html page to prefered site e.g sight/restaurant/shopping
    def transform(self, df):
        df["links"] = df["links"].replace({"/place/": f"/{self.func}/"}, regex=True)
        return df

    def assign_ua(self):
        ua = user_agent("chrome")

        return {"User-Agent": ua}

    # The looping function that retrives all info given a target city/province across all pages
    def scrap_info(self):
        # start session
        session = HTMLSession()

        # loop through each city/province,e.g. shanghai,beijing etc
        for i in range(len(self.df)):
            # set up fake user agent
            ua = self.assign_ua()

            # establish link to the target city/province

            r = session.get(self.df.links[i], headers=ua)

            logger.exception("Unable to get session,potential lock out")

            # check if the next page is available
            next_page = list(r.html.find(".nextpage", first=True).absolute_links)[0]

            # retrieve all information for a target city/province across all pages (limit to self.nums to prevent blocking)
            for _ in range(self.nums):
                if next_page:
                    # find and add all tourist attractions on the current page
                    self._add_info(r)

                    # reassign the next page value
                    ua = self.assign_ua()

                    r = session.get(next_page, headers=ua)

                    next_page = list(
                        r.html.find(".nextpage", first=True).absolute_links
                    )[0]
                    print(next_page, self.count)
                else:
                    break

            # save during scrapping to prevent lost of progress if any errors occured during the scrapping
            try:
                if self.count == FIXED_DIV * self.nums * ITEMS_PER_PAGE:
                    temp = pd.DataFrame(
                        {
                            "names": self.names,
                            "popularity": self.popularities,
                            "scores": self.scores,
                            "links": self.links,
                            "imgs": self.imgs,
                        }
                    )
                    temp.to_csv(f"../csv/sight_data_{i}.csv", index=False)
                    self.count = 0
            except:
                logger.exception(f"Cannot Save to csv file current i == {i}")

    # the main function that retrives information by scrapping the relevant html tags
    # and add the data to memory
    def _add_info(self, r):
        # the class tag amounting up to 10 items, each item contains the main information of the tourist attraction
        items = r.html.find(".list_mod2")

        # loop through all the tourist attraction on the page
        for item in items:
            try:
                # the secondary/temporary holder tag
                temp = item.find("dt", first=True)

                hot_score = temp.find(".hot_score_number", first=True)
                if hot_score:
                    hot_score = hot_score.text

                name = temp.find("a", first=True)
                if name:
                    name = name.text

                link = temp.find("a", first=True)
                if link:
                    link = list(link.absolute_links)[0]

                img = item.find(".leftimg img", first=True)
                if img:
                    img = str(img.html).split('"')[1]

                rating = item.find(".score", first=True)
                rating = rating.find("strong", first=True)
                if rating:
                    rating = rating.text

                # print(name.text, hot_score.text, rating, list(link)[0], img)

                # if else statements to make sure scrapping goes through even if certain variables are not found
                self.names[self.count] = name if name else None
                self.popularities[self.count] = hot_score if hot_score else None
                self.scores[self.count] = rating if rating else None
                self.links[self.count] = link if link else None
                self.imgs[self.count] = img if img else None
            except:
                logger.exception(
                    f"Can not get required data, self.names = {self.names},self.popu = {self.popularities},self.scores={self.scores},self.links={self.scores},self.imgs={self.imgs}"
                )
            finally:
                # updates pointer so that the algo updates in constant time
                self.count += 1
