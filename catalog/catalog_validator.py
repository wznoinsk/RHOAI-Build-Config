import yaml
from collections import defaultdict

build_config = yaml.safe_load(open('build-config.yaml'))

supported_ocp_versions = build_config['config']['supported-ocp-versions']['release']
shipped_rhoai_versions = open('shipped_rhoai_versions.txt').readlines()

shipped_rhoai_versions = sorted(list(set([version.split('-')[0].strip('\n').replace('v', '') for version in shipped_rhoai_versions if version.count('.') > 1])))
print(shipped_rhoai_versions)

def parse_catalog_yaml(catalog_yaml_path):
    # objs = yaml.safe_load_all(open(self.catalog_yaml_path))
    objs = yaml.safe_load_all(open(catalog_yaml_path))
    catalog_dict = defaultdict(dict)
    for obj in objs:
        catalog_dict[obj['schema']][obj['name']] = obj
    return catalog_dict

missing_bundles = {}
for ocp_version in supported_ocp_versions:
    catalog_dict = parse_catalog_yaml(f'{ocp_version}/rhods-operator/catalog.yaml')
    bundles = catalog_dict['olm.bundle']
    missing_bundles[ocp_version] = []
    for rhoai_version in shipped_rhoai_versions:
        operator_name = f'rhods-operator.{rhoai_version}'
        if operator_name not in bundles:
            missing_bundles[ocp_version].append(operator_name)

print(missing_bundles)
