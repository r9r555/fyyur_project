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
      categories = Category.query.all()
      categories_dict = {}
      for category in categories:
        categories_dict[category.id] = category.type

      return jsonify({
                "success": True,
                "categories": categories_dict
            })

    except Exception as e:
      print(f'Exception "{e}"')
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

      categories = Category.query.all()
      categories_dict = {}
      for category in categories:
        categories_dict[category.id] = category.type      
      return jsonify({
        'success': True,
        'questions': questions_list,
        'total_questions': questions_count,
        'categories': categories_dict,
        'current_category': None
      })
    except Exception as e:
      print(f'Exception "{e}"')
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
      except Exception as e:
        print(f'Exception "{e}"')
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
    question = data['question'].strip()
    answer = data['answer'].strip()
    category = data['category']
    difficulty=data['difficulty']
    try:
      new_question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
      new_question.insert()
    except Exception as e:
      print(f'Exception "{e}" ')
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
  def question_search():
    data = request.json
    search_term = data['searchTerm'] 
    # Use filter, not filter_by when doing LIKE search (i=insensitive to case)
    questions_filtered = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()   # Wildcards search before and after
            
    # Still good idea to paginate since search could return a ton (entire list if you search "", 
    # which project doesn't exclude).  However Search Questions view in Frontend doesn't already include
    # support for pagination, so this time I won't do it (or you can't see all valid search results).
    #q_list = paginate(request, questions)
    question_list = []
    for question in questions_filtered:
      question_list.append(question.format())

    return jsonify({
      "success": True,
      "questions": question_list
    })

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/api/categories/<int:id>/questions')
  def get_category_questions(id):
    questions = Question.query.filter_by(category=str(id)).all()
    questions_count = len(questions)
    page = request.args.get('page', 1, type=int)
    questions_list = paginate(page,questions)

    return jsonify({
      'success': True,
      'questions': questions_list,
      'total_questions': questions_count,
      'categories': Category.query.get(id).format(),
      'current_category': id
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
  @app.route('/api/quizzes', methods=['POST'])
  def play_quiz():
    data = request.json
    question = []
    try:
      categ_id = data['quiz_category']['id']
      prev_quest = data['previous_questions']
      if categ_id == 0:
        questions = Question.query.filter(Question.id.notin_(prev_quest))
        questions = [q.format() for q in questions]
        question = random.choice(questions)
      else:
        #questions = Question.query.filter(Question.id.notin_(prev_quest) and_ Question.category = str(categ_id))
        questions = [q.format() for q in questions]
        question = random.choice(questions)   
    except Exception as e:
      print(f'Exception "{e}" ')
      abort(422)
    return jsonify({
      'success': True,
      'question': question
    })

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "Bad Request"
    })

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Not found"
    })

  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "Unprocessable Entity"
    })

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "Internal Server Error"
    })

  return app

    