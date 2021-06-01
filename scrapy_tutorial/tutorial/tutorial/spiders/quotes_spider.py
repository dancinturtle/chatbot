import scrapy

class QuotesSpider(scrapy.Spider):
  # name identifies the spider, must be unique within a project
  name = 'quotes'
  # instead of making start_requests just create start_urls
  # default callback is parse(), called for requests without explicit callback
  start_urls = [
    'http://quotes.toscrape.com/page/1/',
    'http://quotes.toscrape.com/page/2/',
  ]

  # def start_requests(self):
  #   # must return iterable of Requests which Spider will begin to crawl from
  #   urls = [
  #     'http://quotes.toscrape.com/page/1/',
  #     'http://quotes.toscrape.com/page/2/',
  #   ]
  #   for url in urls:
  #     yield scrapy.Request(url=url, callback=self.parse)

  def parse(self, response):
    # will be called to handle the response downloaded for each request made
    # response parameter is instance of TextResponse
    # parse the response, extract scraped data as dicts, find new urls to follow
    # page = response.url.split('/')[-2]
    # filename = f'quotes-{page}.html'
    # with open(filename, 'wb') as f:
    #   f.write(response.body)
    # self.log(f'Saved file {filename}')
    for quote in response.css('div.quote'):
      yield {
        'text': quote.css('span.text::text').get(),
        'author': quote.css('small.author::text').get(),
        'tags': quote.css('div.tags a.tag::text').getall(),
      }
      next_page = response.css('li.next a::attr(href)').get()
      if next_page is not None:
        # urljoin method builds a full absolute url
        # when you yield a request in a callback method, Scrapy will schedule that request to be sent and register a callback to be executed when that request finishes
        next_page = response.urljoin(next_page)
        yield scrapy.Request(next_page, callback=self.parse)

      #shortcut, use response.follow
      # if next_page is not None:
      #   yield response.follow(next_page, callback=self.parse)
