!pip install -q google-generativeai pandas ipywidgets
from google.colab import output; output.enable_custom_widget_manager()

import google.generativeai as genai
import pandas as pd
import ipywidgets as widgets
from IPython.display import display, Markdown

# Configure Gemini API
genai.configure(api_key="AIzaSyCgFcYAigEUSiA29Lwl4A254oLMkg-7_ro")
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# Sample SIEM logs
logs = pd.DataFrame([
    {
        "timestamp": "2025-10-09 12:00",
        "source": "Firewall",
        "event": "Blocked IP 192.168.1.10"
    },
    {
        "timestamp": "2025-10-09 12:05",
        "source": "Endpoint",
        "event": "Failed login attempt"
    }
])

# Log analysis function
def analyse_logs(logs_df):
    log_text = "\n".join(
        f"{row['timestamp']} | {row['source']} | {row['event']}"
        for _, row in logs_df.iterrows()
    )

    prompt = f"""
You are a cybersecurity analyst.
Analyse the following SIEM logs and:
1. Identify suspicious activities
2. Mention potential threats
3. Recommend actions

Logs:
{log_text}
"""

    response = model.generate_content(prompt)
    return response.text

# UI
analyse_btn = widgets.Button(description="Analyse Logs")
output_area = widgets.Output()

def on_click(b):
    with output_area:
        output_area.clear_output()
        result = analyse_logs(logs)
        display(Markdown("### Analysis Result\n" + result))

analyse_btn.on_click(on_click)

display(analyse_btn, output_area)
