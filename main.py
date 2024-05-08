from app import create_app

app = create_app(debug=True)
# app = create_app()


if __name__ == "__main__":
    app.run()