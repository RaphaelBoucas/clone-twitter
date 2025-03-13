from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserModelTest(TestCase):

    def setUp(self):
        """Configuração inicial: cria dois usuários para os testes"""
        self.user1 = User.objects.create_user(username="user1", password="testpass")
        self.user2 = User.objects.create_user(username="user2", password="testpass")

    def test_user_creation(self):
        """Testa se um usuário pode ser criado corretamente"""
        user = User.objects.create_user(username="testuser", password="testpass")
        self.assertEqual(user.username, "testuser")

    def test_following(self):
        """Testa se um usuário pode seguir outro corretamente"""
        self.user1.follows.add(self.user2)
        self.assertIn(self.user2, self.user1.follows.all())
        self.assertIn(self.user1, self.user2.followed_by.all())  # Relacionamento reverso

    def test_unfollow(self):
        """Testa se um usuário pode deixar de seguir outro"""
        self.user1.follows.add(self.user2)
        self.user1.follows.remove(self.user2)
        self.assertNotIn(self.user2, self.user1.follows.all())

    def test_profile_image_upload(self):
        """Testa o upload de uma imagem de perfil"""
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        self.user1.profile_image = image
        self.user1.save()
        self.assertTrue(self.user1.profile_image.name.startswith("images/test_image"))

    def test_bio_fields(self):
        """Testa a atualização dos campos de bio"""
        self.user1.profile_bio = "Isso é um teste."
        self.user1.homepage_link = "https://meusite.com"
        self.user1.save()

        updated_user = User.objects.get(username="user1")
        self.assertEqual(updated_user.profile_bio, "Isso é um teste.")
        self.assertEqual(updated_user.homepage_link, "https://meusite.com")
