import pandas as pd
from requests_html import HTMLSession, user_agent
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(message)s")
file_handler = logging.FileHandler("scrapper.log")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)


logger.addHandler(file_handler)

# total data to be scrapped is around 740 cities/provinces, so a dividen of 20 is enough to split the dataset into 30 sets
FIXED_DIV = 20
# the standard numbers of item on a single page is 10
ITEMS_PER_PAGE = 10


class Scrap:
    def __init__(self, df, func, to_cont, nums=25) -> None:
        # some time the webpage lock us out, we need to restart scrapping from the previous checkpoint
        self.to_cont = to_cont
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

        self.names, self.places, self.links, self.imgs = (
            [None],
            [None],
            [None],
            [None],
        )

    def init_arrs(self):
        self.names = self.names * self.total_data
        self.places = self.places * self.total_data
        self.links = self.links * self.total_data
        self.imgs = self.imgs * self.total_data

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
        self.init_arrs()

        # loop through each city/province,e.g. shanghai,beijing etc
        for i in range(self.to_cont, len(self.df)):
            # set up fake user agent
            ua = self.assign_ua()

            # establish link to the target city/province
            r = session.get(self.df.links[i], headers=ua)
            r.html.render()
            print(r.html)

            # get the city/province name
            p = self.df.city[i]
            print(p)

            # check if the next page is available
            next_page = r.html.find(".nextpage", first=True)

            next_page = next_page.absolute_links if next_page else None
            if next_page:
                next_page = list(next_page)[0]
            else:
                next_page = None

            print(next_page, self.count)
            self.page_loop(session, next_page, r, p, i)

        # to add the last csv file that does not amount up to the desinated quanity
        self.add_csv()

    def page_loop(self, session, next_page, r, p, i):
        # retrieve all information for a target city/province across all pages (limit to self.nums to prevent blocking)
        for _ in range(self.nums):
            if next_page is not None:
                # find and add all tourist attractions on the current page
                self._add_info(r, p)

                # reassign the next page value
                ua = self.assign_ua()

                r = session.get(next_page, headers=ua)
                r.html.render()
                print(r.html)

                next_page = r.html.find(".nextpage", first=True)

                next_page = next_page.absolute_links if next_page else None
                if next_page:
                    next_page = list(next_page)[0]
                else:
                    next_page = None

                print(next_page, self.count)

                # save during scrapping to prevent lost of progress if any errors occured during the scrapping

                if self.count == self.total_data:
                    self.add_csv(i)

            else:
                break

    def create_csv(self):
        temp = pd.DataFrame(
            {
                "names": self.names,
                "places": self.places,
                "links": self.links,
                "imgs": self.imgs,
            }
        )
        return temp

    # to add to csv_file
    def add_csv(self, i):
        print("counted")
        temp = self.create_csv()

        temp.to_csv(f"csv/{self.func}_data_{i}.csv", index=False)
        self.count = 0

    def add_data(self, p, name=None, link=None, img=None):
        self.names[self.count] = name
        self.links[self.count] = link
        self.imgs[self.count] = img
        self.places[self.count] = p

    # the main function that retrives information by scrapping the relevant html tags
    # and add the data to memory
    def _add_info(self, r, p):
        # the class tag amounting up to 10 items, each item contains the main information of the tourist attraction
        items = r.html.find(".list_mod2")

        # loop through all the tourist attraction on the page
        for item in items:
            # try statements to make sure scrapping goes through even if certain variables are not found
            try:
                name, link, img = self.get_standard_items(item)
                self.add_data(p, name, link, img)
            except:
                logger.exception(f"Can not get required data")
            finally:
                # updates pointer so that the algo updates in constant time
                self.count += 1

    def get_standard_items(self, item):
        # the secondary/temporary holder tag
        temp = item.find("dt", first=True)

        name = temp.find("a", first=True)
        if name:
            name = name.text

        link = temp.find("a", first=True)
        if link:
            link = list(link.absolute_links)[0]

        img = item.find(".leftimg img", first=True)
        if img:
            img = str(img.html).split('"')[1]

        return name, link, img
