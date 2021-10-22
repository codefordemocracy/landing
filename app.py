from vue import VueFlask
from flask import Flask, render_template, url_for, request, jsonify
from google.cloud import secretmanager
import datetime
import json
import stripe

app = VueFlask(__name__)

secrets = secretmanager.SecretManagerServiceClient()
stripe.api_key = secrets.access_secret_version(request={"name": "projects/952416783871/secrets/stripe_secret_key/versions/1"}).payload.data.decode()

@app.context_processor
def inject_now():
    return { "now": datetime.datetime.now() }

#########################################################
# frontend routes
#########################################################

@app.route("/")
def route_home():
    return render_template("home.html.j2")

@app.route("/tools/")
def route_tools():
    return render_template("tools.html.j2")

@app.route("/data/")
def route_data():
    return render_template("data.html.j2")

# @app.route("/reports/")
# def route_reports():
#     return render_template("reports.html.j2")

@app.route("/about/")
def route_about():
    return render_template("about.html.j2")

@app.route("/donate/")
def route_donate():
    success = request.args.get("success")
    amount = request.args.get("amount")
    if amount is None:
        amount = 250
    return render_template("donate.html.j2", success=success, amount=amount)

@app.route("/volunteer/")
def route_volunteer():
    roles = [{
        "name": "Technical Roles",
        "listings": [{
            "title": "Frontend Engineer",
            "skills": ["Vue.js"]
        }, {
            "title": "Data Engineer",
            "skills": ["Python", "BigQuery", "Neo4j", "Elasticsearch", "Google Cloud Functions"]
        }, {
            "title": "Data Scientist — Network Analysis",
            "skills": ["Python", "Neo4j"]
        }, {
            "title": "Data Scientist — NLP",
            "skills": ["Python", "Elasticsearch"]
        }]
    }, {
        "name": "Operations Roles",
        "listings": [{
            "title": "Marketing Analyst",
            "skills": ["Adwords"]
        }, {
            "title": "Volunteer Coordinator",
            "skills": ["Google Sheets", "Airtable", "Notion"]
        }]
    }]
    return render_template("volunteer.html.j2", roles=roles)

@app.route("/legal/")
def route_legal():
    return render_template("legal.html.j2")

@app.route("/contact/")
def route_contact():
    return render_template("contact.html.j2")

#########################################################
# backend routes
#########################################################

@app.route("/api/donate/", methods=["POST"])
def api_donate():
    data = request.get_json()
    if data["cents"] is not None:
        session = stripe.checkout.Session.create(
            mode="payment",
            payment_method_types=["card"],
            submit_type="donate",
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "unit_amount": round(data["cents"]),
                    "product_data": {
                      "name": "One-time, tax-deductible donation to Code for Democracy, Inc. (EIN 83-3407325)",
                    }
                },
                "quantity": 1
            }],
            success_url=url_for("route_donate", success=True, amount=data["cents"]/100, _external=True),
            cancel_url=url_for("route_donate", amount=data["cents"]/100, _external=True)
        )
        return jsonify(id=session.id)

if __name__ == "__main__":
    app.run()
