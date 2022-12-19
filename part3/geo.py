#!/usr/bin/python3.10
# coding=utf-8
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import contextily as ctx
import sklearn.cluster
import numpy as np
# muzete pridat vlastni knihovny
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable


def make_geo(df: pd.DataFrame) -> geopandas.GeoDataFrame:
    """ Konvertovani dataframe do geopandas.GeoDataFrame se spravnym kodovani"""

    df2 = df.copy()

    df2 = df2[df2["d"].notna() & df2["e"].notna()]

    df2["date"] = pd.to_datetime(df2["p2a"]).astype('datetime64[ns]')

    # convert all but selected columns to category
    #to_convert = [x for x in df if x not in ["p1", "p2a", "p13a", "p13b", "p13c", "p14", "p34", "p37", "p53", "region", "d", "e"]]
    #df2[to_convert] = df2[to_convert].astype("category")

    # convert dataframe to geopandas with Krovak view
    return geopandas.GeoDataFrame(df2, geometry=geopandas.points_from_xy(df2["d"], df2["e"]), crs="EPSG:5514")


def plot_geo(gdf: geopandas.GeoDataFrame, fig_location: str = None,
             show_figure: bool = False):
    """ Vykresleni grafu s nehodami s alkoholem pro roky 2018-2021 """
    region = "JHM"
    geo = gdf[gdf["region"] == region].copy().to_crs("EPSG:3857")

    # filter region and crashes with drugs or alcohol
    geo = geo[(geo["p11"] >= 3) & (geo["date"].dt.year.isin([2018, 2019, 2020, 2021]))]

    # Subplots
    fig, ax = plt.subplots(2, 2, figsize=(10, 7))
    for i, ax_year in enumerate(fig.axes):
        year = 2018 + i
        geo[geo["date"].dt.year == year].plot(ax=ax_year, color="red", markersize=1, alpha=0.5)

        ax_year.set_axis_off()
        ax_year.set_title(f"{region} kraj ({year})")
        ctx.add_basemap(ax_year, crs=geo.crs.to_string(), source=ctx.providers.Stamen.TonerLite, attribution_size=6, alpha=0.9)

    plt.tight_layout()

    if show_figure:
        plt.show()

    if fig_location:
        fig.savefig(fig_location, bbox_inches="tight")


def plot_cluster(gdf: geopandas.GeoDataFrame, fig_location: str = None,
                 show_figure: bool = False):
    """ Vykresleni grafu s lokalitou vsech nehod v kraji shlukovanych do clusteru """
    region = "ZLK"
    geo = gdf[gdf["region"] == region].copy().to_crs("EPSG:3857")

    # select roads of 1st, 2nd and 3rd class
    geo = geo[(geo["p36"] >= 1) & (geo["p36"] <= 3)]

    # matrix with x, y coordinates
    coords = np.dstack([geo.geometry.x, geo.geometry.y]).reshape(-1, 2)

    # I picked Agglomerative Clustering and 25 clusters because the result
    # looks the most self describing
    geo["cluster"] = sklearn.cluster.AgglomerativeClustering(n_clusters=25).fit(coords).labels_
    geo = geo.dissolve(by="cluster", aggfunc={"p1": "count"})

    fig, ax = plt.subplots(1, 1, figsize=(10, 8))

    # make legend same width as map
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("bottom", size="5%", pad=0.25)

    geo.plot(ax=ax, markersize=1, column="p1", legend=True,
             legend_kwds={"orientation": "horizontal", "cax": cax})
    ax.set_axis_off()
    ax.set_title(f"Nehody v {region} kraji na silnicích 1., 2. a 3. třídy")
    ctx.add_basemap(ax, crs=geo.crs.to_string(), source=ctx.providers.Stamen.TonerLite, attribution_size=6)
    plt.tight_layout()

    if show_figure:
        plt.show()

    if fig_location:
        fig.savefig(fig_location, bbox_inches="tight")


if __name__ == "__main__":
    # zde muzete delat libovolne modifikace
    gdf = make_geo(pd.read_pickle("accidents.pkl.gz"))
    plot_geo(gdf, "geo1.png", True)
    plot_cluster(gdf, "geo2.png", True)
