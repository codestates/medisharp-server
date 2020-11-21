from flask_seeder import Seeder, Faker, generator
from app.main.model.users import Users

# SQLAlchemy database model
class Users(Base):
  def __init__(self, full_name='test', email='test@gmail.com', password='testtest', mobile='010-1234-5678', login='basic'):
    self.full_name = full_name
    self.email = email
    self.password = password
    self.mobile = mobile
    self.login = login

  def __str__(self):
    return "Full_name=%s, Email=%s, Password=%s, Mobile=%s, Login=%s" % (self.full_name, self.email, self.password, self.mobile, self.login)

# All seeders inherit from Seeder
class DemoSeeder(Seeder):

  # run() will be called by Flask-Seeder
  def run(self):
    # Create a new Faker and tell it how to create User objects
    faker = Faker(
      cls=Users,
      init={
        "full_name": generator.String,
        "email": generator.String,
        "password": generator.String,
        "mobile": generator.String,
        "login": generator.String
      }
    )

    # Create 5 users
    for users in faker.create(1):
      print("Adding user: %s" % users)
      self.db.session.add(Users)