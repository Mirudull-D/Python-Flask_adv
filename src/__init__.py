from flask import Flask

def create_app(test_config=None):
    app= Flask(__name__,instance_relative_config=True)
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY='osajgajsgls;djhdd;sjklds',

        )
    else:
        app.config.from_mapping(test_config)

    from .bookmark import bookmark
    app.register_blueprint( bookmark,url_prefix='/')

    @app.route('/')
    def hello_world():
        mylist=['apple', 'banana', 'cherry']
        return "hello world"



    return app
