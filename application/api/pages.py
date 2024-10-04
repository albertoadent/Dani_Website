from flask import Blueprint, request
from .data_validation import validate, error_404
from application.models import Page, db

pages = Blueprint("pages", __name__)

"""
GET ROUTES
"""


@pages.route("")
def get_pages():
    return [t.to_json() for t in Page.query.all()]


@pages.route("published")
def get_published_pages():
    return [t.to_json() for t in Page.query.filter_by(is_public=True).all()]


@pages.route("/<int:page_id>")
def get_page(page_id):
    page = Page.query.get(page_id)
    if not page:
        return {"errors": "Not Found"}, 404

    return page.to_json()


"""
POST ROUTES
"""

p = {"methods": ["POST"]}


@pages.route("", **p)
def post_page():
    data = dict(request.get_json())
    res = validate(
        {"name": str, "isPublic": bool, "templateId": int},
        data,
        ["isPublic", "templateId"],
    )
    if res:
        return res
    page = Page(
        name=data["name"],
        is_public=data.get("isPublic"),
        template_id=data.get("templateId"),
    )
    db.session.add(page)
    db.session.commit()
    return Page.query.get(int(page.id)).to_json()


@pages.route("/<int:page_id>/publish", **p)
def publish_page(page_id):
    page = Page.query.get(page_id)
    page.is_public = True
    db.session.commit()
    return Page.query.get(page_id).to_json()


@pages.route("/<int:page_id>/unpublish", **p)
def unpublish_page(page_id):
    page = Page.query.get(page_id)
    page.is_public = False
    db.session.commit()
    return Page.query.get(page_id).to_json()


"""
PUT ROUTES
"""

pu = {"methods": ["PUT"]}


@pages.route("/<int:page_id>", **pu)
def put_page(page_id):
    data = dict(request.get_json())

    try:
        res = validate(
            {"name": str, "isPublic": bool, "templateId": int},
            data,
            ["isPublic", "templateId"],
        )

        if res:
            return res

        page = Page.query.get(page_id)

        if error_404(page):
            return error_404(page)

        page.name = data["name"]
        page.is_public = data.get("isPublic") or False
        page.template_id = data.get("templateId") or page.template_id
        db.session.commit()
        return Page.query.get(page_id).to_json()
    except ValueError:
        return {"message": "Bad Data", "errors": {}}, 400


"""
DELETE ROUTES
"""

d = {"methods": ["DELETE"]}


@pages.route("/<int:page_id>", **d)
def delete_page(page_id):
    page = Page.query.get(page_id)

    if error_404(page):
        return error_404(page)

    db.session.delete(page)
    db.session.commit()

    return {"message": "deleted successfully"}
