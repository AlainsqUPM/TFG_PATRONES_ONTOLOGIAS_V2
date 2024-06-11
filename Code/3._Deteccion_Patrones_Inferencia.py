import argparse
import os.path
from Code.download_ontology import download_ontologies
from Code.create_structure import create_structure
from Code.identify_patterns import identify_patterns
from Code.infer_structures import infer_structures

try: os.mkdir("registros");
except: None

def main(ontology_path, csv_path, output_path, patterns_type, flatten_lists):
    print(output_path)
    if output_path != '' and check_output_error(output_path):
        error_log_path = os.path.join(output_path, 'error_log.txt')
        structure_csv_path = os.path.join(output_path, 'Structure.csv')
        structure_type_path = os.path.join(output_path, 'Structure_term_type.txt')
        structure_name_path = os.path.join(output_path, 'Structure_term_name.txt')
        inferred_type_path = os.path.join(output_path, 'Structure_term_inferred_type.txt')
        inferred_blank_nodes_path = os.path.join(output_path, 'Structure_term_inferred_blank_nodes.txt')
        patterns_type_path = os.path.join(output_path, 'Patterns_type')
        patterns_name_path = os.path.join(output_path, 'Patterns_name')   
    else:
        error_log_path = 'error_log.txt'
        structure_csv_path = 'Structure.csv'
        structure_type_path = 'Structure_term_type.txt'
        structure_name_path = 'Structure_term_name.txt'
        inferred_type_path = 'Structure_term_inferred_type.txt'
        inferred_blank_nodes_path = 'Structure_term_inferred_blank_nodes.txt'
        patterns_type_path = 'Patterns_type'
        patterns_name_path = 'Patterns_name'

    error_log = open(error_log_path , "w", encoding='utf-8')
    error_log.truncate()
    flatten = True if flatten_lists == 'yes' else False
    if csv_path != '' and check_csv_error(csv_path, error_log): error_log.close(); exit(-1)
    if check_ontology_error(ontology_path, error_log): error_log.close(); exit(-1)
    if csv_path != '': download_ontologies(csv_path, ontology_path, error_log)
    
    create_structure(ontology_path, error_log, flatten, structure_csv_path, structure_type_path, structure_name_path)
    infer_structures(inferred_type_path, inferred_blank_nodes_path, structure_type_path, structure_name_path)
    if patterns_type == 'type': identify_patterns(inferred_type_path, patterns_type_path)
    elif patterns_type == 'name': identify_patterns(inferred_blank_nodes_path, patterns_name_path)
    else: identify_patterns(inferred_type_path, patterns_type_path); identify_patterns(inferred_blank_nodes_path, patterns_name_path)  
    error_log.close()

def check_csv_error(csv_path, error_log):
    if not os.path.isfile(csv_path): error_log.write(f'The path --csv_path {csv_path} is not a file\n'); print(f'The path --csv_path {csv_path} is not a file\n')
    elif not csv_path.endswith('.csv'): error_log.write(f'The path --csv_path {csv_path} is not a csv\n'); print(f'The path --csv_path {csv_path} is not a csv\n')   
    else: return False
    return True

def check_ontology_error(ontology_path, error_log):
    if not os.path.isdir(ontology_path): error_log.write(f'The path --ontology_path {ontology_path} is not a directory\n'); print(f'The path --ontology_path {ontology_path} is not a directory\n')
    else: return False
    return True

def check_output_error(output_path):
    if not os.path.isdir(output_path): print(f'The path --output_path {output_path} is not a directory\n')
    else: return True
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Identify patterns from a set of ontologies')
    parser.add_argument('-ontology', '--ontology_path', type=str, default=r'rdf/')
    parser.add_argument('-csv', '--csv_path', type=str, default='')
    parser.add_argument('-output', '--output_path', type=str,default=r'registros/')
    parser.add_argument('-patterns', '--patterns_type', type=str, choices=['type', 'name', 'both'], default='type')
    parser.add_argument('-flatten', '--flatten_lists', type=str,choices=['yes', 'no'],default='no')
    args = parser.parse_args()
    main(args.ontology_path, args.csv_path, args.output_path, args.patterns_type, args.flatten_lists)
