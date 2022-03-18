# KURAL TABANLI SINIFLANDIRMA İLE POTANSİYEL MÜŞTERİ SEGMENTASYONU ve GETİRİSİ HESAPLAMA #

# ---Kütüphanelerin Import Edilmesi---
import numpy as np
import pandas as pd
import seaborn as sns

# ---Veri Setinin Okunması ve Genel Bilgiler---
df = pd.read_csv("Proje - Potansiyel Musteri Getirisi Hesaplama/persona.csv")
df
df.info() #İki adet nümerik(PRICE, AGE), üç adet kategorik(SOURCE, SEX, COUNTRY) değişken mevcut.
df.shape #(5000,5) boyutunda bir DataFrame
df.head()

# ----------------GOREV1----------------

# Kaç unique SOURCE vardır? Frekansları nedir?
df["SOURCE"].nunique() # 2 farklı unique SOURCE vardır.
df["SOURCE"].unique() # Bunlar android ve ios'dir.

# Kaç unique PRICE vardır?
df["PRICE"].nunique() # 6 farklı unique PRICE vardır.
df["PRICE"].unique() # Bunlar [39, 49, 29, 19, 59, 9] şeklindedir.

# Hangi PRICE'dan kaçar tane satış gerçekleşmiş?
df["PRICE"].value_counts()

# Hangi ülkeden kaçar tane satış olmuş?
df["COUNTRY"].value_counts()

# Ülkelere göre satışlardan toplam ne kadar kazanılmış?
df.groupby("COUNTRY")["PRICE"].sum()

# SOURCE türlerine göre satış sayıları nedir?
df["SOURCE"].value_counts()

# Ülkelere göre PRICE ortalamaları nedir?
df.groupby("COUNTRY")["PRICE"].mean()

# SOURCE'lara göre PRICE ortalamaları nedir?
df.groupby("SOURCE")["PRICE"].mean()

# COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?
df.groupby(["COUNTRY","SOURCE"])["PRICE"].mean()



pd.set_option("display.max_rows",False) # Tüm değerleri görebilmek için ayarlama.
pd.set_option("display.width", 500)
df.groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg({"PRICE":"mean"})



agg_df = df.groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg({"PRICE":"mean"}).sort_values(by="PRICE",ascending=False)

# Index'lerin değişkene çevirme

agg_df.reset_index(inplace = True)

# age değişkenini kategorik değişkene çevirme ve agg_df'ye ekleme

agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"],[0,18,19,23,24,30,31,40,41,70], right=False)

# Seviye tabanlı müşteriler(persona) tanımlama

agg_df["customers_level_based"] = [agg_df["COUNTRY"][index].upper() + "_" + agg_df["SOURCE"][index].upper() + "_" + agg_df["SEX"][index].upper() + "_" + str(agg_df["AGE_CAT"][index]).upper() for index in range(len(agg_df["SEX"]))]

# Gereksiz değişkenler çıkarma

agg_df = agg_df[["customers_level_based", "PRICE"]]

# customers_level_based'e göre groupby işlemi uygulama ve price ortalamaları alma

agg_df = agg_df.groupby("customers_level_based").agg({"PRICE":"mean"}).sort_values(by="PRICE",ascending=False)

# customers_level_based index'ten değişkene çevirme

agg_df = agg_df.reset_index()

# Her bir persona'nın 1 tane olması gerekir

agg_df["customers_level_based"].value_counts()

# Segment adında yeni bir değişken oluşturuldu. Bu değişken'i PRICE değişkeninin kategorik hali gibi düşünebiliriz.

agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels = ["D", "C", "B", "A"])

# Segment değişkeninin Price değişkenine göre betimlenmesi :

agg_df.groupby("SEGMENT").agg({"PRICE":["mean","max","min","sum"]})

# Yeni gelen müşterilere segmentlerine göre sınıflandırma ve getirebileceği geliri tahmin etme
# 33 yaşında ANDROID kullanan bir Türk kadının ait olduğu segmenti bulma
new_user = "TUR_ANDROID_FEMALE_[31, 40)"
agg_df[agg_df["customers_level_based"] == new_user]

# 35 yaşında IOS kullanan bir Fransız kadının ait olduğu segmenti bulma
new_user = "FRA_IOS_FEMALE_[31, 40)"
agg_df[agg_df["customers_level_based"] == new_user]
