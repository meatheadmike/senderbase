import os,sys,unittest,mock,time,requests
from mock import patch

basedir = os.path.abspath(os.path.dirname(__file__) + '/../')
sys.path.insert(0, basedir)

from senderbase import SenderBase

class TestSenderbase(unittest.TestCase):

  '''
      Test a "good" IP
  '''
  @mock.patch('requests.post')
  def test_8_8_8_8(self, requests_post):
    def mock_requests_post(*args,**kwargs):
      class __mock():
        f = open('%s/tests/mocks/8.8.8.8_result.html' % basedir, 'r')
        text = f.read()
      return __mock
    requests_post.side_effect = mock_requests_post
    s = SenderBase()
    result = s.lookup('8.8.8.8')
    assert result is not None
    assert result['ip'] == '8.8.8.8'
    assert result['network_owner'] == 'Google'
    assert result['web_reputation'] == 'Neutral'
    assert result['black_listed'] == False
    assert result['host_name'] == 'google-public-dns-a.google.com'
    assert result['blacklists'][0]['bl.spamcop.net'] == 'Not Listed'
    assert result['blacklists'][2]['pbl.spamhaus.org'] == 'Not Listed'
    assert result['web_category'] == 'Search Engines and Portals'
    assert result['email_reputation'] == 'Good'
    assert result['fwd_rev_dns_match'] == 'Yes'

  '''
      Test a "bad" IP
  '''
  @mock.patch('requests.post')
  def test_4_4_4_4(self, requests_post):
    def mock_requests_post(*args,**kwargs):
      class __mock():
        f = open('%s/tests/mocks/4.4.4.4_result.html' % basedir, 'r')
        text = f.read()
      return __mock
    requests_post.side_effect = mock_requests_post
    s = SenderBase()
    result = s.lookup('4.4.4.4')
    assert result is not None
    assert result['ip'] == '4.4.4.4'
    assert result['network_owner'] == 'Level 3 Communications'
    assert result['web_reputation'] == 'Poor'
    assert result['black_listed'] == True
    assert result['host_name'] == 'alu7750testscr.xyz1.gblx.mgmt.Level3.net'
    assert result['blacklists'][0]['bl.spamcop.net'] == 'Not Listed'
    assert result['blacklists'][2]['pbl.spamhaus.org'] == 'Listed'
    assert 'web_category' not in result
    assert result['email_reputation'] == 'Poor'
    assert result['fwd_rev_dns_match'] == 'No'

  '''
      Test an invalid IP
  '''
  @mock.patch('requests.post')
  def test_192_168_0_1(self, requests_post):
    def mock_requests_post(*args,**kwargs):
      class __mock():
        f = open('%s/tests/mocks/192.168.0.1_result.html' % basedir, 'r')
        text = f.read()
      return __mock
    requests_post.side_effect = mock_requests_post
    s = SenderBase()
    result = s.lookup('192.168.0.1')
    assert result is not None
    assert result == {}

  '''
      Test a "good" domain
  '''
  @mock.patch('requests.post')
  def test_google_com(self, requests_post):
    def mock_requests_post(*args,**kwargs):
      class __mock():
        f = open('%s/tests/mocks/google.com_result.html' % basedir, 'r')
        text = f.read()
      return __mock
    requests_post.side_effect = mock_requests_post
    s = SenderBase()
    result = s.lookup('google.com')
    assert result is not None
    assert 'ip' not in result
    assert 'network_owner' not in result
    assert result['web_reputation'] == 'Neutral'
    assert result['web_category'] == 'Search Engines and Portals'
    assert result['host_name'] == 'google.com'
    assert result['domain'] == 'google.com'

  '''
      test an invalid domain
  '''
  @mock.patch('requests.post')
  def test_a_b_c_d(self, requests_post):
    def mock_requests_post(*args,**kwargs):
      class __mock():
        f = open('%s/tests/mocks/a.b.c.d_result.html' % basedir, 'r')
        text = f.read()
      return __mock
    requests_post.side_effect = mock_requests_post
    s = SenderBase()
    result = s.lookup('a.b.c.d')
    assert result is not None
    assert result == {}

  '''
      Ensure that our timeout value is respected
  '''
  def test_timeout(self):
    s = SenderBase(host='10.255.255.1',timeout=0.25) # This should hang since this IP/port does not host a service!
    timeout_exception_caught = False
    start = time.time()
    try:
      result = s.lookup('1.2.3.4')
    except requests.exceptions.ConnectTimeout:
      timeout_exception_caught = True
    end = time.time()
    assert timeout_exception_caught == True
    assert end-start < 1 # Make sure we didn't take too long to run the whole test
  
if __name__ == '__main__':
    unittest.main(verbosity=2)
