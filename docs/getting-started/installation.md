# Installation

## Prerequisites

Before installing CAI, ensure you have the following prerequisites:

- Python 3.11 or higher
- pip (Python package installer)
- OpenAI API key

## Installation Steps

## 1. Development Installation

The app is currently not available on PyPI, so you will need to install it from source.

1. Clone the repository:

```bash
git clone git@github.com:dullint/se_adaptive.git
```

This will install CAI in the current directory and make it editable.

1. Install the dependencies:

```bash
pip install -e .
```

To install the dependencies for testing and documentation too, run:

```bash
pip install -e .[test,docs]
```

If environment issues arise, we recommend to install `poetry` and use it to install the dependencies.

```bash
pip install poetry
poetry install
```

### 2. Environment Setup

CAI requires an OpenAI API key to function. Two options are available:

- Export the API key as an environment variable:

  ```bash
  export OPENAI_API_KEY=<your_openai_api_key>
  ```

- Create a `.env` file in your project root directory and add your API key:

  ```bash
  cp .env.example .env
  ```

  ```ini title=".env"
  OPENAI_API_KEY=<your_openai_api_key>
  ```

  !!! warning "API Key Security"
  Never commit your `.env` file to version control.

## Running the App

To run the app, use the following command:

```bash
cai-app
```

or with poetry:

```bash
poetry run cai-app
```

This will start the app in your default browser.
