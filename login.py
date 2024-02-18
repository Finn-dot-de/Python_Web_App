import tornado.ioloop
import tornado.web
import psycopg2
import bcrypt


# Funktion zum Hashen eines Passworts
def hash_password(password):
    salt = bcrypt.gensalt(12)
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password


# Funktion zum Überprüfen eines Passworts
def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)


# Funktion zum Durchführen einer sicheren SQL-Abfrage
def login(username, password):
    conn = psycopg2.connect(
        dbname="your_database_name",
        user="your_database_user",
        password="your_database_password",
        host="your_database_host",
        port="5000",
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    conn.close()
    return user


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(
            """<html><body><form action="/login" method="post" style="max-width: 300px; margin: 0 auto; padding: 20px; border: 1px solid #ccc; border-radius: 5px;">
                   Name: <input type="text" required name="name" style="width: 100%; padding: 10px; margin-bottom: 10px; border-radius: 5px; border: 1px solid #ccc;">
                   Password: <input type="password" required name="password" style="width: 100%; padding: 10px; margin-bottom: 10px; border-radius: 5px; border: 1px solid #ccc;">
                   <input type="submit" value="Sign in" style="width: 100%; padding: 10px; border-radius: 5px; border: none; background-color: #4CAF50; color: white; cursor: pointer;">
                   </form></body></html>"""
        )


class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        username = self.get_argument("name")
        password = self.get_argument("password")

        user = login(username, password)

        if user and verify_password(
            password, user[1]
        ): 
            self.write("Login erfolgreich!")
        else:
            self.write("Login fehlgeschlagen!")


def make_app():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/login", LoginHandler),
        ]
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
