#*********************************************************************************************************************
# Author - Adapted for Azure by Microsoft Copilot
# This script operates on Azure Cosmos DB (NoSQL API) to showcase similar operations to AWS DynamoDB
#*********************************************************************************************************************

from azure.cosmos import CosmosClient, PartitionKey, exceptions

# Replace these with your actual Cosmos DB credentials
COSMOS_ENDPOINT = "<your-cosmos-db-endpoint"
COSMOS_KEY = "<your-primary-key>"

# Initialize Cosmos client
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)

# Create database and container
def create_container():
    print('\n*************************************************************************')
    print('Creating database and container')
    try:
        database = client.create_database_if_not_exists(id="inventorydb")
        container = database.create_container_if_not_exists(
            id="inventory",
            partition_key=PartitionKey(path="/category"),
            offer_throughput=400
        )
        print(' DONE')
        return container
    except exceptions.CosmosHttpResponseError as e:
        print(' Skipped due to exception:', e.message)

# Insert data
def insert_data(container, category, sku, description, price, items):
    print('\n*************************************************************************')
    print('Inserting data into the container')
    item = {
        'id': f"{category}-{sku}",  # Cosmos DB requires a unique 'id' field
        'category': category,
        'sku': sku,
        'description': description,
        'price': price,
        'items': items
    }
    container.upsert_item(item)

# Fetch all items
def fetch_all(container):
    print('\n*************************************************************************')
    print('Fetching all items from the container')
    query = "SELECT * FROM inventory"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    print('Total items in the container:', len(items))
    for item in items:
        print(item)

# Fetch items by partition key
def fetch_pk(container, category):
    print('\n*************************************************************************')
    print('Fetching items by partition key')
    query = f"SELECT * FROM inventory WHERE inventory.category = '{category}'"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    print('Total items for this category:', len(items))
    for item in items:
        print(item)

# Fetch individual item
def fetch_data(container, category, sku):
    print('\n*************************************************************************')
    print('Fetching individual item by category and sku')
    item_id = f"{category}-{sku}"
    try:
        item = container.read_item(item=item_id, partition_key=category)
        print(item)
    except exceptions.CosmosResourceNotFoundError:
        print(' Item not found')

# Update item
def update_data(container, category, sku, new_price):
    print('\n*************************************************************************')
    print('Updating item price')
    item_id = f"{category}-{sku}"
    try:
        item = container.read_item(item=item_id, partition_key=category)
        item['price'] = new_price
        container.replace_item(item=item_id, body=item)
        print(' Done')
    except exceptions.CosmosResourceNotFoundError:
        print(' Item not found for update')

# Delete item
def delete_data(container, category, sku):
    print('\n*************************************************************************')
    print('Deleting item')
    item_id = f"{category}-{sku}"
    try:
        container.delete_item(item=item_id, partition_key=category)
        print(' Item deleted')
    except exceptions.CosmosResourceNotFoundError:
        print(' Item not found for deletion')

# Main execution
def main():
    container = create_container()

    insert_data(container, 'tv', 'sku00001', 'SONY 52 inch TV', 250000, 100)
    insert_data(container, 'tv', 'sku00002', 'Samsung 52 inch TV', 175000, 150)

    fetch_all(container)
    fetch_data(container, 'tv', 'sku00003')
    update_data(container, 'tv', 'sku00002', 190000)
    fetch_data(container, 'tv', 'sku00002')
    delete_data(container, 'tv', 'sku00001')
    fetch_all(container)

    insert_data(container, 'laptops', 'sku00010', 'Dell vostro 3000', 45000, 500)
    insert_data(container, 'laptops', 'sku00011', 'Dell latitude 5000', 40000, 400)
    insert_data(container, 'laptops', 'sku00012', 'HP pavilion 4500', 42000, 600)

    fetch_pk(container, 'laptops')
    fetch_all(container)

main()