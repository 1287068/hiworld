import html
import random

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Hello World Motion Lab",
    page_icon="👋",
    layout="wide",
)

# -----------------------------
# Sidebar controls
# -----------------------------
st.sidebar.title("🎛️ Motion Lab Controls")
st.sidebar.caption("Personalize your name, then add motion.")

name = st.sidebar.text_input("Your name", value="Hello World", max_chars=80)
font_family = st.sidebar.selectbox(
    "Font type",
    ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana", "Trebuchet MS", "Impact", "Comic Sans MS"],
)
font_size = st.sidebar.slider("Font size", min_value=20, max_value=120, value=56, step=2)
font_weight = st.sidebar.selectbox("Font weight", ["Normal", "Bold", "Extra bold"])
text_color_choice = st.sidebar.selectbox(
    "Name color",
    ["Auto contrast", "Electric blue", "Hot pink", "Gold", "Mint", "White", "Black"],
)
background = st.sidebar.selectbox(
    "Background",
    [
        "Light",
        "Dark",
        "Sky",
        "Sunset",
        "Forest",
        "Lavender",
        "Ocean",
        "Midnight gradient",
    ],
)
name_mode = st.sidebar.selectbox("Name display mode", ["Centered", "Ticker Tape", "Repeated"])
effect = st.sidebar.selectbox(
    "Dynamic action",
    ["None", "Rain", "Snow", "Hail", "Wind gust", "Confetti", "Tornado"],
)
speed_label = st.sidebar.select_slider(
    "Animation speed",
    options=["Gentle", "Normal", "Fast"],
    value="Normal",
)
density = st.sidebar.slider("Effect density", min_value=12, max_value=90, value=42, step=6)

# -----------------------------
# Theme and typography settings
# -----------------------------
backgrounds = {
    "Light": ("#f7f9fc", "#151923"),
    "Dark": ("#101216", "#ffffff"),
    "Sky": ("linear-gradient(135deg, #c8f0ff, #effbff)", "#12334a"),
    "Sunset": ("linear-gradient(135deg, #ff9966, #ff5e62, #6a3093)", "#ffffff"),
    "Forest": ("linear-gradient(135deg, #d4fc79, #96e6a1)", "#123b2a"),
    "Lavender": ("linear-gradient(135deg, #f3e7ff, #d9e4ff)", "#35244f"),
    "Ocean": ("linear-gradient(135deg, #005c97, #363795)", "#ffffff"),
    "Midnight gradient": ("linear-gradient(135deg, #090979, #020024, #24104f)", "#ffffff"),
}
bg_css, auto_text_color = backgrounds[background]
font_weights = {"Normal": "400", "Bold": "700", "Extra bold": "900"}
text_colors = {
    "Auto contrast": auto_text_color,
    "Electric blue": "#00a8ff",
    "Hot pink": "#ff3cac",
    "Gold": "#ffd166",
    "Mint": "#4fffb0",
    "White": "#ffffff",
    "Black": "#111111",
}
text_color = text_colors[text_color_choice]
durations = {"Gentle": 5.5, "Normal": 3.2, "Fast": 1.7}
duration = durations[speed_label]

# Escape user text so it is displayed as text, not interpreted as HTML.
safe_name = html.escape(name.strip() or "Hello World")
safe_font = font_family  # Chosen from a fixed allow-list above.
weight = font_weights[font_weight]

# -----------------------------
# Generate a field of animated particles
# All animation runs in the browser using CSS keyframes, so it loops smoothly
# without repeatedly rerunning the Streamlit Python script.
# -----------------------------
particle_count = density
particle_specs = []
symbols_by_effect = {
    "Rain": ["💧", "💦", "│"],
    "Snow": ["❄", "❅", "❆", "✳"],
    "Hail": ["🧊", "●", "○"],
    "Wind gust": ["〰", "〜", "﹏", "➝", "🍃"],
    "Confetti": ["●", "■", "▲", "🎉", "✦", "◆"],
    "Tornado": ["〰", "🌀", "·", "✦"],
}
symbols = symbols_by_effect.get(effect, [])

if symbols:
    for i in range(particle_count):
        left = random.uniform(1, 99)
        delay = random.uniform(0, duration)
        size = random.randint(12, 27) if effect != "Hail" else random.randint(12, 24)
        drift = random.randint(-120, 120)
        particle_specs.append(
            f'<span class="particle p{i}" style="left:{left:.2f}%;'
            f'animation-delay:-{delay:.2f}s;animation-duration:{duration * random.uniform(0.75, 1.4):.2f}s;'
            f'font-size:{size}px;--drift:{drift}px;">{html.escape(random.choice(symbols))}</span>'
        )
particles_html = "".join(particle_specs)

effect_class = {
    "None": "effect-none",
    "Rain": "effect-rain",
    "Snow": "effect-snow",
    "Hail": "effect-hail",
    "Wind gust": "effect-wind",
    "Confetti": "effect-confetti",
    "Tornado": "effect-tornado",
}[effect]

if name_mode == "Repeated":
    name_markup = '<div class="repeated">' + "".join(
        f'<div class="name-line">{safe_name}</div>' for _ in range(5)
    ) + "</div>"
elif name_mode == "Ticker Tape":
    name_markup = f'<div class="ticker-track"><span>{safe_name}</span><span aria-hidden="true">{safe_name}</span></div>'
else:
    name_markup = f'<div class="center-name">{safe_name}</div>'

