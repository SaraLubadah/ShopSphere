import boto3

dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-1'
)

products_table = dynamodb.Table('ProductsDB')
reviews_table = dynamodb.Table('Reviews')