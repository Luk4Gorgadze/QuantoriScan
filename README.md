# QuantoriScan

helper commands for me:

[docker]
- docker compose up -d --build

[testing]
- pytest .

[mypy]
- mypy --config-file mypy.ini app

[formatting]
- isort .
- autopep8 --recursive --in-place .

[migrations]
- alembic revision --autogenerate -m 'some comment'
- alembic upgrade head

[dependencies]
- pip freeze > requirements.txt