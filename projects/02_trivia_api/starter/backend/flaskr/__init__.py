import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate(page, data):
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  paginatedData = []
  for question in data[start:end]:
    paginatedData.append(question.format())
  if len(paginatedData)==0:
    raise Exception('page does not exist')

  return paginatedData

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/api/categories')
  def categories_get():
    try:
      categories = Category.get.all()
      categories_dict = {}
      for category in categories:
        categories_dict = {category.id:category.type}

      return jsonify({
                "success": True,
                "categories": categories_dict
            })

    except:
      abort(500)
  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/api/questions')    
  def questions_get():
    try:
      questions = Question.query.all()
      questions_count = len(questions)
      page = request.args.get('page', 1, type=int)
      questions_list = paginate(page,questions)

      categories = Category.get.all()
      categories_dict = {}
      for category in categories:
        categories_dict = {category.id:category.type}      
      return jsonify({
        'success': True,
        'questions': questions_list,
        'total_questions': questions_count,
        'categories': categories_dict,
        'current_category': None
      })
    except:
      abort(404) 
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/api/questions/<int:id>', methods=['DELETE'])
  def question_delete(id):
    question = Question.query.get(id)

    if not question:         
     abort(404)
    else:
            
      try:
        question.delete()   

        return jsonify({
          'success': True,
          'deleted': id
        })
      except:
        abort(422)  
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/api/questions', methods=['POST'])
  def question_post():     
    data = request.json

    if (data['question'].strip() == " ") or (data['answer'].strip() == " "):
    # Don't populate blanks, return a bad request error
      abort(400)

    try:
      new_question = Question(question=form_data['question'].strip(), answer=form_data['answer'].strip(), \
      category=form_data['category'], difficulty=form_data['difficulty'])
      new_question.insert()
    except:
    # Issue creating new question?  422 means understood the request but couldn't do it
      abort(422)

    return jsonify({
      "success": True,
      "added": new_question.id
    })

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/api/questions/search', methods=['POST'])
  def question_post():
    data = request.json
    search_term = data['searchTerm'].strip()

    # Use filter, not filter_by when doing LIKE search (i=insensitive to case)
    questions_filtered = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()   # Wildcards search before and after
            
    # Still good idea to paginate since search could return a ton (entire list if you search "", 
    # which project doesn't exclude).  However Search Questions view in Frontend doesn't already include
    # support for pagination, so this time I won't do it (or you can't see all valid search results).
    #q_list = paginate(request, questions)
    q_list = [q.format() for q in questions]

    return jsonify({
      "success": True,
      "questions": q_list
    })

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/api/categories/<int:cat_id>/questions')
  def get_category_questions(cat_id):
  '''GET all the questions based on a particular category'''
    questions = Question.query.filter_by(category=str(cat_id)).all()

    q_list = paginate(request, questions)

    if len(q_list) == 0:
    # Requested a page past what exists
      abort(404)

    return jsonify({
      'success': True,
      'questions': q_list,
      'total_questions': len(questions),
      'categories': Category.query.get(cat_id).format(),
      'current_category': cat_id
     })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    