import requests
import os
import yaml
import urllib2

NYT_API_KEY = os.environ['nyt_search_api_key']
GENDER_API_KEY = os.environ['gender_api_key']


def fetch_obituaries(page_count):	
	obituaries = []
	base_url = "http://api.nytimes.com/svc/search/v2/articlesearch.json?fq=section_name%3Aobituaries&api-key={0}&page={1}"
	for page_no in range(0, page_count):
		url = base_url.format(NYT_API_KEY, page_no)
		request = requests.get(url)
		json = request.json()
		for doc in json['response']['docs']:
			obituary = extract_obit_from_json(doc)
			if obituary:
				obituaries.append(obituary)
	return obituaries


def extract_obit_from_json(doc):
	persons = extract_persons(doc['keywords'])
	if len(persons) == 1:
		obituary = {}
		obituary['person'] = persons[0]
		obituary['gender'] = get_gender(persons[0])
		obituary['url'] = doc['web_url']
		obituary['headline'] = doc['headline']['main']
		obituary['lead_paragraph'] = doc['lead_paragraph']
		obituary['date'] = doc['pub_date']
		obituary['word_count'] = doc['word_count']
		obituary['news_desk'] = doc['news_desk']
		return obituary
	else:
		return None

def extract_persons(keywords):
	persons = []
	for keyword in keywords:
		if keyword['name'] == 'persons':
			persons.append(keyword['value'])
	return persons

def get_gender(name):
	namelist = name.split(', ') #TODO: Make this more robust
	if len(namelist) == 2:
		first_name = namelist[1]
		urlname = urllib2.quote(first_name, '')
		gender_url = "https://gender-api.com/get?name={0}&key={1}"
		json = requests.get(gender_url.format(urlname, GENDER_API_KEY)).json()
		return json['gender']
	else:
		print namelist
		return "Unknown"

obituaries = fetch_obituaries(2)
obituaries
yaml.safe_dump(obituaries, file("obituaries.yml",'w'), encoding='utf-8', allow_unicode=True, default_flow_style=False)



