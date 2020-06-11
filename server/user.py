import sqlite3
from flask_restx import Namespace, Resource

api = Namespace('users', description='User resources')


# ---------------------------------------------------------------------------
@api.route('/users/<int:user_id>')
@api.param('user_id', description='User ID')
class User(Resource):
    def get(self, user_id):
        db = sqlite3.connect('db.sqlite')
        c = db.cursor()
        c.execute("select * from appuser where id = ?", (user_id,))
        print(c.fetchone())
        for id, name in c:
            return {"id": id, "name": name}


# ---------------------------------------------------------------------------
@api.route('/users', methods=['GET'])
@api.route('/users/<string:user_name> <int:user_id>', methods=['POST'])
@api.param('user_name', description='User Name')
@api.param('user_id', description='User ID')
class AllUsers(Resource):
    def get(self):
        db = sqlite3.connect('db.sqlite')
        c = db.cursor()
        c.execute("select * from appuser")
        users = c.fetchall()
        output = {}
        output2 = []
        for i, user in enumerate(users):
            output.update({i: {"id": user[0], "name": user[1]}})  # Вид с нумерацией
            output2.append({"id": user[0], "name": user[1]})  # Вид без нумерации, массивом
        print(output)
        print(output2)
        return output

    def post(self, user_name, user_id):
        print(user_name)
        print(user_id)
        db = sqlite3.connect('db.sqlite')
        c = db.cursor()
        if user_id:
            c.execute("INSERT INTO appuser VALUES (?, ?)", (user_id, user_name))
            # Вставка пользователя с заданными именем и id
        else:
            c.execute("INSERT INTO appuser VALUES (0, ?)", (user_name,))
            # Вставка пользователя с заданным именем и 0 id, При возможности создания БД с auto_increment, будет добавлен последним
            # Для этого необходимо изменить @api.route и @api.param
            # @api.route('/users/<string:user_name>', methods=['POST'])
            # @api.param('user_name', description='User Name')
        db.commit()
        return "Successfully added"
