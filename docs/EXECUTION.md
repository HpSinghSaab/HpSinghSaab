# How to Execute Resource AI Platform on a Website

This guide details how to run the prototype web application on your local machine.

## Prerequisites
*   **Python 3.8+**: Ensure you have Python installed. You can verify this by running `python3 --version`.
*   **pip**: Python's package installer.

## Step 1: Install Dependencies
Navigate to the root directory of the project and install the required Python packages (Flask).

```bash
pip install -r requirements.txt
```

*(Note: If you haven't created a virtual environment, you might need to use `pip3` or run with `sudo` depending on your system configuration, but using a virtual environment is recommended).*

## Step 2: Start the Web Server
Run the Flask application using the following command from the project root:

```bash
export PYTHONPATH=$PYTHONPATH:.
python3 -m src.app
```

**Expected Output:**
```
 * Serving Flask app 'src.app'
 * Debug mode: off
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
```

## Step 3: Access the Website
Open your web browser (Chrome, Firefox, Safari, etc.) and navigate to:

**[http://127.0.0.1:5000](http://127.0.0.1:5000)**

## Features Available
Once the website is loaded, you will see three main tools:
1.  **Flow-Through Tax Calculator**: Calculate breakeven prices for tax-advantaged mining shares.
2.  **2025 Capital Gains Estimator**: Calculate tax liability based on the new June 2024 inclusion rules (50% vs 66.67%).
3.  **Drill Result Interpreter**: Paste text from a mining press release to extract grades and intervals.

## Troubleshooting
*   **ModuleNotFoundError**: Ensure you are running the command from the root folder and have set `export PYTHONPATH=$PYTHONPATH:.`.
*   **Port in use**: If port 5000 is taken, you can modify `src/app.py` to use a different port (e.g., `port=5001`).
