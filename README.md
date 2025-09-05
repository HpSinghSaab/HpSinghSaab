# AI-Powered Operational Intelligence Suite

This repository contains the implementation of the AI-Powered Operational Intelligence Suite, based on the provided architectural blueprint. The first module being developed is the **Client Qualification & Scoping Engine (CQSE)**.

## Project Structure

- `src/cqse/`: Contains the core logic for the CQSE.
  - `models.py`: Pydantic data models for `IdealClientProfile` and `Lead`.
  - `scorer.py`: The lead scoring function.
- `tests/`: Unit tests for the project.
- `main.py`: A command-line script to demonstrate the basic scoring functionality.
- `api.py`: A FastAPI server to expose the scoring functionality via a web API.

## Setup

1.  Clone the repository.
2.  Install the required Python packages:
    ```bash
    pip install pydantic fastapi uvicorn
    ```

## Usage

### Running the Demo Script

To see a simple demonstration of the lead scoring engine, run the `main.py` script:

```bash
python3 main.py
```

This will score a sample good-fit lead and a poor-fit lead against the "High-Value Construction" ICP and print the results to the console.

### Running the API Server

To make the lead scoring engine available as a web service (e.g., for use with n8n), you can run the FastAPI server:

```bash
uvicorn api:app --reload
```

The API server will be running at `http://127.0.0.1:8000`.

### Testing the API Endpoint

You can test the `/score` endpoint by sending a `POST` request using a tool like `curl`.

**Example Request:**

This example sends the details of a lead who is a good fit for the ICP.

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/score' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "company_name": "SecureBuild Construction",
  "industry": "Construction",
  "self_reported_need": "We are having major issues with equipment theft and trespassing at our new site, leading to costly project delays."
}'
```

**Expected Response:**

```json
{
  "company_name": "SecureBuild Construction",
  "qualification_score": 3
}
```
