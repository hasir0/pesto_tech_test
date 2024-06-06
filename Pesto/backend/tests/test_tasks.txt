import unittest
from app import app, db, Task

class TaskTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_task(self):
        response = self.app.post('/tasks', json={'title': 'Test Task', 'description': 'Test Description', 'status': 'pending'})
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()
