../../hacking/module_formatter.py ../../hacking/templates/rst.j2
PYTHONPATH=../../lib ../../hacking/module_formatter.py -t rst --template-dir=../../hacking/templates --module-dir=../../lib/ansible/modules -o rst/
sphinx-build   "rst" "_build" rst/oneview_*.rst
