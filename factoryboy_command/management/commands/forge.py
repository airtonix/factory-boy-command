import copy

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule

import factory
import inspect


FACTORYBOY_RECIPE_MODULENAME = getattr(settings, "FACTORYBOY_RECIPE_MODULENAME", "foundry")


class Command(BaseCommand):
    args = '<modelpath modelpath:count ...>'
    help = 'Generate model instances using model-mommy'
    foundries = {}

    def get_subklasses(self, module, klass):
        for name, cls in inspect.getmembers(module):
            if inspect.isclass(cls) and issubclass(cls, klass):
                yield cls

    def autodiscover(self, limit_to=None):
        """
        Auto-discover INSTALLED_APPS mockup.py modules and fail silently when
        not present. This forces an import on them to register any mockup bits they
        may want.
        """
        _registry = None
        application_list = getattr(settings, 'INSTALLED_APPS', [])

        if not limit_to is None:
            application_list = [filtered_app for filtered_app in application_list if filtered_app in limit_to]

        for appname in application_list:
            mod = import_module(appname)

            try:
                before_import_registry = copy.copy(_registry)
                path = '{}.{}'.format(appname, FACTORYBOY_RECIPE_MODULENAME)
                print path
                foundry = import_module(path)
                for thing in self.get_subklasses(foundry, factory.Factory):
                    self.foundries[thing.FACTORY_FOR.__name__] = thing

            except Exception as error:
                _registry = before_import_registry
                if module_has_submodule(mod, FACTORYBOY_RECIPE_MODULENAME):
                    raise

    def handle(self, *args, **options):

        appnames = [item.split(".", 1)[0] for item in args]
        model_names = [item.split(".", 1)[1] for item in args]

        self.autodiscover(limit_to=appnames)

        for model_name in model_names :
            count = 1

            if ":" in model_name :
                model_name, count = model_name.split(":")

            factory = self.foundries.get(model_name, None)

            if factory :
                self.stdout.write("Processing: {}".format(model_name))
                factory()
