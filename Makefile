api:
	python ./api_data_treatment.py

main:
	py ./main.py

install-requirements:
	pip install -r requirements.txt

generate-requirements:
	pipreqs

tempo-data:
	python ./get_tempo_data.py