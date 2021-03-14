from activmatesApp import create_app

# creates application
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
