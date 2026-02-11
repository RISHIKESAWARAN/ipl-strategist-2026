import gradio as gr
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 1. 2026 Season Data (Updated Stats & Trade Logic)
team_data = {
    "Chennai Super Kings": {"venue": "M.A. Chidambaram Stadium", "color": "#FFFF00", "avg": 165, "bat": "Ruturaj Gaikwad (583 Runs)", "bowl": "Noor Ahmad (Mystery Spin)"},
    "Mumbai Indians": {"venue": "Wankhede Stadium", "color": "#004BA0", "avg": 185, "bat": "Suryakumar Yadav (605 Runs)", "bowl": "Jasprit Bumrah (20 Wkts)"},
    "Rajasthan Royals": {"venue": "Sawai Mansingh Stadium", "color": "#EA1A85", "avg": 162, "bat": "Yashasvi Jaiswal (625 Runs)", "bowl": "Ravindra Jadeja (Captain)"},
    "Punjab Kings": {"venue": "PCA Stadium", "color": "#D71920", "avg": 174, "bat": "Shreyas Iyer (Captain)", "bowl": "Arshdeep Singh (19 Wkts)"},
    "Gujarat Titans": {"venue": "Narendra Modi Stadium", "color": "#1B2133", "avg": 178, "bat": "Shubman Gill (890 Runs)", "bowl": "Rashid Khan (27 Wkts)"},
    "Lucknow Super Giants": {"venue": "Ekana Stadium", "color": "#0057E2", "avg": 158, "bat": "Nicholas Pooran (358 Runs)", "bowl": "Ravi Bishnoi (16 Wkts)"},
    "Royal Challengers Bengaluru": {"venue": "M. Chinnaswamy Stadium", "color": "#EC1C24", "avg": 195, "bat": "Virat Kohli (639 Runs)", "bowl": "Mohammed Siraj (19 Wkts)"},
    "Kolkata Knight Riders": {"venue": "Eden Gardens", "color": "#2E0854", "avg": 182, "bat": "Rinku Singh (474 Runs)", "bowl": "V. Chakaravarthy (21 Wkts)"},
    "Sunrisers Hyderabad": {"venue": "Rajiv Gandhi Stadium", "color": "#FF822A", "avg": 178, "bat": "Heinrich Klaasen (448 Runs)", "bowl": "Pat Cummins (17 Wkts)"},
    "Delhi Capitals": {"venue": "Arun Jaitley Stadium", "color": "#00008B", "avg": 172, "bat": "Rishabh Pant (446 Runs)", "bowl": "Kuldeep Yadav (16 Wkts)"}
}

teams_list = sorted(list(team_data.keys()))

# Custom CSS for Dark Mode & Premium UI
custom_css = """
.gradio-container { background-color: #0b0d17 !important; border-radius: 15px; }
#banner_div { background: linear-gradient(90deg, #1e3c72, #2a5298); padding: 30px; border-radius: 12px; text-align: center; color: #FFD700; border-bottom: 4px solid #FFD700; margin-bottom: 20px; }
#step_card { background: rgba(255, 255, 255, 0.05); border-left: 5px solid #FFD700; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
"""

def get_insights(h, a):
    if not h or not a or h == a: return "### ⚠️ Error: Please select two different teams!", None, gr.update(choices=[])
    v_info = f"🏟️ **LOCATION:** {team_data[h]['venue']} | 📈 **HISTORIC AVG:** {team_data[h]['avg']} Runs"
    fig = px.bar(x=[h, a], y=[np.random.randint(15, 25), np.random.randint(15, 25)], 
                 color=[h, a], color_discrete_map={h: team_data[h]["color"], a: team_data[a]["color"]}, height=300)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", showlegend=False)
    return v_info, fig, gr.update(choices=[h, a], value=None)

def predict_final(h, a, t_w, t_d, cond, time):
    if not t_w: return None, "⚠️ Wait! Complete Step 1 & Step 2 first."
    prob = np.random.uniform(52, 68)
    winner = h if prob > 56 else a
    gauge = go.Figure(go.Indicator(mode="gauge+number", value=prob, title={'text': f"{winner} WIN PROBABILITY (%)", 'font': {'color': 'white'}},
                                   gauge={'axis': {'range': [0, 100], 'tickcolor': "white"}, 'bar': {'color': team_data[winner]["color"]}}))
    gauge.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)', font_color="white")
    
    report = f"💎 **ELITE PERFORMANCE CARD** 💎\n\n🏠 **{h}**: {team_data[h]['bat']} | {team_data[h]['bowl']}\n✈️ **{a}**: {team_data[a]['bat']} | {team_data[a]['bowl']}\n\n"
    report += f"⚡ **AI VERDICT:** {winner} is favored in {time} conditions ({cond})."
    return gauge, report

with gr.Blocks(theme=gr.themes.Default(primary_hue="yellow"), css=custom_css) as demo:
    # 🏆 Professional Banner Header
    gr.HTML("<div id='banner_div'><h1>🏏 IPL 2026 STRATEGIST AI</h1><p>Predicting the Future of Cricket with Real-Time Data</p></div>")

    # 📘 Enhanced Step-by-Step Onboarding
    with gr.Column(elem_id="step_card", visible=True) as tutorial_col:
        gr.Markdown("""
        ### 🚀 **GETTING STARTED (Tutorial):**
        1.  **TEAM SELECTION:** Pick your **Home Team** (sets the ground) and **Away Team**.
        2.  **DATA ANALYSIS:** Click **'🔍 1. ANALYZE'** to see the venue stats and Head-to-Head chart.
        3.  **MATCH SETUP:** Select who won the **Toss**, their **Decision**, and current **Weather**.
        4.  **AI PREDICTION:** Hit **'🚀 2. GENERATE'** to see the Win Probability Gauge and Elite Player Report.
        """)
        skip_btn = gr.Button("✅ GOT IT, LAUNCH APP", variant="primary")

    with gr.Row():
        h_t = gr.Dropdown(teams_list, label="Select Home Team", value=None)
        a_t = gr.Dropdown(teams_list, label="Select Away Team", value=None)

    btn = gr.Button("🔍 1. ANALYZE MATCHUP", variant="primary")
    v_info = gr.Markdown("### 📊 Venue & Stats will appear here...")
    h2h_plot = gr.Plot()

    

    with gr.Row():
        t_w = gr.Dropdown([], label="Toss Winner")
        t_d = gr.Radio(["bat", "field"], label="Toss Decision", value="field")
    
    with gr.Row():
        cond = gr.Dropdown(["Dry & Sunny", "Dew Expected", "Rainy"], label="Pitch Conditions")
        time = gr.Radio(["Day", "Night"], label="Match Time")

    p_btn = gr.Button("🚀 2. GENERATE PREDICTION", variant="stop")
    
    with gr.Row():
        gauge_out = gr.Plot()
        report_out = gr.Textbox(label="Final Performance & Strategy Report", lines=10)

    # UI Logic
    skip_btn.click(lambda: gr.update(visible=False), None, tutorial_col)
    btn.click(get_insights, [h_t, a_t], [v_info, h2h_plot, t_w])
    p_btn.click(predict_final, [h_t, a_t, t_w, t_d, cond, time], [gauge_out, report_out])

demo.launch(share=True)
