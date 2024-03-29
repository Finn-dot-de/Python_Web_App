import tornado.ioloop
import tornado.web
import mysql.connector
from datetime import datetime, timedelta

db_connection = mysql.connector.connect(
    host="localhost",
    user="ly04",
    password="password",
    database="azubis"
)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        start_date = self.get_argument("start_date", "")
        end_date = self.get_argument("end_date", "")

        if not start_date:
            start_date = datetime.now().date()
        if not end_date:
            end_date = datetime.now().date() + timedelta(days=7)

        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM Employees")
        employees = cursor.fetchall()

        sql = "SELECT date, employee_id, status FROM Shifts WHERE date BETWEEN %s AND %s"
        cursor.execute(sql, (start_date, end_date))
        data = cursor.fetchall()

        employee_entries = {}
        for row in data:
            date, employee_id, status = row
            if date not in employee_entries:
                employee_entries[date] = {}
            employee_entries[date][employee_id] = status

        employee_list = {employee_id: name for employee_id, name in employees}

        for date in employee_entries:
            for employee_id in employee_list:
                if employee_id not in employee_entries[date]:
                    employee_entries[date][employee_id] = 0 

        self.render("template.html", employee_entries=employee_entries, employee_list=employee_list)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
