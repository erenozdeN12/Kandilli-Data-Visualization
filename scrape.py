from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import csv

driver = webdriver.Chrome()

driver.get('http://www.koeri.boun.edu.tr/scripts/lst8.asp')

pre_element = driver.find_element(By.TAG_NAME, "pre")
data = pre_element.text
lines = data.strip().split('\n')
filtered_lines = []

skip_lines = False
header = []

for line in lines:
    if "..................TÜRKİYE VE YAKIN ÇEVRESİNDEKİ SON DEPREMLER...................." in line:
        skip_lines = True
    elif ".....BÖLGESEL DEPREM-TSUNAMİ İZLEME VE DEĞERLENDİRME MERKEZİ HIZLI ÇÖZÜMLERİ....." in line:  
            skip_lines = True
    elif "......(YAPAY SARSINTI ANALİZİ YAPILMAMIŞTIR) Son 500 deprem listelenmiştir......" in line:  
            skip_lines = True
    elif "                                                        Büyüklük" in line:  
            skip_lines = True
    elif "Tarih      Saat      Enlem(N)  Boylam(E) Derinlik(km)  MD   ML   Mw    Yer                                             Çözüm Niteliği" in line:  
            skip_lines = True
            header = line.split()
    elif "---------- --------  --------  -------   ----------    ------------    --------------                                  --------------" in line:  
            skip_lines = True
    else: 
           skip_lines = False

    if not skip_lines and line.strip():
            filtered_lines.append(line)

with open("veriler.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Tarih', 'Saat', 'Enlem(N)', 'Boylam(E)', 'Derinlik(km)', 'MD', 'ML', 'Mw', 'Yer', 'Çözüm Niteliği'])
    for line in filtered_lines:
        writer.writerow(line.split())
driver.quit()
