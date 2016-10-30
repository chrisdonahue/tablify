def range_map_linear_get(w, x, y, z):
	m = (z - y) / (x - w)
	b = (y - (w * m))
	return {
		'm': m,
		'b': b
	}

def generate_table_for_function(
	function,
	table_length,
	p_min,
	p_max,
	headroom_left=0,
	headroom_right=0,
	**kwargs
):
	assert table_length > 0
	assert headroom_left >= 0
	assert headroom_right >= 0
	assert table_length > headroom_left + headroom_right

	# create range map
	idx_to_p_map = range_map_linear_get(
		float(headroom_left),
		float(table_length - headroom_right),
		float(p_min),
		float(p_max)
	)

	# generate table
	table = []
	for idx in xrange(table_length):
		x = idx_to_p_map['m'] * float(idx) + idx_to_p_map['b']
		table.append(function(x, **kwargs))

	return table

def is_power_of_two(n):
	return (n & (n-1) == 0) and (n != 0)

def serialize_table(table, val_fmt_fn):
	serialized = '{'
	serialized += ', '.join([val_fmt_fn(entry) for entry in table])
	serialized += '}'
	return serialized

def generate_header_for_table(
	table,
	name,
	p_min,
	p_max,
	headroom_left=0,
	headroom_right=0,
	precision=10,
	output_type='cont',
	output_type_prim='float',
	includes=[]
):
	assert output_type in ['cont', 'cont_d']
	table_length = len(table)
	assert table_length > 0
	assert headroom_left >= 0
	assert headroom_right >= 0
	assert table_length > headroom_left + headroom_right

	p_to_idx_map = range_map_linear_get(
		float(p_min),
		float(p_max),
		float(headroom_left),
		float(table_length - headroom_right)
	)

	# generate header
	precision_fmt_str = '{:.' + str(precision) + 'f}'
	if output_type == 'cont':
		val_fmt_fn = lambda x: (precision_fmt_str + 'f').format(float(x))
	elif output_type == 'cont_d':
		val_fmt_fn = lambda x: (precision_fmt_str).format(float(x))

	c_h = ''
	c_h += '/* Automatically generated by tablify.py */\n'
	c_h += '\n'
	c_h += '#ifndef {}_TABLIFIED_H\n'.format(name.upper())
	c_h += '#define {}_TABLIFIED_H\n'.format(name.upper())
	c_h += '\n'
	for include in includes:
		c_h += '#include {}\n'.format(include)
	c_h += '\n'
	c_h += '#define {}_TABLE_LENGTH {}\n'.format(name.upper(), table_length)
	if is_power_of_two(table_length) and headroom_left == 0 and headroom_right == 0:
		c_h += '#define {}_TABLE_MASK {}\n'.format(name.upper(), table_length - 1)
	c_h += '#define {}_TABLE_LENGTH_F {}\n'.format(name.upper(), val_fmt_fn(table_length))
	c_h += '\n'
	c_h += '#define {}_DOMAIN_MIN {}\n'.format(name.upper(), val_fmt_fn(p_min))
	c_h += '#define {}_DOMAIN_MAX {}\n'.format(name.upper(), val_fmt_fn(p_max))
	c_h += '#define {}_DOMAIN_TO_IDX_M {}\n'.format(name.upper(), val_fmt_fn(p_to_idx_map['m']))
	c_h += '#define {}_DOMAIN_TO_IDX_B {}\n'.format(name.upper(), val_fmt_fn(p_to_idx_map['b']))
	c_h += '\n'
	c_h += 'static const {} {}_table[{}] = {};\n'.format(output_type_prim, name, table_length, serialize_table(table, val_fmt_fn))
	c_h += '\n'
	c_h += '#endif'

	return c_h
