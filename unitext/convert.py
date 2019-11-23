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
    file = request.files["file"]

    if not file:
        return {'error': 'No file provided'}, 400

    data = file.read()
    mime = magic.from_buffer(data, True)
    ext = mimetypes.guess_extension(mime)[1:]
    if ext not in new_ext:
        return {'error': f'File format "{ext}" is not supported'}, 400

    ext = new_ext[ext]

    res_name = file.filename
    if res_name.count("."):
        res_name = res_name[:res_name.rfind(".")]

    res_name += "." + out_type

    cdata = str.encode(pypandoc.convert(data,
                                        out_type,
                                        format=ext))

    return send_file(io.BytesIO(cdata),
                     mimetype=mimetypes.guess_type(res_name)[0],
                     as_attachment=True,
                     attachment_filename=res_name)
