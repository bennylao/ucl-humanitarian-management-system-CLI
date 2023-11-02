class Resource:
    """A class which tracks all generic attribues of any resource, e.g.:
    total number initially available, total number handed out, total number left. Could have a method
    which alerts volunteer/admin when resource is running out (e.g last 10%)"""

    # Should each resource have a category associated so even if someone entered "shoes" we know that is
    # Clothing that can be distributed.
    # OR alternative: have volunteer select from a dropdown list of categories which their resource fits in to?
    # How can we keep track of a dictionary of all resources we currently have available? Below line as an option?
    # We need this as a requirement is: user can display all resources currently available to the camp. So this method
    #         allows us to keep track of all available resources. Does this mean once a resource has already
    # been distributed though? Or before ..... unclear?
    dictionary_of_available_resources_and_amounts = {}


    def __init__(self, resource_name, initial_amount_available):
        self.resource_name = resource_name
        self.resource_category = resource_category
        # Do we need both resource category and resource name?
        self.initial_amount_available = initial_amount_available
        self.amount_distributed = amount_distributed
        self.amount_left = amount_left


    def track_all_available_resources(self):
        """"Requirement is that you can display all resources currently available to the camp. So this method
        allows us to keep track of all available resources and their amounts (even if that is now 0."""

        if dictionary_of_available_resources_and_amounts[self.resource_name]:
            dictionary_of_available_resources_and_amounts[self.resource_name] = self.amount_left
        else:
            dictionary_of_available_resources_and_amounts[self.resource_name] = self.initial_amount_available
    def distribute_resource(self, amount):
        """Method to take into account the number of refugees in a camp and the total amount of the resource
        left now to distribute amongst the camps to divide the resource evenly.
        Should we also keep track of and account for the amount a camp has received
        of that resource already? Is that too complicated? Or even necessary? """
        # Do we allow the user to put in the names of the camps they want to distribute across?
        # Or should it all just be equal.
        # Should we do checks by category, so if the resource is a vaccination and 1 camp has lots of
        # refugees who aren't vaccinated, that camp should automatically get more even though they camp
        # may have less refugees actually in it
        # Remember to subtract the amount distributed from amount_left
        if amount > self.amount_left:
            print("Sorry, not enough left of this resource to distribute that quantity."
                  f"you have {self.amount_left} left to distribute.")
        amount = input(f"Please enter an amount that is the same as or lower than {self.amount_left}.")
        camps = input("Please enter the names of the camps that you want this resource distributed across: ")
    #     Much more logic to add here
    #     update the dictionary with overview of resources available
        self.track_all_available_resources()
    #    Display resource running out warning if applicable by calling below method
        self.resource_running_out()


    def add_more_resource(self, amount):
        """Method to add more to the total amount of the resource left currently, therefore we can distribute
        more."""
    #     If the amount that is added is large enough that it is greater than the initial amount available,
    #     then we should update the inital amount available so that our resource running out flag is accurate
        self.amount_left += amount
        if self.amount_left > self.initial_amount_available:
            self.initial_amount_available = self.amount_left
    #     update the dictionary with overview of resources available
        self.track_all_available_resources()


    def resource_running_out(self):
        if self.amount_left < (self.initial_amount_available * 0.1):
            print("Warning: This resource is running low. You only have 10% left.")