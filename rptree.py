"""This module provides the RP Tree main module."""

import os
import pathlib
import sys

# Tree symbols
PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "


class DirectoryTree:
    """
    DirectoryTree generates a visual tree structure of a given directory.
    """

    def __init__(self, root_dir, dir_only=False, output_file=sys.stdout):
        self._output_file = output_file
        self._generator = _TreeGenerator(root_dir, dir_only)

    def generate(self):
        """Generate and print the directory tree."""
        tree = self._generator.build_tree()

        # ✅ Handle writing or console output safely
        if isinstance(self._output_file, str):
            with open(self._output_file, mode="w", encoding="UTF-8") as f:
                for entry in tree:
                    print(entry, file=f)
        else:
            # Default: print to console
            for entry in tree:
                print(entry, file=self._output_file)


class _TreeGenerator:
    """
    Helper class that builds the directory structure for DirectoryTree.
    """

    def __init__(self, root_dir, dir_only=False):
        self._root_dir = pathlib.Path(root_dir)
        self._dir_only = dir_only
        self._tree = []

    def build_tree(self):
        """Build and return the tree representation."""
        self._tree_head()
        self._tree_body(self._root_dir)
        return self._tree

    def _tree_head(self):
        """Add the root directory name to the tree."""
        self._tree.append(f"{self._root_dir}{os.sep}")
        self._tree.append(PIPE)

    def _tree_body(self, directory, prefix=""):
        """Recursively build the tree structure."""
        entries = self._prepare_entries(directory)
        entries_count = len(entries)

        for index, entry in enumerate(entries):
            connector = ELBOW if index == entries_count - 1 else TEE
            if entry.is_dir():
                self._add_directory(entry, index, entries_count, prefix, connector)
            else:
                self._add_file(entry, prefix, connector)

    def _prepare_entries(self, directory):
        """Return sorted directory entries (folders first, files later)."""
        entries = list(directory.iterdir())
        if self._dir_only:
            entries = [entry for entry in entries if entry.is_dir()]
        return sorted(entries, key=lambda entry: entry.is_file())

    def _add_directory(self, directory, index, entries_count, prefix, connector):
        """Add a directory entry and recurse into it."""
        self._tree.append(f"{prefix}{connector} {directory.name}{os.sep}")
        new_prefix = prefix + (PIPE_PREFIX if index != entries_count - 1 else SPACE_PREFIX)
        self._tree_body(directory=directory, prefix=new_prefix)
        self._tree.append(prefix.rstrip())

    def _add_file(self, file, prefix, connector):
        """Add a file entry to the tree."""
        self._tree.append(f"{prefix}{connector} {file.name}")
