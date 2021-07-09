import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from CoolProp.HumidAirProp import HAPropsSI as lucht
koelen = []
verwarmen = []
temp = []

temp_uit = 18 #streeftemperatuur
RH_in = 0.7 #relatief in %
RH_uit = 0.7 #relatief uit %
debiet = 29400 #m3/h
referentie_jaar = "2018"

date_cols = ["DATE"]
weer = pd.read_csv("weerdatapunten.csv", index_col='DATE', parse_dates=date_cols)
periode = weer.loc[f'{referentie_jaar}-04-01 0:00:00':f'{referentie_jaar}-09-29 23:00:00']
lijst = periode.values.tolist()

def vermogen_koelblok(temp_in_c, temp_uit_c, RH_in, debiet, RH_uit):
    temp_in = temp_in_c + 273
    temp_uit = temp_uit_c + 273
    volumestroom = debiet/3600
    h_in = lucht('H','T',temp_in,'P',101300,'R',RH_in)
    dauwpunt = lucht('D', 'T', temp_in, 'P', 101325, 'R', RH_in)
    w_in = lucht('W','T',temp_in,'P',101325,'R',RH_in)
    w_uit = lucht('W', 'T', temp_uit, 'P', 101325, 'R', RH_uit)
    h_uit = lucht('H','T',temp_uit,'P',101325,'R',RH_uit)
    koel_kg = h_in - h_uit
    kg_m3 = (1/lucht('Vda','T',temp_in,'P',101325,'R',RH_in))
    return (kg_m3*koel_kg*volumestroom)/1000

def verbruik(l):
  verbruik = 0
  for val in l:
    verbruik = verbruik + val
  return verbruik

def plot_grafiek(koelen, temp):
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Tijd in uren')
    ax1.set_ylabel('koelvermogen [kW]', color=color)
    ax1.plot(koelen, label='koelvermogen', color=color)
    ax1.tick_params(axis='y')
    ax2 = ax1.twinx()

    color = 'tab:blue'
    ax2.set_ylabel('Buiten temperatuur in graC', color=color)
    ax2.plot(temp, label='buiten temp', color=color)
    ax2.tick_params(axis='y')

    fig.tight_layout()
    plt.legend()
    plt.show()

def vermogen_berekenen(lijst):
    for x in lijst:
        RH = x[1] / 100
        print(x[0])
        temp.append(x[0])
        vermogen = round(vermogen_koelblok(x[0], temp_uit, RH, debiet, RH_uit), 3)
        print(vermogen)
        if vermogen < 0:
            vermogen = 0
        koelen.append(vermogen)
    return koelen

def verbruik_max_koelvermogen(koelen):
    print("Uitkomsten")
    print("verbruik:")
    print(str(verbruik(koelen)) + " kWh")
    print("maximaal koelvermogen:")
    print(str(max(koelen)) + " kW")

vermogen_berekenen(lijst)
verbruik_max_koelvermogen(koelen)
plot_grafiek(koelen, temp)
