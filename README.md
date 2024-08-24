1. Create a folder, then in Command Prompt (cmd), navigate to your folder `C:\...\your_folder` and run:

    ```bash
    git clone https://github.com/Kerchiano/comments.git
    ```

2. After cloning, navigate to `C:\...\your_folder\comments`:

    ```bash
    cd comments
    ```

3. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:

    ```bash
    venv\Scripts\activate
    ```

5. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

6. Create the `.env` file:

    ```bash
    echo. > .env
    ```

7. Add the following manually to the `.env` file:

    ```plaintext
    DB_NAME=comments
    DB_USER=postgres
    DB_PASSWORD=1234
    DB_HOST=db
    DB_PORT=5432
    SECRET_KEY=django-insecure-8%_9=y^b%^idigk=n_3w%35h&gvzithycrdq7lq*xdku#20rib
    ```

8. Open the `entrypoint.sh` file in Notepad++ or VSCode and change the line endings from CRLF to LF.

9. Run Docker Compose:

    ```bash
    docker-compose up
    ```

10. Congratulations! Open your browser and go to [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/) to check the API endpoints.

