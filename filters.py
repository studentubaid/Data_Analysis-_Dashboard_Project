import pandas as pd

player = pd.read_csv("C:/Users/Dell/Documents/dashboard_project/data/historical_RAPTOR_by_player.csv")

def apply_filters(season="All", player_name="All", metric="raptor_total", min_minutes=0, max_minutes=None):
    df = player.copy()

    # Season filter
    if season != "All":
        df = df[df["season"] == season]

    # Player filter
    if player_name != "All":
        df = df[df["player_name"] == player_name]

    # Minutes filter (safe handling)
    if max_minutes is None:
        max_minutes = df["mp"].max()  # fallback to max available
    df = df[(df["mp"] >= min_minutes) & (df["mp"] <= max_minutes)]

    return df, metric

