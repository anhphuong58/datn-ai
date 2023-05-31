from flask import Flask, request
from flask_cors import CORS, cross_origin
app = Flask(__name__)
# from bert import process
# from translate import convert, src_lang
CORS(app, support_credentials=True, withCredentials=True,
     CORS_SUPPORTS_CREDENTIALS=True)

@app.route('/api/receive-text', methods=['POST'])
def receive_text():
    # Lấy văn bản nhận được từ spring
    # data =  request.get_json()
    received_text = request.data.decode('utf-8')
    # received_text = data.get('text')
    print("Văn bản nhận được:", received_text)
    # eng_text = convert(received_text,'en')
    # print(eng_text)
    # phân loại tài liệu
    # x = classify(received_text)
    # # tóm tắt tài liệu
    # y = summarization(received_text)
    # trả kết quả về cho spring
    # return [x,y] 
    # a = process(eng_text)
    # # a = received_text + "accbcbcb"
    # # rs = {}
    # # rs['classify']=a
    # a['summary']=convert(a['summary'],src_lang(received_text))
    a= {}
    a['summary']="this is ummary"
    a['classify']=1
    print(a)
    return a

from os import environ


if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)
