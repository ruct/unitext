import io
import mimetypes

import magic
import pypandoc
from flask import send_file, request, abort, Blueprint

bp = Blueprint('convert', __name__, url_prefix='/convert')

new_ext = {
    "htm": "html",
    "md": "md",
    "dot": "docx",
    "wiz": "docx",
    "doc": "docx",
    "docx": "docx",
}


@bp.route("/<out_type>", methods=["POST", "GET"])
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

    file = request.files["file"]
    if not file:
        return

    data = file.read()
    mime = magic.from_buffer(data, True)
    ext = mimetypes.guess_extension(mime)[1:]
    print(ext)
    if ext not in new_ext:
        abort(400, "File format " + ext + " isn't supported")
    ext = new_ext[ext]
    print("New ext = " + ext)

    res_name = file.filename
    if res_name.count("."):
        res_name = res_name[:res_name.rfind(".")]

    res_name += "." + ext
    print(res_name)

    cdata = str.encode(pypandoc.convert(data,
                                        out_type,
                                        format=ext))

    return send_file(io.BytesIO(cdata),
                     mimetype=mimetypes.guess_type(res_name)[0],
                     as_attachment=True,
                     attachment_filename=res_name)
