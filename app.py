from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

cart = []
discount_codes = []
total_purchase_amount = 0
total_discount_amount = 0
rupee_symbol = '₹'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    global cart, total_purchase_amount, discount_codes
    data = request.get_json()
    
    cart.append({"item": data['item'], "price": data['price']})
    total_purchase_amount += data['price']

    # Apply a 10% discount for every item added
    discount_code = f"DISCOUNT_{len(discount_codes) + 1}"
    discount_codes.append(discount_code)

    return jsonify({
        "message": "Item added to cart",
        "cart": cart,
        "total_purchase_amount": f"{rupee_symbol} {total_purchase_amount:.2f}",
        "discount_code": discount_code
    })

@app.route('/checkout', methods=['POST'])
def checkout():
    global cart, discount_codes, total_discount_amount, total_purchase_amount
    discount_code = request.json.get('discount_code', None)

    if discount_code and discount_code in discount_codes:
        total_discount_amount += 0.1 * total_purchase_amount
        total_purchase_amount -= total_discount_amount  # Apply discount

        # Remove the used discount code
        discount_codes.remove(discount_code)

        return jsonify({
            "message": "Order placed with 10% discount",
            "total_discount_amount": f"{rupee_symbol} {total_discount_amount:.2f}",
            "total_purchase_amount": f"{rupee_symbol} {total_purchase_amount:.2f}"
        })
    else:
 # If no discount code or an invalid discount code is provided, proceed without a discount
        return jsonify({
            "message": "Order placed",
            "total_discount_amount": f"{rupee_symbol} {total_discount_amount:.2f}",
            "total_purchase_amount": f"{rupee_symbol} {total_purchase_amount:.2f}"
        })


#  API generates a new discount code and adds it to the list of discount codes.
@app.route('/admin/generate_discount_code', methods=['POST'])
def generate_discount_code():
    global discount_codes
    discount_code = f"DISCOUNT_{len(discount_codes) + 1}"
    discount_codes.append(discount_code)
    return jsonify({"message": "Discount code generated", "discount_code": discount_code})

# Returns details about the current purchases
@app.route('/admin/purchase_details', methods=['GET'])
def purchase_details():
    global cart, discount_codes, total_purchase_amount, total_discount_amount
    return jsonify({
        "item_count": len(cart),
        "total_purchase_amount": total_purchase_amount,
        "discount_codes": discount_codes,
        "total_discount_amount": total_discount_amount
    })

if __name__ == '__main__':
    app.run(debug=True)
