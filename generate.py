import pandas as pd
from faker import Faker
import random

fake = Faker()

# Function to generate a single unique spam email subject
def generate_subject():
    actions = ["Grab", "Don't Miss", "Exclusive Offer:", "Unlock", "Big Savings", "Last Chance", "Special Deal"]
    offers = ["50% Off", "Buy One Get One Free", "Limited Time Deal", "20% Discount", "Clearance Sale"]
    products = ["on All Shoes", "on Your Next Purchase", "on Smartphones", "for New Customers", "on Electronics"]
    exclamations = ["!", "!!", "!!!", "😍", "🚀", "💥", "👍", "😉", "🎉"]
    urgency = ["Now", "Today", "This Week Only", "Before It's Gone", "While Supplies Last"]
    
    action = random.choice(actions)
    offer = random.choice(offers)
    product = random.choice(products)
    exclamation = random.choice(exclamations)
    urgent = random.choice(urgency)
    
    subject = f"{action} {offer} {product} {urgent}{exclamation}"
    return subject

# Function to add subjects to each row in the DataFrame
def add_subjects_to_dataframe(df):
    df['Subject'] = df.apply(lambda x: generate_subject(), axis=1)
    return df

# Main function to process the file
def main():
    file_path = 'spam.csv'  # Adjust this path as necessary
    try:
        df = pd.read_csv(file_path, encoding='utf-8')  # Try default UTF-8 encoding first
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='ISO-8859-1')  # Fallback to ISO-8859-1 if UTF-8 fails

    df_with_subjects = add_subjects_to_dataframe(df)  # Process the DataFrame to add subjects
    
    updated_file_path = 'spam.csv'  # Define path for the updated file
    df_with_subjects.to_csv(updated_file_path, index=False)  # Save the updated DataFrame without the index
    print(f"File saved successfully as {updated_file_path}")

if __name__ == "__main__":
    main()
