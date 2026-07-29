# CampusCare testing guide

Run tests in this order. Do not start GitHub or deployment work until the local checks pass.

## 1. Install the project

Windows PowerShell:

```powershell
cd CampusCare
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

If PowerShell blocks activation, run this once in the same terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## 2. Run automated tests

```powershell
python -m pip check
python -m compileall -q campuscare scripts tests streamlit_app.py
python -m pytest -q
```

The suite checks configuration, password security, NCI email validation, registration, login, donation validation, image validation, search and filters, reservations, cancellation, handover completion, trust scores, profile updates, dashboard metrics and Streamlit startup.

## 3. Test against PostgreSQL

Use a separate disposable PostgreSQL database for integration tests.

Important: the test fixture creates and drops CampusCare tables. Never set `TEST_DATABASE_URL` to the live application database.

PowerShell:

```powershell
$env:TEST_DATABASE_URL="postgresql+psycopg://USER:PASSWORD@HOST:5432/campuscare_test"
python -m pytest -q
Remove-Item Env:TEST_DATABASE_URL
```

A normal hosted application database should instead be configured through `DATABASE_URL` in `.env`.

## 4. Configure the hosted application database

Copy `.env.example` to `.env` and replace the placeholder URL with the external connection string from the PostgreSQL host.

```powershell
Copy-Item .env.example .env
notepad .env
```

Initialise and verify it:

```powershell
python scripts/init_db.py
python scripts/check_database.py
```

Expected output:

```text
CampusCare database schema is ready.
Database connection: OK
Required tables: OK
Database type: postgresql+psycopg
```

## 5. Run the application

```powershell
python -m streamlit run streamlit_app.py
```

Open the local address shown in the terminal, normally `http://localhost:8501`.

## 6. Manual acceptance test

Use one normal browser window and one private/incognito window so two users can stay logged in at the same time.

### Account A: donor

1. Register with an allowed NCI email domain.
2. Confirm the Home page loads.
3. Open Donate an Item.
4. Create a donation with title, category, condition, pickup location, description and a valid image.
5. Confirm it appears under My Activity.

### Account B: receiver

1. Register in the private window with a different NCI email.
2. Browse donations.
3. Search for the item and test category and condition filters.
4. Open its details.
5. Reserve it.
6. Confirm it appears under My Reservations.

### Complete the flow

1. Return to Account A.
2. Confirm the receiver's name and email appear on the reserved donation.
3. Complete the handover.
4. Confirm the item status becomes Completed.
5. Check that both trust scores change.
6. Refresh both browsers and confirm the data remains.
7. Restart Streamlit and confirm the records still exist in PostgreSQL.

## 7. Failure checks

Confirm all of these are rejected cleanly:

- non-NCI registration email;
- weak password;
- duplicate email registration;
- title shorter than three characters;
- description shorter than ten characters;
- invalid or oversized image;
- reserving your own item;
- reserving an already reserved item;
- cancelling another user's reservation;
- completing a handover before reservation.

## 8. Evidence to retain

Keep screenshots of:

- terminal showing all tests passed;
- hosted PostgreSQL resource and connection health;
- registration and login;
- donation creation;
- search and filtering;
- reservation;
- completed handover;
- profile and trust score;
- data still present after restart.
