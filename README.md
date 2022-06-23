Dentist Backend

================================

### Technical Stack

	- Python/Django: python 3.8, Django 3.1

	- Database: PostgreSQL 11.0

	- JWT auth based RESTful API
	
	- Coding style: PEP 8 standards

### Create server

	```
	$ python3.9 -m venv env

	$ source env/bin/activate

	$ pip install -r requirements.txt

	$ pip freeze > requirements.txt
	```

### Get static files

	```
	$ ./manage.py collectstatic
	```

### Migrate models into database
	```
	$ ./manage.py makemigrations
  $ ./manage.py migrate
	```

### Create admin user on server

	```
	$ ./manage.py createsuperuser
	```

### Run server
	```
	$ ./manage.py runserver
	```

	or

	```
	$ ./manage.py runserver 0.0.0.0:8000
	```

### Server urls

- http://127.0.0.1:8000/admin/

- http://127.0.0.1:8000/apis/

- http://127.0.0.1:8000/api-docs/


### Deployment

1. Development mode on local environment

	Deploy this backend with docker mode on local environment.

	```
	$ ./deploy-prod.sh
	```

2. Production mode on global server environment

	Deploy this bakcend with individual docker mode.

  - on development server

		```
		$ ./deploy-prod.sh
		```

### Troubleshooting
- Remove migration files
	After faking the migrations for all apps we need to delete the migrations files inside migrations folder in each app.

	You can use the previous bash script to automate this process in Unix bases OSs.

	```
	$ find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	$ find . -path "*/migrations/*.pyc"  -delete
	$ rm -rf env
	$ python3.8 -m venv env
	$ source env/bin/activate
	$ pip install -r requirements.txt
	```
	This will delete Python source files and also compiled Python files for migrations except for the special Python file init.py

- Make migrations again
	Now you need to re-create the initial database migrations with the usual commands
	```
	$ python manage.py makemigrations
	```

- Save installed python packages into `requirements.txt` file.
	```
	$ pip freeze > requirements.txt
	```

	1. Added global DNS address `8.8.8.8` into docker container when run docker, so that the docker container can resolve IP address of AWS RDS from domain name.

    ```
    $ docker run --name dentist-backend --dns=8.8.8.8 -p 8000:8000 -d dentist-backend
    ```

	Then I connected from inside of docker container to AWS RDS, successfully.

	* Note: Firstly, I tried second way. But I didn't solve the connection problem. When I tried both two ways, I was success.

- Database recovery to synchronize with Django models

	1. Delete all tables in database.

	2. Update database with special model.
	
		```
		$ python manage.py migrate
		```


### Commands

	1. `scan_ens`
		- You can scan ETH names, manually.

		```
		./manage.py scan_ens --name 111 222.eth
		```

		or for all,

		```
		./manage.py scan_ens 
		```

	2. `scan_category`
		- You can scan all eths names in the uploaded file or regular expression of category, manually.

		```
		./manage.py scan_category --name Animals
		```

		or for all,

		```
		./manage.py scan_category
		```

	3. `scan_category_by_id`
		```
		$ docker exec sek9-backend python manage.py scan_category_by_id --id 4 &
		```

### Database backup and restore

	1. Backup

		```
		pg_dump -h app.seck9.com -p 5432 -U postgres -d seck9 -W --format plain --verbose -f ./seck9.sql
		```

	2. Restore

		```
		psql -d seck9 -U postgres -p 5432 -h www.seck9.com -W -f ./seck9.sql
		```

		- After you restored database with dump file, maybe you need to increase sequence in each table. For it, you can do as following:

			In PostgreSQL, run this sql command.
			
			```
			> SELECT setval('tablename_id_seq', (SELECT MAX(id) FROM tablename)+1);
			```

			or In Django project, run this commend.

			```
			$ python manage.py sqlsequencereset member | ./manage.py dbshell
			```
### Reference
	- Pagenation: https://github.com/ashish1997it/filter-pagination-dj
