import math

from tablify import generate_table_for_function, generate_header_for_table

# sine table
def sine(x):
	return math.sin(2.0 * math.pi * x)
sine_table = generate_table_for_function(
	function=sine,
	table_length=1024,
	headroom_left=0,
	headroom_right=0,
	p_min=0.0,
	p_max=1.0,
)
sine_header = generate_header_for_table(
	table=sine_table,
	name='sine',
	headroom_left=0,
	headroom_right=0,
	p_min=0.0,
	p_max=1.0,
	precision=20,
	output_type='cont',
	output_type_prim='t_float',
	includes=['"m_pd.h"']
)
with open('tablify_sine.h', 'w') as f:
	f.write(sine_header)

# cosine table
def cosine(x):
	return math.cos(2.0 * math.pi * x)
cosine_table = generate_table_for_function(
	function=cosine,
	table_length=1024,
	headroom_left=0,
	headroom_right=0,
	p_min=0.0,
	p_max=1.0,
)
cosine_header = generate_header_for_table(
	table=cosine_table,
	name='cosine',
	headroom_left=0,
	headroom_right=0,
	p_min=0.0,
	p_max=1.0,
	precision=20,
	output_type='cont',
	output_type_prim='t_float',
	includes=['"m_pd.h"']
)
with open('tablify_cosine.h', 'w') as f:
	f.write(cosine_header)

# gaussian table
def gaussian(x, mean, sigma):
    var = sigma ** 2.0
    num = math.exp(-((x - mean) ** 2.0) / (2.0 * var))
    den = (2.0 * math.pi * var) ** 0.5
    return num/den
gaussian_table = generate_table_for_function(
	function=gaussian,
	table_length=4096,
	headroom_left=2,
	headroom_right=1,
	p_min=-10.0,
	p_max=10.0,
	mean=0.0,
	sigma=2.23606
)
gaussian_table_max_inverse = 1.0 / max(gaussian_table)
gaussian_table = map(lambda x: x * gaussian_table_max_inverse, gaussian_table)
gaussian_header = generate_header_for_table(
	table=gaussian_table,
	name='gaussian',
	headroom_left=2,
	headroom_right=1,
	p_min=-10.0,
	p_max=10.0,
	precision=20,
	output_type='cont',
	output_type_prim='t_float',
	includes=['"m_pd.h"']
)
with open('tablify_gaussian.h', 'w') as f:
	f.write(gaussian_header)