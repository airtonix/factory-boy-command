factory-boy-command
===================

simple management command for [factory boy](https://github.com/rbarrois/factory_boy)


1. Install with pip
2. Place `foundry.py` recipies in your apps:
    ```
    myapp/
      static/
      templates/
      __init__.py
      models.py
      urls.py
      views.py
      foundry.py
    ```

3. Run with management command, specifying models described in your recipies: 

    `./manage forge myapp.HilariousModelName:9000 appyoucantseeyet.OmgTheseModelNamesLawl:1`



4. Customise the factory boy "recipe" module name with `FACTORYBOY_RECIPE_MODULENAME` in your settings module.
