from django import template
from menu.models import MenuItem

register = template.Library()

@register.inclusion_tag('tree_menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = request.path

    # Получаем все пункты меню 1 запросом засечёт LEFT JOIN
    menu_items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent')

    # Создаём структуру меню
    menu_tree = []
    item_dict = {}

    # Создаём основу для меню
    for item in menu_items:
        item_dict[item.id] = {
            'item': item,
            'children': [],
            'is_active': item.is_active(current_url),
            'is_parent_active': False
        }

    # Собираем структуру дерева
    for item in item_dict.values():
        if item['item'].parent_id:
            parent = item_dict.get(item['item'].parent_id)
            if parent:
                parent['children'].append(item)
                # Если текущий пункт активен/раскрыт — помечаем родителя
                if item['is_active'] or item['is_parent_active']:
                    parent['is_parent_active'] = True
        else:
            menu_tree.append(item)

    return {
        'menu_tree': menu_tree,
        'current_url': current_url,
        'menu_name': menu_name,
    }