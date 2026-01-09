# Welcome to EarnIn Airline.

> !
>
> [Jump to Candidate Submission](#submission-test-guide)
>
> !

This is RESTful API for EarnIn Airline application.

## Up and running

> _Please ensure that you have docker in your machine to run._

To start the service, you can run the following command.

```bash
docker compose up -d
```

**Create DB schema**. You can find `sql` file in [db](./db/) directory. To apply other SQL script, you can place a sql file in db dir, and replace `schema.sql` with your file name.

```bash
docker compose exec -it postgres bash -c "/home/scripts/exec_sql.sh schema.sql"
```

This system does not initial any data. You choose add some data to `flights` table. For `timezone` column, please choose from [List of timezone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List) in `TZ identifier` column.

## APIs

### List all flights

```bash
curl http://localhost:8000/flights
```

### List passengers by flight

```bash
curl http://localhost:8000/flights/[flight-id]/passengers
```

### Create a passenger

The API will validate passenger's firstname and lastname with `Passport API` before creating a record. The customer record will create a new record if the passport ID doesn't exist in the system.

> `Passport API` use wiremock to stubbing the actual service. You can find configuration in [passport_api directory](./passport_api/). If you're new to wiremmock, we recommend to check out [wiremock documentation](https://wiremock.org/docs/stubbing/).

```bash
curl http://localhost:8000/flights/[flight-id]/passengers \
    -d '{"passport_id": "BC1500", "first_name": "Shauna", "last_name": "Davila"}' \
    -H "Content-Type:application/json"
```

### Update a passenger

To update information of customer info, we can use this API to update passport ID, firstname, and lastname.

```bash
curl -X PUT http://localhost:8000/flights/[flight-id]/passengers/[customer_id] \
    -d '{"passport_id": "BC1500", "first_name": "Shauna", "last_name": "Davila"}' \
    -H "Content-Type:application/json"
```

### Delete a passenger

To update information of customer info, we can use this API to update passport ID, firstname, and lastname.

```bash
curl -X DELETE http://localhost:8000/flights/[flight-id]/passengers/[customer_id]
```

# QA Automation Test Assignment

As part of the QA automation testing coverage, the following test scenarios must be automated for the EarnIn Airline API.
Each test case should use its own mock data and services (e.g., Wiremock for Passport API).

### **Test Scenarios and Expected Results**

| **Test Scenario**                                                                            | **Expected Result**                                                                                                                     |
| -------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| Create a flight booking with valid customer and flight details                               | Booking is successfully created. Customer name is verified via Passport API                                                             |
| Attempt to create a booking with mismatched customer name in Passport API                    | Booking fails. The Passport API returns a 'Firstname or Lastname is mismatch.' error.                                                   |
| Retrieve flight details of the different timezone of departure and arrival airport.          | Booking details are retrieved, and departure time is converted to the UK timezone (GMT), and arrival time is converted to BKK timezone. |
| Retrieve flight details of the same timezone of departure and arrival airport (Bangkok, ICT) | Booking details are retrieved, and both departure time and arrival time are converted to the Thailand (Bangkok, ICT) timezone.          |
| Update customer contact information and flight details                                       | Customer information is successfully updated, and name is verified via Passport API.                                                    |
| Attempt to update customer name with mismatched details in Passport API                      | Update fails. The Passport API returns a 'Firstname or Lastname is mismatch.' error.                                                    |
| Delete a valid booking                                                                       | Booking is successfully deleted from the system.                                                                                        |

## Mock Data and Services

- Each test case should use mock data specific to the customer and flight information.
- Passport API service should be stubbed using Wiremock or an equivalent tool.
  - Passport API is used for name verification.

## Bonus: GitHub Actions for Automation

- To ensure the automation test suite runs consistently, integrate the tests into a GitHub Actions pipeline.
- Goal: Configure a GitHub Action that triggers on every Pull Request (PR) build. This action should:
  1.  Set up the necessary environment (including Docker services).
  2.  Run the full suite of automated tests.
  3.  Report any failures back to the PR.

## **Assignment Submission Guidelines**

Candidates are required to create a public or private repository (accessible by the hiring team) on their own GitHub account for the assignment. Please follow these steps for submission:

1. **Fork or clone** this repository to your own GitHub account.
2. Implement the necessary tests and ensure all test scenarios mentioned above are covered using automation.
3. Configure GitHub Actions to run the test suite on each pull request (PR) build as a bonus.
4. Once completed, **push the code** to your repository.
5. Send us the **repository link** via email or the designated platform.
6. Add a description to this file explaining how to run the test and where to find the test results/report.

> **Note**: If your repository is private, ensure to grant access to the provided GitHub account for review.

# More resources

- [List of timezone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
- [Wiremock documentation](https://wiremock.org/docs/stubbing/)

## **[Submission] Test Guide**

The automated tests for the service are running on [pytest](https://docs.pytest.org/en/stable/) framework. Therefore, a minor change was made to `requirements.txt` as shown here.

```txt
...

# test deps
pytest # test framework
requests # http request
```

Any machine that wants to run the test must have these dependencies installed. It can be done via this command below:

```bash
pip install -r requirements.txt
```

> If there is a problem with the installation,
> installing just the test dependencies seperately should work as well since test runnner does not need other dependencies.

All tests are listed inside `/tests`. It consists of the following:

- `/tests/conftest.py`: shared config for all tests
- `/tests/test_test.py`: for sanity test
- `/tests/test_create_booking.py`: convert test scenario "Create a flight booking with valid customer and flight details" and "Attempt to create a booking with mismatched customer name in Passport API"
- `/tests/test_timezone.py`: convert test scenario "Retrieve flight details of the different timezone of departure and arrival airport." and "Retrieve flight details of the same timezone of departure and arrival airport (Bangkok, ICT)"
- `/tests/test_update_passenger.py`: convert test scenario "Update customer contact information and flight details" and "Attempt to update customer name with mismatched details in Passport API"
- `/tests/test_delete_passenger.py`: convert test scenario "Delete a valid booking"

Assuming docker compose and DB init are executed and the services are running, the test can be triggered via

```bash
pytest -v
```

> the `-v` is optional, but recommended for better visibility into individual test execution.

A full-passing test result looks like this:

```bash
tests/test_create_booking.py::test_create_booking_valid PASSED           [ 11%]
tests/test_create_booking.py::test_create_booking_already_exist PASSED   [ 22%]
tests/test_create_booking.py::test_create_booking_passport_mismatch PASSED [ 33%]
tests/test_delete_passenger.py::test_delete_passenger_valid PASSED       [ 44%]
tests/test_test.py::test_test PASSED                                     [ 55%]
tests/test_timezone.py::test_different_timezone_conversion PASSED        [ 66%]
tests/test_timezone.py::test_same_timezone_conversion PASSED             [ 77%]
tests/test_update_passenger.py::test_update_passenger_valid PASSED       [ 88%]
tests/test_update_passenger.py::test_update_passenger_mismatch PASSED    [100%]

============================== 9 passed in 0.99s ===============================
```

A few things to keep in mind: a particular test (`test/test_create_booking.py::test_create_booking_valid`) will fail if it is run more than once because creating an already existing booking for the same passenger is invalid.
I am not sure if I should make any changes to the service codebase, so I will just leave it as a note here.

That is pretty much it regarding `pytest`. Next, let's integrate this as a part of GitHub Actions.

### **GitHub Actions Test Integration**

The integration is done by adding `.github/workflows/ci.yml` into the repo. This file dictates how the pipeline runs. Here's a line-by-line breakdown.

```yml
name: CIhehe
```

The first line is pretty simple, "What is the name of the pipeline?".

```yml
on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]
```

The next section has `on` keyword. It acts as a rule for the determine when the pipeline should be triggered. In the case, the pipeline will be triggered when:

- There is a direct push or a merge into the `main` branch
- A pull request is opened with base branch is `main`

```yml
jobs:
  test:
    name: Test
    runs-on: ubuntu-latest
```

The next section is pipeline stages. Essentially, a pipeline consists of different stages that run in a certain sequence. For our case, there is only one stage, `Test`. Inside the stage, we tell the machine to prepare the specified environment for the task to run on (`ubuntu-latest`).

```yml
steps:
  - name: Checkout repo
    uses: actions/checkout@v4
  - name: Start services
    run: docker compose up -d
  - name: Wait for Postgres to be ready
    run: |
      echo "Waiting for postgres..."
      sleep 5
  - name: Init DB
    run: docker compose exec postgres bash /home/scripts/exec_sql.sh schema.sql
  - name: Install deps
    run: pip install -r requirements.txt
  - name: Run tests
    run: pytest -v
```

Lastly, the commands in a stage are listed in the `steps` block. From the code above, we:

- Check out the repo
- Build and start services
- Wait for the services to be ready: this is crucial since we cannot initialize the DB if there is none.
- Init DB
- Install deps: for this stage, only test dependencies are needed.
- Run tests

If any of the steps fail, the pipeline will be canceled and all artifacts will be cleaned
up.

### Future Improvements

- Database isolation per test: some tests depend on database state which should not be the case.
- Enforce test success before merge: the current CI reports the failed pipeline, but it does not prevent the bad push/merge from happening.
- More tests: service readiness, schema validation
- Environment variable integration: some configs are better to be read from environment variable for more flexibilities (dev/prod test).
