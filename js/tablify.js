(function () {
	var createRangeMapLinear = function (w, x, y, z) {
		m = (z - y) / (x - w);
		b = (y - (w * m));
		return {
			'm': m,
			'b': b
		};
	};

	var onTablifyCallback = function (event) {
		var headers = document.getElementById('includes').value;
		var fn_str = document.getElementById('function').value;
		var xmin = 0.0;
		var xmax = 1.0;
		var headroom_left = 0;
		var headroom_right = 0;
		var precision = 10;
		var output_type = 'cont';
		var output_type_name = 'float';
		var includes = [];
		var size = 1024;

		try {
			eval(fn_str);
		}
		catch(err) {
			alert(err.message);
			return;
		}

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

		alert(tab(0.5));
	};

	document.getElementById('tablify-go').addEventListener("click", onTablifyCallback);
})();