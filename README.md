# scrapy-redflagdeals

This is a Scrapy project to scrape Redflagdeals.com.

This project is for educational purposes.

## Usage

To run the spider:
```python crawl.py```

## Configuration

To configure this scraper, modify config.yml.

This will only crawl the list of forums specified.

Keywords also listed in config.yml.

## Storage

All deals are stored in [TinyDB](https://github.com/msiemens/tinydb)

Storage can easily be adapted to use another database program such as MongoDB.

## Notifications

Sign up to SendGrid to get an API key to use this function.

Update the development environment with your SENDGRID_API_KEY, for example::

    echo "export SENDGRID_API_KEY='YOUR_API_KEY'" > sendgrid.env
    echo "sendgrid.env" >> .gitignore
    source ./sendgrid.env

### License
Apache Version 2.0
