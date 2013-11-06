# -*- coding: utf-8 -*-
import json
import pkg_resources

from youckan.settings.common import conf

DOMAIN = conf['etalab']['domain']
HOME_URL = conf['etalab']['home_url'].format(domain=DOMAIN)
CKAN_URL = conf['etalab']['ckan_url'].format(domain=DOMAIN)
WIKI_URL = conf['etalab']['wiki_url'].format(domain=DOMAIN)
WIKI_API_URL = conf['etalab']['wiki_api_url'].format(domain=DOMAIN)
QUESTIONS_URL = conf['etalab']['questions_url'].format(domain=DOMAIN)

MENU_TOPICS = json.loads(pkg_resources.resource_string('youckan', 'static/bower/etalab-assets/data/main_topics.json'))

CKAN_API_KEY = conf['etalab'].get('ckan_api_key')
