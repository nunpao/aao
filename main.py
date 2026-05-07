from data.instance_loader import load_all_instances
from heuristics.constructive import efficiency_greedy

instances = load_all_instances("instances")
print(f"Successfully loaded {len(instances)} files.")
for instance in instances:
    solution = efficiency_greedy(instance)
    print(f"a solução de merda que encontrei foi esta: {solution.z}, para veres o quao merda ela foi {(instance.optimal - solution.z) / instance.optimal} ")
