from bs4 import BeautifulSoup
import requests
from flask import Flask
from flask import request
app = Flask(__name__)
import json
from flask_cors import CORS, cross_origin
CORS(app)

#deploued api
#https://google-get-trending-netflix.herokuapp.com/netflixToday
def getMovieUrl(language):
    url_hindi = "https://timesofindia.indiatimes.com/entertainment/hindi/bollywood/news"
    url_english="https://timesofindia.indiatimes.com/entertainment/english/hollywood/news"
    if language=="en":
        url=url_english
    else:
        url=url_hindi
    
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "html.parser")
    special_divs = soup.find("div", {"id": "mainlisting"})
    special_anchors=special_divs.find_all("a", href = True)
    #print(special_anchors)
    finalData=[]
    for text in special_anchors:
       
       link="https://timesofindia.indiatimes.com"+text['href']
       
       msg=text.text
       for img in text('img'):
           image_src=img['src']
           image_src=image_src.replace("width-134,height-99","width-500,height-350")
           
       returnData={
            "link":link,
            "msg":msg,
            "image_src":image_src
           }
       finalData.append(returnData)
    finalData.pop()

    finalData2=[]
    for f in finalData:
        print(f)
        if f["msg"]=="":
            continue
        else:
            finalData2.append(f)
    return finalData2

           

@app.route('/hollyBollyToday', methods=['GET'])
def loadData():
    language=request.args.get('language')
    finalData=getMovieUrl(language)
    return json.dumps({"data": finalData})    

@app.route('/', methods=['GET'])
def getData():
    return json.dumps({"msg": "hello"})

if __name__ == '__main__':
    app.run()
    
        
