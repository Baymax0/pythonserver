import os

from flask import Flask
from flask import request

# create and configure the app
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    from . import db
    db.init_app(app)
    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True) # load the instance config, if it exists, when not testing
    else:
        app.config.from_mapping(test_config) # load the test config if passed in

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 查询 SQL语句执行函数
    def selete_excute(query, args=(), one=False):
            cur = db.get_db().execute(query, args)
            rv = cur.fetchall()
            cur.close()
            return (rv[0] if rv else None) if one else rv

    def insert_excute(query):
            connect = db.get_db()
            connect.execute(query)
            connect.commit()

    #主页
    @app.route('/')
    def hello_world():
        return dict(code=1)

    
    # 登录
    #  userid = 1
    #  password = '123sda'
    #  登录成功返回code=1，data=model. 其他code查看msg
    @app.route('/login', methods=['get'])
    def userinfo():
        response = dict(code=-1,msg='')
        if request.method == 'GET':
            userid = request.args.get('userid',0) # get字典，默认返回 1
            password = request.args.get('password','') # get字典，默认返回 1
            query = 'SELECT * FROM user_table WHERE userid = {}'.format(userid)
            result = selete_excute(query,one=True)
            if result is None:
                # 插入 insert
                insertQuery = "INSERT INTO user_table (userid,password,lover_userid) VALUES ({},'{}',{})".format(userid,password,-1)
                insert_excute(insertQuery)
                data = dict(userid=userid,lover_userid='-1',wallet=0)
                response['code'] = 1
                response['data'] = data
                response['msg'] = '创建成功'
            else:
                # 密码正确 返回查询结果
                if (password == result['password']):
                    data = dict(userid=userid,lover_userid=result['lover_userid'],wallet=result['wallet'])
                    response['code'] = 1
                    response['data'] = data
                    response['msg'] = '登录成功'
                else:
                    response['msg'] = '密码错误'
        elif  request.method == 'POST':
            response['msg'] = '请使用get请求'

        return response

    # 绑定对象    
    # userid = 1
    # lover_userid = 32
    @app.route('/connect_lover', methods=['get'])
    def connect_lover():
        response = dict(code=-1,msg='')

        userid = request.args.get('userid',0) #
        lover_userid = request.args.get('lover_userid',0) #

        updateQuery = "UPDATE user_table SET lover_userid = {} WHERE userid = {} AND lover_userid = -1".format(lover_userid,userid)
        insert_excute(updateQuery)
        updateQuery = "UPDATE user_table SET lover_userid = {} WHERE userid = {} AND lover_userid = -1".format(userid,lover_userid)
        insert_excute(updateQuery)
        response['code'] = 1
        response['msg'] = '处理成功'

        return response

          
    #  查询待处理 钱包请求
    #  lover_userid = 1
    #  返回 时间戳数组
    @app.route('/wallet_fixlist', methods=['get'])
    def wallet_fixlist():   
        response = dict(code=-1,msg='')
        userId = request.args.get('lover_userid',0) # get字典，默认返回 1
        query = 'SELECT * FROM wallet_record_table WHERE apply_userid = {} AND status = 0'.format(userId)
        result = selete_excute(query,one=False)
        data = []

        for record in result:
            model = dict(id=record['id'],time=record['apply_time'])
            data.append(model)

        response['code'] = 1
        response['data'] = data

        return response

    # 发起一个钱包加 +1 记录
    # userid = 1
    # apply_time = 231 时间戳
    @app.route('/wallet_request', methods=['get'])
    def wallet_Request(): 
        response = dict(code=-1,msg='')
        userid = request.args.get('userid',0) #
        apply_time = request.args.get('apply_time',0) # 

        insertQuery = "INSERT INTO wallet_record_table (apply_userid,apply_time) VALUES ({},{})".format(userid,apply_time)
        insert_excute(insertQuery)
        response['code'] = 1
        response['msg'] = '创建成功'
        return response

    # 处理一个+1请求    
    # id = 1
    # status = -1、1
    @app.route('/wallet_handle', methods=['get'])
    def wallet_handle(): 
        response = dict(code=-1,msg='')

        record_id = request.args.get('id',0) #
        status = request.args.get('status',0) #

        updateQuery = "UPDATE wallet_record_table SET status = {} WHERE id = {}".format(status,record_id)
        insert_excute(updateQuery)
        response['code'] = 1
        response['msg'] = '处理成功'

        return response


    return app