import scrapy
import random
import time
from urllib.parse import urljoin
from scrapy_selenium import SeleniumRequest


class ASINSpider(scrapy.Spider):
    name = "asin_spider"
    start_urls = ['https://www.amazon.com/best-sellers-electronics/zgbs/electronics/'] # URL of the desired Amazon category

    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
        # Add more user agents here
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 5,  # Add a delay of 5 seconds between consecutive requests
        'CONCURRENT_REQUESTS': 1,  # Limit concurrent requests to 1
        'SELENIUM_DRIVER_NAME': 'chrome',
        'SELENIUM_DRIVER_EXECUTABLE_PATH': '/path/to/chromedriver',  # Update with the actual path to the chromedriver executable
        'SELENIUM_BROWSER_EXECUTABLE_PATH': '/path/to/chrome',  # Update with the actual path to the Chrome browser executable
        'SELENIUM_DRIVER_ARGUMENTS': ['--headless']  # Run Chrome in headless mode
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=10)

    def parse(self, response):
        asin_elements = response.css('.zg-item-immersion .a-link-normal::attr(data-asin)').getall()
        for asin in asin_elements:
            yield {
                'asin': asin
            }
            amazon_reviews_url = f'https://www.amazon.com/product-reviews/{asin}/'
            user_agent = random.choice(self.USER_AGENTS)
            headers = {'User-Agent': user_agent}
            yield scrapy.Request(url=amazon_reviews_url, headers=headers, callback=self.parse_reviews, meta={'asin': asin, 'retry_count': 0})

    def parse_reviews(self, response):
        asin = response.meta['asin']
        retry_count = response.meta['retry_count']

        ## Get Next Page Url
        next_page_relative_url = response.css(".a-pagination .a-last>a::attr(href)").get()
        if next_page_relative_url is not None:
            retry_count = 0
            next_page = urljoin('https://www.amazon.com/', next_page_relative_url)
            yield scrapy.Request(url=next_page, callback=self.parse_reviews, meta={'asin': asin, 'retry_count': retry_count})

        ## Adding this retry_count here to bypass any amazon js rendered review pages
        elif retry_count < 3:
            retry_count = retry_count+1
            yield scrapy.Request(url=response.url, callback=self.parse_reviews, dont_filter=True, meta={'asin': asin, 'retry_count': retry_count})

        ## Parse Product Reviews
        review_elements = response.css("#cm_cr-review_list div.review")
        for review_element in review_elements:
            yield {
                "asin": asin,
                "text": "".join(review_element.css("span[data-hook=review-body] ::text").getall()).strip(),
                "title": review_element.css("*[data-hook=review-title]>span::text").get(),
                "location_and_date": review_element.css("span[data-hook=review-date] ::text").get(),
                "verified": bool(review_element.css("span[data-hook=avp-badge] ::text").get()),
                "rating": review_element.css("*[data-hook*=review-star-rating] ::text").re(r"(\d+\.*\d*) out")[0],
            }
            time.sleep(2)  # Add a delay of 2 seconds before the next request
