from flask import Flask,render_template

app = Flask(__name__,template_folder="templates")

@app.route('/')
def hello_world():
    mylist=['apple', 'banana', 'cherry']
    return render_template('base.html',mylist=mylist)


if __name__ == '__main__':
    app.run(debug=True )