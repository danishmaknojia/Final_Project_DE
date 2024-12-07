install:
	pip install -r requirements.txt
upload_s3:
	python s3_dataprocesses.py