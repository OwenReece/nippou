from django.test import TestCase
from ..logic import nippou_api


class NippouApiTestCase(TestCase):

    def test_crud(self):
        username = "test_user"
        n = nippou_api.create(username)
        self.assertTrue(n)

        n = nippou_api.edit(n.id, {
            "title": "test_title",
            "body": "test_content"
        })
        n_edited = nippou_api.pickup(n.id)
        self.assertEqual(n.title, n_edited.title)

        nippou_api.delete(n.id)
        n_deleted = nippou_api.pickup(n.id)
        self.assertFalse(n_deleted)

