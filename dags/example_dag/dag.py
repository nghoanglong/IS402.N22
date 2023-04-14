from jinja2 import Template
from yaml import load, Loader
import pprint, os, inspect
import airflow, logging, sys
from dag_builder import DagBuilder

pp = pprint.PrettyPrinter(indent=2)


# script directory
current_path = os.path.dirname(
	os.path.abspath(
		inspect.getfile(
			inspect.currentframe()
		)
	)
)

# create Jinja Template from template file
with open(os.path.join(current_path, 'config.yaml'), 'r') as infile:
    template = Template(infile.read())


value = {
    'checking': os.path.join(current_path, "processing", "process_data.py"),
    "local_ds_nodash": "{{macros.hmd_plugins.local_ds_nodash(ts)}}",
    'check_date': "{{data_interval_start.to_date_string()}}"
}

configs = load(template.render(value), Loader=Loader)


dag = DagBuilder(configs).build()
