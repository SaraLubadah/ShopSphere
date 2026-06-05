\# ShopSphere-Project Overview



ShopSphere is a platform allows vendors to add and manage products while customers can browse products and submit reviews and ratings.



The project demonstrates CRUD operations, DynamoDB + Global Secondary Indexes (GSI), Python and Flask web development.



\---



\# Technologies Used



\* Python 3

\* Flask

\* AWS DynamoDB

\* boto3

\* HTML

\* CSS

\* Git \& GitHub



\---



\# Features



\## Product Catalog



\* Add products

\* View all products

\* View product details

\* Edit products

\* Delete products



\## Customer Reviews



\* Submit reviews

\* Rate products from 1–5

\* View all reviews

\* Average product ratings



\## DynamoDB Features



\* NoSQL schema design

\* Partition and sort keys

\* Global Secondary Index (GSI)

\* Query operations

\* Scan operations



\---



\# DynamoDB Schema



\## ProductsDB Table



| Attribute   | Purpose                |

| ----------- | ---------------------- |

| ProductID   | Partition Key          |

| name        | Product name           |

| description | Product description    |

| category    | Product category       |

| price       | Product price          |

| stock       | Product stock quantity |

| image\_url   | Product image          |



\## Reviews Table



| Attribute     | Purpose          |

| ------------- | ---------------- |

| product\_id    | Partition Key    |

| review\_id     | Sort Key         |

| customer\_name | Reviewer name    |

| rating        | Product rating   |

| comment       | Review comment   |

| timestamp     | Review timestamp |



\---



\# Global Secondary Index (GSI)



\## category-index



The project uses a Global Secondary Index on the `category` attribute to allow efficient product filtering by category.



This improves performance compared to full table scans because DynamoDB can directly query products by category.



\---



\# Project Structure



```text

ShopSphere/

│

├── app.py

├── README.md

├── services/

│   └── db.py

├── templates/

├── static/

│   └── style.css

```





\---



