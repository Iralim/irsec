import os
import requests

BASE_URL = 'https://irsec-iralim.pythonanywhere.com/api/'
CATEGORY_URL = f'{BASE_URL}categories/'
TOPIC_URL = f'{BASE_URL}topics/'

api_url_category = 'https://irsec-iralim.pythonanywhere.com/api/categories/get_or_create/'
api_url_topic = 'https://irsec-iralim.pythonanywhere.com/api/topics/get_or_create/'


def load_folders_files(path, parent_id=None, parent_name=""):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)

        # Process directories
        if os.path.isdir(item_path):
            tree = f"{parent_name}/{item}" if parent_name else item
            data = {'name': item, 'parent_id': parent_id, 'tree': tree}

            try:
                # Send request to create category
                response = requests.post(api_url_category, json=data)
                response_data = response.json()

                if response.status_code == 201:
                    print(f"Created category: {response_data['name']})")
                elif response.status_code == 200:
                    print(f"Syncronized category: {response_data['name']}")
                else:
                    print(f"Error creating category: {response.status_code}, {response_data}")
                    continue 

                # Recursively process contents of the directory
                load_folders_files(item_path, response_data['id'], tree)

            except requests.exceptions.RequestException as e:
                print(f"Network error while processing folder {item}: {e}")
            except ValueError as e:
                print(f"Error processing data for folder {item}: {e}")

        # Process files
        elif os.path.isfile(item_path):
            try:
                # Read file content (handle encoding errors)
                try:
                    with open(item_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    content = None  

                # Prepare data for file
                topic_name = os.path.splitext(item)[0]  # File name without extension
                file_name = item  # Full file name
                tree = os.path.join(parent_name, file_name)
                data = {
                    'topic_name': topic_name,
                    'file_name': file_name,
                    'category_id': parent_id,
                    'content': content,
                    'tree': tree
                }

                # Send request to create topic (file)
                response = requests.post(api_url_topic, json=data)
                response_data = response.json()

                if response.status_code == 201:
                    print(f"Created topic: {response_data['name']}")
                elif response.status_code == 200:
                    print(f"Syncronized topic: {response_data['name']} ({tree})")
                else:
                    print(f"Error creating topic: {response.status_code}, {response_data}")

            except requests.exceptions.RequestException as e:
                print(f"Network error while processing file {item}: {e}")
            except ValueError as e:
                print(f"Error processing data for file {item}: {e}")
            except Exception as e:
                print(f"General error while processing file {item}: {e}")


def remove_old_entries(path, category_id=None):
    categories = requests.get(CATEGORY_URL).json()
    topics = requests.get(TOPIC_URL).json()

    for category in categories:
        category_tree = category['tree']
        full_tree = os.path.join(path, category_tree)

        if not os.path.exists(full_tree):
            print(f"Path DOES NOT EXIST: {full_tree}")
            requests.delete(f"{CATEGORY_URL}{category['id']}/").raise_for_status()
            print(f"Category DELETED: {category['name']}")

    for topic in topics:
        full_tree = os.path.join(path, topic['tree'])
        if not os.path.exists(full_tree):
            print(f"Topic DELETED: {topic['name']}")
            requests.delete(f"{TOPIC_URL}{topic['id']}/").raise_for_status()



if __name__ == '__main__':
    root_path = '/media/erik/637738823CDCAF57/Element/IT'
    load_folders_files(root_path)
    remove_old_entries(root_path)
