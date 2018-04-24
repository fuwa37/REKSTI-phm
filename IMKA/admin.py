import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime

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

# daftar('123456789101112', "Obat Flu", "Obat Flu", "", "Meredakan Flu", 100, datetime.datetime.now())

def keluarbarang(id, jumlah):
    obat = obat_ref.document(id)
    jmlobat = obat.get().get("Jumlah")
    data = {'Jumlah': jmlobat-jumlah}
    obat.update(data)

# keluarbarang('123456789101112',30)

def bacasuhu(suhu):


from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/')
def main():
    return 0

@app.route('/masuk/<id>/<jumlah>', methods = ['GET', 'POST', 'DELETE'])
def masuk(id, jumlah):
    if request.method == 'POST':
        return 0


# app.run(host='0.0.0.0')