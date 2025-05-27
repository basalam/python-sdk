#!/usr/bin/env python
"""Setup script for the Basalam SDK package."""

import setuptools

if __name__ == "__main__":
    # Use setuptools_scm for versioning from git tags
    setuptools.setup(
        # Most configuration is in pyproject.toml
        # This file exists mainly for backward compatibility
        package_dir={"": "src"},
        packages=setuptools.find_packages(where="src"),
    )
