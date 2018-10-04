from random import choice

class DNA():
    def __init__(self, lngth):
        self.lngth = lngth
        self.genes = [random(0,1) for x in range(lngth)]
        self.fitness = 0.0
        
    def set_genes(self, newgenes):
        self.genes = newgenes
        
    def getPhrase(self):
        return "".join(self.genes)
        
    def crossover(self, partner):
        child = DNA(self.lngth)
        midpoint = int(random(len(self.genes)))
        
        for i in range(len(self.genes)):
            if i > midpoint:
                child.genes[i] = self.genes[i]
            else:
                child.genes[i] = partner.genes[i]
        return child
    
    def mutate(self, mutationRate):
        for i in range(len(self.genes)):
            if random(1) < mutationRate:
                self.genes[i] = random(1)

    
class Organism():
    def __init__(self, dna_):
        self.dna = dna_
        self.fitness = 1

    def getFitness(self):
        return self.fitness
    
    def getDNA(self):
        return self.dna    

class Ball(Organism):
    def __init__(self, dna_):
        Organism.__init__(self, dna_)
        self.pos = PVector(
                           random(width), 
                           random(height)
                           )
        self.acc = PVector(
                           map(self.dna.genes[5], 0,1, -1,1), 
                           map(self.dna.genes[6], 0, 1, -1, 1)
                           )
        self.vel = PVector(0,0)
        
        self.r1 = 100
        self.r2 = 100
        
        self.body_color = (
                           map(self.dna.genes[0], 0, 1, 0, 255), 
                           map(self.dna.genes[1], 0, 1, 0, 255),  
                           map(self.dna.genes[2], 0, 1, 0, 255)
                           )
        
        
    def update(self):        
        self.vel += self.acc
        self.pos += self.vel
        self.acc.mult(0)
        
    def display(self):
        theta = self.vel.heading2D()
        with pushMatrix():
            translate(self.pos.x, self.pos.y)
            rotate(theta)
            #body
            fill(
                 self.body_color[0],
                 self.body_color[1],
                 self.body_color[2],
                 50
                )
            #noStroke()
            stroke(0)
            strokeWeight(3)
            ellipse(
                    0,
                    0, 
                    self.r1, 
                    self.r2)
      
        textSize(16)
        fill(0)
        text(floor(self.getFitness()), self.pos.x,self.pos.y+self.r2)
        
    def warp(self):
        if self.pos.x > width + self.r1:
            self.pos.x = 0
        elif self.pos.x < 0 - self.r1:
            self.pos.x = width
        if self.pos.y > height + self.r2:
            self.pos.y = 0
        elif self.pos.y < 0 - self.r2:
            self.pos.y = height
            
    def apply_force(self,f):
        self.acc += f
        
    def apply_behaviors(self, vehicles):
        pass

    def ellipse_contains(self,a,b):
        if(
            (a > self.pos.x-self.r1) and 
            (a < self.pos.x+self.r1) and  
            (b < self.pos.y+self.r2) and 
            (b > self.pos.y-self.r2)
         ):
            return True
        else:
            return False  

class Population():
    def __init__(self, mutationRate, popmax, dna_length):
        self.mutationRate = mutationRate
        self.matingPool = []
        self.generations = 0
        self.popmax = popmax
        self.population = [ Ball( DNA(dna_length)) for x in range(self.popmax) ]   
             
    def step(self):
        for p in self.population:
            p.display()
            p.apply_behaviors(self.population)
            p.update()

    def selection(self):
        self.matingPool = []
        maxFitness = self.getMaxFitness()
        for i in range(len(self.population)):
            fitnessNormal = map(self.population[i].getFitness(), 0, maxFitness, 0, 1)
            n = int(fitnessNormal * 100)
            for j in range(n):
                self.matingPool.append(self.population[i])
    
    def reproduction(self):
        for i in range(len(self.population)):
            mom = choice(self.matingPool)
            dad = choice(self.matingPool)
            momgenes = mom.getDNA()
            dadgenes = dad.getDNA()
            child = momgenes.crossover(dadgenes)
            child.mutate(self.mutationRate)
            self.population[i] = Ball(child)
        self.generations += 1
        
    def getGenerations(self):
        return self.generations

    def getMaxFitness(self):
        record = 0
        for i in range(len(self.population)):
            if self.population[i].getFitness() > record:
                record = self.population[i].getFitness()
        return record
                        
class BallPopulation(Population):
    def __init__(self, mutationRate, popmax, dna_length):
        Population.__init__(self, mutationRate, popmax, dna_length)
        
    def step(self, raise_fitness=False):
        Population.step(self)
        for p in self.population:
            p.warp()

            if raise_fitness:
                if p.ellipse_contains(mouseX, mouseY):
                    p.fitness += 0.1