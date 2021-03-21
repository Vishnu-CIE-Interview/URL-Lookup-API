from application import *

if __name__ == '__main__':
    app_function().run(host=os.getenv('API_SERVER_IP'), port=int(os.getenv('API_SERVER_PORT')), debug=True)
