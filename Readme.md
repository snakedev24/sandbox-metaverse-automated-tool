# Sandbox Metaverse Automated Tool

## Project Overview

The Sandbox Metaverse Automated Tool is designed to streamline interactions within the Sandbox Metaverse platform. This tool leverages web scraping, automation, and data processing techniques to facilitate various tasks, such as data extraction, manipulation, and automated actions within the metaverse environment.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/snakedev24/sandbox-metaverse-automated-tool.git
    cd sandbox-metaverse-automated-tool
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Ensure the virtual environment is activated.
2. Run the main script:
    ```bash
    python main.py
    ```

## Dependencies

The project relies on the following libraries:

- `pandas`: For data manipulation and analysis.
- `beautifulsoup4`: For web scraping and HTML parsing.
- `requests`: For making HTTP requests.
- `selenium`: For browser automation.
- `pyperclip`: For clipboard operations.

## Configuration

### Selenium WebDriver

Ensure you have the appropriate WebDriver installed for your browser (e.g., ChromeDriver for Google Chrome). Place the WebDriver executable in your PATH or specify its location in the script.
