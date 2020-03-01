import math
from matplotlib import pyplot as plt

eTruckOrders = 140

# Age: Population Count
eTrucks = {
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
dTrucks = {
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
    return ((6.1789 - (2.425216 * math.exp(-0.01918301 * time))) - 3.753684) * 100000

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
DemandTracker = [demandNewTrucks(0)]
budgetTracker = [0]
eTruckSupplyTracker = [eTruckSupply(0)]
maintenenceDelta = (dCost + dMaintenance) - (eCost + eMaintenance)
addedElectricBudgetTracker = [0]
eTrucksPurchasedTracker = [0]
dTrucksPurchasedTracker = [0]

for year in range(1, 21):
    print(year)
    print(eTrucks)
    print(dTrucks)
    print("\n")
    yearTracker.append(year)

    eTruckPriceCurr = eTruckPriceAnnual(year)
    dTruckPriceCurr = dTruckPriceAnnual(year)

    eTruckPriceTracker.append(eTruckPrice(year))
    dTruckPriceTracker.append(dTruckPrice(year))
    DemandTracker.append(int(demandNewTrucks(year) + dTrucks[dLifeSpan] + eTrucks[eLifeSpan]))
    newDemandTracker.append(int(demandNewTrucks(year)))
    budgetTracker.append(truckBudget)
    addedElectricBudgetTracker.append(sum(eTrucks.values()) * maintenenceDelta)
    eTruckSupplyTracker.append(int(eTruckSupply(year)))
    
    if eTruckPriceCurr > dTruckPriceCurr:
        eTrucksPurchased = 0
        dTrucksPurchased = demandNewTrucks(year) + dTrucks[dLifeSpan] + eTrucks[eLifeSpan]

    else:
        neededTrucks = dTrucks[dLifeSpan] + eTrucks[eLifeSpan] + demandNewTrucks(year)

        if eTruckPrice(year) >= dTruckPrice(year):
            eTrucksDesired = (truckBudget) - (dTruckPrice(year) * neededTrucks) / (eTruckPrice(year) - dTruckPrice(year))
            if eTrucksDesired > neededTrucks:
                eTrucksDesired = neededTrucks
        else:
            eTrucksDesired = neededTrucks

        dTrucksDesired = neededTrucks - eTrucksDesired

        eTrucksPurchased = eTrucksDesired
        dTrucksPurchased = dTrucksDesired

        if eTrucksDesired > eTruckSupply(year):
            eTrucksPurchased = eTruckSupply(year)
            dTrucksPurchased = neededTrucks - eTrucksPurchased

    eTrucksPurchasedTracker.append(int(eTrucksPurchased))
    dTrucksPurchasedTracker.append(int(dTrucksPurchased))

    eTrucks = updateTruckPopulation(eTrucksPurchased, eTrucks)
    dTrucks = updateTruckPopulation(dTrucksPurchased, dTrucks)
    truckBudget = truckBudgetAdjuster(sum(eTrucks.values()), truckBudget, eCost + eMaintenance, dCost + dMaintenance)
    
    eTrucksByYear.append(int(sum(eTrucks.values())))
    dTrucksByYear.append(int(sum(dTrucks.values())))

print("Total truck populations by year")
print("\n")
print(eTrucksByYear)
print(dTrucksByYear)
plt.plot(dTrucksByYear)
plt.plot(eTrucksByYear)
plt.show()

print("Truck prices by year")
print(dTruckPriceTracker)
print(eTruckPriceTracker)
print("\n")
plt.plot(dTruckPriceTracker)
plt.plot(eTruckPriceTracker)
plt.show()

print("New demand by year")
print(newDemandTracker)
print("\n")
plt.plot(newDemandTracker)
plt.show()

print("Total demand by year")
print(DemandTracker)
print("\n")
plt.plot(DemandTracker)
plt.show()

print("Budget by year")
print(budgetTracker)
print("\n")
plt.plot(budgetTracker)
plt.show()

print("Added electric budget by year")
print(addedElectricBudgetTracker)
print("\n")
plt.plot(addedElectricBudgetTracker)
plt.show()

print("Electric truck supply by year")
print(eTruckSupplyTracker)
print("\n")
plt.plot(eTruckSupplyTracker)
plt.show()

print("Number of each truck purchased by year")
print(eTrucksPurchasedTracker)
print(dTrucksPurchasedTracker)
print("\n")
plt.plot(eTrucksPurchasedTracker)
plt.plot(dTrucksPurchasedTracker)
plt.show()
