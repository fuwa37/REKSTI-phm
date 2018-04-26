from flask import Flask
import adminfirebase as af
import selenium.webdriver as webdriver

app = Flask(__name__)

browser = webdriver.Firefox(executable_path=r'geckodriver.exe')
iptarget = "http://192.168.43.150:5000/antrian"

@app.route('/<id>')
def antrian(id):
    af.createantri(id)
    browser.get(iptarget)

app.run(host='0.0.0.0', port=5000)
