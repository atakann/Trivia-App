import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random


from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    """
    Initializes and configures the Flask app, setting up CORS and the database connection.
    """
    app = Flask(__name__)
    setup_db(app)


    CORS(app, resources={r"*":  {"origins": "*"}})


    @app.after_request
    def after_request(response):
        """
        Adds Access-Control-Allow headers to the response.
        :param response: HTTP response object
        :return: HTTP response object with added headers
        """
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response


    @app.route('/categories', methods=["GET"])
    def get_categories():
        """
        Handles GET requests for all available categories.
        :return: JSON object containing a list of categories
        """
        categories = Category.query.all()
        formatted_categories = {category.id: category.type for category in categories}
        return jsonify({
            'success': True,
            'categories': formatted_categories
        })

    
    def paginate_questions(request, all_questions):
        """
        Paginates a list of questions.
        :param request: HTTP request object
        :param all_questions: list of all questions
        :return: list of paginated questions
        """
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = [question.format() for question in all_questions[start:end]]
        return questions

    @app.route('/questions', methods=['GET'])
    def get_paginated_questions():
        """
        Handles GET requests for questions, including pagination.
        :return: JSON object containing a list of paginated questions, total questions count, and categories
        """
        all_questions = Question.query.order_by(Question.id).all()
        questions = paginate_questions(request, all_questions)
        categories = Category.query.all()
        formatted_categories = {category.id: category.type for category in categories}

        if len(questions) == 0:
            abort(404)
        
        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': len(all_questions),
            'categories': formatted_categories,
            'current_category': None
        })
    

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """
        Handles DELETE requests for questions using a question ID.
        :param question_id: ID of the question to delete
        :return: JSON object indicating the success of the deletion
        """
        question = Question.query.filter(Question.id == question_id).one_or_none()

        if question is None:
            abort(404)

        question.delete()
        return jsonify({
            'success': True,
            'deleted': question_id
        })


    @app.route('/questions', methods=['POST'])
    def create_question():
        """
        Handles POST requests for creating a new question.
        :return: JSON object indicating the success of the creation and the ID of the new question
        """
        body = request.get_json()
        if not ('question' in body and 'answer' in body and 'difficulty' in body and 'category' in body):
            abort(422)
        
        new_question = Question(
            question=body.get('question'),
            answer=body.get('answer'),
            difficulty=body.get('difficulty'),
            category=body.get('category')
        )
        new_question.insert()

        return jsonify({
            'success':True,
            'created': new_question.id
        })


    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        """
        Handles POST requests for searching questions based on a search term.
        :return: JSON object containing a list of questions containing the search term
        """
        body = request.get_json()
        search_term = body.get('searchTerm', '')

        if search_term == '':
            abort(422)
        
        search_results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        formatted_questions = [question.format() for question in search_results]

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(search_results),
            'current_category': None
        })


    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        """
        Handles GET requests for questions based on category.
        :param category_id: ID of the category to filter questions by
        :return: JSON object containing a list of questions in the specified category
        """
        category = Category.query.filter_by(id=category_id).one_or_none()
        if category is None:
            abort(404)
        
        questions = Question.query.filter_by(category=category_id)
        formatted_questions = [question.format() for question in questions]

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(questions),
            'current_category': category.type
        })


    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        """
        Handles POST requests for playing the quiz game, returning a random question from the specified category.
        :return: JSON object containing a random question within the specified category
        """
        body = request.get_json()
        previous_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category', None)

        if quiz_category is None:
            abort(422)
        
        if quiz_category['id'] == 0:
            questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
        else:
            questions = Question.query.filter(Question.category == quiz_category['id'], Question.id.notin_(previous_questions)).all()
        
        if not questions:
            return jsonify({
                'success': True,
                'question': None
            })

        question = random.choice(questions).format()

        return jsonify({
            'success': True,
            'question': question
        })


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable entity'
        }), 422
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500

    return app