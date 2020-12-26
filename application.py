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
        if (len(email) == 0):
             return render_template("certification.html",error="Email cannot be  blank!")
        name = request.form.get("name")
        if (len(name) == 0):
             return render_template("certification.html",error="Name cannot be blank!")

        value = db.execute("Select * from members WHERE course=:course and email=:email", course=course,email=email)

        if (len(value) == 0):
            return render_template("certification.html",error="Email or track is wrong!")

        if (value[0]['status'] <= 0):
            db.execute("UPDATE members set status = status + 1 WHERE course=:course and email=:email", course=course,email=email)
            db.execute("UPDATE members set name = :name WHERE course=:course and email=:email", name=name, course=course,email=email)
        elif (value[0]['status'] == 1):
            name = db.execute("Select name from members WHERE course=:course and email=:email", course=course,email=email)[0]['name']
        else:
            return render_template("certification.html",error="Something went wrong contact us!")


        course_name = db.execute("Select course_name from members WHERE course=:course and email=:email", course=course,email=email)[0]['course_name']
        im = Image.open(r'empty.jpg')
        d = ImageDraw.Draw(im)
        if len(name) < 35:
            location = (590-((len(name)/2)*19), 440)
        else:
            location = (590-((len(name)/2)*17), 440)
        text_color = (0, 0, 0)
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        d.text(location, name, fill = text_color,font=font)
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)

        text_color = (104, 104, 104)
        course = "For active participation and successfully completing " + course_name + " course organized by"
        location = (590-((len(course)/2)*9),545)
        d.text(location,course,fill=text_color,font=font)
        im.save("certifications" +"/" +email + ".pdf")
        return send_file("certifications" +"/" +email + ".pdf", as_attachment=True)





    else:
        return render_template("certification.html")
