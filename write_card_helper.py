# -*- coding: utf-8 -*-
import pathlib
base = pathlib.Path(r"C:\Bariari-web\src\components\hashvaot")
def w(name, content): (base / name).write_text(content, encoding="utf-8"); print(f"{name}: OK")
print("helper loaded")
