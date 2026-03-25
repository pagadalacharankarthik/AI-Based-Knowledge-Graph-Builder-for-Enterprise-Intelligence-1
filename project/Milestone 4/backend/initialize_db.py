from graph import build_knowledge_graph
import os

# Ensure the data directory exists and the file is in the right place
csv_path = os.path.join(os.path.dirname(__file__), 'data', 'cleaned_enron_emails.csv')

if os.path.exists(csv_path):
    print(f"Found dataset at {csv_path}. Starting Neo4j initialization...")
    try:
        build_knowledge_graph(csv_path)
        print("Knowledge Graph initialization complete.")
    except Exception as e:
        print(f"Error during Graph initialization: {e}")
else:
    print(f"Error: {csv_path} not found. Please run create_mock_data.py first.")
