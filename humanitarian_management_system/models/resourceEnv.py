from resourceTesting import ResourceTest

test_instance = ResourceTest(campID=1, pop=100, total_pop=1000)

print(test_instance.calculate_resource_jess())

alloc_ideal = test_instance.calculate_resource_jess()
alloc_ideal = test_instance.determine_above_below(threshold = 0.10)
redistribute_sum_checker = test_instance.redistribute()

print(alloc_ideal.groupby('resourceID')['current'].sum())
print(redistribute_sum_checker)

print("hi all good")
