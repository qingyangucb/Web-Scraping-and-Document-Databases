from splinter import Browser
from bs4 import BeautifulSoup


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "D:\chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    listings = {}


    # Mars news scrape
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    try:
        listings["headline"] = soup.find("div", class_="content_title").get_text()
        listings["content"] = soup.find("div", class_ = "article_teaser_body").get_text()

    except AttributeError:
        listings["headline"] = None
        listings["content"] = None


    # featured_image scrape
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    feature_click = browser.find_by_id("full_image")
    feature_click.click()

    browser.is_element_present_by_text("more info", wait_time=0.5)
    feature_click = browser.find_link_by_partial_text("more info")
    feature_click.click()
    # spinter browser is able to return a html after you click something on the website from 
    # the original url
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # give me class lede under figure tag, then go to a tag, then go to img tag.
    image_ele = soup.find("figure.lede a img")

    try:
        img_url = image_ele.get('src')
    except AttributeError:
        img_url = None
        listings["featured_image"] = None

    image_url = f"https://www.jpl.nasa.gov{img_url}"
    listings["featured_image"] = image_url


    # Hemisphere scrape
    # to break up long url
    url = (
        "https://astrogeology.usgs.gov/search/"
        "results?q=hemisphere+enhanced&k1=target&v1=Mars"
    )
    browser.visit(url)

    hemi_list = []

    for i in range(4):
        browser.find_by_css("a.product-item h3")[i].click()
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        try:
            hemi_title = soup.find("h2", class_="title").get_text()
            hemi_img = soup.find("a", text="Sample").get("href")
        except AttributeError:
            hemi_title = None
            hemi_img = None

        hemi_list.append([hemi_title, hemi_img])
        
    listings["hemi_list"] = hemi_list
    

    # scrape mars weather from twitter
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    soup = Beautifulsoup(html, "html.parser")
    class_name = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"
    tweet_weather = weather_soup.find("p", class_=class_name)[0].get_text()
    listings["tweet_weather"] = tweet_weather



    # scrape mars fact
    # you don't need splinter browser object to use pandas.read_html, cool.
    try:
        df = pd.read_html("http://space-facts.com/mars/")[0]
    except BaseException:
        df = None

    df.columns = ["description", "value"]
    df.set_index("description", inplace=True)
    listings['df'] = df

    return listings