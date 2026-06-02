# 🏀 NBA RAPTOR Dashboard

An interactive data visualization tool built with **Gradio**, **Pandas**, **Matplotlib**, and **Seaborn** to explore NBA player performance using **RAPTOR metrics** and **Wins Above Replacement (WAR)**.  

This dashboard allows users to filter by season, player, metric, and minutes played, then visualize results across multiple chart types. It also provides **Quick Stats** highlighting the top players by WAR.

---

## ✨ Features

- **Interactive Filters**
  - Select season, player, metric, and minutes range.
  - Apply or clear filters instantly.

- **Multiple Chart Types**
  - Pie, Histogram, Line, Bar, Scatter, Box, Heatmap, Area, Count, Violin.
  - Each chart comes with a short **insight note** explaining what it shows.

- **Quick Stats**
  - Displays the top 3 players by WAR for the selected filters.
  - Centered, clean design for easy readability.

- **Modern UI**
  - Rounded corners, yellow theme.
  - Parallel notes section explaining metrics and minutes filters.

---

## 📊 Metric Notes

- `raptor_total`: Overall RAPTOR rating (works well with Bar, Line, Histogram, Violin).  
- `raptor_offense`: Offensive RAPTOR rating (best for Scatter, Bar, Histogram).  
- `raptor_defense`: Defensive RAPTOR rating (best for Scatter, Heatmap, Histogram).  
- `war_total`: Wins Above Replacement (best for Bar, Area, Line).  
- `mp`: Minutes Played (best for Box, Violin, Histogram).  

---

## ⏱ Minutes Filter Notes

- Min/Max Minutes filters apply correctly to charts that use **player-level data**:
  - Histogram, Box, Violin → show distributions restricted by minutes played.  
  - Bar, Scatter → show only players within the minutes range.  
- Charts based on **aggregated or correlation data** (Heatmap, Area, Count) may ignore or flatten the minutes filter.  

---

## ⚙️ Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/studentubaid/Data_Analysis-_Dashboard_Project
cd nba-raptor-dashboard
pip install -r requirements.txt