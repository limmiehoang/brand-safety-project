PYTHONPATH=./src

setup: 
	pip install -r requirements.txt

gen_links:
	PYTHONPATH=$(PYTHONPATH) python src/spider/gen_links.py

scrape_pages:
	PYTHONPATH=$(PYTHONPATH) python src/spider/scrape_pages.py

gen_csv:
	PYTHONPATH=$(PYTHONPATH) python src/spider/gen_csv.py	

train:
	PYTHONPATH=$(PYTHONPATH) python src/model/train.py

predict_test_set:
	PYTHONPATH=$(PYTHONPATH) python src/model/predict.py

predict_specific_url:
	PYTHONPATH=$(PYTHONPATH) python src/model/predict_url.py ${url}