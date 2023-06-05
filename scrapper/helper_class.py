import pandas as pd


class FuncOption:
    # This function helps to change the html page to sight-seeing page
    def transform(self, df, replace):
        df = df.copy()
        df["links"] = df["links"].replace({"/place/": f"/{replace}/"}, regex=True)
        return df
