# -*- coding: utf-8 -*-
from youckan.settings.common import conf

DOMAIN = conf['etalab']['domain']
HOME_URL = conf['etalab']['home_url']
WIKI_URL = conf['etalab']['wiki_url']
WIKI_API_URL = conf['etalab']['wiki_api_url']
QUESTIONS_URL = conf['etalab']['questions_url']
MENU_TOPICS = (
    (u'Culture et communication', 'culture', None),
    (u'Développement durable', 'wind', '{wiki}/Le_D%C3%A9veloppement_Durable'),
    (u'Éducation et recherche', 'education', None),
    (u'État et collectivités', 'france', None),
    (u'Europe', 'europe', None),
    (u'Justice', 'justice', None),
    (u'Monde', 'world', None),
    (u'Santé et solidarité', 'heart', None),
    (u'Sécurité et défense', 'shield', None),
    (u'Société', 'people', None),
    (u'Travail, économie, emploi', 'case', None),
)
