install:
	pip install -r requirements.txt
upload_s3:
	python read_write_files_s3.py