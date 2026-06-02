import gradio as gr
import charts
import filters

def show_all_charts(season, player_name, metric, min_minutes, max_minutes):
    df, metric = filters.apply_filters(
        season=season,
        player_name=player_name,
        metric=metric,
        min_minutes=min_minutes,
        max_minutes=max_minutes
    )

    # Quick stats: top 3 players by WAR
    top_players = df.groupby("player_name")["war_total"].sum().sort_values(ascending=False).head(3)
    stats_text = "Top Players by WAR:\n" + "\n".join([f"{p}: {v:.2f}" for p, v in top_players.items()])

    # KPI summary values
    avg_offense = df["raptor_offense"].mean()
    avg_defense = df["raptor_defense"].mean()
    avg_minutes = df["mp"].mean()
    total_war = df["war_total"].sum()

    # Generate all charts
    pie = charts.pi_chart(df)
    histo = charts.histo_chart(df[metric])
    line = charts.line_chart(df["season"], df[metric])
    bar = charts.bar_chart(df)
    scatter = charts.scatter_chart(df["raptor_offense"], df["raptor_defense"])
    box = charts.box_chart(df["mp"])
    heatmap = charts.heatmap_chart(df)
    area = charts.area_chart(df)
    count = charts.count_chart(df)
    violin = charts.violin_chart(df)

    return (stats_text,
            f"{avg_offense:.2f}", f"{avg_defense:.2f}", f"{avg_minutes:.0f}", f"{total_war:.2f}",
            pie, histo, line, bar, scatter, box, heatmap, area, count, violin)


def clear_filters():
    return "All", "All", "raptor_total", 0, 3000


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

    # Filter bar
    with gr.Row():
        season = gr.Dropdown(["All"] + sorted(filters.player["season"].unique().tolist()), value="All", label="Season")
        player_name = gr.Dropdown(["All"] + sorted(filters.player["player_name"].unique().tolist()), value="All", label="Player")
        metric = gr.Dropdown(["raptor_total","raptor_offense","raptor_defense","war_total","mp"], value="raptor_total", label="Metric")

    with gr.Row():
        min_minutes = gr.Slider(0, 3000, value=0, step=100, label="Min Minutes")
        max_minutes = gr.Slider(0, 3000, value=3000, step=100, label="Max Minutes")

    with gr.Row():
        apply_btn = gr.Button("Apply Filters")
        clear_btn = gr.Button("Clear Filters")

    # KPI summary cards
    with gr.Row():
        kpi_offense = gr.Textbox(label="Avg RAPTOR Offense", interactive=False)
        kpi_defense = gr.Textbox(label="Avg RAPTOR Defense", interactive=False)
        kpi_minutes = gr.Textbox(label="Avg Minutes Played", interactive=False)
        kpi_war = gr.Textbox(label="Total WAR", interactive=False)

    # Quick Stats
    stats_box = gr.Textbox(label="Quick Stats", interactive=False)

    # Charts grid
    with gr.Row():
        pie_output = gr.Plot(label="Pie Chart")
        histo_output = gr.Plot(label="Histogram")
        line_output = gr.Plot(label="Line Chart")

    with gr.Row():
        bar_output = gr.Plot(label="Bar Chart")
        scatter_output = gr.Plot(label="Scatter Chart")
        box_output = gr.Plot(label="Box Chart")

    with gr.Row():
        heatmap_output = gr.Plot(label="Heatmap")
        area_output = gr.Plot(label="Area Chart")
        
    
    with gr.Row():
            count_output = gr.Plot(label="Count Chart")
            violin_output = gr.Plot(label="Violin Chart")
    # Connect buttons
    apply_btn.click(
        show_all_charts,
        inputs=[season, player_name, metric, min_minutes, max_minutes],
        outputs=[stats_box, kpi_offense, kpi_defense, kpi_minutes, kpi_war,
                 pie_output, histo_output, line_output,
                 bar_output, scatter_output, box_output,
                 heatmap_output, area_output, count_output, violin_output]
    )

    clear_btn.click(
        clear_filters,
        inputs=[],
        outputs=[season, player_name, metric, min_minutes, max_minutes]
    )

if __name__ == "__main__":
    demo.launch()
