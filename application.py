import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tracks")
def tracks():
    return render_template("tracks.html")


@app.route("/ranking")
def ranking():
    return render_template("ranking.html")

@app.route("/certification", methods= ["GET","POST"])
def certification():
    if request.method == "POST":

        return render_template("index.html")

    else:
        im = Image.open(r'certificate.jpg')
        d = ImageDraw.Draw(im)
        location = (360, 298)
        text_color = (0, 137, 209)
        # font = ImageFont.truetype("arial.ttf", 120)
        d.text(location, "text here", fill = text_color)
        im.save("certificate_" + "1" + ".pdf")
        return render_template("certification.html")