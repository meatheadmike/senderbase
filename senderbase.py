import requests, re
from lxml import html

class SenderBase(object):

  config = {
    'proto': 'http',
    'host': 'www.senderbase.org',
    'lookup': '/lookup/?search_string=',
    'lookup_domain': '/lookup/domain/?search_string=',
    'lookup_ip': '/lookup/ip/?search_string=',
    'timeout': 30 # Some requests can take a LONG time.
  }  

  payload = {
    'tos_accepted': 'Yes, I Agree'
  }

  '''
      Override any config values upon init.
      Example: s = SenderBase(timeout=10)
  '''
  def __init__(self, **kwargs):
    # override config:
    for key,val in kwargs.iteritems():
      self.config[key] = val

  def __get_x_val(self, xpath, xobj):
    result = None
    try:
      result = xobj.xpath(xpath)[0].strip()
    except IndexError:
      pass
    return result

  def __parse_results(self, html_result):
    result = {}
    clean_html = re.sub(r'<\\?wbr\\?>','',html_result.text)
    self.tree = html.fromstring(clean_html)

    for row in self.tree.xpath('//*[@class="tabular info_table"]/tr'):
      elm_key = self.__get_x_val('.//td[1]/text()',row)
      if elm_key == 'IP Address':
        result['ip'] = self.__get_x_val('.//td[2]/text()',row)
      elif elm_key == 'Fwd/Rev DNS Match':
        result['fwd_rev_dns_match'] = self.__get_x_val('.//td[2]/text()',row)
      elif elm_key == 'Email Reputation':
        result['email_reputation'] = self.__get_x_val('.//td[2]/div[1]/text()',row)
      elif elm_key == 'Web Reputation':
        result['web_reputation'] = self.__get_x_val('.//td[2]/div[1]/text()',row)
      elif elm_key == 'Web Category':
        result['web_category'] = self.__get_x_val('.//td[2]/span/span/text()',row)
      elif elm_key == 'Email Volume':
        result['email_volume'] = {}
        result['email_volume']['last_day'] = self.__get_x_val('.//td[2]/text()',row)
        result['email_volume']['last_month'] = self.__get_x_val('.//td[3]/text()',row)
      elif elm_key == 'Volume Change':
        result['volume_change'] = {}
        result['volume_change']['last_day'] = self.__get_x_val('.//td[2]/text()',row)
        result['volume_change']['last_month'] = self.__get_x_val('.//td[3]/text()',row)
      elif elm_key == 'Hostname':
        result['host_name'] = self.__get_x_val('.//td[2]/a/text()',row)
      elif elm_key == 'Domain':
        result['domain'] = self.__get_x_val('.//td[2]/a/text()',row)
        if result['domain'] is None:
          result['domain'] = self.__get_x_val('.//td[2]/text()',row)
      elif elm_key == 'Network Owner':
        result['network_owner'] = self.__get_x_val('.//td[2]/a/text()',row)
    if self.tree.xpath('//*[@class="tabular bl_table zebra_table"]') != []:
      result['blacklists'] = []
      result['black_listed'] = False
      for row in self.tree.xpath('//*[@class="tabular bl_table zebra_table"]/tr'):
        blacklist = {}
        key = self.__get_x_val('.//td[1]/a/text()',row)
        val = self.__get_x_val('.//td[2]/text()',row)
        blacklist[key] = val
        if val == 'Listed':
          result['black_listed'] = True
        result['blacklists'].append(blacklist)
    return result

  '''
      Look up either an IP or a domain name with senderbase.org.
      When there are multiple results (ie amazon.com), then it comes back blank.
      Example: s = SenderBase()
               result = s.lookup('8.8.8.8')
               result = s.lookup('google.com')
  '''
  def lookup(self, search_string):
    req = '%(proto)s://%(host)s%(lookup)s' % self.config
    html_result = requests.post('%(req)s%(search_string)s' % {'req':req, 'search_string':search_string}, data=self.payload, timeout=self.config['timeout'])
    return self.__parse_results(html_result)

  '''
      Look up a specific domain
  '''
  def lookup_domain(self, search_string):
    req = '%(proto)s://%(host)s%(lookup_domain)s' % self.config
    html_result = requests.post('%(req)s%(search_string)s' % {'req':req, 'search_string':search_string}, data=self.payload, timeout=self.config['timeout'])
    return self.__parse_results(html_result)

  '''
      Look up a specific ip
  '''
  def lookup_ip(self, search_string):
    req = '%(proto)s://%(host)s%(lookup_ip)s' % self.config
    html_result = requests.post('%(req)s%(search_string)s' % {'req':req, 'search_string':search_string}, data=self.payload, timeout=self.config['timeout'])
    return self.__parse_results(html_result)

