# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## API Endpoints Documentation

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```json
{
    "success": False,
    "error": 404,
    "message": "not found"
}
```

The API will return two error types when requests fail:

- 404: Resource Not Found
- 422: Not Processable

### Endpoints

#### GET /api/v1/categories

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

#### GET /api/v1/categories/{category_id}/questions
- General
  - requests argument: category_id:int
  - gets all questions in the specified category and returns the questions in the specified category, success value, total number of questions in the specified category, and current category.
  - `curl http://127.0.0.1:5000/api/v1/categories/5/questions `

  ```json
  {
  "current_category": 5,
  "questions": [
    {
  "answer": "Apollo 13",
  "category": 5,
  "difficulty": 4,
  "id": 2,
  "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
  },
    {
  "answer": "Tom Cruise",
  "category": 5,
  "difficulty": 4,
  "id": 4,
  "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
  }
  ],
  "success": true,
  "total_questions": 2
  }
  ```

#### GET /api/v1/questions

- General:
  - Request parameters (optional): page:int
  - Returns a list of questions, a dictionary of categories, current category, success value, total questions
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1
- Sample: `curl http://127.0.0.1:5000/api/v1/questions`

```json
{
"categories": {
  1: "Science",
  2: "Art",
  3: "Geography",
  4: "History",
  5: "Entertainment",
  6: "Sports"
},
"currentCategory": "Science",
"questions": [
  {
  "answer": "Muhammad Ali",
  "category": 4,
  "difficulty": 1,
  "id": 9,
  "question": "What boxer's original name is Cassius Clay?"
},
  {
  "answer": "Apollo 13",
  "category": 5,
  "difficulty": 4,
  "id": 2,
  "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
},
  {
  "answer": "Tom Cruise",
  "category": 5,
  "difficulty": 4,
  "id": 4,
  "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
},
  {
  "answer": "Uruguay",
  "category": 6,
  "difficulty": 4,
  "id": 11,
  "question": "Which country won the first ever soccer World Cup in 1930?"
},
  {
  "answer": "George Washington Carver",
  "category": 4,
  "difficulty": 2,
  "id": 12,
  "question": "Who invented Peanut Butter?"
},
  {
  "answer": "Lake Victoria",
  "category": 3,
  "difficulty": 2,
  "id": 13,
  "question": "What is the largest lake in Africa?"
},
  {
  "answer": "The Palace of Versailles",
  "category": 3,
  "difficulty": 3,
  "id": 14,
  "question": "In which royal palace would you find the Hall of Mirrors?"
},
  {
  "answer": "Agra",
  "category": 3,
  "difficulty": 2,
  "id": 15,
  "question": "The Taj Mahal is located in which Indian city?"
},
  {
  "answer": "Escher",
  "category": 2,
  "difficulty": 1,
  "id": 16,
  "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
},
  {
  "answer": "Mona Lisa",
  "category": 2,
  "difficulty": 3,
  "id": 17,
  "question": "La Giaconda is better known as what?"
}
],
"success": true,
"totalQuestions": 22
}
```

#### POST /api/v1/quizzes
- General:
    - fetches one random question within a specified category. Previously asked questions are not asked again
    - request body: (previous_questions: list, quiz_category: {id:int, type:string})
    - returns a question object and success value

    `curl -X POST http://127.0.0.1:5000/api/v1/quizzes -H "Content-Type: application/json" -d '{"previous_questions":[],"quiz_category": {"id":"6", "type":"Sports"}}`

  ```json
  {
    "question": {
    "answer": "Uruguay",
    "category": 6,
    "difficulty": 4,
    "id": 11,
    "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    "success": true
  }
  ```

#### POST /api/v1/questions/search

- General:
    - request body: (question, answer, category, diificulty.)
    - Creates a new questions using the submitted title, author and rating. Returns the id of the created questions, success value, total questions, and questions list based on current page number to update the frontend.
- `curl -X POST http://127.0.0.1:5000/api/v1/questions  -H "Content-Type: application/json" -d '{"question": "Where does digestion start?", "answer": "mouth", "difficulty":2, "category":1}`

```json
  {
    "question": {
      "answer": "mouth",
      "category": 1,
      "difficulty": 2,
      "id": 41,
      "question": "Where does digestion start?"
    },
    "success": true
  }
```

#### POST /api/v1/questions/search
-General:
- Request body: searchTerm
  - Searches through the questions in the database for the given keywords. returns a list of all available questions which has the keyword, returns success value, and total number of questions gotten from the search, and current category.
  - `curl -X POST http://127.0.0.1:5000/api/v1/questions/search -H "Content-Type: application/json" -d '{"searchTerm":"ing"}`

  ```json
  {
    "current_category": "Science",
    "questions": [
      {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
      {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
      {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
    ],
    "success": true,
    "total_questions": 3
  }
  ```

#### DELETE /api/v1/questions/{question_id}

- General:
  - request arguments: question_id:int
  - Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value
- `curl -X DELETE http://127.0.0.1:5000/api/v1/questions/5`

```json
{
  "id": 5,
  "success": true,
}
```

## Deployment N/A

## Authors

Yours truly, Alex Kiborgok

## Acknowledgements

- Arthur Kalule
- Caryn McCarthy

## Testing
Tests are located in th test_flaskr.py file

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python3 test_flaskr.py
```
