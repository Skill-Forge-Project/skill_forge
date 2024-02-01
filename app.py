from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

if __name__ == '__main__':
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=True, host = '0.0.0.0', port = '5000')
    app.run()
