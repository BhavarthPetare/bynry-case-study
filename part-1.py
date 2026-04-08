@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json
    required_fields = ['name', 'sku', 'price', 'warehouse_id', 'initial_quantity']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required data"}), 400

    # Create new product
  try:
      product = Product(
          name=data['name'],
          sku=data['sku'],
          price=data['price'],
          warehouse_id=data['warehouse_id']
      )
      db.session.add(product)
      db.session.flush()
  
      # Update inventory count
      inventory = Inventory(
          product_id=product.id,
          warehouse_id=data['warehouse_id'],
          quantity=data['initial_quantity']
      )
      db.session.add(inventory)
      db.session.commit()
  
      return {"message": "Product created", "product_id": product.id}
  except Exception as e:
      db.session.rollback()
      return jsonify({"error": str(e)}), 500

# Issues:
#   1. db.session.commit running twice: the 2 databases are linked using product_id and warehouse_id. If one commit is successful and second isn't,
#      there will be a problem in database where you have a product object with no inventory object linked
#   2. data=request.json not checked: there is no block of code that checks whether the json contains the data required. an error handling mechanism is required.
# Your Tasks:

# Identify Issues: List all problems you see with this code (technical and business logic)
# Explain Impact: For each issue, explain what could go wrong in production
# Provide Fixes: Write the corrected version with explanations
# Additional Context (you may need to ask for more):
# Products can exist in multiple warehouses
# SKUs must be unique across the platform
# Price can be decimal values
# Some fields might be optional
