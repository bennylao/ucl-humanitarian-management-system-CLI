class Camp:
    """A class to hold information about the size/capacity of the camp,
     and a collective overview of things like the amount of refugees,
      how many are vaccinated, how many need extra medical attention (ie doctors) etc."""

    def __init__(self, location, is_camp_available=True):
        # location should be simply a country for simplicity
        self.is_camp_available = is_camp_available
#         option to make the camp unavailable for whatever reason (e.g. it's flooded or infected
#         by disease and so other refugees shouldn't be added to that camp
#         Location should be a COUNTRY only - for simplicity ?
          self.location = location


# Need to think about other methods which might be needed in this class?

