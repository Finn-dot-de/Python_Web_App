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
        new_note = tornado.escape.json_decode(self.request.body)
        notes = self.load_notes()
        notes.append(new_note)
        self.save_notes(notes)
        self.set_status(201)  # HTTP-Statuscode für "Created"

    def delete(self, note_id):
        notes = self.load_notes()
        try:
            del notes[int(note_id)]
            self.save_notes(notes)
            self.set_status(204)  # HTTP-Statuscode für "No Content"
        except IndexError:
            self.set_status(404)  # HTTP-Statuscode für "Not Found"

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


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/api/notes", NoteHandler),
        (r"/api/notes/(\d+)", NoteHandler),
    ], template_path=os.path.join(os.path.dirname(__file__), "templates"))

if __name__ == "__main__":
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w") as f:
            json.dump([], f)
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
