
from models.db.users import User
from models.db.roles import Roles
from api.client.db import DBClient

client = DBClient(url="postgresql://postgres:sql@192.168.72.11:5432/aa_test")

if __name__ == '__main__':
    user = User(id=111, username='123', password='333')
    # user = client.base.read_all(model=User, where={})
    # client.users.create(user)
    a = client.users.read_all()
    print(a)





    #
    # a = client.base.read_by(User, filter={'deleted': 'false'}, limit=1)
    # print(a)

