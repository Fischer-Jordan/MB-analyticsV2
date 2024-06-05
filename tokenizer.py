from transformers import GPT2Tokenizer

# Load the GPT-2 tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Example text
text = """
Answer: Sure, based on the SQL query result you provided, the final answer to the user's question "How many users have purchased from Zomato?" is: One user has purchased from Zomato.

Classification: SQL

Reason for classification: The query is asking for the number of users who have purchased from Zomato, which does not contain any keywords useful for semantic analysis. Therefore, the category is SQL.

SQL: SELECT dp.id AS transaction_id, COUNT(DISTINCT dp.user_id) AS user_count FROM data_purchase dp JOIN data_purchaseitem dpi ON dp.id = dpi.purchase_id JOIN data_item di ON dpi.item_id = di.id JOIN data_vendor dv ON dp.vendor_id = dv.id WHERE dv.name ILIKE 'Zomato' GROUP BY dp.id

SQL Reason: This query will return the primary key (id) of data_purchase and the count of unique users who have made purchases from Zomato. It does this by joining the necessary tables and filtering for purchases from Zomato. The COUNT(DISTINCT dp.user_id) function is used to count the number of unique users.
    """

# Tokenize the text
tokens = tokenizer.encode(text)

# Print the tokens
print(len(tokens))