html_doc = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; padding: 0; }}
  body {{ font-family: Arial, sans-serif; }}
  .stage {{
    position: relative;
    width: 100%;
    height: 650px;
    overflow: hidden;
    isolation: isolate;
    border-radius: 20px;
    background: {bg_css};
    color: {text_color};
    box-shadow: 0 12px 36px rgba(0,0,0,.14);
  }}
  .stage::before {{
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 50% 45%, rgba(255,255,255,.14), transparent 58%);
    pointer-events: none;
    z-index: 1;
  }}
  .particles {{ position: absolute; inset: 0; overflow: hidden; z-index: 2; pointer-events: none; }}
  .particle {{
    position: absolute;
    top: -45px;
    display: block;
    line-height: 1;
    opacity: .88;
    user-select: none;
    will-change: transform;
  }}
  .effect-rain .particle, .effect-hail .particle {{
    animation-name: fall;
    animation-timing-function: linear;
    animation-iteration-count: infinite;
  }}
  .effect-snow .particle {{
    animation-name: snowfall;
    animation-timing-function: linear;
    animation-iteration-count: infinite;
  }}
  .effect-wind .particle {{
    top: auto;
    animation-name: gust;
    animation-timing-function: ease-in-out;
    animation-iteration-count: infinite;
  }}
  .effect-confetti .particle {{
    animation-name: confetti;
    animation-timing-function: linear;
    animation-iteration-count: infinite;
  }}
  .effect-tornado .particle {{
    top: 50%;
    left: 50%;
    animation-name: tornado;
    animation-timing-function: linear;
    animation-iteration-count: infinite;
  }}
  .effect-rain .particle {{ color: #38a9ff; }}
  .effect-hail .particle {{ filter: drop-shadow(0 2px 2px rgba(0,0,0,.18)); }}
  .effect-wind .particle {{ left: -15% !important; }}
  .effect-wind .particle:nth-child(3n) {{ top: 25%; }}
  .effect-wind .particle:nth-child(3n + 1) {{ top: 52%; }}
  .effect-wind .particle:nth-child(3n + 2) {{ top: 76%; }}
  .effect-confetti .particle:nth-child(3n) {{ color: #ff4d6d; }}
  .effect-confetti .particle:nth-child(3n + 1) {{ color: #ffd166; }}
  .effect-confetti .particle:nth-child(3n + 2) {{ color: #06d6a0; }}
  .name-layer {{
    position: absolute;
    z-index: 5;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    font-family: "{safe_font}", sans-serif;
    font-size: {font_size}px;
    font-weight: {weight};
    line-height: 1.15;
    color: {text_color};
    text-shadow: 0 2px 10px rgba(0,0,0,.16);
    overflow-wrap: anywhere;
    padding: 28px;
  }}
  .center-name {{ text-align: center; max-width: 100%; }}
  .ticker-track {{
    display: flex;
    align-items: center;
    width: max-content;
    white-space: nowrap;
    gap: 100px;
    animation: ticker 12s linear infinite;
  }}
  .ticker-track span {{ padding-right: 20px; }}
  .repeated {{ width: 100%; text-align: center; display: flex; flex-direction: column; gap: 8px; }}
  .name-line {{ opacity: .94; }}
  .name-line:nth-child(2n) {{ opacity: .55; transform: translateX(4%); }}
  .name-line:nth-child(3n) {{ opacity: .72; transform: translateX(-4%); }}
  .hint {{
    position: absolute;
    z-index: 6;
    bottom: 14px;
    left: 0;
    right: 0;
    text-align: center;
    font: 12px/1.4 Arial, sans-serif;
    opacity: .68;
    letter-spacing: .08em;
    text-transform: uppercase;
    pointer-events: none;
  }}
  @keyframes fall {{ from {{ transform: translate3d(0,-20px,0); }} to {{ transform: translate3d(25px,720px,0); }} }}
  @keyframes snowfall {{ 0% {{ transform: translate3d(0,-30px,0) rotate(0deg); }} 50% {{ transform: translate3d(55px,330px,0) rotate(180deg); }} 100% {{ transform: translate3d(-25px,720px,0) rotate(360deg); }} }}
  @keyframes gust {{ 0% {{ transform: translateX(-20vw) rotate(0deg); opacity: 0; }} 15% {{ opacity: .9; }} 85% {{ opacity: .9; }} 100% {{ transform: translateX(130vw) rotate(15deg); opacity: 0; }} }}
  @keyframes confetti {{ 0% {{ transform: translate3d(0,-30px,0) rotate(0deg); }} 100% {{ transform: translate3d(var(--drift),720px,0) rotate(800deg); }} }}
  @keyframes tornado {{ 0% {{ transform: rotate(0deg) translateX(20px) scale(.65); opacity: .1; }} 50% {{ opacity: .95; }} 100% {{ transform: rotate(720deg) translateX(170px) scale(1.2); opacity: 0; }} }}
  @keyframes ticker {{ from {{ transform: translateX(55vw); }} to {{ transform: translateX(-55%); }} }}
  @media (prefers-reduced-motion: reduce) {{
    .particle, .ticker-track {{ animation-duration: 20s !important; }}
  }}
</style>
</head>
<body>
  <main class="stage">
    <div class="particles {effect_class}">{particles_html}</div>
    <div class="name-layer">{name_markup}</div>
    <div class="hint">Hello World Motion Lab · {html.escape(effect)} effect</div>
  </main>
</body>
</html>
"""

st.title("👋 Hello World Motion Lab")
st.write("A tiny app-building playground: enter a name, choose its style, and watch the scene come alive.")
components.html(html_doc, height=670, scrolling=False)
st.caption("Tip: change the controls in the sidebar to experiment with fonts, colors, backgrounds, and looping motion.")
