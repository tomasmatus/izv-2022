#!/usr/bin/env python3.9
# coding=utf-8

from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import zipfile

# muzete pridat libovolnou zakladni knihovnu ci knihovnu predstavenou na prednaskach
# dalsi knihovny pak na dotaz

# Ukol 1: nacteni dat ze ZIP souboru
def load_data(filename : str) -> pd.DataFrame:
    # tyto konstanty nemente, pomuzou vam pri nacitani
    headers = ["p1", "p36", "p37", "p2a", "weekday(p2a)", "p2b", "p6", "p7", "p8", "p9", "p10", "p11", "p12", "p13a",
                "p13b", "p13c", "p14", "p15", "p16", "p17", "p18", "p19", "p20", "p21", "p22", "p23", "p24", "p27", "p28",
                "p34", "p35", "p39", "p44", "p45a", "p47", "p48a", "p49", "p50a", "p50b", "p51", "p52", "p53", "p55a",
                "p57", "p58", "a", "b", "d", "e", "f", "g", "h", "i", "j", "k", "l", "n", "o", "p", "q", "r", "s", "t", "p5a"]

    #def get_dataframe(filename: str, verbose: bool = False) -> pd.DataFrame:
    regions = {
        "PHA": "00",
        "STC": "01",
        "JHC": "02",
        "PLK": "03",
        "ULK": "04",
        "HKK": "05",
        "JHM": "06",
        "MSK": "07",
        "OLK": "14",
        "ZLK": "15",
        "VYS": "16",
        "PAK": "17",
        "LBK": "18",
        "KVK": "19",
    }

    frame_list = []
    with zipfile.ZipFile(filename, 'r') as root_zip:
        for zip_file in root_zip.filelist:
            with zipfile.ZipFile(root_zip.open(zip_file)) as zip:
                for reg_name, reg_code in regions.items():
                    df = pd.read_csv(zip.open(f'{reg_code}.csv'), encoding="cp1250", sep=";", quotechar='"', low_memory=False, names=headers)
                    df["region"] = reg_name
                    frame_list.append(df)

    return pd.concat(frame_list, axis=0)
                    

def parse_data(df : pd.DataFrame, verbose : bool = False) -> pd.DataFrame:
    df2 = df.copy()
    
    # region, rok vyroby, vyser skody, gps X, gps Y
    to_convert = [x for x in df2 if x not in ["p1", "p13a", "p13b", "p13c", "p14", "p34", "p37", "p53", "region", "d", "e"]]
    df2[to_convert] = df2[to_convert].astype("category")
    print(df2["d"].dtype)
    print(df2["e"].dtype)
    
    print(f'orig_size={df.memory_usage(deep=True).sum() / 1_000_000} MB')
    print(f'new_size={df2.memory_usage(deep=True).sum() / 1_000_000} MB')


# Ukol 3: počty nehod v jednotlivých regionech podle viditelnosti
def plot_visibility(df: pd.DataFrame, fig_location: str = None,
                    show_figure: bool = False):
    pass

# Ukol4: druh srážky jedoucích vozidel
def plot_direction(df: pd.DataFrame, fig_location: str = None,
                   show_figure: bool = False):
    pass

# Ukol 5: Následky v čase
def plot_consequences(df: pd.DataFrame, fig_location: str = None,
                    show_figure: bool = False):
    pass

if __name__ == "__main__":
    # zde je ukazka pouziti, tuto cast muzete modifikovat podle libosti
    # skript nebude pri testovani pousten primo, ale budou volany konkreni 
    # funkce.
    df = load_data("data/data.zip")
    df2 = parse_data(df, True)
    
    plot_visibility(df2, "01_visibility.png")
    plot_direction(df2, "02_direction.png", True)
    plot_consequences(df2, "03_consequences.png")


# Poznamka:
# pro to, abyste se vyhnuli castemu nacitani muzete vyuzit napr
# VS Code a oznaceni jako bunky (radek #%%% )
# Pak muzete data jednou nacist a dale ladit jednotlive funkce
# Pripadne si muzete vysledny dataframe ulozit nekam na disk (pro ladici
# ucely) a nacitat jej naparsovany z disku
