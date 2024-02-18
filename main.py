import tornado.ioloop
import tornado.web
import mysql.connector
from datetime import datetime, timedelta


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # Datenbereich aus dem Formular abrufen
        start_date = self.get_argument("start_date", default=None)
        end_date = self.get_argument("end_date", default=None)

        # Wenn keine Daten bereitgestellt wurden, verwende Standardbereich von heute bis 365 Tage später
        if not start_date or not end_date:
            start_date = datetime.now().date()
            end_date = start_date + timedelta(days=365)
        else:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        # Verbindung zur MySQL-Datenbank herstellen
        db_connection = mysql.connector.connect(
            host="localhost", user="ly04", password="password", database="azubis"
        )

        # Cursor erstellen
        cursor = db_connection.cursor()

        # Daten aus der Datenbank abrufen basierend auf dem Datumsbereich
        cursor.execute(
            "SELECT e.name, s.date, s.status FROM Employees e LEFT JOIN Shifts s ON e.id = s.employee_id AND s.date BETWEEN %s AND %s",
            (start_date, end_date),
        )
        employee_data = cursor.fetchall()

        # Verbindung schließen
        cursor.close()
        db_connection.close()

        # Eine leere Liste erstellen, um alle Mitarbeiter-IDs zu speichern
        employee_ids = set(range(1, 10))

        # Eine Liste mit den Daten aller Mitarbeiter erstellen
        employee_entries = []

        # Durchlauf der Datenbankergebnisse
        for entry in employee_data:
            employee_ids.discard(
                entry[0]
            )  # Entfernen der Mitarbeiter-ID aus der Set, wenn ein Eintrag gefunden wird
            employee_entries.append(
                (entry[1], entry[2])
            )  # Hinzufügen des Eintrags zur Liste der Mitarbeiterdaten

        # Hinzufügen der fehlenden Mitarbeiter mit leeren Einträgen
        # Hinzufügen der fehlenden Mitarbeiter mit leeren Einträgen

        # Hinzufügen der fehlenden Mitarbeiter mit leeren Einträgen
       # Durchlaufen der fehlenden Mitarbeiter und Hinzufügen von Einträgen mit leeren Werten
        for missing_employee_id in employee_ids:
            for i in range(365):
                date_to_insert = start_date + timedelta(days=i)
                # Fügen Sie Einträge für fehlende Mitarbeiter mit leeren Werten hinzu
                employee_entries.append((date_to_insert, missing_employee_id, 0))  # 0 für "Abwesend"

        # HTML-Template rendern und Daten einfügen
        self.render("template.html", employee_entries=employee_entries)



def make_app():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
        ]
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
