import pandas as pd
import glob
import os


def join_files(name):
    joined_files = os.path.join("csv", f"*{name}.csv")
    joined_list = glob.glob(joined_files)
    joined_list.sort(key=lambda item: int(item.split("_")[2]))
    return joined_list


def remove_dup_n_combine(name):
    joined_list = join_files(name)
    df = pd.concat(map(pd.read_csv, joined_list), ignore_index=True)
    print(len(df.places.unique()))
    print(f"------{name}-------")
    print(f"Before dropping duplicate : {len(df)}")
    df = df.drop_duplicates()
    print(f"After dropping duplicate: {len(df)}")
    return df


def main():
    shop_df = remove_dup_n_combine("amended")
    shop_df.to_csv('total_amended_505_661.csv',index=False)


if __name__ == "__main__":
    main()
