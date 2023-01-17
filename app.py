from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prudcts.db.sqlite3'
app.config['SECRET_KEY'] = "PRODUCT CRUD TEMPLATE"
db = SQLAlchemy(app)

CORS(app)



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description


@app.route("/product/<int:id>", methods = ["POST", "GET", "DELETE", "PUT"])
@app.route("/product/", methods = ["POST", "GET", "DELETE", "PUT"])
def product(id = -1):
    if request.method == "POST":            # ADD PRODUCT
        data = request.json
        name = data["name"]
        price = data["price"]
        description = data["description"]

        new_product = Product(name = name, price = price, description = description)
        db.session.add(new_product)
        db.session.commit()

        return (f"'{new_product.name}' has been added successfully.")

    if request.method == "GET":            # SEARCH PRODUCT
        product = Product.query.get(id)
        if product:
            return (f"Your product: '{product.name}'")
        return ("Product not found.")

    if request.method == "PUT":            # UPDATE PRODUCT
        product = Product.query.get(id)

        if product:
            product.name = request.json["name"]
            product.price = request.json["price"]
            product.description = request.json["description"]

            db.session.commit()
            return ("Product updated successfully.")
        return ("Product not found.")

    if request.method == "DELETE":            # DELETE PRODUCT
        product = Product.query.get(id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return (f"{product.name} has been deleted successfully.")
        return ("Product not found.")





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug = True)
