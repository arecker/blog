"""Functions and objects for introspection and reflection."""

import pathlib
import typing

src_dir: typing.Annotated[pathlib.Path,
                          "source code directory"] = pathlib.Path(
                              __file__).absolute().parent
"""source code directory"""
assert src_dir.name == 'src'
