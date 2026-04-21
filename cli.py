import argparse
from commands.list_command import setup_parser as setup_list
from commands.add_command import setup_parser as setup_add
from commands.remove_command import setup_parser as setup_remove
from commands.edit_command import setup_parser as setup_edit
from commands.tags_command import setup_parser as setup_tags
from commands.status_command import setup_parser as setup_status
from orders import OrderManager
from storage import load, save


def create_cli():
    """Создаёт парсер CLI с поддержкой всех команд."""
    parser = argparse.ArgumentParser(description="Управление заказами")
    subparsers = parser.add_subparsers(
        dest="command", help="Доступные команды")

    # Подключаем все команды
    setup_list(subparsers)
    setup_add(subparsers)
    setup_remove(subparsers)
    setup_edit(subparsers)
    setup_tags(subparsers)
    setup_status(subparsers)

    return parser


def run_cli():
    """Запускает CLI с загрузкой/сохранением данных."""
    # Загружаем данные при старте
    orders_data = load()
    order_manager = OrderManager()
    order_manager._orders = orders_data

    parser = create_cli()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Обрабатываем команду
    if args.command == "list":
        from commands.list_command import handle_list
        handle_list(order_manager, args)
    elif args.command == "add":
        from commands.add_command import handle_add
        handle_add(order_manager, args)
    elif args.command == "remove":
        from commands.remove_command import handle_remove
        handle_remove(order_manager, args)
    elif args.command == "edit":
        from commands.edit_command import handle_edit
        handle_edit(order_manager, args)
    elif args.command == "tags":
        from commands.tags_command import handle_tags
        handle_tags(order_manager, args)
    elif args.command == "status":
        from commands.status_command import handle_status
        handle_status(order_manager, args)

    # Сохраняем данные после выполнения команды
    save(order_manager.list_orders())
