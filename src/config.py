import os

def isFloat(s):
	return s.replace('.','',1).isdigit()

def isInteger(s):
	return s.isdigit()

def convert_value(value):
	if value == "True":
		return True
	elif value == "False":
		return False
	elif isInteger(value):
		return int(value)
	elif isFloat(value):
		return float(value)
	else:
		return value

def create_config(path):
	config_specification = {}
	with open(os.path.join(path)) as rf:
		for line in rf:
			field, value = line.strip().split("\t")
			if "," in value:
				value = value.split(",")
				value_list = []
				for subsetting in value:
					subsetting_type_converted = convert_value(subsetting)
					value_list.append(subsetting_type_converted)
				config_specification[field] = value_list
			else:
				config_specification[field] = convert_value(value)

	return config_specification
