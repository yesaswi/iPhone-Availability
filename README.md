# iPhone Availability Checker

## Description

This tool is a Python-based API that checks for iPhone availability in various Apple Stores. Upon providing a City and State, the API returns a JSON object detailing the available iPhone models in the corresponding Apple Stores. As of now, this API is configured to check availability within the United States, however, it can be easily tailored to serve other countries as well.

## Usage

### Requirements

- Python 3.6+
- FastAPI
- requests
- pandas

### Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/username/iphone-availability-checker.git
```

2. Navigate to the project directory:

```bash
cd iphone-availability-checker
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Run the API:

```bash
uvicorn main:app --host '0.0.0.0' --port '8080' --reload
```
The application should now be running at `http://localhost:8080` / `http://<ip>:8080`.

1. Navigate to the following URL in your browser:

```bash
http://localhost:8080/docs
```

2. Enter the City and State in the corresponding fields and click on the "Try it out!" button. The API will return a JSON object detailing the available iPhone models in the corresponding Apple Stores.



### Endpoints

- `POST /availability`: Checks the availability of iPhones in the provided city and state.

Request body:
```json
{
    "city": "Chicago",
    "state": "IL"
}
```

3. To stop the API, press `Ctrl + C` in the terminal.

4. To run the API in the background, use the following command:

```bash
nohup uvicorn main:app --host '0.0.0.0' --port '8080' --reload &
```
