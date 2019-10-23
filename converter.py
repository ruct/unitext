import pypandoc
import mimetypes
import magic
from flask import request, Flask

app = Flask(__name__)
@app.route("/to/<out_type>", methods = ["POST", "GET"])
def convert(out_type):
    print(out_type)
    if request.method == "GET":
        return '''
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form action="" method=post enctype=multipart/form-data>
                 <input type=file name=input_file> <br>
                 <input type=submit value=Upload>
            </form>        
            '''

    file = request.files["input_file"]
    if not file:
        return

    data = file.read()
    mime = magic.from_buffer(data, True)
    ext = mimetypes.guess_extension(mime)[1:]
    return ext


if __name__ == "__main__":
    app.run("127.0.0.1", "8080")