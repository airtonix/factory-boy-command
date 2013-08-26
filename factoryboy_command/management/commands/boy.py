import copy

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule

import factory
import inspect


class Command(BaseCommand):
    args = '<modelpath modelpath:count ...>'
    help = 'Generate model instances using model-mommy'
    factories = {}

    def get_subklasses(self, module, klass):
        for name, cls in inspect.getmembers(module):
            if inspect.isclass(cls) and issubclass(cls, klass):
                yield cls


    def autodiscover(self):
        """
        Auto-discover INSTALLED_APPS mockup.py modules and fail silently when
        not present. This forces an import on them to register any mockup bits they
        may want.
        """
        _registry = None

        for app in getattr(settings, 'INSTALLED_APPS', []):
            mod = import_module(app)
            # Attempt to import the app's mockup module.
            try:
                before_import_registry = copy.copy(_registry)
                recipe = import_module('%s.boy' % app)
                for thing in self.get_subklasses(recipe, factory.Factory):
                    self.factories[thing.FACTORY_FOR.__name__] = thing

            except Exception as error:
                _registry = before_import_registry
                if module_has_submodule(mod, 'boy'):
                    raise

    def handle(self, *args, **options):
        self.autodiscover()

        for modelpath in args:
            count = 1
            if ":" in modelpath:
                modelpath, count = modelpath.split(":")

            model_name = modelpath.split(".", 1)[1]
            factory = self.factories.get(model_name, None)
            if factory:
                self.stdout.write("Processing: {}".format(model_name))
                factory()
