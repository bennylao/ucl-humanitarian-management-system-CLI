#Martha: Question: are we to assume that if someone adds a resource, it will be
# immediately distributed across camps, on the assumption
#that we probably won't want volunteers to just be storing resources ?
#This influences the logic of distribution quite a lot.
#E.g. amount left will only be amount left per camp.

from humanitarian_management_system.models.refugee import Refugee
from humanitarian_management_system.models.camp import Camp
import pandas as pd

class Resource:
    list_of_resource_categories = []

    """A class which tracks all generic attributes of any resource, e.g.:
    total number available, total number handed out, total number left. Could have a method
    which alerts volunteer/admin when resource is running out (e.g last 10%)"""

    # OR alternative: have volunteer select from a dropdown list of categories which their resource fits in to?
    # How can we keep track of a dictionary of all resources we currently have available? Below line as an option?
    # We need this as a requirement is: user can display all resources currently available to the camp. So this method
    #         allows us to keep track of all available resources. Does this mean once a resource has already
    # been distributed though? Or before ..... unclear?
    # dictionary_of_available_resources_and_amounts = {}


    def __init__(self, resource_category):
       # Should resource category be here or should there be a seperate method? confused...
       self.resource_category = resource_category
       if self.resource_category.lower() not in Resource.list_of_resource_categories:
            Resource.list_of_resource_categories.append(self.resource_category.lower())



    def resource_report(self):
        """"Requirement is that you can display all resources currently available to the camp. So this method
        allows us to keep track of all available resources and their amounts (even if that is now 0."""

        # JESS: 
        # Reading the first CSV file
        resourceLibrary_df = pd.read_csv('data/resourceType.csv')
        resourceAllocs_df = pd.read_csv('data/resourceAllocation.csv')

        resource_menu = int(input('Please select the type of resource report: [1] view total stock levels of all resources; [2] view resource levels by assigned camp'))

        if resource_menu == 1:
            
            joined_df = pd.merge(resourceLibrary_df, resourceAllocs_df, on = 'resourceID', how = 'inner')
            # now need to sum the quantity column by the resourceID
            resourceSum_df = joined_df.groupby('resourceID').agg({
                'name': 'first',  # Keeps the first name for each group
                'priorityLvl': 'first',  # Keeps the first priorityLvl for each group
                'qty': 'sum'  # Sums the allocatedQuantity for each group
            }).reset_index()

            print(resourceSum_df)

        elif resource_menu == 2:
            pivot_df = joined_df.pivot_table(index=['name', 'priorityLvl'], columns='campID', values='qty', aggfunc='sum')
            print(pivot_df)
            ### JESS: maybe add conditional alerts in here later... as an extra 
            ### later, can also create a global view with resources compared to capacity in camps or something 
        else:
            ####
            pass

        # Do we need this dictionary if we're using pd?
        # if dictionary_of_available_resources_and_amounts[self.resource_category]:
        #     dictionary_of_available_resources_and_amounts[self.resource_category] = self.amount_left
        # else:
        #     dictionary_of_available_resources_and_amounts[self.resource_name] = self.initial_amount_available


    def add_resource(self):
        """Method to call when we are distributing a resource so that we update the camp figures"""
        # Shouold this be in camp file?
        pass


    def distribute_resource(self):
        """Method to take into account the number of refugees in a camp and the total amount of the resource
        left now to distribute amongst the camps to divide the resource evenly.
        Should we also keep track of and account for the amount a camp has received
        of that resource already? Is that too complicated? Or even necessary? """
        self.resource_category = input("Please select the category of resource you want to distribute: ")
        distribution_method = int(input("Please enter 1 to specify the name of the camps that you want this resource distributed across."
                            "Or enter 2 for us to distribute the resource fairly across the camps for you: "))
        #     Much more logic to add here
        #     update the dictionary with overview of resources available
        if distribution_method == 1:
            self.distribute_resource_specific_camps()
        elif distribution_method == 2:
            self.distribute_resource_automatically()
        else:
            "Sorry! that's not an option. Let's go again"
            self.distribute_resource()

    def distribute_resource_automatically(self):
        amount = float(input("Please enter the amount of this resource you have to distribute: "))
        #Need to iterate through camps to get the number of refugees, and how much of this category of resource is there in each
        #Below is a potential algoriothm to distribute the amounts fairly. We could top up camps whose current level of resource is less than the average %?
        # total_refugees = sum(camp.num_refugees for camp in camps)
        total_refugees = Refugee.total_number
        average_per_refugee = amount / total_refugees if total_refugees > 0 else 0
        total_current_resources = sum(camp.current_resource_amount for camp in camps)

        for camp in Camp.camp_data:
            # Calculate how much to distribute to this camp
            difference = max(0, average_per_refugee - camp.current_resource_amount)

            # Calculate the proportional share based on the difference
            proportional_share = (difference / total_current_resources) * amount

            # Update the camp's resource amount
            camp.current_resource_amount += proportional_share

            # Output distribution information (optional)
            print(f"Distributed {proportional_share} to {camp.name}")

        # Output total distribution information (optional)
        print(f"Total distributed: {amount}")


    def distribute_resource_specific_camps(self):
        resource_category = self.resource_category
        # user want to distribute this specific resource and this specific amount across the camps that they specify
        # camp_list = []
        # number_of_camps = int(input("Please enter the number of camps you want to distribute this resource to now: "))
        # for i in range(number_of_camps):
        #     amount = float(input("Please enter the amount of this resource you have to distribute to the first camp: "))
        #     camp = input("Now please enter the name of the camp you wish to distribute this to: ")
        #     camp_list.append(camp)
        # for camp in camp_list:
            #SOme logic to update teh amount of this resource in the camps!
        camps = input("Enter the names of the camps that you will be allocating this resource to (comma-separated): ").split(',')
        # Need some logic to make sure non comma separated list doesn't break the code. Or use above method? Maybe better
        for camp in camps:
             amount = float(input("Enter amount for {}: ".format(camp)))
            # SOme logic to update teh amount of this resource in the camps!

            # camp.add_resource()
        pass




        self.resource_report()
        #    Display resource running out warning if applicable by calling below method
        # self.resource_running_out()


    # def add_more_resource(self, amount):
    # Is this needed if we distribute resources immediately?
    #     """Method to add more to the total amount of the resource left currently, therefore we can distribute
    #     more."""
    #     #     If the amount that is added is large enough that it is greater than the initial amount available,
    #     #     then we should update the inital amount available so that our resource running out flag is accurate
    #     self.amount_left += amount
    #     if self.amount_left > self.initial_amount_available:
    #         self.initial_amount_available = self.amount_left
    #     #     update the dictionary with overview of resources available
    #     self.resource_report()

    # def resource_running_out(self):
    #     if self.amount_left < (self.initial_amount_available * 0.1):
    #         print("Warning: This resource is running low. You only have 10% left.")
