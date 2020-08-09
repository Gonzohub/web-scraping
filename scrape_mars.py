
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import pymongo

def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless = False)

    #important variables saved in this assignment
    '''
    news_title
    news_p
    featured_image_url
    tweet
    mars_facts
    hemis_urls
    '''

    mars_url = 'https://mars.nasa.gov/news/'
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    twt_url = 'https://twitter.com/marswxreport?lang=en'
    facts_url = 'https://space-facts.com/mars/'
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(mars_url)
    time.sleep(2)

    html = browser.html
    soup = bs(html, 'html.parser')
    #scraping NASA Mars News for newest article
    news_title = soup.select('div.content_title > a')[0].text
    news_p = soup.select('div.article_teaser_body')[0].text


    #visiting JPL webpage
    #jpl_link is used for str concatenation after finding img link
    browser.visit(jpl_url)
    img_html = browser.html
    time.sleep(2)
    soup = bs(img_html, 'html.parser')
    jpl_link = 'https://www.jpl.nasa.gov'


    #locating tag with featured img
    foot_tag = soup.find('footer')


    img_link = foot_tag.contents[1]['data-fancybox-href']


    featured_image_url = jpl_link + img_link
    #featured_image_url
    browser.visit(featured_image_url)


    browser.visit(twt_url)
    time.sleep(3)


    html_weather = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html_weather, 'html.parser')

    # Find all elements that contain tweets
    tweets = soup.select("div.css-1dbjc4n > article")[0].text


    tweet = tweets[32:]


    browser.visit(facts_url)
    time.sleep(3)



    html_facts = browser.html
    soup = bs(html_facts, 'html.parser')
    facts= soup.find('table')


    mars_facts = facts.text


    browser.visit(hemi_url)
    html_hemi = browser.html
    time.sleep(4)
    soup = bs(html_hemi, 'html.parser')


    results = soup.find('div', class_='collapsible results')
    hemis=results.find_all('a')
    hemis_urls=[]
    for hemi in hemis:
        if hemi.h3:
            title = hemi.h3.text
            next_ = hemi["href"]
            browser.visit("https://astrogeology.usgs.gov/" + next_)
            time.sleep(3)
            soup = bs(browser.html, 'html.parser')
            hemisphere2 = soup.find("div",class_= "downloads")
            img=hemisphere2.ul.a["href"]
            hemisphere_dict={}
            hemisphere_dict['title']=title
            hemisphere_dict["image_url"]=img
            hemis_urls.append(hemisphere_dict)


    cloud_data = [{
    "NewsTitle": news_title,
    "NewsParagraph": news_p,
    "featuredImage": featured_image_url,
    "tweets": tweet,
    "marsFacts": mars_facts,
    "pictureUrls": hemis_urls
    }]

    conn = "mongodb+srv://PrivateUser:dw765svWVsSWbsQavfhH@missiontomars.33wx7.mongodb.net/<dbname>?retryWrites=true&w=majority"
    client = pymongo.MongoClient(conn)
    db = client.mars
    mars_data = db.mars_data

    mars_data.insert_many(cloud_data)
    
    return cloud_data









