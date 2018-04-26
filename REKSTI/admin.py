import adminfirebase as af
from flask import Flask, request, render_template, jsonify
from datetime import date, datetime

app = Flask(__name__, template_folder='dashboard')


@app.route("/", methods = ['GET', 'POST'])
def daftar():
    id=af.createid()
    if request.method == 'GET':
        return render_template('/pages/adminpd.html', id=id)
    if request.method == 'POST':
        nm = request.form['nm']
        em = request.form['em']
        tgl = datetime.strptime(request.form['tgl'], '%d %b %Y')
        jk = request.form['jk']
        br = int(request.form['br'])
        tg = int(request.form['tg'])
        gd = request.form['gd']

        af.createps(id,nm,em,tgl,br,tg,jk,gd)

        return id

@app.route("/<id>", methods = ['GET', 'POST'])
def daftarid(id):
    id=id
    if request.method == 'GET':
        return render_template('/pages/adminpd.html', id=id)
    if request.method == 'POST':
        nm = request.form['nm']
        em = request.form['em']
        tgl = datetime.strptime(request.form['tgl'], '%d %b %Y')
        jk = request.form['jk']
        br = int(request.form['br'])
        tg = int(request.form['tg'])
        gd = request.form['gd']

        af.createps(id,nm,em,tgl,br,tg,jk,gd)

        return id

@app.route("/data")
def data():
    a=af.getallpenyakit()
    return render_template("/pages/data.html", data=a)

app.run(host='0.0.0.0', port=5002)