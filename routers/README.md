
1. The application allows user to register and login. Each login is authenticated using JWT token. Using bear tokens user authenticated or allowed to access the application.
Also the passwords are hashed and stored in database and hashed passwords are used for verification.
Python version used is 3.13
2. Create Environment and install dependency
       py -m venv .venv
   Activate the virtual environment.
       Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
        .venv\Scripts\Activate.ps1
   Create a new file in VS Code called requirements.txt
          fastapi==0.141.1
          uvicorn==0.52.4
          sqlalchemy==2.0.55
          pwdlib[argon2]==0.3.1
          PyJWT==2.15.1
          email-validator==2.3.0
          pytest==9.1.1
          httpx==0.28.1
   Install the packages:
         python -m pip install -r requirements.txt

 3. Before starting the app, generate a secret:
          python -c "import secrets; print(secrets.token_hex(32))"
  Copy the result into an environment variable in the terminal where you run Uvicorn.
  
  $env:JWT_SECRET = "paste-your-generated-value-here"
  
 4.  Run the app:
         uvicorn main:app --reload
 5.  Open your browser and visit:
     http://127.0.0.1:8000/docs
     
 6.   Test POST /auth/register :
    {
      "username": "Laxmi",
      "email": "Laxmi@example.com",
      "password": "secret345"
     }
     Registration should return 201

 7.    Test POST /auth/login with the same email and password:
     You should receive:

          {
            "access_token": "...",
            "token_type": "bearer"
          }

 8.    Copy the access_token value.
       Click the Authorize button at the top of the docs page.Paste only the token value, without quotes or the word Bearer.
       Click Authorize.

9.    Test GET /profile/me.
How to run pytest, and a short summary of the results.
That SQLite creates auth.db locally and the tests use a separate temporary database.
