grab:
	scrapy runspider grabbers/countries.py -t json -L ERROR -o - | jq "sort_by(.position)" > web/data/countries.json


