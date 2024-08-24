Create a folder, then in Command Prompt (cmd), navigate to your folder C:\...\your_folder and run:

`git clone https://github.com/Kerchiano/comments.git`

After cloning, navigate to C:\...\your_folder\comments:

`cd comments`

Create a virtual environment:

`python -m venv venv`

Activate the virtual environment:

`venv\Scripts\activate`

Install the required packages:

`pip install -r requirements.txt`

Create the .env file:

`echo. > .env`

Add the following manually to the .env file:

DB_NAME=comments

DB_USER=postgres

DB_PASSWORD=1234

DB_HOST=db

DB_PORT=5432

SECRET_KEY=django-insecure-8%_9=y^b%^idigk=n_3w%35h&gvzithycrdq7lq*xdku#20rib

Open the entrypoint.sh file in Notepad++ or VSCode and change line endings from CRLF to LF.

Run Docker Compose:

`docker-compose up`

Congratulations! Open your browser and go to http://127.0.0.1:8000/swagger/ to check the API endpoints.
