from flask import Blueprint, request
from .data_validation import validate, error_404
from app.models import Template, db

templates = Blueprint("templates", __name__)

"""
GET ROUTES
"""


@templates.route("")
def get_templates():
    return [t.to_json() for t in Template.query.all()]


@templates.route("/<int:template_id>")
def get_template(page_id):
    page = Template.query.get(page_id)
    if not page:
        return {"errors": "Not Found"}, 404

    return page.to_json()


"""
POST ROUTES
"""

p = {"methods": ["POST"]}


@templates.route("", **p)
def post_template():
    data = dict(request.get_json())
    res = validate(
        {"name": str},
        data,
    )
    if res:
        return res
    template = Template(
        name=data["name"],
    )
    db.session.add(template)
    db.session.commit()
    return Template.query.get(int(template.id)).to_json()


"""
PUT ROUTES
"""

pu = {"methods": ["PUT"]}


@templates.route("/<int:template_id>", **pu)
def put_template(template_id):
    data = dict(request.get_json())

    try:
        res = validate(
            {"name": str},
            data
        )

        if res:
            return res

        template = Template.query.get(template_id)

        if error_404(template):
            return error_404(template)

        template.name = data["name"]
        db.session.commit()
        return Template.query.get(template_id).to_json()
    except ValueError:
        return {"message": "Bad Data", "errors": {}}, 400


"""
DELETE ROUTES
"""

d = {"methods": ["DELETE"]}


@templates.route("/<int:template_id>", **d)
def delete_template(page_id):
    page = Template.query.get(page_id)

    if error_404(page):
        return error_404(page)

    db.session.delete(page)
    db.session.commit()

    return {"message": "deleted successfully"}
