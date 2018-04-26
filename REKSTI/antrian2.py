import adminfirebase as af
from flask import Flask, jsonify, render_template

app = Flask(__name__, template_folder="dashboard")


@app.route("/")
def antrian2():
    dictlist=[]
    a=af.getlistantripasien()
    for key, value in a.items():
        temp = value
        dictlist.append(temp)
    return render_template("pages/antrian.html", antri=dictlist)


app.run(host='0.0.0.0', port=5001)