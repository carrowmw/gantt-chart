from app.serve_app import serve_app

app = serve_app()

if __name__ == "__main__":
    app.run_server(debug=True)
