import json
import subprocess
import dtlpy as dl
import sys

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

arguments = sys.argv
env = 'rc'
project="DataloopTasks"
publish = False
for arg in arguments:
    if arg.startswith('--env='):
        env = arg.split('=')[-1]
    elif arg.startswith('--project='):
        project = arg.split('=')[-1]
    elif arg.startswith('--publish'):
        publish = True
if publish:
    print(f'publishing dpk {dpk["name"]} version {dpk["version"]} in env {env} and in project {project}...')
    dl.projects.get(project_name=project)
    dl.dpks.publish(dpk)
    print(f'published dpk {dpk["name"]} version {dpk["version"]} in env {env} and in project {project}!')