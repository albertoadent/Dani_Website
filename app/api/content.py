from flask import Blueprint, request
from .data_validation import validate, error_404
from .aws_upload import upload_file_to_s3, remove_file_from_s3
from app.models import Content, Page, db

contents = Blueprint("contents", __name__)


@contents.route("")
def get_contents():
    return [t.to_json() for t in Content.query.all()]


@contents.route("/<content_id>")
def get_content(content_id):
    content = Content.query.get(content_id)
    if not content:
        return {"errors": "Not Found"}, 404
    return content.to_json()


@contents.route("/page/<int:page_id>")
def get_page_content(page_id):
    page = Page.query.get(page_id)
    if not page:
        return {"errors": "Not Found"}, 404

    cons = [content.to_json() for content in page.content]

    return cons


"""
POST ROUTES
"""

p = {"methods": ["POST"]}


@contents.route("", **p)
def post_content():
    data = request.form
    res = validate(
        {"header": str, "subHeader": str, "text": str, "pageId": str, "linkTo": str},
        dict(data),
        ["header", "subHeader", "text", "linkTo"],
    )
    file = request.files.get("file")
    if res:
        return res
    urlObj = {"url": None}
    if file:
        urlObj = upload_file_to_s3(file=file)
    if "errors" in urlObj.keys():
        return urlObj, 400
    content = Content(
        header=data.get("header"),
        sub_header=data.get("subHeader"),
        text=data.get("text"),
        image_url=urlObj["url"],
        page_id=int(data["pageId"]),
        link_to=data.get("linkTo"),
    )
    db.session.add(content)
    db.session.commit()
    return Content.query.get(content.id).to_json()


"""
PUT ROUTES
"""

pu = {"methods": ["PUT"]}


@contents.route("/<content_id>", **pu)
def put_content(content_id):
    data = request.form
    res = validate(
        {"header": str, "subHeader": str, "text": str, "linkTo": str},
        dict(data),
        ["header", "subHeader", "text", "linkTo"],
    )
    if res:
        return res

    content = Content.query.get(content_id)

    if error_404(content):
        return error_404(content)

    file = request.files.get("file")
    urlObj = {"url": None}
    if file:
        urlObj = upload_file_to_s3(file=file)
        if "errors" in urlObj.keys():
            return urlObj, 400
        if content.image_url:
            remove_file_from_s3(content.image_url)
        content.image_url = urlObj["url"]

    content.header = data.get("header")
    content.text = data.get("text")
    content.sub_header = data.get("subHeader")
    content.link_to = data.get("linkTo")
    db.session.commit()
    return Content.query.get(content_id).to_json()


"""
DELETE ROUTES
"""

d = {"methods": ["DELETE"]}


@contents.route("/<content_id>", **d)
def delete_content(content_id):
    content = Content.query.get(content_id)

    if error_404(content):
        return error_404(content)

    db.session.delete(content)
    db.session.commit()

    return {"message": "deleted successfully"}
