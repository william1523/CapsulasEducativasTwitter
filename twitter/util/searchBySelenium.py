from random import randint
from typing import Union
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from urllib.parse import quote
import time
import logging
import pickle
from .element_finder import Finder
import random

logger = logging.getLogger(__name__)
format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch = logging.StreamHandler()
ch.setFormatter(format)
logger.addHandler(ch)

class searchBySelenium:
    
    def __init__(self,usr,pwd):
        self.usr=usr
        self.pwd=pwd
        self.tweets_count = 10
        self.posts_data = {}
        self.retry = 1
        self.cookies_file_path="cookies.pkl"
        # list of websites to reuse cookies with
        self.cookies_websites=["https://twitter.com/home"]
        self.start_driver()

    def start_driver(self):
        opt = webdriver.ChromeOptions()
        opt.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=opt)
        try:
            # load cookies for given websites
            cookies = pickle.load(open(self.cookies_file_path, "rb"))
            for website in self.cookies_websites:
                self.driver.get(website)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
                self.driver.refresh()
        except Exception as e:
            # it'll fail for the first time, when cookie file is not present
            print(str(e))
            print("Error loading cookies")

    def close_driver(self):
        self.driver.close()
        self.driver.quit()
    def save_cookies(self):
        # save cookies
        cookies = self.driver.get_cookies()
        pickle.dump(cookies, open(self.cookies_file_path, "wb"))

    def close_all(self):
        # close all open tabs
        if len(self.driver.window_handles) < 1:
            return
        for window_handle in self.driver.window_handles[:]:
            self.driver.switch_to.window(window_handle)
            self.driver.close()

    def quit(self):
        self.save_cookies()
        self.close_all()
        self.driver.quit()
    
    def is_tweeter_logged_in(self):
        self.driver.get("https://twitter.com/home")
        self.wait_until_completion
        print(self.driver.title)
        if 'https://twitter.com/home' in self.driver.current_url:
            return True
        else:
            return False
        
    def loginTwitter(self):
        self.start_driver()
        #aqui implementar autenticacion
        self.driver.get('https://twitter.com/login?lang=es')
        self.wait_until_completion(self.driver)
        time.sleep(20)
        winHandls=self.driver.window_handles
        self.driver.switch_to.window(winHandls[0]) 
        #original_window = self.driver.current_window_handle
        caja_busqueda = self.driver.find_element(
            By.XPATH, "//input[@type='text']"
            )
        caja_busqueda.send_keys(self.usr)
        caja_busqueda.send_keys(Keys.ENTER)
        self.wait_until_completion(self.driver)
        time.sleep(5)
        caja_password = self.driver.find_element(
            By.XPATH, "//input[@type='password']"
        )
        caja_password.send_keys(self.pwd)
        caja_password.send_keys(Keys.ENTER)
        self.wait_until_completion(self.driver)
        self.save_cookies()
        
    def searchTweets(self, keyword:str, tweets_count:int, recientes:bool):
        self.tweets_count=tweets_count
        self.driver.execute_script("document.body.style.zoom='70%'")
        if not self.is_tweeter_logged_in():
            self.loginTwitter()
        target_url = self.url_generator(keyword=keyword)
        if recientes:
            target_url = target_url + "&f=live"
        self.driver.get(target_url)
        self.wait_until_completion(self.driver)
        
        self.wait_until_tweets_appear(self.driver)
        self.fetch_and_store_data()
        data = dict(list(self.posts_data.items())
                    [0:int(self.tweets_count)])
        return data
    
    def exploreTweet(self, url:str,tweets_count:int):
        self.posts_data = {}
        self.retry = 1
        self.tweets_count=tweets_count
        target_url = url
        print(target_url)
        self.driver.get(target_url)
        self.wait_until_completion(self.driver)
        self.wait_until_tweets_appear(self.driver)
        self.fetch_and_store_data()
        data = dict(list(self.posts_data.items())
                    [0:int(self.tweets_count)])
        return data



    
    
    

    
    
    def url_generator(self,keyword: str, since: Union[int, None] = None, until: Union[str, None] = None,
                      since_id: Union[int, None] = None, max_id: Union[int, None] = None,
                      within_time: Union[str, None] = None) -> str:
        """Generates Twitter URL for passed keyword

        Args:
            keyword (str): Keyword to search on twitter.
            since (Union[int, None], optional): Optional parameter,Since date for scraping,a past date from where to search from. Format for date is YYYY-MM-DD or unix timestamp in seconds. Defaults to None.
            until (Union[str, None], optional): Optional parameter,Until date for scraping,a end date from where search ends. Format for date is YYYY-MM-DD or unix timestamp in seconds. Defaults to None.
            since_id (Union[int, None], optional): After (NOT inclusive) a specified Snowflake ID. Defaults to None.
            max_id (Union[int, None], optional): At or before (inclusive) a specified Snowflake ID. Defaults to None.
            within_time (Union[str, None], optional): Search within the last number of days, hours, minutes, or seconds. Defaults to None.

        Returns:
            str: Twitter URL
        """
        base_url = "https://twitter.com/search?q="
        if within_time is None:
            words = [self.set_value_or_none(since, "since:"),
                     self.set_value_or_none(
                until, "until:"),
                self.set_value_or_none(
                since_id, "since_id:"), self.set_value_or_none(max_id, "max_id:")]
            query = ""
            for word in words:
                if word is not None:
                    query += word
            query += keyword
            query = quote(query)
            #base_url = base_url + query + "&src=typed_query&f=live"
            base_url = base_url + query + "&src=typed_query"
        else:
            word = self.set_value_or_none(
                within_time, "within_time:")
            query = keyword + " " + word
            #base_url = base_url + quote(query) + "&src=typed_query&f=live"
            base_url = base_url + quote(query) + "&src=typed_query"
        return base_url

    def wait_until_completion(self,drivera) -> None:
        """waits until the page have completed loading"""
        try:
            state = ""
            while state != "complete":
                time.sleep(randint(3, 5))
                state = drivera.execute_script("return document.readyState")
        except Exception as ex:
            logger.exception('Error at wait_until_completion: {}'.format(ex))
    
    def wait_until_tweets_appear(self,driver):
        """Wait for tweet to appear. Helpful to work with the system facing
        slow internet connection issues
        """
        try:
            WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="tweet"]')))
        except WebDriverException:
            logger.exception(
                "Tweets did not appear!, Try setting headless=False to see what is happening")
    
    def set_value_or_none(self,value, string) -> Union[str, None]:
        return string+str(value)+" " if value is not None else None   

    def scroll_down(self,driver):
        """Helps to scroll down web page"""
        try:
            body = driver.find_element(By.CSS_SELECTOR, 'body')
            for _ in range(randint(1, 3)):
                body.send_keys(Keys.PAGE_DOWN)
        except Exception as ex:
            logger.exception("Error at scroll_down method {}".format(ex))

    def check_tweets_presence(self, tweet_list):
        if len(tweet_list) <= 0:
            self.retry -= 1

    def check_retry(self):
        return self.retry <= 0
    
    def fetch_and_store_data(self):
        try:
            all_ready_fetched_posts = []
            present_tweets = Finder.find_all_tweets(self.driver)
            self.check_tweets_presence(present_tweets)
            all_ready_fetched_posts.extend(present_tweets)

            while len(self.posts_data) < self.tweets_count:
                for tweet in present_tweets:
                    properties = self.driver.execute_script('return window.getComputedStyle(arguments[0], null);', tweet)
                    status, tweet_url = Finder.find_status(tweet)
                    posted_time = Finder.find_timestamp(tweet)
                    if not tweet_url.endswith('analytics') and not posted_time is None:
                        name = Finder.find_name_from_tweet(tweet)
                        replies = Finder.find_replies(tweet)
                        retweets = Finder.find_shares(tweet)
                        username = tweet_url.split("/")[3]
                        status = status[-1]
                        is_retweet = Finder.is_retweet(tweet)
                        posted_time = Finder.find_timestamp(tweet)
                        content = Finder.find_content(tweet)
                        likes = Finder.find_like(tweet)
                        images = Finder.find_images(tweet)
                        videos = Finder.find_videos(tweet)
                        hashtags = re.findall(r"#(\w+)", content)
                        mentions = re.findall(r"@(\w+)", content)
                        profile_picture = Finder.find_profile_image_link(tweet)
                        user_id= '1'
                        if not profile_picture is None:
                            user_id = profile_picture.split("/")[4]
                        if not user_id.isnumeric():
                            user_id = random.randint(0,35000)
                        link = Finder.find_external_link(tweet)
                        self.posts_data[status] = {
                            "tweet_id": status,
                            "username": username,
                            "user_id" :user_id,
                            "name": name,
                            "profile_picture": profile_picture,
                            "replies": replies,
                            "retweets": retweets,
                            "likes": likes,
                            "is_retweet": is_retweet,
                            "posted_time": posted_time,
                            "content": content,
                            "hashtags": hashtags,
                            "mentions": mentions,
                            "images": images,
                            "videos": videos,
                            "tweet_url": tweet_url,
                            "link": link
                        }
                self.scroll_down(self.driver)
                self.wait_until_completion(self.driver)
                self.wait_until_tweets_appear(self.driver)
                present_tweets = Finder.find_all_tweets(
                    self.driver)
                present_tweets = [
                    post for post in present_tweets if post not in all_ready_fetched_posts]
                self.check_tweets_presence(present_tweets)
                all_ready_fetched_posts.extend(present_tweets)
                print("self.tweets_count")
                print(self.tweets_count)
                print("len(self.posts_data)")
                print(len(self.posts_data))
                if self.check_retry() is True:
                    break

        except Exception as ex:
            logger.exception(
                "Error at method fetch_and_store_data : {}".format(ex))