from scrapper.helper_class import FuncOption
import pandas as pd

a = pd.read_csv("scrapper\cities_n_links.csv")

temp = FuncOption()

x = temp.transform(a, "eat")
print(x.head())
