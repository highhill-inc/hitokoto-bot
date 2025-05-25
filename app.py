from flask import Flask, render_template, jsonify, request
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

def generate_hitokoto(theme=None):
    base_prompt = (
        "あなたは開発者の人格を反映したBotです。\n"
        "特徴は以下の通りです：\n"
        "- 優しめの関西弁混じりで自然体\n"
        "- 本質を突く\n"
        "- ユーモアと皮肉が少しある\n"
        "- 冷静で地に足のついた視点\n"
        "- ブラックジョークやたまにズバッとくる\n"
    )

    if theme:
        prompt = base_prompt + f"- 以下のテーマに沿って、80文字以内で、今日のひとことを1つください：\n「{theme}」"
    else:
        prompt = base_prompt + "- 80文字以内で、今日のひとことを1つください"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response['choices'][0]['message']['content']

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    theme = data.get("theme", "").strip() if data else None
    message = generate_hitokoto(theme)
    return jsonify({"message": message})

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/howto")
def howto():
    return render_template("howto.html")

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
