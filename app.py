# ---- IMPORTS ----
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date

# ---- APP SETUP ----
app = Flask(__name__)

# ---- DATABASE CONFIGURATION ----
# This tells Flask: the database is a file called insurance.db
# sitting in the same folder as this app.py file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///insurance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ---- DATABASE MODEL ----
# This is the Python representation of your policies table
# Each attribute here maps directly to a column in the table
class Policy(db.Model):
    __tablename__ = 'policies'

    id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_name = db.Column(db.String(100), nullable=False)
    policy_type   = db.Column(db.String(50),  nullable=False)
    sum_assured   = db.Column(db.Float,        nullable=False)
    status        = db.Column(db.String(20),   default='active')
    created_date  = db.Column(db.String(20),   default=str(date.today()))

    # This method converts one Policy object into a dictionary
    # so jsonify() can turn it into JSON easily
    def to_dict(self):
        return {
            'id':            self.id,
            'customer_name': self.customer_name,
            'policy_type':   self.policy_type,
            'sum_assured':   self.sum_assured,
            'status':        self.status,
            'created_date':  self.created_date
        }


# ============================================================
# ENDPOINT 1 — ADD A NEW POLICY
# ============================================================
@app.route('/addPolicy', methods=['POST'])
def add_policy():

    data = request.get_json()

    customer_name = data.get('customer_name')
    policy_type   = data.get('policy_type')
    sum_assured   = data.get('sum_assured')

    # Validation — return 400 if anything is missing
    if not customer_name or not policy_type or not sum_assured:
        return jsonify({
            'error': 'Missing fields. Required: customer_name, policy_type, sum_assured'
        }), 400

    # Create a new Policy object
    new_policy = Policy(
        customer_name = customer_name,
        policy_type   = policy_type,
        sum_assured   = sum_assured
    )

    # Add it to the database session and commit
    db.session.add(new_policy)
    db.session.commit()

    return jsonify({'message': 'Policy added successfully'}), 201


# ============================================================
# ENDPOINT 2 — GET ALL POLICIES
# ============================================================
@app.route('/getAllPolicies', methods=['GET'])
def get_all_policies():

    # Fetch every row from the policies table
    all_policies = Policy.query.all()

    # Convert each Policy object to a dictionary
    result = [policy.to_dict() for policy in all_policies]

    return jsonify(result), 200


# ============================================================
# ENDPOINT 3 — GET ONE POLICY BY ID
# ============================================================
@app.route('/getPolicy/<int:policy_id>', methods=['GET'])
def get_policy(policy_id):

    # Look for a policy with this exact ID
    policy = Policy.query.get(policy_id)

    # If nothing found, return 404
    if policy is None:
        return jsonify({'error': 'Policy not found'}), 404

    return jsonify(policy.to_dict()), 200


# ============================================================
# RUN THE SERVER
# ============================================================
if __name__ == '__main__':
    # This creates the table if it doesn't already exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)