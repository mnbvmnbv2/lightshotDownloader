import re
import io
from requests_html import HTMLSession
import shutil
from bs4 import BeautifulSoup
import nest_asyncio

if __name__ == "__main__":
    with io.open("bookmarks.html",'r',encoding='utf8') as f:
        bookmarks = f.read()
        links = re.findall("http://prntscr.com/[a-zA-z0-9]+|http://prnt.sc/[a-zA-z0-9]+", bookmarks)
        print(len(links))

    i = 0
    for link in links:
        i += 1
        nest_asyncio.apply()

        session = HTMLSession()
        r = session.get(link)

        html_str = r.text
        soup = BeautifulSoup(html_str, 'html.parser')
        imgLink = re.findall("i.imgur.com/[a-zA-z0-9]+.png|i.imgur.com/[a-zA-z0-9]+.jpg|image.prntscr.com/image/[a-zA-z0-9]+.png|image.prntscr.com/image/[a-zA-z0-9]+.jpg", str(soup))
        if len(imgLink) > 0:
            print(i,imgLink[0])
            image_url = "http://"+imgLink[0]+"?"

            filename = 'pictures/'+str(i)+".png"

            session = HTMLSession()
            r = session.get(image_url, stream = True)

            if r.status_code == 200:
                r.raw.decode_content = True

                with open(filename,'wb') as f:
                    shutil.copyfileobj(r.raw, f)