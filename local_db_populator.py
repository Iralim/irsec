import os
from django.utils.timezone import now

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'irsec.settings')
django.setup()



from app_irsec.models import Category, Topic

def load_folders_files(path, parent_dir=None):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)

        # FOLDER
        if os.path.isdir(item_path):
            category, created = Category.objects.get_or_create(name=item, parent=parent_dir)
            if created:
                print(f"Added category: {category.name} ")
            else:
                print(f"Syncronized category: {category.name}")
            
            load_folders_files(item_path, parent_dir=category)

        # FILE
        elif os.path.isfile(item_path):
            with open(item_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if not content:
                    print(f"Warning: File {item_path} is empty.")
                    content = None
            
            topic_name = os.path.splitext(item)[0]
            

            topic, created = Topic.objects.get_or_create(
                name=topic_name, 
                category=parent_dir,
                file_name=item
                )

            if created:
                print(f"Added topic {topic.name} in category {parent_dir.name}")
                topic.content = content
            else:
                print(f"Syncronized topic {topic.name} in category {parent_dir.name}")
                
            

            if topic.content != content:
                topic.content = content
                topic.updated_at = now()
                topic.save()
                print(f"Topic: {topic.name} updated")
            topic.save()
        
        else:
            print(f"Skiped {item_path}, not a folser or file.")

def remove_old_entries(root_path, category_dir=None):
    categories = Category.objects.filter(parent=category_dir)
    topics = Topic.objects.filter(category=category_dir)

    # FOLDER
    for category in categories:
        folder_path = os.path.join(root_path, category.name)
        if not os.path.exists(folder_path):
            category.delete()
            print(f"Category: {category.name} deleted")
            continue
        remove_old_entries(folder_path, category_dir=category)

    # FILE
    for topic in topics:
        file_path = os.path.join(root_path, topic.file_name)
        if not os.path.exists(file_path):
            topic.delete()
            print(f"Topic: {topic.name} deleted")


if __name__ == '__main__':
    load_folders_files('/media/erik/637738823CDCAF57/Element/IT')
    remove_old_entries('/media/erik/637738823CDCAF57/Element/IT')
   