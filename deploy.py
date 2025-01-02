
import dtlpy as dl

dl.setenv('rc')
dl.login()
p = dl.projects.get(project_id='f8a4b8ce-5ff3-4386-84dc-1bda3a5bc92a')
d = p.dpks.publish()