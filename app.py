from flask import Flask
from flask import render_template
from faker import Faker
import requests

the_app = Flask(__name__)
fake = Faker()

@the_app.route("/requirements/")
def require():
    with open("requirements/requirements.txt", "r") as f:
        text = f.readlines()

    return render_template("main.html", content = text)


def func(amount):
    data_names = set()
    data_emails = set()
    data_full = []
    
    while len(data_names) <= amount or len(data_emails) <= amount:
        data_names.add(fake.first_name())
        data_emails.add(fake.email())

    with open("templates/users.txt", "w") as file:
        num = 0
        for i in range(amount):
            num +=1
            data_full = str(num) + ". " + list(data_names)[num] + " " + list(data_emails)[num] + " "
            file.write(data_full + '\n' )


@the_app.route("/generate-users/<int:number>")
@the_app.route("/generate-users/")
def generate(number=100):
    func(number)
    
    with open("templates/users.txt", "r") as f:
        text = f.readlines()

    return render_template("users.html", content = text)


@the_app.route("/mean/")
def mean():
    amount = 0
    height_result = 0
    weight_result = 0

    with open("templates/hw.csv", "r") as f:
        file = f.readlines()

    for i in file[1:]:
        if i == "\n":
            continue
        i = i.split(",")
        
        height_result = height_result + float(i[1])
        weight_result = weight_result + float(i[2])
        amount += 1

    arithmetic_mean_height = height_result/amount
    arithmetic_mean_weight = weight_result/amount
    w = round(arithmetic_mean_weight, 5)     
    h = round(arithmetic_mean_height, 5)

    return render_template("arithmetic_mean.html", weight = w, height = h)


@the_app.route("/space/")
def space():
    responce = requests.get('http://api.open-notify.org/astros.json')
    result = responce.json()
    return render_template("space.html", content = result)


@the_app.route("/")
def index():
    return render_template("base.html")


if __name__ == "__main__":
    the_app.run(debug=True)




