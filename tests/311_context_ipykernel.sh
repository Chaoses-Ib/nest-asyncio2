# https://github.com/Chaoses-Ib/nest-asyncio2/pull/4
# Only breaks in `jupyter notebook`, not in VS Code, `ipython -c "%run 311_ipykernel.ipynb"` and `jupyter execute`.
# Looks like there is no easy way to add an end-to-end test...
# uvx --with nbformat --with-editable ../ ipython==7.3.0 -c "%run 311_context_ipykernel.ipynb"

echo Manually open 311_context_ipykernel.ipynb and run all
uvx --with-editable ../ --with ipython==7.3.0 --python 3.14 jupyter notebook
