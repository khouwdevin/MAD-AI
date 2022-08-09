from django.shortcuts import render
from django.http import HttpResponse
from django import forms
import json
from json import dumps
# Create your views here.

import tensorflow as tf
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from . import model_prediction
import pickle

def push_to_talk():
    import speech_recognition as sr
    r = sr.Recognizer()
    with sr.Microphone() as source: #buat aktifin microfon
        print('Say something into the microphone')
        audio = r.listen(source,timeout= 3, phrase_time_limit= 10)
    try: #try except kalo misal audio nya ga jelas
        text = r.recognize_google(audio, language='id') #buat ngubah voice ke tulisan
    except sr.UnknownValueError:
        print('Audio unintelligible')
    except sr.RequestError as e:
        print("Cannot obtain result: {0}".format(e))
    return text

def prediction_process(input_from_user):
    disease_temp = input_from_user
    #untuk modelnya ai
    data = pd.read_csv(r'D:\AABinus\ProjectAIMAD\mywebsite\checking\Penyakit.csv')

    tags_split = [tags.split(',') for tags in data['Penyakit'].values]

    tag_encoder = MultiLabelBinarizer()
    tag_encoder.fit_transform(tags_split)

    classifier = model_prediction.CustomModelPrediction.from_path(r'D:\AABinus\ProjectAIMAD\mywebsite\checking')
    results = classifier.predict(disease_temp)

    disease_grup = [0, 1]

    for i in range(len(results)):
        for idx,val in enumerate(results[i]):
            if val > disease_grup[0]:
                disease_grup[0] = val
                disease_grup[1] = tag_encoder.classes_[idx]
    if disease_grup[0] < 0.5:
        prediction_ai = 'Prediksi kami adalah %s dan disarankan langsung ke dokter karena akurasi prediksi kecil.' %disease_grup[1]
        #prediction_ai = 'Prediksi penyakit Anda adalah %s, dengan tingkat akurasi %.2f%s' %(disease_grup[1], disease_grup[0] * 100, '%')
    else:
        prediction_ai = 'Prediksi penyakit Anda adalah %s, dengan tingkat akurasi %.2f%s' %(disease_grup[1], disease_grup[0] * 100, '%')
    #yg {'data': disease_temp} untuk disease_tempnya diganti sama hasil ainya
    return prediction_ai

def checking(request):
    awal = 'Selamat datang, keluhan apa yang hendak disampaikan?'
    if request.method == 'POST':
        if request.POST.get("speech_input"):
            input_from_user = []
            a = str(push_to_talk())
            input_from_user.append(a)
            prediction_ai = prediction_process(input_from_user)
        else:
            input_from_user = request.POST.getlist('chat')
            prediction_ai = prediction_process(input_from_user)
        return render(request, 'ChatBotPage.html', {'data': prediction_ai})
    return render(request, 'ChatbotPage.html', {'data': awal})