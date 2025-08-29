# secure-vm-cosmosdb-integration

## 🚀 Azure Cosmos DB Integration from Secure Ubuntu VM

### Overview
This project demonstrates how to provision and interact with Azure Cosmos DB (NoSQL API) from a secure Ubuntu VM using Python. It mirrors AWS DynamoDB-style operations—insert, query, update, delete—while showcasing Azure-native infrastructure and CLI tooling.

---

### 🧱 Infrastructure Setup (via Azure Portal)
Provision the following resources manually in the Azure Portal under a resource group named `CosmosDB`:
- Ubuntu VM (`CosmosDb3`)
- Virtual Network (`CosmosDb3-vnet`)
- Network Security Group (`CosmosDb3-nsg`)
- Public IP (`CosmosDb3-ip`)
- Managed Disk (`CosmosDb3_disk1...`)
- SSH Key (`CosmosDb3`)
- Network Interface (`cosmoscloud_v1`)

---

### 🧰 Python Environment Setup (Inside VM)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 -m venv ~/cosmosenv
source ~/cosmosenv/bin/activate
pip install azure-cosmos
```

---

### 🏗️ Cosmos DB Provisioning (via Azure CLI)
```bash
az login --use-device-code

az cosmosdb create \
  --name cosmosdbcfmfa \
  --resource-group CosmosDB \
  --kind GlobalDocumentDB \
  --locations regionName=eastus failoverPriority=0 isZoneRedundant=False

az cosmosdb sql database create \
  --account-name cosmosdbcfmfa \
  --name inventorydb \
  --resource-group CosmosDB

az cosmosdb sql container create \
  --account-name cosmosdbcfmfa \
  --database-name inventorydb \
  --name inventory \
  --partition-key-path "/category" \
  --resource-group CosmosDB
```

---

### 🔐 Retrieve Credentials
```bash
az cosmosdb show \
  --name cosmosdbcfmfa \
  --resource-group CosmosDB \
  --query documentEndpoint \
  --output tsv

az cosmosdb keys list \
  --name cosmosdbcfmfa \
  --resource-group CosmosDB \
  --type keys \
  --query primaryMasterKey \
  --output tsv
```

Update your Python script with:
```python
COSMOS_ENDPOINT = "https://cosmosdbcfmfa.documents.azure.com:443/"
COSMOS_KEY = "<your-primary-key>"
```

---

### 🧪 Run the Python Script
```bash
nano inventory.py  # Paste the full script
python inventory.py
```

---

### 📊 Validate in Azure Portal
- Navigate to your Cosmos DB account (`cosmosdbcfmfa`)
- Open **Data Explorer**
- Browse: `inventorydb → inventory → Items`
- View inserted documents and run queries

---

### 🧠 Optional Enhancements
- Use `.env` file for secure credential handling
- Add logging for audit trails
- Refactor into modular Python files
- Integrate with VNet or private endpoints for production security
- Package as a mentorship lab or classroom module

