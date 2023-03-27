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

### 1. GET /questions

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
