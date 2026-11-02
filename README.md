
## Objective 
1. The application allows user to register and login. Each login is authenticated using JWT token. Using bear tokens user authenticated or allowed to access the application.
Also the passwords are hashed and stored in database and hashed passwords are used for verification.
Python version used is 3.13

## Create virtual environment and install related requirements
3. Create Environment and install dependency
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
## Generate JWT (Json web token)
 4. Before starting the app, generate a secret:
          python -c "import secrets; print(secrets.token_hex(32))"
  Copy the result into an environment variable in the terminal where you run Uvicorn.
  
  $env:JWT_SECRET = "paste-your-generated-value-here"

## Run app
 4.  Run the app:
         uvicorn main:app --reload
## Test the application    
 6.  Open your browser and visit:
     http://127.0.0.1:8000/docs
     
 7.   Test POST /auth/register :
    {
      "username": "Laxmi",
      "email": "Laxmi@example.com",
      "password": "secret345"
     }
     Registration should return 201

 8.    Test POST /auth/login with the same email and password:
     You should receive:

          {
            "access_token": "...",
            "token_type": "bearer"
          }

 9.    Copy the access_token value.
       Click the Authorize button at the top of the docs page.Paste only the token value, without quotes or the word Bearer.
       Click Authorize.

10.    Test GET /profile/me. you should be able to fetch below details:
         {
      "username": "Laxmi",
      "email": "Laxmi@example.com"
         }

## Automated test
11. Run python -m pytest -v

Here is the test result:
tests/test_auth.py::test_password_hash PASSED                                                          [  7%]
tests/test_auth.py::test_login_and_profile PASSED                                                      [ 15%]
tests/test_auth.py::test_profile_requires_token PASSED                                                 [ 23%]
tests/test_auth.py::test_duplicate_registration PASSED                                                 [ 30%]
tests/test_auth.py::test_bad_login[body0] PASSED                                                       [ 38%]
tests/test_auth.py::test_bad_login[body1] PASSED                                                       [ 46%]
tests/test_auth.py::test_invalid_registration PASSED                                                   [ 53%]
tests/test_auth.py::test_reject_token[missing] PASSED                                                  [ 61%]
tests/test_auth.py::test_reject_token[invalid] PASSED                                                  [ 69%]
tests/test_auth.py::test_reject_token[expired] PASSED                                                  [ 76%]
tests/test_auth.py::test_reject_token[no-expiry] PASSED                                                [ 84%]
tests/test_auth.py::test_reject_token[unknown-user] PASSED                                             [ 92%]
tests/test_auth.py::test_reject_token[bad-signature] PASSED                                            [100%]
How to run pytest, and a short summary of the results.

12. SQLite creates auth.db locally and the tests use a separate temporary database.
