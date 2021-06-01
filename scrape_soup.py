import requests
from bs4 import BeautifulSoup

url = 'https://veganbootcamp.org/course-progress/497/overview-of-dairy'
headers = {
    'authority': 'veganbootcamp.org',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://veganbootcamp.org/login',
    'accept-language': 'en-US,en;q=0.9,es;q=0.8',
    'cookie': 'googtrans=/en/en; googtrans=/en/en; vbcommunity_k=; googtrans=/en/en; _ga=GA1.2.1818705141.1621926329; _fbp=fb.1.1622009394616.990287943; vbcommunity_u=4947; _gid=GA1.2.443184538.1622230205; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6Ii9vTThpQkcveXNmeFVrem9nOFRzQ0E9PSIsInZhbHVlIjoiRFJsMERUZUJOa3JXaGgvNUN3cDBOcDVzQUNsL1FYMzNCaVMvcW9ncDhVTksyWGNjU0V1eFlWM09QWUd4Ump5aDI4UGliKy9odTErdCtrSTYrekRDU3dhNWV0YStmU1R1NWhsdk1GUGFYOUViTzN1QnpXMTROa0pVNmtHQU9FL0pRY0F3QnlXblJ3NlVDZWs5MEczcE8vMlZXTDgyV05Qb2FoZlA0ZFFkczJvPSIsIm1hYyI6IjI4NTYxNWNhMGQ5YjRjM2Q0ZjNhNzE2NTVjNTliNjgzZGMxNjUzZmEyMGFlYjA4MTc0YzBkYWUxODYzNzU0NTAifQ%3D%3D; XSRF-TOKEN=eyJpdiI6IkRzNFd0VHZBNkE5M0dyeGZ6aVVhcWc9PSIsInZhbHVlIjoiV2x1Y3ZLc210QlQrbFRzenhpS0VTM1NaaDBRd2svWFU4TGhuSU5vaVhsUnAveUdscHJnSU9jYXlNTk1SNm80cSIsIm1hYyI6ImU3MzUzODBiYTFmMjM2ZTAwZjM3YjdlZDZkZGYwYWZlMTUxMWI3NGYxOTdmMGQxMGY5ODlmNGJhYjZlOTc1ZDgifQ%3D%3D; vegan_bootcamp_session=eyJpdiI6InBueUVvd1ZxQTVuVkNxYU9Rc0tDV2c9PSIsInZhbHVlIjoicnUzWGNFOFJtSXpCQ3RKdEc0MmNPZmZPd015TEZGak1XTzhucVV4TDlBaHZWcy9RK0oyYkd2Ky85K3pNTGNJViIsIm1hYyI6ImQ0NmEzMDE0YmVkOWQ2MDk5MTA1ZWRhZjhlMjZiMTUxNGZhMzFhNmQ2ZmI5YWZlMWY2NGU3NGNiZTRjYjdkZGMifQ%3D%3D; vbcommunity_sid=a441ec28a294d85bf94c783db34b7c49',
}

response = requests.get(url, headers=headers)
print(response)


# In[7]:


soup = BeautifulSoup(response.content, 'lxml')


# In[8]:


tag = soup.find('b')
tag = tag.text
tag


# In[44]:


course_info = soup.find("div", {"class": "gutenberg__content"})
documents = []
for p in course_info.find_all('p'):
    doc = {}
    doc['tag'] = tag
    doc['text'] = p.text
    doc['description'] = 'lesson'
    doc['url'] = url
    documents.append(doc)


# In[50]:


for quote in course_info.find_all('blockquote'):
    doc = {}
    doc['tag'] = tag
    doc['text'] = quote.text
    doc['description'] = 'quote'
    doc['url'] = url
    documents.append(doc)


# In[53]:


df = pd.DataFrame(documents).tail()


# In[54]:


df.to_json('data.json')

