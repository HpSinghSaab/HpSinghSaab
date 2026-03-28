# Resource AI Platform

## Overview
**Resource AI Platform** is a specialized investment research tool designed for the Canadian Resource and Venture market. It addresses the "Canadian Gap" left by generalist platforms like FinChat and Koyfin, which are optimized for large-cap US equities.

This platform focuses on:
*   **The Drill Bit**: Understanding geological data (grade, width, recovery rates) as the primary value driver for pre-revenue explorers.
*   **Structured Data from Unstructured Sources**: extracting insights from NI 43-101 Technical Reports and PDF assay tables.
*   **Tax-Alpha**: Tools for Flow-Through Shares and Warrant tracking.
*   **Capital Gains Planning**: Estimating tax liability under the new 2025 Canadian inclusion rules.

## Key Features
*   **Geo-LLM Prototype**: Regex-based drill result parser.
*   **Drill Result Interpreter**: Automated parsing and normalization of drill intercepts.
*   **Flow-Through Calculator**: Real-time calculation of effective breakeven prices for tax-advantaged financing.
*   **2025 Capital Gains Estimator**: Logic for tiered inclusion rates (50% vs 66.67%).

## Getting Started

### Prerequisites
*   Python 3.8+
*   Flask

### Installation
1.  Clone the repository.
2.  Install dependencies: `pip install -r requirements.txt`

### Usage

**Run the Web Application:**
See [docs/EXECUTION.md](docs/EXECUTION.md) for detailed instructions.

```bash
export PYTHONPATH=$PYTHONPATH:.
python3 -m src.app
```
Then open `http://127.0.0.1:5000` in your browser.

**Run the CLI:**
```bash
export PYTHONPATH=$PYTHONPATH:.
python3 src/main.py
```

## Documentation
*   [Execution Guide](docs/EXECUTION.md)
*   [Strategic Vision](docs/STRATEGY.md)
*   [Implementation Roadmap](docs/ROADMAP.md)

## License
MIT
