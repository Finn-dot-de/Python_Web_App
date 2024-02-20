import tornado.ioloop
import tornado.web
import mysql.connector

# Verbindung zur MySQL-Datenbank herstellen
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    database="Esap"
)

# Tornado-Handler für die Anzeige der Einsätze
class ErfassteEinsaetzeHandler(tornado.web.RequestHandler):
    def get(self):
        # Datenbankabfrage durchführen, um die erfassten Einsätze abzurufen
        cursor = conn.cursor()
        cursor.execute("SELECT s.start_date, s.end_date, s.status, m.name FROM schichten s INNER JOIN mitarbeiter m ON s.azubi_id = m.azubi_id")
        einsaetze = cursor.fetchall()
        

        # Datenbankabfrage durchführen, um die Azubis abzurufen
        cursor.execute("SELECT azubi_id, name FROM mitarbeiter")
        azubis = cursor.fetchall()
        

        print("Einsätze:", einsaetze)  # Überprüfen Sie die Struktur der Einsätze
        print("Azubis:", azubis)  # Überprüfen Sie die Struktur der Azubis

        # Daten in das HTML-Template einfügen
        self.render("template.html", einsaetze=einsaetze, azubis=azubis)

# Tornado-Anwendung konfigurieren
def make_app():
    return tornado.web.Application([
        (r"/einsaetze", ErfassteEinsaetzeHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)  # Der Webserver wird auf dem Port 8888 gestartet
    print("Server läuft auf http://localhost:8888/einsaetze")
    tornado.ioloop.IOLoop.current().start()
