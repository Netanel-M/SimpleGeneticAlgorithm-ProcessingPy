from genetic import DNA, Ball, BallPopulation

def setup():
    global population
    size(900,900)
    popmax = 10
    mutationRate = 0.02
    population = BallPopulation(mutationRate, popmax, 30)
    
def draw():
    background(127)
    if mousePressed and mouseButton == LEFT:
        population.step(raise_fitness=True)
    else:
        population.step()
    text("Generation: "+str(population.generations), 0,height-10)

       
def mousePressed():
    if mouseButton == RIGHT:
        background(127)
        population.selection()
        population.reproduction()
        