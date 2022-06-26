from ast import Try
import os
from unicodedata import category
from flask import Flask, request, abort, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# Paginate helper function that return 10 questions per page


def paginate_questions(request, Question, search=None):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    if search:
        questions = Question.query.filter(
            Question.question.ilike("%{}%".format(search))
        ).slice(start, end).all()
        questions_to_display = [question.format() for question in questions]
        return questions_to_display

    questions = Question.query.slice(start, end).all()
    if len(questions) == 0:
        abort(404)
    questions_to_display = [question.format() for question in questions]
    return questions_to_display


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/api/v1/categories', methods=['GET'])
    # Retrieve categories function
    def get_categories():
        categories = Category.query.all()
        if len(categories) == 0:
            abort(404)
        categories_to_display = {category.format()["id"]: category.format()[
            "type"] for category in categories}
        return jsonify({
            'success': True,
            'categories': categories_to_display
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/api/v1/questions', methods=['GET'])
    # Retrieve paginated questions
    def get_questions():
        questions = paginate_questions(request, Question)
        categories = Category.query.all()
        if len(categories) == 0:
            abort(404)
        categories_to_display = {category.format()["id"]: category.format()[
            "type"] for category in categories}
        return jsonify({
            'success': True,
            'questions': questions,
            'totalQuestions': len(Question.query.all()),
            'categories': categories_to_display,
            'currentCategory': categories[0].type
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/api/v1/questions/<int:question_id>', methods=['DELETE'])
    # Delete a single question from the questions table with the specified
    # question_id
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            if question is None:
                abort(404)
            else:
                question.delete()
                return jsonify({
                    'success': True,
                    "id": question.id
                })
        except BaseException:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/api/v1/questions', methods=['POST'])
    # Insert a question into the questions database
    def create_question():
        body = request.get_json()

        question = body.get('question', None)
        answer = body.get('answer', None)
        difficulty = body.get('difficulty', None)
        category = body.get('category', None)
        if difficulty:
            difficulty = int(difficulty)
        if category:
            category = int(category)

        try:
            if question and answer and difficulty and category:
                question = Question(question=question, answer=answer,
                                    difficulty=difficulty, category=category)
                question.insert()
                return jsonify({
                    'success': True,
                    "question": question.format()
                })
            else:
                abort(422)
        except BaseException:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/api/v1/questions/search', methods=['POST'])
    # Get all questions that have a substring of the request body search term
    def search_question():
        body = request.get_json()

        search = body.get('searchTerm', None)
        try:
            if search is None:
                abort(404)
            total_found_questions = Question.query.filter(
                Question.question.ilike("%{}%".format(search))
            ).all()
            questions_to_display = paginate_questions(
                request, Question, search)
            categories = [category.format()
                          for category in Category.query.all()]
            return jsonify({
                'success': True,
                'current_category': categories[0]["type"],
                'questions': questions_to_display,
                'total_questions': len(total_found_questions)
            })
        except BaseException:
            abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/api/v1/categories/<int:category_id>/questions',
               methods=['GET'])
    # Retrieve all questions that are of the specified catecory id
    def get_questions_by_category(category_id):
        try:
            questions = Question.query.filter(
                Question.category == str(category_id)).all()
            return jsonify({
                'success': True,
                'questions': [question.format() for question in questions],
                'total_questions': len(questions),
                'current_category': category_id
            })
        except BaseException:
            abort(404)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/api/v1/quizzes', methods=['POST'])
    # Returns one random question within a specified category, and
    # previously returned questions are not returned
    def play():
        body = request.get_json()
        category = body.get('quiz_category', None)
        previous_questions = body.get('previous_questions')
        try:
            if category is None:
                abort(422)
            if category['type'] == 'click':
                questions_to_play = Question.query.filter(
                    Question.id.notin_((previous_questions))).all()
            else:
                category_questions = Question.query.filter(
                    Question.category == str(category['id']))
                questions_to_play = category_questions.filter(
                    Question.id.notin_((previous_questions))).all()

            random_question = questions_to_play[random.randrange(
                0, len(questions_to_play))].format() if len(questions_to_play) > 0 else None

            return jsonify({
                'success': True,
                'question': random_question
            })
        except BaseException:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": 'unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'bad request'
        }), 400

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": 'method not allowed'
        }), 405

    return app
