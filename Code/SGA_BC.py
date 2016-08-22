# -*- coding: cp1252 -*-
"""
SGA_BC.py
Simple Genetic Algorithm for the Brachistochrone Curve problem .
Pedro Geadas, May, 2011.
"""

from operator import itemgetter

import matplotlib as mplib
from pylab import *
import random
import pylab
from string import *
from BrachFitness import *
import time
import pickle
import csv


def sga(numb_genera, size_pop, num_pontos,  alphabet, size_tournament, prob_crossover, n_crossover, prob_mutation, size_elite, selection_mode, spacement,mut_type,times):

  
    total = 0.0
    file = open('population_alldata.txt','w')
    file2 = open ('population_avg.txt','w')
    count_mutation = 0
    count_crossover = 0
    i = 0
    avg_pop = 0.0
    pop_times = 0.0
    the_less_fitest = 0.0
    the_fitest = 99999999.0
    the_best = 0.0
    the_worst = 0.0
    af = []
    dp = []
    total_mut = total_cross = 0
    resultWriter = csv.writer(open('results.csv', 'wb'), delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
     # create initial population
    population = create_population(size_pop, alphabet, num_pontos,spacement)

    desvio = 0.0

    #print 'POPULACAO ' + `len(population)`

    for vezes in range(times):
        # evaluate population
        population =[[indiv[0], calcBrachTime(indiv[0], False)] for indiv in population ]
        best_generation = [population[0][1]]
        count_mutation = count_crossover = 0
      
        for generation in range(numb_genera):
            # Select parents
            if(selection_mode == 1):
                parents = [tournament_selection(population, size_tournament) for i in range(size_pop)]
            else:
                total= 0
                for indiv in population: #calcula as probabilidades totais (calcula fora da propria funcao, para evitar calculos desnecessarios)
                    total += indiv[1]
                parents = [roulette_selection(population, size_tournament, total) for i in range(size_pop)]
           
            # Produce offspring
            # a) crossover
            offspring = []
            for i in range(0, size_pop, 2): # population must have an even size...
                if random.random() < prob_crossover:
                    offspring.extend(n_point_crossover(parents[i], parents[i + 1],n_crossover, spacement))
                    count_crossover += 2
                    total_cross +=2
                else:
                    offspring.extend([parents[i], parents[i + 1]])
                #print 'off - >  ' + `offspring`
            # b) mutation
            
        
            for j in range(size_pop):
                if random.random() < prob_mutation:
                    if(spacement==1):
                        if(mut_type==2):

                            offspring[j] = mutation_gaussian(offspring[j][0], alphabet) #mutacao gaussiana, apenas em y
                        else:
                            offspring[j] = mutation(offspring[j][0], alphabet) #mutacao normal, apenas em y
                    else:
                        if(mut_type==2):

                            offspring[j] = mutation_gaussian_xy(offspring[j][0], alphabet) #mutacao gaussiana, no caso de partiçoes aleatorias em x e y
                        else:

                            offspring[j] = mutation(offspring[j][0], alphabet) #mutacao normal, em x e y
                    count_mutation += 1
                    total_mut += 1
            # Evaluate offspring
           # print 'off '+`offspring`
            #print len(offspring)

            offspring = [[indiv[0], calcBrachTime(indiv[0], False)] for indiv in offspring]
            #print 'off '+`offspring`
            offspring.sort(key=itemgetter(1))
            # Select Survivors
            population = elitism_selection(population, offspring, size_elite)
            # show best
            population.sort(key=itemgetter(1))
            #print "Generation: %d\tindividual: %s\tfitness: %f" % (generation, population[0][0], population[0][1])
            best_generation.append(population[0][1])


        pop_times = 0.0
        for indiv in population: #calcula a media de 1 populacao
            if(indiv[1]> the_less_fitest):
                the_less_fitest = indiv[1]
            if(indiv[1]< the_fitest):
                the_fitest = indiv[1]
            pop_times+=indiv[1]


        
        avg_pop += pop_times/float(len(population)) #(xBarra)

        s = 0.0
        sBarra = pop_times/float(len(population))

        for indiv in population: #calcula o desvio padrao
            s+=pow((indiv[1] - sBarra),2)
            #print s
        
        s=sqrt(s*(1/float((len(population)-1)))) #desvio padrao

        desvio += s
        #interessa guardar os valores do best fitness e avg fitness(e tambem posso guardar do pior) separado por virgulas e guardar num ficheiro cvs
        dp.extend([s])
        print s
        print desvio
        print desvio/times
        
        print "AVG POP %d, is %f!" %(vezes, pop_times/len(population)) #media da populacao i
        af.extend([pop_times/len(population)])
        pickle.dump("AVG POP %d, is %f!" %(vezes, pop_times/len(population)), file)
        print "DESVIO PADRAO: %f!" %(s)
        pickle.dump("DESVIO PADRAO: %f!" %(s), file)
        print "Crossovers: %d"%(count_crossover)
        pickle.dump("Crossovers: %d"%(count_crossover), file)
        print "Mutations: %d"%(count_mutation)
        pickle.dump("Mutations: %d"%(count_mutation), file)
        print "Crossovers:%d\tMutations:%d" % (total_cross, total_mut)
        pickle.dump("Crossovers:%d\tMutations:%d" % (total_cross, total_mut), file)
        #print "BEST GEN " + `best_generation`
        print "the_best_fitness "+`population[0][1]`
        pickle.dump("the_best_fitness "+`population[0][1]`, file)
        print "the_worst_fitness "+`population[-1][1]`
        pickle.dump("the_worst_fitness "+`population[-1][1]`, file)
        print "THE FITEST %f" %(the_fitest)
        pickle.dump("THE FITEST %f" %(the_fitest), file)
        print "THE LESS FITEST %f\n" %(the_less_fitest)
        pickle.dump("THE LESS FITEST %f\n" %(the_less_fitest), file)
        the_best +=population[0][1]
        the_worst += population[-1][1]
        print vezes
        print desvio/times


    print "desvio padrão médio: %f "  %(desvio/float(times))
    pickle.dump("desvio padrão médio: %f "  %(desvio/float(times)), file2)
    print "aptidao media do melhor %d vezes: %f " %(times,the_best/times)
    pickle.dump("aptidao media do melhor %d vezes: %f " %(times,the_best/times), file2)
    print "aptidao media do worst %d vezes: %f " %(times,the_worst/times)
    pickle.dump("aptidao media do worst %d vezes: %f " %(times,the_worst/times), file2)
    print "AVG TOTAL POPULATION: %f " %(avg_pop/times) #media de todas as populacoes
    pickle.dump("AVG TOTAL POPULATION: %f " %(avg_pop/times), file2)
    print "THE FITEST %f" %(the_fitest)
    pickle.dump("THE FITEST %f" %(the_fitest), file2)
    print "THE LEAST FIT %f" %(the_less_fitest)
    pickle.dump("THE LEAST FIT %f" %(the_less_fitest), file2)

    af.sort()
    af.reverse()
    resultWriter.writerow(af)
    resultWriter.writerow(dp)
    return [best_generation,population[0][0],population]


def create_indiv_random_spacement(alphabet, num_pontos):
    #cria 1 individuo, que consiste num conjunto de [num_pontos] pontos
    indiv = []
    maxHeight = alphabet[1]
    x_max = alphabet[2]
    x_0 = alphabet[0]
    xx = []
    yy = []

    indiv.extend([x_0,maxHeight]) # adiciona o ponto inicial a lista

    while(len(xx) != (num_pontos)-2): # enquanto n existirem n_pontos no array ( o -2 e pq ja la ta o inicial, e vai ter ainda o final )

        new_x = uniform(x_0, x_max) #gera um x entre o x actual e o x maximo
        while(new_x <= x_0 or new_x >=x_max):# se e menor q o x anterior ou maior q o maximo
            new_x = uniform(x_0, x_max) #gera um x entre o x actual e o x maximo

        if new_x not in xx:
            xx.extend([new_x])

    while(len(yy) != (num_pontos)-2): # enquanto n existirem n_pontos no array ( o -2 e pq ja la ta o inicial, e vai ter ainda o final )

        new_y = uniform(0, alphabet[1]+alphabet[3]) - alphabet[3] #gera o segundo ponto (possibilidade de gerar numeros negativos tambem)
        while(new_y >= maxHeight ):# se e maior q a altura maxima
            new_y = uniform(0, alphabet[1]+alphabet[3]) - alphabet[3] #gera o segundo ponto (possibilidade de gerar numeros negativos tambem)

        if new_y not in yy:
            yy.extend([new_y])


    xx.sort()
    for i in range(len(xx)):
         point = [xx[i],yy[i]]
         indiv.extend(point)
        
    point = [alphabet[2],alphabet[3]]
    indiv.extend(point)
    #print 'o indiv e E ' + `indiv`
   
    return [indiv, 0]


def create_indiv_same_spacement(alphabet, num_pontos):
    #cria 1 individuo, que consiste num conjunto de [num_pontos] pontos
    indiv = []
    maxHeight = alphabet[1]
    offset=0.0

    indiv.extend([alphabet[0],alphabet[1]]) # adiciona o ponto inicial a lista

    offset = (alphabet[2]-alphabet[0])/num_pontos #calcula o espaço entre os x's
    i = offset + alphabet[0]

    while(len(indiv) != (num_pontos *2)-2): # enquanto n existirem n_pontos no array ( o -2 e pq ja la ta o inicial, e vai ter ainda o final )
        point = [i, uniform(0, alphabet[1]+alphabet[3]) - alphabet[3]] #gera o segundo ponto (possibilidade de gerar numeros negativos tambem)

        while(point[1] >= maxHeight ):# se e maior q a altura maxima
            point = [i, uniform(0, alphabet[1]+alphabet[3]) - alphabet[3]] #gera o segundo ponto

        indiv.extend(point)
        #print 'dentro: indiv e E ' + `indiv`
        i = i+offset

    point = [alphabet[2],alphabet[3]] # adiciona o ponto final
    indiv.extend(point)
    #print 'o indiv e E ' + `indiv`
    return [indiv, 0]

def create_population(size_pop, alphabet, num_pontos,spacement):
    #cria uma populacao de [size_pop] individuos
    if(spacement==1):
        pop = [ create_indiv_same_spacement(alphabet, num_pontos) for i in range(size_pop) ]
    else:
        pop = [ create_indiv_random_spacement(alphabet, num_pontos) for i in range(size_pop) ]
    print 'a pop e' + `pop`
    return pop



# Basic mechanisms and operators
def tournament_selection(population, size_tournament):
    # escolhe um elemento aleatorio da populacao
    tournament = random.sample(population, size_tournament)
    # e do escolhido escolhe o q tem melhor fitness
    tournament.sort(key=itemgetter(1)) # minimization
    #print "O TOURNAMENT 0 = " + `tournament[0]`
    return tournament[0]

# Basic mechanisms and operators
def roulette_selection(population, size_tournament, total):
    # calcula o fitness total da populacao
    new_total = 0
    probab = []
    roulette = []
    tam = len(population)
    #print "populacao " + `population`
    
    probab.extend([0.0])
    for i in range(tam):#como os melhores sao os q teem menos fitness, temos q calcular o novo total
        inverte = (total-population[i][1])/total #igual a fazer 1 - (fi/ft)
        probab.extend([probab[i]+ inverte]) #somo os valores da probabilidade invertida
        new_total += inverte    #calculo o novo total para multiplicar pelo random, para ter valores nesta nova gama

    probab[-1]=new_total # o valor maximo vai ser igual ao do novo_total
    probab.remove(0.0) #remove o 0, que so serviu para a primeira iteraçao do ultimo for

   # for j in range(size_tournament): #gera o numero aleatorio que vai escolher o individuo, [size_tournament] vezes
    x = random.random() * new_total #para dar valores correctos
        #print x
    for i in range(tam): # procura o elemento correspondente
        if( x < probab[i]): # se o valor gerado for menor do que o valor[i] da lista, entao é esse o elemento correspondente
            roulette.extend([population[i]])
            break

   # roulette.sort(key=itemgetter(1)) # minimization
    #print 'roleta  ' + `roulette`
    return roulette[0]


def elitism_selection(parents, offspring, size_elite):
    #seleciona uma percentagem dos melhores individuos
    size = int(len(parents) * size_elite)
    new_pop = parents[:size] + offspring[:len(parents) - size]
    new_pop.sort(key=itemgetter(1))
    return new_pop


def mutation(indiv, alphabet):
    #print 'INDIV........ '+ `indiv`
    #escolhe o y a mutar
    index = random.choice(range(4,len(indiv)-2)) # devolve um num da sequencia (4 a len -2 pa nao apanhar o ponto inicial nem o final )
    #print 'index = ' + `index`
    # se for par, temos q meter impar para q seja um y (4-1=3, que e o primeiro indice valido de y)
    if(index % 2 == 0):
        index = index - 1
       # print 'index '+`index`

    new_gene = uniform(0, alphabet[1]+alphabet[3]) - alphabet[3]# gera o novo numero
    while(new_gene > indiv[1]):
       #gera um novo y, menor que a altura maxima
        new_gene = uniform(0, alphabet[1]+alphabet[3]) - alphabet[3]

    indiv[index] = new_gene

    #print 'new indiv '+ `indiv`
    return [indiv, 3]

#nao foi criado a funcao mutation_xy pq para dar certo tinha q gerar um x entre o anterior e o proximo, e isso e quase o mesmo que fazer a gaussian

def mutation_gaussian(indiv, alphabet):
    #print 'INDIV........ '+ `indiv`
    #escolhe o y a mutar
    index = random.choice(range(4,len(indiv)-2)) # devolve um num da sequencia (4 a len -2 pa nao apanhar o ponto inicial nem o final )
    #print 'index = ' + `index`
    # se for par, temos q meter impar para q seja um y (4-1=3, que e o primeiro indice valido de y)
    if(index % 2 == 0):
        index = index - 1
       # print 'index '+`index`
   # print "indiv i "+`indiv[index]`
    new_gene = random.gauss(0,1)
    new_gene+=indiv[index]
    while(new_gene > indiv[1]):
       #gera um novo y, menor que a altura maxima
        new_gene = random.gauss(0,1) + indiv[index]

   # print "new_gene "+ `new_gene`
    indiv[index] = new_gene

    #print 'new indiv '+ `indiv`
    return [indiv, 3]


def mutation_gaussian_xy(indiv, alphabet):
    #print 'INDIV........ '+ `indiv`
    #escolhe o y a mutar
    index = random.choice(range(4,len(indiv)-2)) #nao escolhe nem o 1 nem o ultimo

    if(index%2==0):
        new_gene= random.gauss(0,1) + indiv[index]
        while(new_gene > indiv[index+2] or new_gene < indiv[index-2]):
            #gera um novo y, menor que a altura maxima
            #print "new_gene preso x "+ `new_gene`
            new_gene = random.gauss(0,1) + indiv[index]

    else:
        new_gene= random.gauss(0,1) + indiv[index]
        while(new_gene > indiv[1]):
            #gera um novo y, menor que a altura maxima
           # print "new_gene preso  y"+ `new_gene`
            new_gene = random.gauss(0,1) + indiv[index]
  
   # print 'indiv '+ `indiv[index]`
    

    #print "new_gene "+ `new_gene`
    indiv[index] = new_gene

    #print 'new indiv '+ `indiv`
    return [indiv, 3]



def n_point_crossover(parent_1, parent_2, n_crossover,spacement):
    if(n_crossover>0):
        if(spacement==1): #caso em que o espaçamento e igual, e ja tao ordenados
            return crossover_same_spacement(parent_1,parent_2,n_crossover) #o 1 e o 2 no fitness foi apenas para debug, e indiferente pq vai ser alterado mais tarde
        else:
            return crossover_random_spacement(parent_1,parent_2,n_crossover)
    else:
        return [[parent_1,0], [parent_2,0]]


def crossover_same_spacement(parent_1,parent_2,n_crossover):
    offspring_1 = []
    offspring_2 = []
    cross_point = []

    ptr = [parent_1[0], parent_2[0]]
    bool = True

    while( len(cross_point) != n_crossover):#gera os cross_points aleatorios, diferentes do ponto inicial e final, e q nao seja repetido
        x = random.choice(range(len(parent_1[0])/2 - 1) )
        if(x not in cross_point and x!=0 and x != (len(parent_1[0])/2 - 1) and x!= 1 ):
            cross_point.extend([ x ])

    cross_point.extend([0,len(parent_1[0])/2]) # mete o 0 e o ultimo tambem no array
    cross_point.sort()
    #print 'CROSS_POINTS ' + `cross_point`

    pai = 0
    i = 0
    #coloca a parte inicial nos offsprings
    offspring_1.extend( ptr[pai][cross_point[i]*2:cross_point[(i+1)]*2] )
    pai = (pai + 1 )%2
    offspring_2.extend(ptr[pai][cross_point[i]*2:cross_point[(i+1)]*2])
    i = i + 1


    while( bool == True): #faz o crossover
        #print 'Pai 0 ' + `parent_1`
       # print 'Pai 1 ' + `parent_2`
        if(i >= len(cross_point) -1 ):#chegou ao ultimo cross_point
            bool = False
        else:
            #print 'iteracao ---------------------------- ' + `i`
            offspring_1.extend( ptr[pai][cross_point[i]*2:cross_point[(i+1)]*2] )
           # print 'OFFSPRIN 1: i= ' + `i`+ ' ' +`offspring_1`
            pai = (pai + 1 )%2
            offspring_2.extend(ptr[pai][cross_point[i]*2:cross_point[(i+1)]*2])
           # print 'OFFSPRIN 2: i= ' + `i`+ ' ' + `offspring_2`

        i = i + 1


        return [[offspring_1,1], [offspring_2,2]]


def crossover_random_spacement(parent_1,parent_2,n_crossover):
    offspring_1 = []
    offspring_2 = []
    cross_point = []

    ptr = [parent_1[0], parent_2[0]]
    bool = True

    while( len(cross_point) != n_crossover):#gera os cross_points aleatorios, diferentes do ponto inicial e final, e q nao seja repetido
        x = random.choice(range(len(parent_1[0])/2 - 1) )
        if(x not in cross_point and x!=0 and x != (len(parent_1[0])/2 - 1) and x!= 1 ):
            cross_point.extend([ x ])

    cross_point.extend([0,len(parent_1[0])/2]) # mete o 0 e o ultimo tambem no array
    cross_point.sort()
    #print 'CROSS_POINTS ' + `cross_point`

    pai = 0
    i = 0
    #coloca a parte inicial nos offsprings
    offspring_1.extend( ptr[pai][cross_point[i]*2:cross_point[(i+1)]*2] )
    pai = (pai + 1 )%2
    offspring_2.extend(ptr[pai][cross_point[i]*2:cross_point[(i+1)]*2])
    i = i + 1



    while( bool == True): #faz o crossover
      
        if(i >= len(cross_point) - 1):#chegou ao ultimo cross_point
            bool = False
        else:
          #  print 'i %d'%(i)
            element_aux = ptr[pai][cross_point[i]*2:cross_point[(i+1)]*2] #copia os elementos respectivos para uma lista auxiliar

            while(len(element_aux)!=0): #enquanto houver elementos

                if(offspring_1[-2]<element_aux[0]): #compara o proximo elemento dessa lista auxiliar, com o ultimo que ja esta ordenado em offspring
                    #caso esteja em ordem, adiciona o x e o y
                    offspring_1.insert(len(offspring_1),element_aux.pop(0))
                    offspring_1.insert(len(offspring_1),element_aux.pop(0))
                 
                elif(offspring_1[-2]>=element_aux[0]): #caso em que nao esta ordenado, e se vai ter que procurar a posiçao correcta em x para inserir o ponto
                 
                    for k in range(len(offspring_1)-2,-2,-2):
                        if(element_aux[0]>offspring_1[k]):
                            offspring_1.insert(k+2,element_aux.pop(0))
                            offspring_1.insert(k+1+2,element_aux.pop(0))
                            break
                        elif(element_aux[0]==offspring_1[k]):

                            if(offspring_1[-2]==element_aux[0]):
                                x_actual = offspring_1[-4]
                            else:
                                x_actual = offspring_1[-2]
                            x_max = element_aux[0]
                            new_x = uniform(x_actual,x_max)
                            while(new_x in offspring_1 or new_x in element_aux):
                                 new_x = uniform(x_actual,x_max)
                            element_aux[0]=new_x

                            break
                 
            pai = (pai + 1 )%2 # muda de parent para efectuar a copia, e o processo é repetido
            element_aux = ptr[pai][cross_point[i]*2:cross_point[(i+1)]*2] #copia os elementos respectivos para uma lista auxiliar

            while(len(element_aux)!=0):

                if(offspring_2[-2]<element_aux[0]):
              
                    offspring_2.insert(len(offspring_2),element_aux.pop(0))
                    offspring_2.insert(len(offspring_2),element_aux.pop(0))
                 
                elif(offspring_2[-2]>=element_aux[0]):
                
                    for k in range(len(offspring_2)-2,-2,-2):
                    
                        if(element_aux[0]>offspring_2[k]):
                            offspring_2.insert(k+2,element_aux.pop(0))
                            offspring_2.insert(k+1+2,element_aux.pop(0))
                            break
                        elif(element_aux[0]==offspring_2[k]):
                   
                            if(offspring_2[-2]==element_aux[0]):
                                x_actual = offspring_2[-4]
                            else:
                                x_actual = offspring_2[-2]
                            
                            x_max = element_aux[0]
                            
                            new_x = uniform(x_actual,x_max)
                            while(new_x in offspring_2 or new_x in element_aux):
                                 new_x = uniform(x_actual,x_max)
                            element_aux[0]=new_x
                            break
               
        i = i+1

    return [[offspring_1,1], [offspring_2,2]] #o 1 e o 2 no fitness foi apenas para debug, e indiferente pq vai ser alterado mais tarde

