import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import date, datetime
import time

cred = credentials.Certificate('kunci.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
obat_ref=db.collection('Obat')
suhu_ref=db.collection('Suhu')
klb_ref=db.collection('Kelembapan')

def dataobat(nama, jenis, produsen, keterangan, jumlah, kdl):
    data = {
        'Nama': nama,
        'Jenis': jenis,
        'Produsen': produsen,
        'Keterangan': keterangan,
        'Jumlah': jumlah,
        'Kadaluarsa': kdl,
    }
    return data

def masukbarang(id, jumlah):
    obat=obat_ref.document(id)
    jmlobat=obat.get().get("Jumlah")
    data={'Jumlah': jumlah+jmlobat}
    obat.update(data)

# masukbarang('vkUN4JYraEw7BmAId2Ei',30)

def daftar(id, nm, jn, pd, ket, jml, kdl):
    data=dataobat(nm,jn,pd,ket,jml,kdl)
    obat_ref.add(data, document_id=id)

# daftar('123456789101112', "Obat Flu", "Obat Flu", "", "Meredakan Flu", 100, datetime.now())

def keluarbarang(id, jumlah):
    obat = obat_ref.document(id)
    jmlobat = obat.get().get("Jumlah")
    data = {'Jumlah': jmlobat-jumlah}
    obat.update(data)

# keluarbarang('123456789101112',30)


def ceklastsuhu():
    docs=suhu_ref.get()
    for doc in docs:
        a=doc.id
    b=int(a)+1

    print(a)
    t1=suhu_ref.document(a).get().get("Tanggal").date()
    t2=datetime.now().date()

    if t1==t2:
        return a
    else:
        return b


def todaysuhu():
    idx = ceklastsuhu()
    suhu_ref.document(str(idx)).set({'Tanggal':datetime.now()})
    return str(idx)

def inputsuhu(sh):
    data = {
        'Sehu': sh,
        'Waktu': datetime.now()
    }
    suhu_ref.document(todaysuhu()).collection('1').document().set(data)

# inputsuhu(31)

from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__, template_folder='templates')


@app.route('/')
def main():
    return 0


@app.route('/masuk/<id>', methods = ['GET', 'POST', 'DELETE'])
def masuk(id):
    if request.method == 'GET':
        return render_template('/masuk_barang.html', id=id)
    if request.method == 'POST':
        id = request.form['ID']
        nm = request.form['nama']
        jn = request.form['jenis']
        pd = request.form['pd']
        ket = request.form['ket']
        jml = request.form['jml']
        kdl = request.form['kdl']

        print(id,nm,jml)
        daftar(id,nm,jn,pd,ket,jml,datetime.now())
        return '<p>aaaaaa</p>'


app.run(debug=True,host='0.0.0.0')