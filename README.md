scrapy-redflagdeals
====================

This is a `Scrapy`_ project to scrape `Redflagdeals.com`_ forums.

This project is for educational purposes.

.. _Scrapy: http://www.scrapy.org
.. _Redflagdeals.com: http://forums.redflagdeals.com

Usage
=====

To run the spider::

    python crawl.py

If you are wondering how the scraper works, check out the `Scrapy Tutorial`_.

.. _Scrapy Tutorial: http://doc.scrapy.org/en/latest/intro/tutorial.html

Configuration
=============

To configure this scraper, modify config.yml.

This will only crawl the list of forums specified.

Keywords also listed in config.yml.

Storage
=======

All deals are stored in `TinyDB`_.

Storage can easily be adapted to use another database program such as `MongoDB`_.

.. _TinyDB: https://github.com/msiemens/tinydb

.. _MongoDB: https://www.mongodb.com/

Notifications
=============

Sign up to `SendGrid`_ to get an API key to use this function.


.. _SendGrid: http://sendgrid.com/

Update the development environment with your SENDGRID_API_KEY, for example::

    echo "export SENDGRID_API_KEY='YOUR_API_KEY'" > sendgrid.env
    echo "sendgrid.env" >> .gitignore
    source ./sendgrid.env

License
=======
Apache Version 2.0
