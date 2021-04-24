from django.test import TestCase
from django.contrib.auth.models import User
from tutorial.quickstart.models import Follow


class PutFollowTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username="Leon")
        self.user2 = User.objects.create(username="Kate")

    def test_simple_add_follow(self):
        self.assertEqual(Follow.objects.count(), 0)
        self.client.force_login(self.user1)
        response = self.client.post(f'/v1/follow/{self.user2.username}/')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Follow.objects.count(), 1)

    def test_simple_delete_follow(self):
        self.assertEqual(Follow.objects.count(), 0)
        self.client.force_login(self.user1)
        self.client.post(f'/v1/follow/{self.user2.username}/')
        self.assertEqual(Follow.objects.count(), 1)
        response = self.client.delete(f'/v1/follow/{self.user2.username}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Follow.objects.count(), 0)

    # def test_add_follow_twice_without_errors(self):
    #     self.assertEqual(Follow.objects.count(), 0)
    #     self.client.force_login(self.user1)
    #     self.assertEqual(self.client.post(f'/v1/follow/{self.user2.username}/').status_code, 201)
    #     self.assertEqual(Follow.objects.count(), 1)
    #     self.assertEqual(self.client.post(f'/v1/follow/{self.user2.username}/').status_code, 201)
    #     self.assertEqual(Follow.objects.count(), 1)


class GetUserTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="Leon")

    def test_get_existing_user_200(self):
        response = self.client.get(f'/v1/users/{self.user.username}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['username'], self.user.username)

    def test_get_not_existing_user_404(self):
        self.assertEqual(self.client.get(f'/v1/users/incorrect/').status_code, 404)


class GetUsersTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username="Leon")
        self.user2 = User.objects.create(username="Kate")
        self.user3 = User.objects.create(username="John")

    def test_get_users_all(self):
        response = self.client.get(f'/v1/users/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['count'], 3)
        self.assertEqual(
            [r['username'] for r in data['results']],
            [self.user3.username, self.user2.username, self.user1.username]
        )

    def test_get_users_page_1(self):
        response = self.client.get(f'/v1/users/', {'page': 1})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['count'], 3)
        self.assertEqual(
            [r['username'] for r in data['results']],
            [self.user3.username, self.user2.username, self.user1.username]
        )

    def test_get_users_page_2(self):
        self.assertEqual(self.client.get(f'/v1/users/', {'page': 2}).status_code, 404)

#
# class GetUserFollowersAndFollowsTestCase(TestCase):
#
#     def setUp(self):
#         self.user1 = User.objects.create(username="Kelly")
#         self.user2 = User.objects.create(username="Molly")
#         self.user3 = User.objects.create(username="Sally")
#         Follow.objects.create(follower=self.user1, follows=self.user2)
#         Follow.objects.create(follower=self.user3, follows=self.user1)
#         Follow.objects.create(follower=self.user3, follows=self.user2)
#
#     def test_user3_followed_by_nothing(self):
#         response = self.client.get(f'/v1/users/{self.user3.username}/followed/')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()['count'], 0)
#
#     def test_user2_follows_nothing(self):
#         response = self.client.get(f'/v1/users/{self.user2.username}/follows/')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()['count'], 0)
#
#     def test_user1_followed_by_one(self):
#         response = self.client.get(f'/v1/users/{self.user1.username}/followed/')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()['count'], 1)
#         self.assertEqual(response.json()['results'][0]['follower']['username'], self.user3.username)
#
#     def test_user1_follows_one(self):
#         response = self.client.get(f'/v1/users/{self.user1.username}/follows/')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()['count'], 1)
#         self.assertEqual(response.json()['results'][0]['follows']['username'], self.user2.username)
#
#     def test_user2_followed_by_several(self):
#         response = self.client.get(f'/v1/users/{self.user2.username}/followed/')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()['count'], 2)
#
#     def test_user3_follows_several(self):
#         response = self.client.get(f'/v1/users/{self.user3.username}/follows/')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()['count'], 2)


from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.

class UserTestCase(TestCase):

    def test_simple (self):
        self.assertEqual(1 + 1, 2)

    def test_unknown_url(self):
        response = self.client.get('/incorrect')
        self.assertEqual(response.status_code,404)

    def test_list_user_with_one_user(self):
        User.objects.create(username='Alex')
        response = self.client.get('/v1/users/')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),
        {
            "count": 1,
            "next": None,
            "previous": None,
            "results":
            [
                {
                    "url": "http://127.0.0.1:8000/v1/users/Alex/",
                    "username": "Alex",
                    "email": "",
                    "last_name": "",
                    "first_name": "",
                }
            ]
        }
    )

    def test_new_folow_correct(self):
        response = self.client.get('/v1/follow/MO')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Follow.objects.filter(follows = self.user3,
                                               follower= self.user1))

        self.assertIsNone(Follow.objects.get(follows = self.user3,
                                             follower= self.user1))

    def test_unfollow_correct(self):
        self.client.force_login(self.user1)
        response = self.client.delete(f'/v1/follow/{self.user2.username}')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Follow.objects.count(),1)

    #
    # def test_follow_yourself_faild(self):
    #     self.client.force_login(self.user1)
    #     response = self.client.delete(f'/v1/follow/{self.user1.username}')
    #     self.assertEqual(response.status_code, 400)


    def test_unfollow_not_exist_faild(self):
        self.client.force_login(self.user1)
        response = self.client.post(f'/v1/follow/{self.user1.username}')
        self.assertEqual(response.status_code, 400)

    # def test_follow_duplicate_faild(self):