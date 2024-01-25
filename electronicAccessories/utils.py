class DefaultValue:
    def get_default_context(self):
        return {'title': 'Страница обычная'}

    def add_default_context(self, context: dict) -> dict:
        context['name'] = 'Страница по умолчанию'
        return context

    def add_title_context(self, context: dict, title_name: str) -> dict:
        context['name'] = title_name
        return context
