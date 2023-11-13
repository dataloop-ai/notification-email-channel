import json
import subprocess

with open('./dataloop.json') as json_file:
    dpk = json.load(json_file)
    current_version = dpk['version'].split('.')
    current_version[-1] = str(int(current_version[-1]) + 1)
    dpk['version'] = '.'.join(current_version)
    dpk['codebase']['gitTag'] = f'v{dpk["version"]}'
    current_version = dpk['codebase']['gitTag']
    print(current_version)
    
with open("./dataloop.json", "w") as jsonFile:
    json.dump(dpk, jsonFile, indent=2)

cmd = ['git', 'commit', '-am', current_version]
p = subprocess.Popen(cmd)
p.communicate()
cmd = ['git', 'tag', '-a', current_version, '-m', current_version]
p = subprocess.Popen(cmd)
p.communicate()
cmd = ['git', 'push', '--follow-tags']
p = subprocess.Popen(cmd)
p.communicate()