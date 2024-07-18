import json
import os

# File paths
NEWS_FILE = 'Rss.json'
TWEETS_FILE = 'X.json'
REDDIT_FILE = 'Reddit.json'

# Function to read JSON file
def read_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

# Function to write JSON file
def write_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Function to add new News
def add_new_news():
    news_data = read_json(NEWS_FILE)
    new_news = {
        "id": input("ID: "),
        "Page": input("Page: "),
        "DatePublication": input("DatePublication (DD-MM-YYYY): "),
        "Title": input("Title: "),
        "Autor": input("Autor (comma separated): ").split(','),
        "Summary": input("Summary: "),
        "BodyText": input("BodyText: ")
    }
    news_data["news"].append(new_news)
    write_json(NEWS_FILE, news_data)
    print("New News added successfully!")

# Function to add new Tweet
def add_new_tweet():
    tweets_data = read_json(TWEETS_FILE)
    new_tweets = {
        "Id": input("ID: "),
        "UserProfile": input("UserProfile: "),
        "NameProfile": input("NameProfile: "),
        "TextPublic": input("TextPublic: "),
        "CantLikes": int(input("CantLikes: ")),
        "CantRetweets": int(input("CantRetweets: ")),
        "CantComents": int(input("CantComents: "))
    }
    tweets_data["tweets"].append(new_tweets)
    write_json(TWEETS_FILE, tweets_data)
    print("New Tweets added successfully!")

# Function to add new Reddit post
def add_new_reddit():
    reddit_data = read_json(REDDIT_FILE)
    new_reddit = {
        "Id": input("ID: "),
        "DatePub": input("DatePub (YYYY-MM-DD): "),
        "NameProfile": input("NameProfile: "),
        "TitlePub": input("TitlePub: "),
        "TextPub": input("TextPub: "),
        "CantUpVotes": int(input("CantUpVotes: ")),
        "CantDownVotes": int(input("CantDownVotes: ")),
        "CantShares": int(input("CantShares: "))
    }
    reddit_data["reddit"].append(new_reddit)
    write_json(REDDIT_FILE, reddit_data)
    print("New Reddit post added successfully!")

# Main menu
def main_menu():
    while True:
        print("\nMenu:")
        print("1. Agregar news")
        print("2. Agregar tweet")
        print("3. Agregar reddit")
        print("4. Salir")
        choice = input("Seleccione una opción: ")

        if choice == '1':
            add_new_news()
        elif choice == '2':
            add_new_tweet()
        elif choice == '3':
            add_new_reddit()
        elif choice == '4':
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main_menu()

def read_and_print_json(file_path):
    """Reads a JSON file and prints its contents to the console."""

    try:
        # Open the JSON file in read mode
        with open(file_path, 'r') as json_file:
            # Load the JSON data into a Python object
            data = json.load(json_file)

        # Print the JSON data to the console
        print(json.dumps(data, indent=4))  # Use indent=4 for better readability

    except FileNotFoundError as e:
        print(f"Error: File not found: {file_path}")
        raise e

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in file: {file_path}")
        raise e

if __name__ == "__main__":
    # Example usage: Read and print a JSON file named "data.json"
    read_and_print_json("data.json")