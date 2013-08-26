factory-boy-command
===================

simple management command for factory boy


1. Install with pip
2. Place `factory.py` recipies in your apps::

    myapp/
      static/
      templates/
      __init__.py
      models.py
      urls.py
      views.py
      factories.py

3. Run with management command, specifying models described in your recipies: 

    ./manage boy someotherapp.HilariousModelName:9000 yetanotherapp.OmgTheseModelNamesLawl:1
