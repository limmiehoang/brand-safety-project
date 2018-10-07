PYTHONPATH=./src

setup: 
	pip install -r requirements.txt
	pip install -r requirements.dev.txt

gen_requirements:
	pip freeze -r requirements.txt

test:
	pytest ./test


train:
	PYTHONPATH=$(PYTHONPATH) python src/model/train.py

predict:
	PYTHONPATH=$(PYTHONPATH) python src/model/predict.py

prepare:
	PYTHONPATH=$(PYTHONPATH) python src/spider/gen_csv.py