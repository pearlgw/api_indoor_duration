setup:
	python db_manage.py setup

migrate:
	python db_manage.py migrate

rollback:
	python db_manage.py rollback

reset:
	python db_manage.py reset

run: 
	uvicorn main:app --host 0.0.0.0 --port 8000 --reload