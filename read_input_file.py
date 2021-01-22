import yaml

def read_input_value(load_path):
    with open(load_path, 'r') as yml:
        print('###########################')
        print(f"load input file{load_path}")
        print('###########################')

        input_data = yaml.safe_load(yml)
    return input_data