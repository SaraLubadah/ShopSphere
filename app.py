from flask import Flask, render_template, request, redirect
from services.db import products_table, reviews_table
from boto3.dynamodb.conditions import Key
app = Flask(__name__)





# Home page
@app.route('/')
def home():

    response = products_table.scan()

    products = response['Items']

    return render_template('index.html', products=products)





# Add product page
@app.route('/add', methods=['GET', 'POST'])
def add_product():

    if request.method == 'POST':

        if not request.form['name']:
            return "Name required"

        products_table.put_item(
            Item={
                'ProductID': request.form.get('product_id'),
                'name': request.form.get('name'),
                'description': request.form.get('description'),
                'category': request.form.get('category'),
                'price': int(request.form.get('price')),
                'stock': int(request.form.get('stock')),
                'image_url': request.form.get('image_url')
            }
        )

        return render_template('success.html')

    return render_template('addProducts.html')



# Product detail page
@app.route('/product/<product_id>')
def product_detail(product_id):

    # Get product
    response = products_table.get_item(
        Key={
            'ProductID': product_id
        }
    )

    product = response.get('Item')

    if not product:
        return "Product not found"

    # Get reviews
    from boto3.dynamodb.conditions import Key

    review_response = reviews_table.query(
        KeyConditionExpression=Key('product_id').eq(product_id)
    )

    reviews = review_response['Items']

    reviews = sorted(
    reviews,
    key=lambda x: x['timestamp'],
    reverse=True
)

    # Average rating
    if reviews:
        average_rating = sum(
            int(review['rating']) for review in reviews
        ) / len(reviews)
    else:
        average_rating = 0

    return render_template(
        'product_detail.html',
        product=product,
        reviews=reviews,
        average_rating=average_rating
    )

    return redirect(f'/product/{product_id}')

# Add review
@app.route('/review/<product_id>', methods=['POST'])
def add_review(product_id):

    import uuid
    from datetime import datetime

    reviews_table.put_item(
        Item={
            'product_id': product_id,
            'review_id': str(uuid.uuid4()),
            'customer_name': request.form['customer_name'],
            'rating': int(request.form['rating']),
            'comment': request.form['comment'],
            'timestamp': datetime.now().isoformat()
        }
    )

    return redirect(f'/product/{product_id}')

# Edit product

@app.route('/edit/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):

    if request.method == 'POST':

        products_table.update_item(
            Key={
                'ProductID': product_id
            },
            UpdateExpression="""
                SET #n = :name,
                    description = :description,
                    category = :category,
                    price = :price,
                    stock = :stock,
                    image_url = :image_url
            """,
            ExpressionAttributeNames={
                '#n': 'name'
            },
            ExpressionAttributeValues={
                ':name': request.form['name'],
                ':description': request.form['description'],
                ':category': request.form['category'],
                ':price': int(request.form['price']),
                ':stock': int(request.form['stock']),
                ':image_url': request.form['image_url']
            }
        )

        return "Product Updated"

    response = products_table.get_item(
        Key={
            'ProductID': product_id
        }
    )

    product = response['Item']

    return render_template('edit_product.html', product=product)



# Delete product
@app.route('/delete/<product_id>')
def delete_product(product_id):

    products_table.delete_item(
        Key={
            'ProductID': product_id
        }
    )

    return "Product Deleted"




# Filter by category
@app.route('/category/<category>')
def filter_category(category):

    response = products_table.query(
        IndexName='category-index',
        KeyConditionExpression=Key('category').eq(category)
    )

    products = response['Items']

    return render_template(
        'index.html',
        products=products
    )




if __name__ == '__main__':
    app.run(debug=True)