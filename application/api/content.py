from flask import Blueprint
from application.models import Content,Page, db

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
    
    cons= [content.to_json() for content in page.content]

    return cons
