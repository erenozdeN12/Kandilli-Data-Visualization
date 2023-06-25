from flask import Flask, render_template, redirect 
import csv
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    data = read_csv_file('veriler.csv')

    locations = extract_locations(data)
    derinlik_ml_yer = extract_derinlik_ml_yer(data)
    son_depremler = derinlik_ml_yer[:10] 

    return render_template('harita.html', locations=locations, derinlik_ml_yer=derinlik_ml_yer, son_depremler=son_depremler)

@app.route('/yenile')
def yenile_veriler():
    subprocess.run(['python', 'scrape.py'])  
    return redirect('/')

def read_csv_file(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    return data

def extract_locations(data):
    locations = []
    for row in data[1:]:
        enlem = float(row[2])
        boylam = float(row[3])
        locations.append((enlem, boylam))
    return locations

def extract_derinlik_ml_yer(data):
    derinlik_ml_yer = []
    for row in data[1:]:
        tarih = row[0]
        saat = row[1]
        derinlik = float(row[4])
        ml = float(row[6])
        yer = row[8]
        cozum = row[9]
        if yer == '-.-':
            yer = 'Bilinmiyor'
        derinlik_ml_yer.append((tarih, saat, derinlik, ml, yer))
    return derinlik_ml_yer

if __name__ == '__main__':
    app.run(debug=True)
