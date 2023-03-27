## API Documentation

### 1. GET /categories

- Description: Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.
- Request Parameters: None
- Response Body:

  ```json
  {
    "success": True,
    "categories": {
      "1": "Science",
      "2": "Art",
      "3": "Geography",
      "4": "History",
      "5": "Entertainment",
      "6": "Sports"
    }
  }

### 2. GET /questions

- Description: Fetches a paginated list of questions, total number of questions, current category, and all categories.

- Request Parameters: None

- Query Parameters: page (optional) - The page number for pagination. Default is 1.

- Response Body:

  ```json
  {
  "success": True,
  "questions": [
    {
      "id": 1,
      "question": "Example question",
      "answer": "Example answer",
      "category": 1,
      "difficulty": 2
    },
    ...
  ],
  "total_questions": 100,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
    },
  "current_category": None
  }

### 3. DELETE /questions/{question_id}

- Description: Deletes a question using a question ID.

- Request Parameters: question_id - The ID of the question to be deleted.

- Response Body:

  ```json
  {
  "success": True,
  "deleted": 1
  }

### 4. POST /questions

- Description: Creates a new question with the specified question text, answer text, category, and difficulty score.

- Request Body:

  ```json
  {
    "question": "Example question",
    "answer": "Example answer",
    "category": 1,
    "difficulty": 2
  }

- Response Body:

  ```json
  {
  "success": True,
  "created": 1
  }

### 5. POST /questions/search

- Description: Searches for questions that contain the specified search term.

- Request Body:
  ```json
  {
    "searchTerm": "example"
  }

- Response Body:
  ```json
    {
    "success": True,
    "questions": [
        {
        "id": 1,
        "question": "Example question",
        "answer": "Example answer",
        "category": 1,
        "difficulty": 2
        },
        ...
    ],
    "total_questions": 10,
    "current_category": None
    }

### 6. GET /categories/{category_id}/questions

- Description: Fetches questions that belong to the specified category.

- Request Parameters:  `category_id` - The ID of the category.

- Response Body:
  ```json
    {
    "success": True,
    "questions": [
        {
        "id": 1,
        "question": "Example question",
        "answer": "Example answer",
        "category": 1,
        "difficulty": 2
        },
        ...
    ],
    "total_questions": 10,
    "current_category": "Science"
    }



### 7. POST /quizzes

- Description: Fetches a random question for a quiz. This endpoint takes the category and previous question parameters and returns a random question within the given category (if provided) and that is not one of the previous questions.

- Request Body:
  ```json
    {
    "previous_questions": [1, 2, 3],
    "quiz_category": {
        "type": "Science",
        "id": 1
    }
    }


- Response Body:
  ```json
    {
    "success": True,
    "question": {
        "id": 4,
        "question": "Example question",
        "answer": "Example answer",
        "category": 1,
        "difficulty": 2
    }
    }

