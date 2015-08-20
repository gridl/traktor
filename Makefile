grab:
	scrapy runspider grabbers/countries.py -t json -L ERROR -o - | jq "sort_by(.position)" > web/data/countries.json

deploy_pages:
	venv/bin/ghp-import web
	git push origin gh_pages
