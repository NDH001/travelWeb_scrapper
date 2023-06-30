import pandas as pd
import glob
import os


def find_relevant_csv(name, idx):
    joined_files = os.path.join("csv", f"{name}.csv")
    joined_list = glob.glob(joined_files)
    joined_list.sort(key=lambda item: int(item.split("_")[idx]))
    return joined_list


def join_drop_dup(name, joined_list):
    df = pd.concat(map(pd.read_csv, joined_list), ignore_index=True)
    print(f"------{name}-------")
    print(f"Before dropping duplicate : {len(df)}")
    df = df.drop_duplicates()
    print(f"After dropping duplicate: {len(df)}")
    return df


def remove_ref_files():
    shop_df = find_relevant_csv("fooditem_data*", 2)
    print(shop_df)
    for file in shop_df:
        os.remove(file)


def check_unique(name):
    ls = pd.read_csv(f"csv/{name}.csv")
    return ls.places.unique()


def all_unique():
    au = pd.read_csv(f"csv/cities_n_links.csv")
    return au.city.unique()


def check_not_seen(name):
    all_ls = all_unique()
    shop_ls = check_unique(name)
    not_seen = []
    for city in all_ls:
        if city not in shop_ls:
            not_seen.append(city)

    return not_seen


def amend(name, not_seen):
    links = pd.read_csv("csv/cities_n_links.csv", index_col="city")
    df = links.loc[not_seen]
    df.to_csv(f"csv/{name}_amended.csv")


def add_amend(name, file):
    not_seen = check_not_seen(file)
    print(not_seen)
    amend(name, not_seen)


def verify_len(file, amfile):
    s_a = pd.read_csv(f"csv/{file}.csv")
    s_am = pd.read_csv(f"csv/{amfile}.csv")
    print(len(s_a.places.unique()) + len(s_am.city.unique()) == len(all_unique()))


if __name__ == "__main__":
    temp = find_relevant_csv("sight_data*", 2)
    print(temp)
