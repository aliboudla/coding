#!/usr/bin/env python
#-*- coding:utf-8 -*-
# coding: UTF-8



from flask import Flask, request,render_template
import json
import requests
import datetime


app = Flask(__name__)

@app.route('/language_extract/')
def language_extract():
    git_data=[]
    languages_count={}
    gitdata={}
    date= str(datetime.date(2020, 1, 25))
    
    resp= requests.get(("https://api.github.com/search/repositories?q=created:>{}&sort=stars&order=desc&per_page=100").format(date))
    json_object= resp.json()
    
    # Extract fields from Json object
    
    for r in json_object["items"]:
       
        gitdata={
            'date_c': r["created_at"],
            'name': r["name"],
            'language': r["language"],
        }
        
        if gitdata["language"]==None:
           gitdata["language"]="unspecified"

        language=gitdata["language"]

        #// Count the same laguage

        if language in languages_count:
           languages_count[language]=languages_count[language]+1
           
        else:
           languages_count[language]=1
        #print (gitdata)
        git_data.append(gitdata)

    return render_template('language.html', titre="Number of languages and repositories", git_data=git_data,languages_count=languages_count)
if __name__ == '__main__':
    app.run()
