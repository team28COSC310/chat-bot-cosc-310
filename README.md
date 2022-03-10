# chat-bot-cosc-310


## Development Installation
1. Ensure you have the latest version of [Python](https://www.python.org/downloads/) installed.

2. Install `pipenv` ([Pipenv Documentation](https://pypi.org/project/pipenv/))
    1. Open the command terminal
    2. Run `pip install pipenv`

3. Download the project dependencies
    1. Open the command terminal in the project root directory
    2. Run `pipenv shell` to start the virtual environment
    3. Run `pipenv update --dev` to download the project's dependencies
    
## Running Unit Tests

- To run all tests run `python -m unittest discover -s ./`

- To run a specific test file:
    - Run the test file directly `python <test_file>.py`
    - Or run `python -m unittest <test_file>.<TestClass>`

- To run a specific test
    - Run `python -m unittest <test_file>.<TestClass>.<test_name>`

### Important Note: 
Run all tests from the `tests` directory. 
This ensures the mock files are located correctly by Python.

## Running the Application
Run `python chatbot_run.py` to start the application.

