#!/usr/bin/env python3
"""
IZV cast1 projektu
Autor: 

Detailni zadani projektu je v samostatnem projektu e-learningu.
Nezapomente na to, ze python soubory maji dane formatovani.

Muzete pouzit libovolnou vestavenou knihovnu a knihovny predstavene na prednasce
"""


from bs4 import BeautifulSoup
import requests
import numpy as np
import matplotlib.pyplot as plt
from typing import List


def integrate(x: np.array, y: np.array) -> float:
    return np.sum(np.multiply(np.subtract(x[1:], x[:-1]), np.divide(np.add(y[:-1], y[1:]), 2)))


def generate_graph(a: List[float], show_figure: bool = False, save_path: str | None=None):
    x = np.linspace(-3, 3, 10000)
    fx = np.multiply(np.power(x, 2), np.array(a).reshape(-1, 1))

    fig, ax = plt.subplots()
    ax.plot(x, fx[0], label=r'$\gamma_{1.0}(x)$')
    ax.plot(x, fx[1], label=r'$\gamma_{2.0}(x)$')
    ax.plot(x, fx[2], label=r'$\gamma_{-2.0}(x)$')
    ax.fill_between(x, fx[0], 0, alpha=0.1)
    ax.fill_between(x, fx[1], 0, alpha=0.1)
    ax.fill_between(x, fx[2], 0, alpha=0.1)
    ax.set_xlabel('x')
    ax.set_ylabel(r'$f_a(x)$')
    ax.annotate(r'$\int f_{1.0}(x)dx$', xy=(3, 8.5), xycoords="data")
    ax.annotate(r'$\int f_{2.0}(x)dx$', xy=(3, 17.5), xycoords="data")
    ax.annotate(r'$\int f_{-2.0}(x)dx$', xy=(3, -18.5), xycoords="data")
    ax.legend(loc='lower center', bbox_to_anchor=(0.6, 1.0), ncol=3)
    ax.set_xlim([-3, max(x)])
    ax.set_ylim([-20, 20])
    ax.spines["top"].set_bounds(-3, 4)
    ax.spines["bottom"].set_bounds(-3, 4)
    ax.spines["right"].set_position(("data", 4))

    if show_figure:
        plt.show()
    else:
        fig.savefig(save_path, bbox_inches="tight", pad_inches=0.5)


def generate_sinus(show_figure: bool=False, save_path: str | None=None):
    t = np.linspace(0, 100, 10000)
    f1 = np.multiply(0.5, np.sin(np.multiply(np.pi / 50, t)))
    f2 = np.multiply(0.25, np.sin(np.multiply(np.pi, t)))
    f3 = np.add(f1, f2)

    ylabels = [r'$f_1(x)$', r'$f_2(x)$', r'$f_1(x) + f_2(x)$']

    fig, axes = plt.subplots(ncols=1, nrows=3, constrained_layout=True)
    for i, ax in enumerate(axes):
        ax.set_xlim([0, max(t)])
        ax.set_xlabel('t')
        ax.set_ylim([-0.8, 0.8])
        ax.set_yticks([-0.8, -0.4, 0.0, 0.4, 0.8])
        ax.set_ylabel(ylabels[i])
    
    ax1, ax2, ax3 = axes
    ax1.plot(t, f1)
    ax2.plot(t, f2)
    green = f3.copy()
    green[green < f1] = np.nan
    f3[f3 >= f1] = np.nan
    ax3.plot(t, green, color="green")
    ax3.plot(t, f3, color="red")

    if show_figure:
        plt.show()
    else:
        fig.savefig(save_path)


def download_data(url="https://ehw.fit.vutbr.cz/izv/temp.html"):
    with requests.get(url) as f:
        # raise exception when HTTP code is not OK (200)
        f.raise_for_status()
        soup = BeautifulSoup(f.text, "html.parser")
    
    lines = soup.find_all("tr")
    data = []
    for line in lines:
        year, month, *rest = line.find_all("p")
        temp = [float(val.contents[0].replace(',', '.')) for val in rest]
        entry = {}
        entry['year'] = int(year.contents[0])
        entry['month'] = int(month.contents[0])
        entry['temp'] = np.asarray(temp)
        data.append(entry)

    return data


def get_avg_temp(data, year=None, month=None) -> float:
    if year and month:
        filtered = filter(lambda x: x['year'] == year and x['month'] == month, data)
    elif year is None and month:
        filtered = filter(lambda x: x['month'] == month, data)
    elif year and month is None:
        filtered = filter(lambda x: x['year'] == year, data)
    else:
        filtered = data

    sum = 0
    days = 0
    for f in filtered:
        sum += np.sum(f['temp'])
        days += f['temp'].size

    return sum / days


if __name__ == "__main__":
    data = download_data()

    m = get_avg_temp(data)
    print(m)