import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, send_file
from flask_session import Session
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
db = SQL("sqlite:///data.db")


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
        course = request.form.get("course")
        email = request.form.get("email")
        name = request.form.get("name")
        value = db.execute("Select * from members WHERE course=:course and email=:email", course=course,email=email)
        if (True):
            db.execute("UPDATE members set status = status + 1 WHERE course=:course and email=:email", course=course,email=email)
            im = Image.open(r'certificate.jpg')
            d = ImageDraw.Draw(im)
            location = (180, 270)
            text_color = (0, 0, 0)
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
            d.text(location, name, fill = text_color,font=font)
            im.save("certificate_" + "1" + ".pdf")
            return send_file("certificate_" + "1" + ".pdf", as_attachment=True)



    else:
        return render_template("certification.html")
