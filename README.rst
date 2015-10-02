Senderbase
==========
A python-based screen scraper for the senderbase.org website

Installation
============
python setup.py test
sudo python setup.py install

Usage
=====
In your code::

  from senderbase import SenderBase 
   
  sb = SenderBase(timeout=30) 
  my_result = sb.lookup('8.8.8.8') 


Make sure you limit your queries to 1000 per day or less. Be a good netizen!
