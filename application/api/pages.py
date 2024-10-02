from flask import Blueprint
from application.models import Page, db

pages = Blueprint("pages", __name__)


@pages.route("")
def get_pages():
    return [t.to_json() for t in Page.query.all()]


@pages.route("/<int:page_id>")
def get_page(page_id):
    page = Page.query.get(page_id)
    if not page:
        return {"errors": "Not Found"}, 404
    return page.to_json()
