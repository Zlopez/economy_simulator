# Percentage of fertility - 0 means no young people are born
# 100 means that there is one young on one adult (keep in mind
# that this works even when the young becomes adult, so the adult
# will have another child)
# The fertility rate could be more then 100 percent, this means that
# there is more then one young on one adult
# The number of young people is always rounded up
FERTILITY_RATE=100
# Age at which the young becomes adult
ADULTHOOD_AGE=20
# Age at which the adult becomes old
SENIOR_AGE=50
# Age at which the old people die
LONGEVITY=70
# Starting amount of coin in circulation
STARTING_AMOUNT_OF_COIN = 100000
# Starting population
YOUNG=0
ADULTS=100
SENIOR=0
# Number of years to run simulation for
YEARS=100


def calculate_salary(adults:int, total_coin_amount:int) -> float:
    """
    Calculate salary of adults. This will take the total
    amount of coins currently available in circulation and
    distribute it equally between the adults.

    Params:
      adults: Number of adults to distribute the coins between.
      total_coin_amount: Total amount of coins available.

    Returns:
      Amount of coins in salary.
    """
    return total_coin_amount/adults


def calculate_population(
        year:int, young:int, adults:int,
        old:int, population_history:dict
    ) -> dict:
    """
    Calculate the new population for this year, add the
    change to population_history and updates the dictionary.

    Params:
      year: Year for which the population would be calculated
      young: Current number of young people in population
      adults: Current number of adults in population
      old: Current number of old people in population
      population_history: Dictionary containing the history of population
        {
            0: { # Year the data are relevant to
                "born": 10, # How many young were born that year
                "adulthood": 10, # How many people became adults that year
                "senior": 10, # How many people became seniors that year
                "died": 10, # How many people died that year
            }
        }

    Returns:
      New population history with current year.
    """
    born = 0
    if not round(adults*(FERTILITY_RATE/100)) == young:
        born = round(adults*(FERTILITY_RATE/100)) - young
    if born < 0:
        born = 0

    reached_adulthood = 0
    if year-ADULTHOOD_AGE >= 0:
        reached_adulthood = population_history[year-ADULTHOOD_AGE]["born"]

    reached_senior = 0
    if year-SENIOR_AGE >= 0:
        reached_senior = population_history[year-SENIOR_AGE]["born"]

    died = 0
    if year-LONGEVITY >= 0:
        died = population_history[year-LONGEVITY]["born"]

    population_history[year+1] = {
        "born": born,
        "adulthood": reached_adulthood,
        "senior": reached_senior,
        "died": died
    }

    return population_history


def year_tick(economy:dict, population_history: dict, total_coin_amount: int) -> dict:
    """
    This is a year of economy simulation. This function takes economy
    dictionary and uses the content of the dictionary as starting
    values for this year and generates a new economy dictionary.

    Params:
      economy: Dictionary containing the state of the economy.
        Example::
        {
            "year": 0, # What year this is
            "goods_consumption": 150, # How many goods are being consumed by population
            "young": 50, # How many young people are in population (not getting salary)
            "adults": 50, # How may adults are in population
            "old": 50, # How many old people are in population (not getting salary)
            "salary": 1000, # How high is the salary
            "dependent": 3, # How many people are dependent on one adult
            "coin value": 1 # How much is the value of one coin
        }
      population_history: Dictionary containing the history of population
        {
            0: { # Year the data are relevant to
                "born": 10, # How many young were born that year
                "adulthood": 10, # How many people became adults that year
                "senior": 10, # How many people became seniors that year
                "died": 10, # How many people died that year
            }
        }
    total_coin_amount: Amount of the coins available in circulation

    Returns:
      Economy dictionary with new values.
    """
    next_year_economy = {}
    next_year_economy["year"] = economy["year"] + 1
    next_year_economy["young"] = (
        economy["young"] + population_history[next_year_economy["year"]]["born"] - population_history[next_year_economy["year"]]["adulthood"]
    )
    next_year_economy["adults"] = (
        economy["adults"] + population_history[next_year_economy["year"]]["adulthood"] - population_history[next_year_economy["year"]]["senior"]
    )
    next_year_economy["old"] = (
        economy["old"] + population_history[next_year_economy["year"]]["senior"] - population_history[next_year_economy["year"]]["died"]
    )
    next_year_economy["salary"] = calculate_salary(next_year_economy["adults"], total_coin_amount)
    next_year_economy["dependent"] = (next_year_economy["young"] + next_year_economy["old"]) / next_year_economy["adults"]
    next_year_economy["coin_value"] = ((total_coin_amount/ADULTS) / next_year_economy["salary"])

    return next_year_economy


if __name__=="__main__":
    economy = {
        "year": 0,
        "young": YOUNG,
        "adults": ADULTS,
        "old": SENIOR,
        "salary": float(STARTING_AMOUNT_OF_COIN/ADULTS),
        "dependent": 1.0,
        "coin_value": 1.0
    }
    population_history = {}
    population_history[0] = {
        "born": 0,
        "adulthood": ADULTS,
        "senior": 0,
        "died": 0
    }
    print("{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}".format(
        "Year", "Young", "Adults", "Old", "Salary", "dependent", "Coin value", "Born", "Adulthood", "Senior", "Died"
    ))
    print("{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}".format(
        economy["year"], economy["young"], economy["adults"], economy["old"],
        economy["salary"], economy["dependent"], economy["coin_value"],
        population_history[0]["born"], population_history[0]["adulthood"],
        population_history[0]["senior"], population_history[0]["died"]
    ))

    for year in range(1,YEARS):
        population_history = calculate_population(
            year-1, economy["young"],
            economy["adults"], economy["old"], population_history)

        economy = year_tick(economy, population_history, STARTING_AMOUNT_OF_COIN)
        print("{:<10}{:<10}{:<10}{:<10}{:<10.2f}{:<10.2f}{:<10.2f}{:<10}{:<10}{:<10}{:<10}".format(
            economy["year"], economy["young"], economy["adults"], economy["old"],
            economy["salary"], economy["dependent"], economy["coin_value"],
            population_history[year]["born"], population_history[year]["adulthood"],
            population_history[year]["senior"], population_history[year]["died"]
        ))
