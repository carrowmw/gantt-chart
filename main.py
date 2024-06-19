from app.serve_app import serve_app

if __name__ == "__main__":
    app = serve_app()
    app.run_server(debug=True)
