from waitress import serve

from mysite.wsgi import application

if __name__ == '__main__':
    serve(application, port='8100', url_prefix='/mysite')
    
