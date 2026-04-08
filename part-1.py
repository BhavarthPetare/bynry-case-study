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
