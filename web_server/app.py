from flask import Flask,render_template,request
from sql_select import select


app = Flask(__name__, static_url_path='/source', static_folder='./static')

# @app.route('/')
# def index():
#     return render_template('mainpage.html')

@app.route('/', methods = ['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('mainpage.html')
    elif request.method == 'POST':
        titles = ['','NAME','PRICE']
        shop = request.form.get('shopname')
        datas = select(shop)
        return render_template('mainpage.html', titles=titles, datas=datas, requestMethod='POST')


    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)