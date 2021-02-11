import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category 


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('postgres:123456789@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """



    def test_categories_get(self):
        """Gets the /api/categories endpoint and checks valid results"""
        res = self.client().get('/api/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), 6)
        self.assertEqual(data['categories']['1'],'Science')

    def test_questions_get(self):
        """Gets all questions, including paginations (every 10 questions).  This endpoint should 
        return a list of questions, number of total questions, current category, categories."""
        res = self.client().get('/api/questions?page=1')
        data = json.loads(res.data)

        # This endpoint should default to page one, which should have id 5 first
        # and total questions of 19
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), 6)
        self.assertEqual(data['total_questions'], 19)
        self.assertEqual(len(data['questions']), 10)
        self.assertEqual(data['questions'][0]['id'], 5)

        """Tests the pagination by getting page 2 and looking for known features"""
        res = self.client().get('/api/questions?page=2')
        data = json.loads(res.data)

        # This endpoint should default to page one, which should have id 5 first
        # and total questions of 19
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), 6)
        self.assertEqual(data['total_questions'], 19)
        self.assertEqual(len(data['questions']), 9)     # Should be 9 left
        self.assertEqual(data['questions'][0]['id'], 15)

        """Make sure we get a 404 error on a page which we know doesn't exist"""
        res = self.client().get('/api/questions?page=9999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)  # Now using API-friendly custom error handlers
        self.assertEqual(data['error'], 404)

    def test_delete_question(self):
        """Create a new question, then test deleting it"""
        new_question = {
            "question": "How many spoons in a dish ?",
            "answer": "9",
            "category": "6",
            "difficulty": 3
        }
        # Create a test question to delete
        old_len = len(Question.query.all())
        new_question = Question(question=new_question['question'], answer=new_question['answer'], \
            category=new_question['category'], difficulty=new_question['difficulty'])
        new_question.insert()
        new_id = new_question.id

        # Test added successfully
        new_len = len(Question.query.all())
        self.assertEqual(new_len, old_len+1)    # 19 originally in test DB

        # Delete it through route
        res = self.client().delete(f'/api/questions/{new_id}')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], new_id)

        """Try to delete a question that doesn't exist, should get a 404 error"""
        res = self.client().delete(f'/api/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(data['error'], 404)
        
    def test_post_new_question(self):
        """POST a new question and make sure it's in there on the last page"""
        # Count first and before doing any changes
        new_question = {
            "question": "How many spoons in a dish ?",
            "answer": "9",
            "category": "6",
            "difficulty": 3
        }
        old_len = len(Question.query.all())

        self.assertEqual(old_len, 19)    # 19 originally in test DB

        # POST a new question using API endpoint
        res = self.client().post('/api/questions', json=new_question)
        data = json.loads(res.data)
        new_id = data['added']
       

        self.assertEqual(data['success'], True)
        self.assertEqual(len(Question.query.all()), old_len + 1) 
        
        # Delete question from database again with another client request.  
        # API returns the primary key
        res = self.client().delete(f'/api/questions/{new_id}')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], new_id)

    def test_get_questions_of_category(self):
        """Test GET request of questions only by a certain category"""
        # Get all the questions for Geography (id=3), should be 3 questions
        res = self.client().get('/api/categories/5/questions')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 3)

        # Get questions for category 100 (doesn't exist, should 404)
        res = self.client().get('/api/categories/999/questions')
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)

    def test_question_search(self):
        """Search for a term in a question"""
        res = self.client().post('/api/questions/search', json={"searchTerm": "title"})   # Who invented Peanut Butter?
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 2)
        self.assertEqual(data['questions'][0]['id'], 5)

    # For testing the Quiz:
    # 
    # We'll test on the Geography category (3), which has 3 questions [13, 14, 15]
    # 
    # From Developer Tools, examples of the Request Payload looks like this:
    # {previous_questions: [], quiz_category: {type: "click", id: 0}} # 0 is ALL
    # {previous_questions: [], quiz_category: {type: "Art", id: "2"}}
    # {previous_questions: [17, 16, 18], quiz_category: {type: "Art", id: "2"}}

    def test_play_quiz_1(self):
        """Tests out the quiz playing functionality"""
        # Test Quiz when all 3 questions are left
        res = self.client().post('/api/quizzes', json={"previous_questions": [], "quiz_category": {"type": "Entertainment", "id": "5"}})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)                 # check success
        self.assertIsNotNone(data['question'])                  # check question is not blank
        self.assertEqual(data['question']['category'], 5)       # check correct category

    def test_play_quiz_2(self):
        """Tests out the quiz playing functionality"""
        # Test Quiz when 2 of 3 have been asked and only one choice left (15)
        res = self.client().post('/api/quizzes', json={"previous_questions": [2, 6], "quiz_category": {"type": "Entertainment", "id": "5"}})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)                 # check success
        self.assertEqual(data['question']['id'], 4)            # check question 15 returns (only choice left)
        
    def test_play_quiz_3(self):
        """Tests out the quiz playing functionality"""
        # Test Quiz when no questions are left in category
        res = self.client().post('/api/quizzes', json={"previous_questions": [2, 4, 6], "quiz_category": {"type": "Entertainment", "id": "5"}})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)                 # check success

    



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()