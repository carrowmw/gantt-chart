from main import app


def simple_app(environ, start_response):
    status = "200 OK"
    headers = [("Content-type", "text/plain")]
    start_response(status, headers)
    return [b"Hello, World"]


if __name__ == "__main__":
    app.run_server(debug=True)
else:
    application = app.server  # Flask app to be used by Gunicorn
