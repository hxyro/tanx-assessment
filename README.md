# Files

- [`task.py`](./task.py): This file contains all the task-related code.
- [`test.py`](./test.py): This file contains all the test cases.
- [`orders.csv`](./orders.csv): This file contains the dataset. | [Google Sheets](https://docs.google.com/spreadsheets/d/1cVe7fjC4fWmSQCKhS3TYYkWYNYNFx-FVSHikLMP2UlI/edit?usp=sharing)

## Clone the repositery
```
  git clone https://github.com/hxyro/tanx-assessment.git
  cd tanx-assessment
```
## Run on Local System:
Make sure you have the correct Python version installed:
```
python --version
```

Create a Python virtual environment and install all required packages
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the tests
```
python -m unittest test
```

Run the main task

```
python task.py
```

## Run Using Docker

Make sure you have Docker and Docker Compose installed

```
docker --version
docker-compose --version
```

Run the tests
```
docker-compose up test
```

Run the task
```
docker-compose up task
```
---
<b>`NOTE`</b>: Due to the large number of data entries in orders.csv, the output is limited to 50 lines.
