from flask import Flask
from flask import request
from flask import Response
from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/scrape')
def scrape():
    search = request.args.get('url')
    
    try:   
        vetor = [] 
        response = requests.get(f"https://www.google.com/search?q={search}&num=5")
        content = BeautifulSoup(response.content, "html.parser")
        contentUrl = content.find_all('a')
         
        index = 0
        
        for link in contentUrl:
            link_href = link.get('href')
            if(index == 5):
                break
            elif "url?q="in link_href and not"webcache"in link_href:
                vetor.append({"url": link.get('href').split("?q=")[1].split("&sa=U")[0], "title": link.text})
                index +=1
            else:
                continue
    except:
        flash('Failed to retrieve URL "%s"' % search, 'danger')
        content = ''
    return render_template('scrape.html', content=vetor)

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True, threaded=True)
