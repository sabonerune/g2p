from PyInstaller.utils.hooks import collect_submodules

_MODULE_NAME = "inflect"

module_collection_mode = {
    i: "py" if i == _MODULE_NAME else "pyz" for i in collect_submodules(_MODULE_NAME)
}
