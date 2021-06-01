import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from . import secretvariables
secrets = secretvariables.Secret

"""
starts from the main page
follow all links to authors pages and calls parse_author
also follows the pagination links with the parse callback
"""
"""
_token: SAzqpEdF3Sq1FzS4U9hXeTogsjKSCs5vimyzvdHU
email: amydsi.ga@gmail.com
password: snowballpw
"""
class DairySpider(scrapy.Spider):
  name = 'dairy'
  start_urls = ('https://veganbootcamp.org/login',)
  dairy_urls = ['https://veganbootcamp.org/course-progress/497/overview-of-dairy']

  def parse(self, response):
    token = response.xpath('//*[@name="_token"]/@value').extract_first()
    data = {'_token': token,
            'email': secrets.EMAIL,
            'password': secrets.PASSWORD,
            'remember': 'true'
    }
    return FormRequest.from_response(response, formdata=data, callback=self.auth_check, meta={'dont_redirect': True, 'handle_httpstatus_list': [302]})

  def auth_check(self, response):
    open_in_browser(response)
    logged_in = response.xpath('//title/text()').get()
    if logged_in == 'Redirecting to https://veganbootcamp.org':
      print('auth success')
      return scrapy.Request(url=self.dairy_urls[0], callback=self.parse_data, dont_filter=True,errback=self.error)
    else:
      print('bad auth')


  def get_data(self):
    self.logger.info('Got logged in, going to try getting data on dairy')
    yield scrapy.Request(url=self.dairy_urls[0], callback=self.parse_data, dont_filter=True,errback=self.error)

  def parse_data(self, response):
    self.logger.info('Dairy request was successful')
    data = response.xpath('//title/text()').get()
    open_in_browser(response)
    print("data!", data)
    return data

  def error(self, failure):
    self.logger.error(repr(failure))
    print('whoooah error', failure)
