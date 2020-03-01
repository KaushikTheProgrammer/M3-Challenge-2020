import math
from matplotlib import pyplot as plt

eTruckOrders = 140

# Age: Population Count
eTrucks =	{
    0: eTruckOrders,
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0,
    10: 0,
    11: 0,
    12: 0,
    13: 0,
    14: 0,
    15: 0,
    16: 0,
    17: 0,
    18: 0,
    19: 0,
    20: 0
}
totalTrucks = 3680000
dTrucks =	{
    0: totalTrucks / 16,
    1: totalTrucks / 16,
    2: totalTrucks / 16,
    3: totalTrucks / 16,
    4: totalTrucks / 16,
    5: totalTrucks / 16,
    6: totalTrucks / 16,
    7: totalTrucks / 16,
    8: totalTrucks / 16,
    9: totalTrucks / 16,
    10: totalTrucks / 16,
    11: totalTrucks / 16,
    12: totalTrucks / 16,
    13: totalTrucks / 16,
    14: totalTrucks / 16,
    15: totalTrucks / 16
}

dCost = 24167 # $/year = (truckLifetimeRange/trucklifetime)*(($/g)/(mpg)) = (750000/15)*(2.9/6)
eCost = 11000 # $/year = (eRange/eLifetime) * ($/mi) = (750000/20) * (0.22)

dMaintenance = 20000 # $/year
eMaintenance = 10000 # $/year

eLifeSpan = 20
dLifeSpan = 15

# Initializing arrays to track truck population through years with year 0 values
dTrucksByYear = [totalTrucks]
eTrucksByYear = [eTruckOrders]

# Model increasing truck budget each year
def truckBudgetAdjuster(total_eTrucks, truckBudget, eTruckMaintenence, dTruckMaintenence):
    print("maintenence delta: ", dTruckMaintenence - eTruckMaintenence)
    print("added electric budget: ", total_eTrucks * (dTruckMaintenence - eTruckMaintenence))
    return truckBudget + (total_eTrucks * (dTruckMaintenence - eTruckMaintenence))

# Model decrease of electric truck prices
def eTruckPrice(time):
    return -102725500 + ((69012.05 + 102826500)/(1 + math.pow((time/1825022000000), 0.3197167)))

# Model decrease of diesel truck prices
def dTruckPrice(time):
    return (103.4393 - (-18.31066 / 1.100271) * (1 - math.exp(-1.100271*(time + 1)))) * 1000

def eTruckPriceAnnual(time):
        return (eTruckPrice(time) / eLifeSpan) + eCost + eMaintenance

def dTruckPriceAnnual(time):
    return (dTruckPrice(time) / dLifeSpan) + dCost + dMaintenance

def demandNewTrucks(time):
    return int(((6.1789 - (2.425216 * math.exp(-0.01918301 * time))) - 3.753684) * 100000)

def eTruckSupply(time):
    return int(300000 + ((2627.477 - 300000) / (1 + math.pow((time / 1.261193), 5.087))))

def updateTruckPopulation(numBought, trucks):
    trucksNew = {}

    trucksNew[0] = numBought
    for counter in range(len(trucks) - 1):
        trucksNew.update({counter + 1: trucks[counter]})
    return trucksNew

def truckSum(trucks):
    total = 0
    for item in trucks:
        total += trucks[item]
    
    return int(total)


truckBudget = (3.79 - 3.68) * 1000000 * dTruckPrice(0) # Spending on new trucks in 2020
yearTracker = [0]
eTruckPriceTracker = [eTruckPrice(0)]
dTruckPriceTracker = [dTruckPrice(0)]
newDemandTracker = [demandNewTrucks(0)]
budgetTracker = [truckBudget]
eTruckSupplyTracker = [eTruckSupply(0)]
maintenenceDelta = (dCost + dMaintenance) - (eCost + eMaintenance)
addedElectricBudgetTracker = [sum(eTrucks.values()) * maintenenceDelta]

for year in range(1, 21):
    eTruckPriceCurr = eTruckPriceAnnual(year)
    dTruckPriceCurr = dTruckPriceAnnual(year)
    yearTracker.append(year)
    
    print(year)
    print("eTruckPrice(year): ", eTruckPrice(year))
    print("dTruckPrice(year): ", dTruckPrice(year))

    electricIsCheaper = False
    
    if(eTruckPriceCurr < dTruckPriceCurr):
        electricIsCheaper = True

    neededTrucks = dTrucks[dLifeSpan] + eTrucks[eLifeSpan] + demandNewTrucks(year)
    print("neededTrucks: ", neededTrucks)
    print("truckBudget: ", truckBudget)

    if eTruckPrice(year) >= dTruckPrice(year):
        eTrucksDesired = (truckBudget) - (dTruckPrice(year) * neededTrucks) / (eTruckPrice(year) - dTruckPrice(year))
        if eTrucksDesired > neededTrucks:
            eTrucksDesired = neededTrucks
    else:
        eTrucksDesired = neededTrucks
     
    dTrucksDesired = neededTrucks - eTrucksDesired
    
    eTrucksPurchased = eTrucksDesired
    dTrucksPurchased = dTrucksDesired

    print("eTruckSupply: ", eTruckSupply(year))

    if eTrucksDesired > eTruckSupply(year):
        eTrucksPurchased = eTruckSupply(year)
        dTrucksPurchased = neededTrucks - eTrucksPurchased

    print("eTrucksPurchased: ", eTrucksPurchased)
    print("dTrucksPurchased: ", dTrucksPurchased)
    eTrucks = updateTruckPopulation(eTrucksPurchased, eTrucks)
    dTrucks = updateTruckPopulation(dTrucksPurchased, dTrucks)
    truckBudget = truckBudgetAdjuster(sum(eTrucks.values()), truckBudget, eCost + eMaintenance, dCost + dMaintenance)
    
    eTrucksByYear.append(sum(eTrucks.values()))
    dTrucksByYear.append(sum(dTrucks.values()))
    print('\n')

print(eTrucksByYear)
print(dTrucksByYear)

plt.plot(dTrucksByYear)
plt.plot(eTrucksByYear)
plt.show()
