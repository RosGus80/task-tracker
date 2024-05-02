from django.core.management.utils import get_random_secret_key  
new_key = get_random_secret_key()

print(f'Ваш новый ключ для джанго проекта: {new_key}\n'
      f'Скопируйте его и сохраните. Избегайте его распространения.')
