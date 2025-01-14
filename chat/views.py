from django.shortcuts import render
from chat.models import Group, Chat

def index(request, group_name):
    group, created = Group.objects.get_or_create(name=group_name)

    # If group is created, initialize chats as an empty queryset
    if created:
        print(f"Group '{group}' created.")
        chats = Chat.objects.none()  # Empty queryset
    else:
        chats = Chat.objects.filter(group=group)

    return render(request, 'chat/index.html', {'group_name': group_name, 'chats': chats})
