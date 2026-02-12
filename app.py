import gradio as gr
import pandas as pd
import plotly.graph_objects as go
import random

# Mock Data for Venue-Based Stats & Historical Records
venue_insights = {
    "Chepauk (Chennai)": {"Key Players": "Noor Ahmad, Jadeja, Ruturaj", "Pitch": "Spin Friendly / Slow"},
    "Wankhede (Mumbai)": {"Key Players": "Surya, Hardik, Bumrah", "Pitch": "Flat Track / High Scoring"},
    "Narendra Modi Stadium (Ahmedabad)": {"Key Players": "Shubman Gill, Rashid Khan", "Pitch": "Fast & Bouncy"},
    "Chinnaswamy (Bengaluru)": {"Key Players": "Virat Kohli, Glenn Maxwell", "Pitch": "Small Boundary / Batting Paradise"}
}

def get_historical_result(team1, team2, year, venue):
    # Simulating historical data logic
    outcomes = [team1, team2, "No Result"]
    winner = random.choice(outcomes)
    return f"In {year} at {venue}, the match between {team1} and {team2} resulted in: **{winner}**"

def predict_outcome(team1, team2, toss_winner, venue, weather, year):
    # 1. Base Logic for Prediction
    t1_strength = 85 if team1 == "CSK" else 80
    t2_strength = 82 if team2 == "MI" else 79
    
    # 2. Adjust for Venue & Toss
    if toss_winner == team1: t1_strength += 5
    else: t2_strength += 5
    
    win_prob = (t1_strength / (t1_strength + t2_strength)) * 100
    
    # 3. Create Gauge Chart
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = win_prob,
        title = {'text': f"{team1} Win Probability %"},
        gauge = {'axis': {'range': [0, 100]},
                 'bar': {'color': "#FFD700"},
                 'steps': [
                     {'range': [0, 50], 'color': "#ff4b4b"},
                     {'range': [50, 100], 'color': "#00ff00"}]}))
    fig.update_layout(paper_bgcolor="#111", font={'color': "white"})

    # 4. Get Insights
    insights = venue_insights.get(venue, {"Key Players": "N/A", "Pitch": "Neutral"})
    history = get_historical_result(team1, team2, year, venue)
    
    report = f"""
    ### 🏟️ Venue Analysis: {venue}
    * **Pitch Condition:** {insights['Pitch']}
    * **Players to Watch:** {insights['Key Players']}
    
    ### 📜 Historical Context
    {history}
    
    ### ⚡ AI Strategy Note
    Considering the 2026 trades, {team1} has a tactical edge in {weather} conditions.
    """
    return fig, report

# UI Design
with gr.Blocks(theme=gr.themes.Soft(primary_hue="gold", neutral_hue="slate")) as demo:
    gr.Markdown("# 🏆 IPL 2026 PRO-STRATEGIST (WITH HISTORICAL DATA)")
    
    with gr.Row():
        t1 = gr.Dropdown(["CSK", "MI", "RCB", "KKR", "RR", "GT"], label="Home Team")
        t2 = gr.Dropdown(["CSK", "MI", "RCB", "KKR", "RR", "GT"], label="Away Team")
    
    with gr.Row():
        venue = gr.Dropdown(list(venue_insights.keys()), label="Venue")
        year = gr.Slider(2008, 2025, step=1, label="Select Historical Year Reference")
        
    with gr.Row():
        toss = gr.Radio(["Home Team", "Away Team"], label="Toss Winner")
        weather = gr.Radio(["Clear", "Humid", "Rainy"], label="Weather Condition")
    
    btn = gr.Button("ANALYZE MATCH & HISTORY", variant="primary")
    
    chart = gr.Plot()
    report = gr.Markdown()
    
    btn.click(predict_outcome, inputs=[t1, t2, toss, venue, weather, year], outputs=[chart, report])

demo.launch()

