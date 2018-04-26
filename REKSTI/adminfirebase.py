import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import date, datetime, timedelta
import time
import random
from google.cloud import storage
from collections import Counter
import heapq
import json

# Instantiates a client
storage_client = storage.Client.from_service_account_json('kunci.json')
bucket = storage_client.get_bucket("rekstiphm.appspot.com")
cred = credentials.Certificate('kunci.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
pasien_ref = db.collection('Pasien')
antrian_ref = db.collection('Antrian')


def createid():
    strid = ""
    randid = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
    for j in randid:
        strid += str(j)
    return strid


def upload_foto(idp):
    blob = bucket.blob("foto_pasien/"+ idp +"/" + str(datetime.datetime.now()) + '.jpg')
    blob.upload_from_filename(idp+".jpg")

# idp: id pasien
# idrm: id rekam medis suatu pasien


def pasien(nama, email, tgl, br, tg, jk, gd):
    data = {
        u'Nama': nama,
        u'Email': email,
        u'Tanggal Lahir': tgl,
        u'Berat': br,
        u'Tinggi': tg,
        u'Jenis Kelamin': jk,
        u'Golongan Darah': gd,
    }
    return data


def createps(id, nm, e, tgl, br, tg, jk, gd):
    ps_ref=pasien(nm,e, tgl, br,tg,jk,gd)
    pasien_ref.document(id).set(ps_ref)
    #upload_foto(id)


def rekam_medis(gj, pn, tk, nm, jn, ds, t):
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


def createrm(gj, pn, tk, nm, jn, ds, t, idp):
    rm_ref=rekam_medis(gj, pn, tk, nm, jn, ds, t)
    pasien_ref.document(idp).collection(u'Rekam Medis').add(rm_ref)


def getdatapasien(idp, **par):
    if 'par' in par:
        if par['par'] == 'Nama':
            return pasien_ref.document(idp).get().get("Nama")
        elif par['par'] == 'Email':
            return pasien_ref.document(idp).get().get("Email")
        elif par['par'] == 'Tanggal Lahir':
            return pasien_ref.document(idp).get().get("Tanggal Lahir")
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
    # rekam_ref = pasien_ref.document(idp).collection(u'Rekam Medis')
    if 'idrm' not in kwargs:
        reks = pasien_ref.document(idp).collection(u'Rekam Medis').get()
        for rek in reks:
            return rek.to_dict()
    else:
        reks=pasien_ref.document(idp).collection(u'Rekam Medis').document(kwargs['idrm']).get()
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


def getallpenyakit():
    i=0
    x=[]
    docs=pasien_ref.get()
    for doc in docs:
        rms=doc.reference.collection('Rekam Medis').get()
        for rm in rms:
            x.append(getdatarm(doc.id,idrm=rm.id,par="Penyakit"))
    xx=Counter(x)
    result = [{'name': key, 'value': value} for key, value in xx.items()]
    return result


# print(getallpenyakit())

def ceklastantri():
    global noantri
    antri = antrian_ref.get()
    for doc in antri:
        a=doc.id

    t1=antrian_ref.document(a).get().get("Tanggal").date()
    t2=datetime.now().date()

    if t1 == t2:
        noantri = str(a)
    else:
        noantri = str(int(a)+1)

ceklastantri()

def todayantri():
    return antrian_ref.document(noantri).set({'Tanggal':datetime.now()})


def getantrian():
    return antrian_ref.document(noantri).get().get("No Antri")[:2]


# print(getantrian())

def getlistantripasien():
    antrian = getantrian()
    data={
        'No Antri': []
    }
    for i in antrian:
        data['No Antri'].append(getdatapasien(i)['Nama'])
    return data

# print(getlistantripasien())


def getantrian1():
    return antrian_ref.document(noantri).get().get("No Antri")[:1]


# print(getantrian())

def getlistantripasien1():
    antrian = getantrian1()
    return antrian[0]

# print(getlistantripasien1())

def createantri(idp):
    lastantri = getantrian()
    data={
        'No Antri':[]
    }
    for i in range(len(lastantri)):
        data["No Antri"].append(lastantri[i])
    data["No Antri"].append(idp)
    antrian_ref.document(noantri).update(data)


def delantri():
    lastantri = getantrian()
    data = {
        'No Antri': []
    }
    for i in range(len(lastantri)):
        data["No Antri"].append(lastantri[i])
    data["No Antri"].pop(0)
    antrian_ref.document(noantri).update(data)

# delantri()

def gen_datetime(min_year=1970, max_year=2000):
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()


'''
file = open("Dummy/pasien/nama.csv", "r")
listnama = file.read().splitlines()
file = open("Dummy/pasien/berat.csv", "r")
listberat = file.read().splitlines()
file = open("Dummy/pasien/email.csv", "r")
listemail = file.read().splitlines()
file = open("Dummy/pasien/golongan darah.csv", "r")
listgol = file.read().splitlines()
file = open("Dummy/pasien/jenis kelamin.csv", "r")
listjk = file.read().splitlines()
file = open("Dummy/pasien/tinggi.csv", "r")
listtinggi = file.read().splitlines()

file = open("Dummy/rekam medis/gejala.csv", "r")
listgj = file.read().splitlines()
file = open("Dummy/rekam medis/pengobatan_jenis.csv", "r")
listpj = file.read().splitlines()
file = open("Dummy/rekam medis/pengobatan_nama.csv", "r")
listpn = file.read().splitlines()
file = open("Dummy/rekam medis/penyakit.csv", "r")
listpe = file.read().splitlines()
file = open("Dummy/rekam medis/tindakan.csv", "r")
listti = file.read().splitlines()

# for i in range(50):
#strid = ""
#randid = [213, 55, random.randint(0, 255), random.randint(0, 255)]
#for j in randid:
strid = str(961919286) # 21355249209, 193213199, 130105103, 961919286
nm = random.choice(listnama)
br = int(random.choice(listberat))
em = random.choice(listemail)
gol = random.choice(listgol)
jk = random.choice(listjk)
tg = int(random.choice(listtinggi))

createps(strid, nm, em, gen_datetime(), br, tg, jk, gol)

for j in range(random.randint(1,5)):
    gj = random.choice(listgj)
    pj = random.choice(listpj)
    pn = random.choice(listpn)
    pe = random.choice(listpe)
    ti = random.choice(listti)
    createrm(gj, pe, ti, pn, pj, random.randint(1, 5), gen_datetime(min_year=2008, max_year=2017), strid)
'''

# a = antrian_ref.document('2').get().get("No Antri")

# for aa in a:

# print(a)
# createantri("RKUVA4WJShyrchXw3Z3N")

# docs=antrian_ref.document('RUKPQ2x7ENoVGPlSHTZC').get()

# a = docs.get('No Antri')

# print(a[0])

