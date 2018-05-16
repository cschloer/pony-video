from django.test import TestCase, Client
from django.contrib.auth.models import User

from .models import BlogPost

class BlogPostTestCase(TestCase):
    def setUp(self):
        self.test_user_1 = User.objects.create_user(username='testuser1', password='12345')
        self.test_user_2 = User.objects.create_user(username='testuser2', password='12345')
        BlogPost.objects.create(title='Title 1', body='Just writing a first test', user=self.test_user_1)
        BlogPost.objects.create(title='Title 2', body='Just writing a second test', user=self.test_user_2)

    def test_model(self):
        post = BlogPost.objects.get(title='Title 1')
        self.assertEqual(post.body, 'Just writing a first test')
        self.assertEqual(post.user, self.test_user_1)

    def test_list_view(self):
        client = Client()
        request = client.get('/blog/')
        object_list = request.context_data['object_list']

        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(object_list), 2)
        self.assertEqual(object_list[0].title, 'Title 1')
        self.assertEqual(object_list[1].title, 'Title 2')

    def test_detail_view(self):
        client = Client()
        request = client.get('/blog/1')
        obj = request.context_data['object']

        self.assertEqual(request.status_code, 200)
        self.assertEqual(obj.title, 'Title 1')
        self.assertEqual(obj.body, 'Just writing a first test')
        self.assertEqual(obj.user, self.test_user_1)

    def test_create_view(self):
        client = Client()
        # Test that GET is protected
        request = client.get('/blog/create/')
        self.assertEqual(request.status_code, 302)

        request = client.post('/blog/create/', {'title': 'Title 3', 'body': 'Just writing a third test'})
        # Test that POST is protected
        self.assertEqual(BlogPost.objects.last().title, 'Title 2')


        # Now confirm that logging in fixes things up
        client.login(username='testuser1', password='12345')
        request = client.get('/blog/create/')
        self.assertEqual(request.status_code, 200)

        request = client.post('/blog/create/', {'title': 'Title 3', 'body': 'Just writing a third test'})
        self.assertEqual(request.status_code, 302)
        self.assertEqual(BlogPost.objects.last().title, 'Title 3')

    def test_update_view(self):
        client = Client()
        # Test that GET is protected
        request = client.get('/blog/update/1')
        self.assertEqual(request.status_code, 302)

        request = client.post('/blog/update/1', {'title': 'Title -1', 'body': 'Just writing a -1 test'})
        # Test that POST is protected
        self.assertEqual(BlogPost.objects.get(id=1).title, 'Title 1')

        # Now confirm that logging in fixes things up
        client.login(username='testuser1', password='12345')
        request = client.get('/blog/update/1')
        self.assertEqual(request.status_code, 200)

        request = client.post('/blog/update/1', {'title': 'Title -1', 'body': 'Just writing -1 third test'})
        self.assertEqual(request.status_code, 302)
        self.assertEqual(BlogPost.objects.get(id=1).title, 'Title -1')

        # Also confirm that you can't edit objects you're not an owner of
        request = client.post('/blog/update/2', {'title': 'Title -2', 'body': 'Just writing -2 third test'})
        self.assertEqual(request.status_code, 403)
        self.assertEqual(BlogPost.objects.get(id=2).title, 'Title 2')
