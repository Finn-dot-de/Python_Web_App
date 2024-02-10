import tornado.ioloop
import tornado.web
import json
import os

NOTES_FILE = "notes.json"


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        notes = self.load_notes()
        self.render("index.html", notes=notes)

    def load_notes(self):
        if os.path.exists(NOTES_FILE):
            with open(NOTES_FILE, "r") as f:
                notes = json.load(f)
        else:
            notes = []
        return notes


class NoteHandler(tornado.web.RequestHandler):
    def post(self):
        new_note = self.get_body_argument("note")
        notes = self.load_notes()
        notes.append(new_note)
        self.save_notes(notes)
        self.redirect("/")

    def post_with_id(self, note_id):
        notes = self.load_notes()
        try:
            del notes[int(note_id)]
            self.save_notes(notes)
            self.redirect("/")
        except IndexError:
            pass

    def delete(self, note_id):
        notes = self.load_notes()
        try:
            del notes[int(note_id)]
            self.save_notes(notes)
            self.redirect("/")
        except IndexError:
            pass

    def load_notes(self):
        if os.path.exists(NOTES_FILE):
            with open(NOTES_FILE, "r") as f:
                notes = json.load(f)
        else:
            notes = []
        return notes

    def save_notes(self, notes):
        with open(NOTES_FILE, "w") as f:
            json.dump(notes, f)

    def post(
        self, note_id=None
    ):  # Fügt die Post-Methode für Anfragen an /api/notes/<id> hinzu
        if note_id is not None:
            self.post_with_id(note_id)
        else:
            super().post()


def make_app():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/api/notes", NoteHandler),
            (r"/api/notes/(\d+)", NoteHandler),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
    )


if __name__ == "__main__":
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w") as f:
            json.dump([], f)
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
