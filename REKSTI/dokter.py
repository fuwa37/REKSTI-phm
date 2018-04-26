import adminfirebase as af
import adminemail as ae
from flask import Flask, request, render_template, redirect, url_for, jsonify
from datetime import date, datetime


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


app = Flask(__name__, template_folder='dashboard')

@app.route("/", methods = ['GET', 'POST'])
def dokter():
    id = af.getlistantripasien1()
    if request.method == 'GET':
        nm = af.getdatapasien(id, par="Nama")
        temp = af.getdatapasien(id, par="Tanggal Lahir")
        um = calculate_age(temp)
        tg = af.getdatapasien(id, par="Tinggi")
        br = af.getdatapasien(id, par="Berat")
        gd = af.getdatapasien(id, par="Golongan Darah")

        b=af.getdatarm(id)

        return render_template("/pages/dokter.html", id=id, nm=nm, um=um, tg=tg, br=br, gd=gd, rm=b)
    if request.method == 'POST':
        af.delantri()
        ae.send("irfanreynaldi37@gmail.com","Hai","Tes")
        return redirect(url_for('dokter'),code=302)

@app.route("/isi/<id>", methods = ['GET', 'POST'])
def isi(id):
    if request.method == 'GET':
        return render_template("/pages/isirm.html")
    if request.method == 'POST':

        return redirect(url_for('dokter'),code=302)

app.run(host='0.0.0.0', port=5003)