import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime

from google.cloud import storage

# Instantiates a client
storage_client = storage.Client.from_service_account_json('REKSTI/kunci.json')
bucket = storage_client.get_bucket("rekstiphm.appspot.com")
cred = credentials.Certificate('REKSTI/kunci.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


def upload_foto(idp):
    blob = bucket.blob("foto_pasien/"+ idp +"/" + str(datetime.datetime.now()) + '.jpg')
    blob.upload_from_filename(idp+".jpg")

# idp: id pasien
# idrm: id rekam medis suatu pasien

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


def createps(nm,e,br,tg,jk,gd):
    ps_ref=pasien(nm,e,br,tg,jk,gd)
    pasien_ref.document().set(ps_ref)


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


def createrm(gj, pn, tk, t, ds, jn, nm, idp):
    rm_ref=rekam_medis(gj, pn, tk, t, ds, jn, nm)
    pasien_ref.document(idp).collection(u'Rekam Medis').add(rm_ref)


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


pasien_ref = db.collection(u'Pasien')
antrian_ref = db.collection('Antrian')

docs=antrian_ref.get()

for doc in docs:
    a=doc.to_dict()

print(a.keys())
