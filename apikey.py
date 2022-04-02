import requests
import telegram_send
import time
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

sommaInizialeInvestitaEth = 32775.51163 #30504.48163
sommaInizialeInvestitaAda = 2050
bloccatiEarnEth = 3.85078471          #scadenza 24/02522
bloccatiEarnEthFlexible = 0   #scadenza 23/02/22
bloccatiEarnUsdt = 2250               #scadenza 27/02/22
detenutiEth = 11.37546975
detenutiAda = 940.452545

headers_ = {
    'X-CMC_PRO_API_KEY': '68cee308-f641-4813-9d0b-57ef7a6e7846',
    'Accepts' : 'application/json'
}

params_ = {
    'start' : '1',
    'limit' : '10',
    'convert' : 'EUR'
}

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

def calcoloGuadagno(CryptoAcquired, CryptoInvested, Currency, CryptoPrice, time):
    CryptoAcquistati=CryptoAcquired
    CryptoInvestiti=CryptoInvested
    CryptoSaldoAttuale=CryptoPrice*CryptoAcquistati
    
    print('Saldo '+Currency+str(round(CryptoSaldoAttuale,2)))
    CryptoGuadagnoAttuale=CryptoSaldoAttuale-CryptoInvestiti
    print('Guadagno '+Currency+str(round(CryptoGuadagnoAttuale,2)))
    #plt.scatter(10,CryptoGuadagnoAttuale)
    #plt.pause(0.05)
    
    
    #if Currency=='ETH ' and CryptoGuadagnoAttuale <2000:
    telegram_send.send(messages=['\n'+time+'\n'+Currency+' investiti: '+str(round(CryptoInvestiti,2))+'\n'+Currency+' acquistati: '+str(round(CryptoAcquistati,2))+'\nSaldo: '+Currency+': '+str(round(CryptoSaldoAttuale,2))+'\nGuadagno da '+Currency+': '+str(round(CryptoGuadagnoAttuale,2))])
    #if Currency=='ADA ' and CryptoGuadagnoAttuale <50:
    #telegram_send.send(messages=['\n'+time+'\n'+Currency+' investiti: '+str(CryptoInvestiti)+'\n'+Currency+' acquistati: '+str(CryptoAcquistati)+'\nSaldo attuale'+Currency+': '+str(CryptoSaldoAttuale)+'\nGuadagno attuale da '+Currency+': '+str(CryptoGuadagnoAttuale)])
    return CryptoGuadagnoAttuale

def calcoloCryptoEarn(CryptoBlocked, Percentage, CryptoPrice):
    earnAmountinCrypto = ((CryptoBlocked/100)*Percentage)/12  #AMOUNT MENSILE
    EarningAmount = earnAmountinCrypto*CryptoPrice
    return round(EarningAmount,2)


while True:
    json = requests.get(url, params=params_, headers=headers_).json()
    coins=json['data']

    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M)")

    #print(timestampStr)
    for x in coins:
        if x['symbol']=='ETH':
            ethPrice=x['quote']['EUR']['price']
            print(timestampStr)
            print('##################### ETH #####################')
            print('Valore '+x['symbol'],x['quote']['EUR']['price'])
            guadEth = calcoloGuadagno( detenutiEth, sommaInizialeInvestitaEth, 'ETH ' , ethPrice, timestampStr) #11.33590781 + 0.03956194 (di earn)
            #CRYPTO.COM EARN
            print('\n##################### (EARN ETH mese) ######################')
            guadEarningETH = calcoloCryptoEarn(bloccatiEarnEth, 5.5, ethPrice)
            guadEarningETHFlexible= calcoloCryptoEarn(bloccatiEarnEthFlexible, 3.5, ethPrice)
            print(str(round(guadEarningETH + guadEarningETHFlexible,2)))
        if x['symbol']=='ADA':
            adaPrice=x['quote']['EUR']['price']
            print('\n##################### ADA #####################')
            print('\nValore '+x['symbol'],x['quote']['EUR']['price'])
            guadAda = calcoloGuadagno( detenutiAda, sommaInizialeInvestitaAda, 'ADA ', adaPrice, timestampStr)
        if x['symbol']=='USDT':
            usdtPrice=x['quote']['EUR']['price']
            guadEarningUSDT = calcoloCryptoEarn(bloccatiEarnUsdt, 10, usdtPrice)
            print('##################### (EARN USDT mese) #####################')
            print(guadEarningUSDT)
    guadTot = guadAda + guadEth
    guadEarnTot = str(round(guadEarningUSDT + guadEarningETH + guadEarningETHFlexible,2))
    totInvestiti = sommaInizialeInvestitaEth + sommaInizialeInvestitaAda
    print('\n-----------------------------------------------------------------------------')
    print('Somma iniziale investita: '+ str(round(sommaInizialeInvestitaEth+sommaInizialeInvestitaAda,2)))
    print('Guadagno totale (senza earn): '+ str(round(guadTot,2)))
    print('Rendita passiva (earn) al mese: '+ guadEarnTot ) 
    print('Totale (investito + guadagno): ' + str(round(totInvestiti+guadTot,2)))
    print('Totale con valore 1 gennaio (solo ETH e senza earn): ' + str(round(detenutiEth*3305.7,2))) #3305.7 euro è il valore MAX di ETH al 01/01/2022 (secondo Market Cap)
    print('-----------------------------------------------------------------------------\n')
    #plt.show()
    time.sleep(500)
