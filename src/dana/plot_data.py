import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import os

from utils import check_type

import scipy.spatial as sp 
import scipy.cluster.hierarchy as hc


def plot_age_data(
    dataset: pd.DataFrame, 
    outdir: str, 
    debug: bool, 
    erbose: bool
) -> None:
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(20,18))
    labels = [
        "<= 25 years", "26 - 45 years", "46 - 65 years", "66 - 85 years", "> 85 years"
    ]
    # age distribution
    counts_dict = dataset["Age.at.diagnosis"].value_counts().to_dict()
    counts = [counts_dict[age] for age in labels]
    colors = ["#138B29", "#EE9C0D", "#C51307", "#23429B", "#B64220"]
    assert len(labels) == len(counts)
    ax1.bar(labels, counts, color=colors, width=.4)
    ax1.set_xlabel("Age group", size=18)
    ax1.set_ylabel("Total number", size=18)
    ax1.set_ylim(0, max(counts) + 100)
    ax1.set_xticklabels(labels, {"fontsize":14, "rotation":70})
    ax1.set_title("Age distribution", fontsize=20, fontweight="bold")
    
    # age by sex distribution
    colors = ["#0D58B7", "#DC661A"]
    series_labels = ["Male", "Female"]
    barplot_data = {}
    for age in labels:
        males_num = dataset[ (dataset["Age.at.diagnosis"] == age) & (dataset["Sex"] == "Male") ].shape[0]
        females_num = dataset[ (dataset["Age.at.diagnosis"] == age) & (dataset["Sex"] == "Female") ].shape[0]
        barplot_data[age] = [males_num, females_num]
    counts_males = [barplot_data[age][0] for age in labels]
    counts_females = [barplot_data[age][1] for age in labels]
    x = np.arange(len(labels))
    width = .2
    ax2.set_ylim(0, max([max(counts_males), max(counts_females)]) + 100)
    ax2.bar(x - width/2, counts_males, width, label="Males", color=colors[0])
    ax2.bar(x + width/2, counts_females, width, label="Females", color=colors[1])
    ax2.tick_params(axis="x", labelsize=14)
    ax2.tick_params(axis="y", labelsize=14)
    ax2.set_ylabel("Total number", size=18)
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, {"fontsize":14, "rotation":70})
    ax2.legend(series_labels, prop={"size":18})
    ax2.set_xlabel("Age group", size=18)
    ax2.set_title("Age distribution by sex", fontsize=20, fontweight="bold")
    plt.suptitle("Descriptive Analysis", fontsize=26, fontweight="bold")
    outfile = os.path.join(outdir, "age_data.png")
    plt.savefig(outfile, format="png")


def plot_recovery_data(
    dataset: pd.DataFrame, 
    outdir: str, 
    debug: bool, 
    erbose: bool
) -> None:
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(20,18))
    colors = ["#31B417", "#989B98"]
    series_labels = ["Recovered", "Dead from COVID-19"]
    # stacked bar chart by age category
    labels = [
        "<= 25 years", "26 - 45 years", "46 - 65 years", "66 - 85 years", "> 85 years"
    ]
    stack_data_rec = {}
    for age in labels:
        stack_data_rec[age] = dataset[
            (dataset["Last.known.patient.status"] == "Recovered") & (dataset["Age.at.diagnosis"] == age)
        ].shape[0]
    stack_data_dead = {}
    for age in labels:
        stack_data_dead[age] = dataset[
            (dataset["Last.known.patient.status"] == "Dead from COVID-19") & (dataset["Age.at.diagnosis"] == age)
        ].shape[0]
    stack_data = np.array([list(stack_data_rec.values()), list(stack_data_dead.values())])
    stack_data_pct = np.array([
        [(count / stack_data.sum(0)[i]) * 100 for i,count in enumerate(stack_data[0,:])],
        [(count / stack_data.sum(0)[i]) * 100 for i,count in enumerate(stack_data[1,:])]
    ])
    ax1.set_ylim(0, 110)
    ny = len(stack_data[0])
    ind = np.arange(ny)
    axes = []
    cumul_size = np.zeros(ny)
    for i, counts in enumerate(stack_data_pct):
        color = colors[i]
        axes.append(
            ax1.bar(ind, counts, bottom=cumul_size, label=series_labels[i], color=color)
        )
        cumul_size += counts
    ax1.set_xticks(ind)
    ax1.set_xticklabels(labels, {"fontsize":14, "rotation":70})
    ax1.set_yticks([20 * i for i in range(6)])
    ax1.set_yticklabels([f"{20 * i}%" for i in range(6)], {"fontsize":14})
    ax1.set_ylabel("Patients number", size=18)
    ax1.legend(series_labels, prop={"size":18})

    # stacked bar chart by sex
    labels = ["Male", "Female"]
    stack_data_rec = {}
    for sex in labels:
        stack_data_rec[sex] = dataset[
            (dataset["Last.known.patient.status"] == "Recovered") & (dataset["Sex"] == sex)
        ].shape[0]
    stack_data_dead = {}
    for sex in labels:
        stack_data_dead[sex] = dataset[
            (dataset["Last.known.patient.status"] == "Dead from COVID-19") & (dataset["Sex"] == sex)
        ].shape[0]
    stack_data = np.array([list(stack_data_rec.values()), list(stack_data_dead.values())])
    stack_data_pct = np.array([
        [(count / stack_data.sum(0)[i]) * 100 for i,count in enumerate(stack_data[0,:])],
        [(count / stack_data.sum(0)[i]) * 100 for i,count in enumerate(stack_data[1,:])]
    ])
    ax2.set_ylim(0, 110)
    ny = len(stack_data[0])
    ind = np.arange(ny)
    axes = []
    cumul_size = np.zeros(ny)
    for i, counts in enumerate(stack_data_pct):
        color = colors[i]
        axes.append(
            ax2.bar(ind, counts, bottom=cumul_size, label=series_labels[i], color=color)
        )
        cumul_size += counts
    ax2.set_xticks(ind)
    ax2.set_xticklabels(labels, {"fontsize":14, "rotation":70})
    ax2.set_yticks([20 * i for i in range(6)])
    ax2.set_yticklabels([f"{20 * i}%" for i in range(6)], {"fontsize":14})
    ax2.set_ylabel("Patients number", size=18)
    ax2.legend(series_labels, prop={"size":18})
    outfile = os.path.join(outdir, "recovery_data.png")
    plt.savefig(outfile, format="png")


def plot_clusters(
    dist_mat: np.ndarray, 
    outdir: str,
    debug: bool, 
    verbose: bool
) -> None:
    check_type(np.ndarray, dist_mat)
    check_type(str, outdir)
    outfile = os.path.join(outdir, "distance_matrix.png")
    linkage = hc.linkage(sp.distance.squareform(dist_mat), method="average")
    fig = plt.figure(figsize=(15,15))
    sns.clustermap(dist_mat, row_linkage=linkage, col_linkage=linkage)
    plt.savefig(outfile, format="png")





    

