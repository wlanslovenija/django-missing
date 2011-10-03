from docutils import nodes

def setup(app):
	app.add_generic_role('filter', nodes.literal)
	app.add_generic_role('tag', nodes.literal)
