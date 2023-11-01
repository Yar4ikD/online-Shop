from celery import shared_task

from shops.management.commands.import_yaml import Command


@shared_task(name="Импорт товаров")
def etl_task(email=None, file=None):
    func = Command().handle(email=email, file=file)
    if func:
        unloads = func.load()
        multiplication = func.transform(unloads)
        func.extract(multiplication)

    return "my result data"
