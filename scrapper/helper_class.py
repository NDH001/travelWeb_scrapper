import pandas as pd


class FuncOption:
    # This function helps to change the html page to sight-seeing page
    def sight_see(df):
        sight_df = df.copy()
        sight_df = df.replace("place", "sight")
        return sight_df

    # This function helps to change the html page to shopping page
    def shopping(df):
        shopping_df = df.copy()
        shopping_df = shopping_df.replace("place", "shopping")
        return shopping_df

    # This function helps to change the html page to restaurant page
    def eat(df):
        eat_df = df.copy()
        eat_df = eat_df.replace("place", "eat")
        return eat_df

    # This function helps to change the html page to blog page
    def blog(df):
        blog_df = df.copy()
        blog_df = blog_df.replace("place", "blog")
        return blog_df
