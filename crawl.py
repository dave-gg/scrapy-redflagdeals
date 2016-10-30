import os
import yaml
import sendgrid
from sendgrid.helpers.mail import *

from scrapy.crawler import CrawlerProcess
from scraper.spiders.deals import DealsSpider
from scrapy.utils.project import get_project_settings


from database import Database

config = yaml.safe_load(open("config.yml"))
db = Database(config['tiny_db']['db_file'])

SETTINGS = get_project_settings()
FORUM_LIST = config['scrapy']['forums']  # .split('\n')

def complete_url(string):
    return config['scrapy']['base_url'] + string


def get_subject(subject):
    checked_subject = (subject[:75].strip() + '...') if len(subject) > 78 else subject
    return checked_subject


def create_email(recipient, first_name, deal):
    deal_description = str(deal['description'])
    posted_by = str(deal['postedby'])
    first_post_date = str(deal['firstpostdate'])
    deal_url = str(complete_url(deal['url']))

    email = """
    <html><head></head><body style="font-size:18px">
    <h2>%s</h2>
    """ % (deal['title'])
    if 'price_posted' in deal and 'deal_link' in deal:
        email += """
        <p><a href="%s"> >> Jump to Deal << </a></p>
        <p>Price: <strong>%s</strong></p>
        """ % (deal['deal_link'], deal['price_posted'])
    elif 'price_posted' in deal:
        email += '<p>Price: <strong>%s</strong></p>' % (deal['price_posted'])
    elif 'deal_link' in deal:
        email += '<p><a href="%s"> >> Jump to Deal << </a></p>' % (
            deal['deal_link'])
    email += """
    <p>User: <strong>%s</strong>
    </p><p>First Posted: <strong>%s</strong></p><p><a href="%s">[SOURCE]</a></p>
    <div style="border: 1px solid black;border-radius: 5px; background-color: #c9d2e3">
    <div style="margin: 10px;">%s</div></div>
    <p>Mail powered by <a href="http://www.sendgrid.com">SendGrid</a></p>
    """ % (posted_by, first_post_date, deal_url, deal_description)
    email += '</body></html>'
    return email


def send_notification(recipient, first_name, deal):
    print('sending email to: ' + recipient)

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))

    from_email = Email('Notify <' + config['mail']['from'] + '>')
    subject = get_subject(deal['title'])
    to_email = Email(recipient)
    created_email = create_email(recipient, first_name, deal)
    content = Content("text/html", created_email)

    mail = Mail(from_email, subject, to_email, content)

    try:
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
    except Exception as e:
        print(e.read())


def json_exists():
    return os.path.isfile(str(SETTINGS.get('FEED_URI')))


def setup_crawler(forums):
    process = CrawlerProcess(SETTINGS)
    if json_exists():
        os.remove(SETTINGS.get('FEED_URI'))
    process.crawl(DealsSpider, forums, domain='scrapinghub.com')
    process.start()


def scan_deals():
    """
    Scan deals, archive them in the DB, and send out a notification
    """
    with open(SETTINGS.get('FEED_URI')) as json_file:
        try:
            deals_json = json.load(json_file)
        except Exception as e:
            print('Failed to JSON file.' + str(e))

    mail_to = config['user']['email']
    keywords = config['user']['keywords']
    first_name = config['user']['name']

    for deal in deals_json:
        for keyword in keywords:
            # Check if any keywords are found (case insensitive)
            if keyword.lower() in deal['title'].lower():
                print('> MATCHED KEYWORD: [ ' + keyword + ' ]')
                # Check if collection is empty
                if not db.match_old_deal(deal['url'], deal['title'], deal['firstpostdate']):
                    db.add_deal(deal)
                    print('>> ADDING DEAL TO DB')
                    send_notification(mail_to, first_name, deal)


setup_crawler(FORUM_LIST)
scan_deals()
