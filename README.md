
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
   ```
          fastapi==0.141.1
          uvicorn==0.52.4
          sqlalchemy==2.0.55
          pwdlib[argon2]==0.3.1
          PyJWT==2.15.1
          email-validator==2.3.0
          pytest==9.1.1
          httpx==0.28.1
   ```
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
```
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

```

12. SQLite creates auth.db locally and the tests use a separate temporary database.





## File Dependency Diagram
```
1     main.py
2      │
3      ├── database.py
4      │      │
5      │      └── SQLite
6      │
7      ├── models.py
8      │      │
9      │      └── User Table
10      │
11      ├── schemas.py
12      │      │
13      │      └── Input Validation
14      │
15      ├── security.py
16      │      │
17      │      ├── Hash Password
18      │      ├── Verify Password
19      │      └── JWT Token
20      │
21      └── routers
22             │
23             ├── auth.py
24             │      ├── schemas.py
25             │      ├── models.py
26             │      ├── database.py
27             │      └── security.py
28             │
29             └── profile.py
30                    ├── database.py
31                    ├── models.py
32                    └── security.py
```






## Complete Request Flow
```
1     1. User Registers
2            │
3            ▼
4     schemas.py validates input
5            │
6            ▼
7     security.py hashes password
8            │
9            ▼
10     models.py creates User object
11            │
12            ▼
13     database.py saves to SQLite
14            │
15            ▼
16     User Created
17     ────────────────────────────
18     
19     2. User Logs In
20            │
21            ▼
22     schemas.py validates request
23            │
24            ▼
25     database.py finds user
26            │
27            ▼
28     security.py verifies password
29            │
30            ▼
31     security.py creates JWT
32            │
33            ▼
34     Token Returned
35     ────────────────────────────
36     
37     3. Protected Endpoint
38            │
39            ▼
40     Authorization Header
41            │
42            ▼
43     get_current_user()
44            │
45            ▼
46     JWT Decode
47            │
48            ▼
49     Find User
50            │
51            ▼
52     Return Profile

```
