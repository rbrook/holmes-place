import re
from sre_parse import parse_template
import requests
from bs4 import BeautifulSoup

url = "https://holmesplace-amoreiras.virtuagym.com//classes/week/?embedded=1&event_type=0&pref_club=48110"

res = requests.get(url)
assert res.ok
soup = BeautifulSoup(res.text, "html.parser")

reg=re.compile('internal-event-day-.*')

part_class_name = 'internal-event-day-'
old_date = None
for elem in soup.body.find_all("div", {"class" : reg}):
    classes = elem.attrs['class']
    date = None
    for _cls in classes:
        if part_class_name in _cls:
            date = _cls[_cls.find(part_class_name)+len(part_class_name):]
    if not date:
        raise Exception(f"Can't find date! {classes}")
    if old_date != date:
        old_date = date
        print()

    name = elem.find('span', {"class": "classname"}).text.strip()
    time = elem.find('span', {"class": "time"}).text.strip()

    for word in ['hidro', 'swim']:
        if word in name.lower():
            print(date, name, time)
