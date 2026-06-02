import matplotlib.pyplot as plt
import seaborn as sns

# Pie chart function
def pi_chart(x):
    top5 = x.groupby("player_name")["poss"].sum().sort_values(ascending=False).head(5)
    fig, ax = plt.subplots()
    top5.plot.pie(autopct='%1.1f%%', ax=ax)
    ax.set_title("Top 5 Players by Possessions")
    return fig

# Histogram chart function
def histo_chart(x):
    fig, ax = plt.subplots()
    sns.histplot(x, bins=30, kde=True, ax=ax)
    ax.set_xlabel("Raptor Values")
    ax.set_ylabel("Frequency")
    ax.set_title("Distribution of Raptor Values")
    return fig

# Line chart function
def line_chart(x, y):
    fig, ax = plt.subplots()
    sns.lineplot(x=x, y=y, ax=ax)
    ax.set_xlabel("Season")
    ax.set_ylabel("WAR Total")
    ax.set_title("WAR Total Over Time")
    return fig

# Bar chart function
def bar_chart(x):
    top10 = x.groupby("player_name")["war_total"].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    sns.barplot(x=top10.index, y=top10.values, ax=ax)
    ax.set_xlabel("Player Name")
    ax.set_ylabel("WAR Total")
    ax.set_title("Top 10 Players by WAR Total")
    ax.tick_params(axis='x', rotation=45)
    return fig

# Scatter chart function
def scatter_chart(x, y):
    fig, ax = plt.subplots()
    sns.scatterplot(x=x, y=y, ax=ax)
    ax.set_xlabel("Raptor Offense")
    ax.set_ylabel("Raptor Defense")
    ax.set_title("Offense vs Defense")
    return fig

# Box chart function
def box_chart(x):
    fig, ax = plt.subplots()
    sns.boxplot(y=x, ax=ax)
    ax.set_ylabel("Minutes Played")
    ax.set_title("Players Data by Minutes Played")
    return fig

# Heatmap chart function

def heatmap_chart(df):
    # Select only numeric columns
    numeric_df = df.select_dtypes(include=["number"])
    
    # If no numeric data, return empty figure
    if numeric_df.empty:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "No numeric data available", 
                ha="center", va="center", fontsize=12)
        return fig
    
    # Compute correlation matrix
    corr = numeric_df.corr()

    # Plot heatmap
    fig, ax = plt.subplots(figsize=(8,6))
    sns.heatmap(corr, annot=True, cmap="Purples", ax=ax)
    ax.set_title("Correlation Heatmap of Metrics")
    return fig


# Area chart function
def area_chart(x):
    cumulative = x.groupby("season")["war_total"].sum().cumsum()
    fig, ax = plt.subplots()
    ax.fill_between(cumulative.index, cumulative.values, alpha=0.5)
    sns.lineplot(x=cumulative.index, y=cumulative.values, ax=ax)
    ax.set_xlabel("Season")
    ax.set_ylabel("Cumulative WAR Total")
    ax.set_title("Cumulative WAR Total Over Seasons")
    return fig

# Count chart function
def count_chart(df):

    fig, ax = plt.subplots(figsize=(10, 7.3))  # wider figure for spacing
    sns.countplot(x="season", data=df, ax=ax, color="#1d0dad")

    # Rotate x-axis labels for readability
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")

    # Add title and layout
    ax.set_ylabel("Number of Players")
    ax.set_title("Number of Players per Season")
    plt.tight_layout()

    return fig


# Violin chart function
def violin_chart(x):
    fig, ax = plt.subplots()
    sns.violinplot(y=x["war_total"].dropna(), ax=ax)
    ax.set_ylabel("WAR Total")
    ax.set_title("Distribution of WAR Total")
    return fig
