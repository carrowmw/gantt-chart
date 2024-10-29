from app.serve_app import serve_app

print("__name__ is:", __name__)

app = serve_app()

print("App instantiated:", app)

if __name__ == "__main__":
    print("Running in standalone mode")
    app.run_server(debug=True, port=8050)
else:
    application = app.server  # Flask app to be used by Gunicorn
