raters = ['Yashika', 'Krish', 'Jaskaran',
          'Jatin', 'Rajdeep', 'Badal', 'Deepak']

raterCombinations = []

index = 0
for rater in raters:
    j = 0
    combi = []
    while j < len(raters):
        if j != index:
            subcombi = []
            subcombi.append(rater)
            subcombi.append(raters[j])
            combi.append(subcombi)

        j += 1
    raterCombinations.append(combi)
    index += 1

totalIterations = 26
start = 0

initialIndex = 0
ratersCombiIndex = 7
output = []
while start <= totalIterations:

    # Base Conditions
    if ratersCombiIndex == len(raters):
        ratersCombiIndex = 0

    if initialIndex == len(raters) - 1:
        initialIndex = 0

    # Operations
    textIndex = raterCombinations[ratersCombiIndex][initialIndex]
    output.append(textIndex[0]+','+textIndex[1])
    print(textIndex[0]+','+textIndex[1])

    initialIndex += 1
    ratersCombiIndex += 1
    start += 1
