import requests
from bs4 import BeautifulSoup
import pandas

url="https://www.halooglasi.com/nekretnine/prodaja-stanova/jagodina?page="
lista_oglasa=[]  #lista u kojoj smestamo sve podatke koje smo pokupili iz svih oglasa
page=0

while True:
    page+=1
    r=requests.get(url+str(page))
    c=r.content

    #izvlacenje html koda stranice
    soup=BeautifulSoup(c,'html.parser')

    #izvlacenje html koda unutar kog se nalaze podaci vezani za pojedinacne top oglase
    top_ads=soup.find_all("div",{"class":"product-item product-list-item Top real-estates my-product-placeholder"})

    #izvlacenje html koda unutar koga se nalaze ostali oglasi(nisu u top sekciji na vrhu)
    regular_ads= soup.find_all("div",{"class":"product-item product-list-item Standard real-estates my-product-placeholder"})
    
    #if statement je koriscen kako bi se while loop prekinuo na prvoj praznoj strani na kojoj nema oglasa
    if regular_ads!=[]:
        
        #IZVLACENJE PODATAKA IZ TOP OGLASI SEKCIJE

        for index in range(len(top_ads)):
            top_ads_dict={}  #dict u kome smestamo podatke vezane za pojedinacne oglase
            #naslov oglasa
            top_ads_dict["Naslov"]=top_ads[index].find("h3",{"class","product-title"}).text

            #lokacija
            location_data=top_ads[index].find_all("ul",{"class","subtitle-places"})[0]
            data_list=[]
            for item in location_data.find_all("li"):
                data_list.append(item.text)

            #mesto
            top_ads_dict["Mesto"]=data_list[0].replace("\xa0","")

            #gradska lokacija
            try:
                top_ads_dict["Gradska lokacija"]=data_list[-1].replace("\xa0","")
            except:
                top_ads_dict["Gradska lokacija"]=None

            inner_apa_data=top_ads[index].find_all("div",{"class":"value-wrapper"})
            inner_apa_data_list=[]
            for item in inner_apa_data:
                inner_apa_data_list.append(item.text)

            #ukupna povrsina stana
            top_ads_dict["Povrsina stana"]=inner_apa_data_list[0].replace("\xa0m2Kvadratura","m2")

            #broj soba
            top_ads_dict["Broj soba"]=inner_apa_data_list[1].replace("\xa0Broj soba","")

            #spratnost
            try:
                top_ads_dict["Spratnost"]=inner_apa_data_list[2].replace("\xa0Spratnost","")    
            except:
                top_ads_dict["Spratnost"]=None

            #Cena stana
            top_ads_dict["Cena nekretnine"]=top_ads[index].find("div",{"class":"central-feature"}).text.replace("\xa0","")

            #cena po kvadratu
            top_ads_dict["Cena po kvadratu"]=top_ads[index].find("div",{"class":"price-by-surface"}).text

            #oglasivac
            top_ads_dict["Oglasivac"]=top_ads[index].find("span",{"class":"basic-info"}).text.upper().replace("\xa0","")


            lista_oglasa.append(top_ads_dict)



        #IZVLACENJE PODATAKA IZ OGLASA KOJI NISU UNUTAR TOP SEKCIJE

        for index in range(len(regular_ads)):

            reg_ads_dict={}  #dict u kome smestamo podatke vezane za pojedinacne oglase koji nisu u top sekciji

            #naslov oglasa
            reg_ads_dict["Naslov"]=regular_ads[index].find("h3",{"class","product-title"}).text

            #lokacija
            location_data=regular_ads[index].find_all("ul",{"class","subtitle-places"})[0]
            data_list=[]
            for item in location_data.find_all("li"):
                data_list.append(item.text)

            #mesto
            reg_ads_dict["Mesto"]=data_list[0].replace("\xa0","")

            #gradska lokacija
            reg_ads_dict["Gradska lokacija"]=data_list[-1].replace("\xa0","")

            inner_apa_data=regular_ads[index].find_all("div",{"class":"value-wrapper"})
            inner_apa_data_list=[]
            for item in inner_apa_data:
                inner_apa_data_list.append(item.text)

            #ukupna povrsina stana
            reg_ads_dict["Povrsina stana"]=inner_apa_data_list[0].replace("\xa0m2Kvadratura","m2")

            #broj soba
            reg_ads_dict["Broj soba"]=inner_apa_data_list[1].replace("\xa0Broj soba","")

            #spratnost
            try:
                reg_ads_dict["Spratnost"]=inner_apa_data_list[2].replace("\xa0Spratnost","")
            except:
                reg_ads_dict["Spratnost"]=None

            #Cena stana
            reg_ads_dict["Cena nekretnine"]=regular_ads[index].find("div",{"class":"central-feature"}).text.replace("\xa0","")

            #cena po kvadratu
            reg_ads_dict["Cena po kvadratu"]=regular_ads[index].find("div",{"class":"price-by-surface"}).text

            #oglasivac
            reg_ads_dict["Oglasivac"]=regular_ads[index].find("span",{"class":"basic-info"}).text.upper().replace("\xa0","")

            lista_oglasa.append(reg_ads_dict)
        
    else:
        break
#Podatke iz liste otpremamo u pandas dataframe(tabelu)
df=pandas.DataFrame(lista_oglasa)
#export tabele u csv doc
df.to_csv("output.csv")
