
# Checks to see if the src package is a package and if it is, it will print out the submodules.
import pkgutil
import src

package = src
for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
    print(f"Found submodule {modname} (is a package: {ispkg})")

# This file is the entry point of the application. It creates the app and runs it.
from src.app.serve_app import create_app

if __name__ == "__main__":
    create_app().run_server(debug=True)