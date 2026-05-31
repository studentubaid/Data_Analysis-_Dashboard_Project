import gradio as gr
import charts
import filters

def show_chart(chart_type, season, player_name, metric, min_minutes, max_minutes):
    df, metric = filters.apply_filters(season=season,
                                       player_name=player_name,
                                       metric=metric,
                                       min_minutes=min_minutes,
                                       max_minutes=max_minutes)

    # Quick stats: top 3 players by WAR
    top_players = df.groupby("player_name")["war_total"].sum().sort_values(ascending=False).head(3)
    stats_text = "Top Players by WAR:\n" + "\n".join([f"{p}: {v:.2f}" for p, v in top_players.items()])

    fig, insight = None, ""
    if chart_type == "Pie Chart":
        fig = charts.pi_chart(df)
        insight = "Pie chart shows top players by possessions."
    elif chart_type == "Histogram":
        fig = charts.histo_chart(df[metric])
        insight = f"Histogram shows distribution of {metric}."
    elif chart_type == "Line Chart":
        fig = charts.line_chart(df["season"], df[metric])
        insight = f"Line chart shows {metric} trend across seasons."
    elif chart_type == "Bar Chart":
        fig = charts.bar_chart(df)
        insight = "Bar chart shows top players by WAR total."
    elif chart_type == "Scatter Chart":
        fig = charts.scatter_chart(df["raptor_offense"], df["raptor_defense"])
        insight = "Scatter plot compares offense vs defense."
    elif chart_type == "Box Chart":
        fig = charts.box_chart(df["mp"])
        insight = "Box chart shows distribution of minutes played."
    elif chart_type == "Heatmap":
        fig = charts.heatmap_chart(df)
        insight = "Heatmap shows correlations between metrics."
    elif chart_type == "Area Chart":
        fig = charts.area_chart(df)
        insight = "Area chart shows cumulative WAR total over seasons."
    elif chart_type == "Count Chart":
        fig = charts.count_chart(df)
        insight = "Count chart shows number of players per season."
    elif chart_type == "Violin Chart":
        fig = charts.violin_chart(df)
        insight = "Violin chart shows distribution of WAR total."

    return stats_text, fig, insight


def clear_filters():
    return "Pie Chart", "All", "All", "raptor_total", 0, 3000


with gr.Blocks(title="NBA RAPTOR Dashboard", css="""
    body { background-color: #fef9e7; }
    .gradio-container { background-color: #fef9e7; }
    .gr-button { background-color: #6a0dad; color: white; font-size: 12px; padding: 6px 12px; border-radius: 8px; }
    .gr-dropdown, .gr-slider, .gr-textbox, .gr-plot { border: 2px solid #6a0dad; border-radius: 8px; }
    h1, h2, h3, label { color: #6a0dad; text-align: center; }
""") as demo:
    gr.Markdown("## 🏀 NBA RAPTOR Dashboard")

    # Notes section in parallel
    with gr.Row():
        with gr.Column():
            gr.Markdown("""
            **Metric Notes:**
            - `raptor_total`: Overall RAPTOR rating (works well with Bar, Line, Histogram, Violin).
            - `raptor_offense`: Offensive RAPTOR rating (best for Scatter, Bar, Histogram).
            - `raptor_defense`: Defensive RAPTOR rating (best for Scatter, Heatmap, Histogram).
            - `war_total`: Wins Above Replacement (best for Bar, Area, Line).
            - `mp`: Minutes Played (best for Box, Violin, Histogram).
            """)

        with gr.Column():
            gr.Markdown("""
            **Minutes Filter Notes:**
            - `Min/Max Minutes` filters apply correctly to charts that use **player-level data**:
            - `Histogram, Box, Violin` → show distributions restricted by minutes played.
            - `Bar, Scatter` → show only players within the minutes range.
            - `Charts based on` **aggregated or correlation data** (Heatmap, Area, Count) may ignore or flatten the minutes filter.
            """)

    # Horizontal filter bar
    with gr.Row():
        chart_type = gr.Dropdown(
            ["Pie Chart", "Histogram", "Line Chart", "Bar Chart", "Scatter Chart",
             "Box Chart", "Heatmap", "Area Chart", "Count Chart", "Violin Chart"],
            value="Pie Chart", label="Chart Type"
        )
        season = gr.Dropdown(["All"] + sorted(filters.player["season"].unique().tolist()), value="All", label="Season")
        player_name = gr.Dropdown(["All"] + sorted(filters.player["player_name"].unique().tolist()), value="All", label="Player")
        metric = gr.Dropdown(["raptor_total","raptor_offense","raptor_defense","war_total","mp"], value="raptor_total", label="Metric")

    # Min/Max sliders in one row
    with gr.Row():
        min_minutes = gr.Slider(0, 3000, value=0, step=100, label="Min Minutes")
        max_minutes = gr.Slider(0, 3000, value=3000, step=100, label="Max Minutes")

    # Buttons row
    with gr.Row():
        apply_btn = gr.Button("Apply Filters")
        clear_btn = gr.Button("Clear Filters")

    # Centered Quick Stats + chart + insight
    stats_box = gr.Textbox(label="Quick Stats", interactive=False)
    chart_output = gr.Plot(label="Visualization")
    explanation = gr.Textbox(label="Chart Insight", interactive=False)

    # Connect buttons
    apply_btn.click(show_chart,
                    inputs=[chart_type, season, player_name, metric, min_minutes, max_minutes],
                    outputs=[stats_box, chart_output, explanation])

    clear_btn.click(clear_filters,
                    inputs=[],
                    outputs=[chart_type, season, player_name, metric, min_minutes, max_minutes])

if __name__ == "__main__":
    demo.launch()
