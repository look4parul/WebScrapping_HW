import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from splinter import browser
from selenium import webdriver
import urllib.request

# Create a dict for mars data collected using web scrapping
#mars_facts_data = {}

## NASA MARS NEWS
def scrape():
    # Create a dict for mars data collected using web scrapping
    mars_results = {}
    url = "https://mars.nasa.gov/news"
    driver = webdriver.Firefox()
    driver.get(url)
    html = driver.page_source
    # Scrape the webpage using beautiful soup
    soup = bs(html, 'html.parser')
    # Latest title and remove the new line 
    news_title = soup.find('div', class_ = 'content_title').get_text(strip=True)
    # print("News Title: ", news_title)
    # Latest Paragraph
    news_p = soup.find('div', class_ = 'article_teaser_body').get_text()
    #latest_news={"title":news_title,"text":news_p}
    mars_results["News_title"] = news_title
    mars_results["News_p"] = news_p
    ######################################################################################
    # #### Featured Image
    ######################################################################################
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    # Retrieve page with the requests module
    response = requests.get(image_url)
    soup = bs(response.text, 'html.parser')
    featured_url = soup.find("article", class_="carousel_item")["style"]
    featured_url = featured_url.strip("background-image: url('")
    featured_url = featured_url.strip("');")
    print("featured_url: "+featured_url)
    featured_image_url = "https://www.jpl.nasa.gov" + featured_url
    mars_results["featured_image_url"] = featured_image_url
    
    ######################################################################################
    #### Latest_weather
    ######################################################################################
    weather_url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(weather_url)
    driver = webdriver.Firefox()
    driver.get(weather_url)
    html = driver.page_source
    soup = bs(response.text, 'html.parser')
    # Extract the tweet text
    mars_weather = soup.find(class_='tweet-text').text
    mars_results["mars_weather"] = mars_weather
    
    ######################################################################################
    #### Mars Facts
    ######################################################################################
    facts_url = "http://space-facts.com/mars/"
    data = pd.read_html(facts_url)
    df = data[0]
    #df.columns = ["Mars-Earth Comparison", "Mars", "Earth"]
    df.columns = ["Fact","Value"]
    # Get rid of trailing colon
    df["Fact"] = df["Fact"].str[:-1]
    df = df.set_index("Fact")
    print(df)

    facts_html_table = df.to_html()
    facts_html_table = facts_html_table.replace('\n', '')
    #mars_facts = df.to_html()
    #facts_dict = dict(mars_facts)
    #print(mars_facts)
    mars_results['facts_html_table'] = facts_html_table
    
    ######################################################################################
    #### Hemisphere_info
    ######################################################################################
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    response = requests.get(hemisphere_url)
    soup = bs(response.text, 'html.parser')
    hemi_img_url_list = []
    title = []
    for item in soup.select("a.itemLink"):
        title.append(item.select("h3")[0].get_text())
        url_new = "https://astrogeology.usgs.gov"+item["href"]
        response_new = requests.get(url_new)
        soup_new = bs(response_new.text, 'html.parser')
        hemi_img_url_list.append("https://astrogeology.usgs.gov"+soup_new.select('img.wide-image')[0]['src'])
        hemisphere_image_urls = [{"Title":title[i],'img_url':hemi_img_url_list[i]} for i in range(len(title))]
        
    mars_results["hemisphere_image_urls"] = hemisphere_image_urls
    return mars_results
    #hemisphere_image_urls

# #Now we put all the data into Mongo:

#             # Initialize PyMongo to work with MongoDBs
#             # conn = 'mongodb://localhost:27017'
#             # conn="mongodb://heroku_dxww20g1:2m85ei2jvb8o3u8j6r994d8rqh@ds263791.mlab.com:63791/heroku_dxww20g1"
            


#     str0=os.environ.get("MONGODB_URI")
#             # str0="mongodb://heroku_dxww20g1:2m85ei2jvb8o3u8j6r994d8rqh@ds263791.mlab.com:63791/heroku_dxww20g1"
#     print("str0=",str0)
#     str1=str0.split('/');str1.pop;Mars_db=str1[-1];
#     print("str1=",str1)
#     str0='/'.join(str1)
           

#     conn=str0
#     client = pymongo.MongoClient(conn)

            
#             # Define database and collection
#             # client.drop_database('Mars_db')
#             # db = client.Mars_db

#     client.drop_database(Mars_db)
#     db = client[Mars_db]


#             # collection = db.Mars_hemisphere_image_urls
#             # collection.drop()
#             # collection.insert_many(hemisphere_image_urls)
#             # results=collection.find()
#             # results=[result for result in results]
#             # results

#     collection = db.Mars_facts_dict
#     collection.drop()
#     collection.insert_one(facts_dict)
#     results=collection.find()
#     results[0]

            

#     collection = db.Mars_weather
#     collection.drop()
#     collection.insert_one({"mars_weather":mars_weather})
#     results=collection.find()
#     results[0]

#     collection = db.Mars_latest_news
#     collection.drop()
#     collection.insert_one(latest_news)
#     results=collection.find()
#     results[0]

#     collection = db.Mars_featured_image_url
#     collection.drop()
#     collection.insert_one({"featured_image_url":featured_image_url})
#     results=collection.find()
#     results[0]
#     client.close()

#     return None
