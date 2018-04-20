import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask
import datetime


def pasien(nama, email, br, tg, jk, gd):
    data = {
        u'Nama': nama,
        u'Email': email,
        u'Berat': br,
        u'Tinggi': tg,
        u'Jenis Kelamin': jk,
        u'Golongan Darah': gd,
    }
    return data


def rekam_medis(gj, pn, tk, t, ds, jn, nm):
    data = {
        u'Gejala': gj,
        u'Penyakit': pn,
        u'Tindakan': tk,
        u'Pengobatan': {
            u'Nama': nm,
            u'Jenis': jn,
            u'Dosis': ds,
        },
        u'Waktu': t
    }
    return data


ps = pasien("", "", 0, 0, "", "")
rm = rekam_medis("", "", "", datetime.datetime.now(), "", "", "")
app = Flask(__name__)


@app.route('/')
def hello():
    return


@app.route('/tes')
def tes1():
    return u'{} => {}'.format(docs.id, docs.to_dict())


cred = credentials.Certificate('kunci.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

pasien_ref = db.collection(u'Pasien')

# print(ps)
# print(rm)
# pasien_ref.document().set(ps)
docs = pasien_ref.limit(1).get()

def getdatapasien(idp, **par):
    if 'par' in par:
        if par['par'] == 'Nama':
            return pasien_ref.document(idp).get().get("Nama")
        elif par['par'] == 'Email':
            return pasien_ref.document(idp).get().get("Email")
        elif par['par'] == 'Berat':
            return pasien_ref.document(idp).get().get("Berat")
        elif par['par'] == 'Tinggi':
            return pasien_ref.document(idp).get().get("Tinggi")
        elif par['par'] == 'Jenis Kelamin':
            return pasien_ref.document(idp).get().get("Jenis Kelamin")
        elif par['par'] == 'Golongan Darah':
            return pasien_ref.document(idp).get().get("Golongan Darah")
    else:
        return pasien_ref.document(idp).get().to_dict()


def getdatarm(idp, **kwargs):
    rekam_ref = pasien_ref.document(idp).collection(u'Rekam Medis')
    reks = rekam_ref.get()
    if 'idrm' not in kwargs:
        for rek in reks:
            return rek.to_dict()
    else:
        reks=rekam_ref.document(kwargs['idrm']).get()
        if 'par' in kwargs:
            if kwargs['par'] == 'Gejala':
                return reks.get("Gejala")
            elif kwargs['par'] == 'Pengobatan':
                return reks.get("Pengobatan")
            elif kwargs['par'] == 'Penyakit':
                return reks.get("Penyakit")
            elif kwargs['par'] == 'Tindakan':
                return reks.get("Tindakan")
            elif kwargs['par'] == 'Waktu':
                return reks.get("Waktu")
        else:
            return reks.to_dict()


for doc in docs:
    print(getdatapasien(doc.id))
    print(getdatarm(doc.id,idrm='VWAzZAfqhK20FYFoibFB',par='Waktu'))
    # print(pasien_ref.document(doc.id).get().get("Tinggi"))
    # rekam_ref = pasien_ref.document(doc.id).collection(u'Rekam Medis')
    #rekam_ref.collection('Rekam Medis').add(rm)
    # reks=rekam_ref.get()
    # for rek in reks:
        # print(u'{} => {}'.format(rek.id, rek.to_dict()))




# app.run(host='0.0.0.0')
