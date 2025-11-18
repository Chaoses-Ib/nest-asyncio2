rm -r -Force dist, build
uv run setup.py sdist bdist_wheel
uvx twine upload dist/*
rm -r -Force dist, build, *.egg-info
