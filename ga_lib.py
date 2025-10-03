## Componenets of genetic algorithm 
# 1 - spawning population 
# 2 - crossover operator
# 3 - mutation operator
# 4 - fitness evaluator 
import random
import numpy as np


class ga:
    def __init__(self,n_evo,n_spawn , n_comp , search_space , n_parents = 2 , n_kids = 3 , n_families = 2):
        self.n_spawn = n_spawn
        self.n_evo = n_evo
        self.evo_status = 0
        self.n_comp = n_comp
        self.search_space = search_space
        self.n_parents = n_parents
        self.n_kids = n_kids
        self.n_param = len(search_space)
        self.kids = []
        self.fitness_score = []
        self.avg_fitness = []
        # self.fitness_val = []
        self.n_families = n_families
        self.best_param = []
        self.fitness_best_param = []
        self.net_population_storage = []
        return
    
    # def world(self):
    #     return

    def spawn(self):
        if(self.evo_status == 0):
            self.population = []
            for i in range(self.n_spawn):
                param_lst = []
                for param in range(self.n_param):
                    param_lst.append(random.choice(self.search_space[param]))
                self.population.append(param_lst)
            self.evo_status = 1
            print("initial spawn done sucessfully")
            self.net_population_storage += self.population

        else:
            self.population = self.population[:self.n_spawn]
            self.fitness_score = self.fitness_score[:self.n_spawn]
            self.cum_prob = np.array(self.cum_prob)
            self.cum_prob = self.cum_prob[:self.n_spawn]/max(self.cum_prob[:self.n_spawn])
            self.cum_prob = (self.cum_prob).tolist()
            print("best individuals spawned sucessfully")

        return
    
    def combination_selector(self): #biased roullete selection
        self.id = []
        randn_val = np.random.uniform(size = (self.n_parents)) 
        cum_prob = np.array(self.cum_prob)
        # print(f"random values ; {randn_val}")
        for i in range(self.n_parents):
            # print(f"selected id : {np.where(cum_prob > randn_val[i])}")
            self.id.append(np.where(cum_prob > randn_val[i])[0][0])
        return
    
    def fitness_sorter(self):
        pop_char_fit_score = zip(self.fitness_score , self.population)
        sort = sorted(pop_char_fit_score , reverse = True)
        self.population = [item for _,item in sort]
        self.fitness_score = np.array([item for item,_ in sort])
        self.best_param.append(self.population[0])
        self.fitness_best_param.append(self.fitness_score[0])
        self.prob = self.fitness_score - min(self.fitness_score)
        print(f"best_param : {self.population[0]}")
        print(f"best_param : {self.fitness_score[0]}")
        self.prob = self.prob/(sum(self.prob)+1e-10)
        self.prob = list(self.prob)
        cum_prob = 0
        self.cum_prob = []
        for i in self.prob: #biased roulette
            cum_prob += i
            self.cum_prob.append(cum_prob)
        # self.cum_prob[0] = 0
        self.cum_prob[-1] = 1  
        self.fitness_score = self.fitness_score.tolist()
        return
    
    def cross_over(self):
        pop_breed = []
        for id in self.id:
            pop_breed.append(np.array(self.population[id]))
        pop_breed = np.array(pop_breed)
        for i in range(self.n_kids):
            cross = np.random.normal(size = (self.n_parents , self.n_param))
            row_indices = np.argmax(cross, axis=0)
            col_indices = np.arange(cross.shape[1])
            offspring = pop_breed[row_indices, col_indices]
            self.kids.append(offspring.tolist())
            # self.population.append(list(offspring))a

        # self.population.append(self.kids)
        return
    
    def mutate(self,sa_temp):
        pop_before_mutation = np.array(self.population)
        prob = np.random.uniform(size = pop_before_mutation.shape)
        zombie_list = []
        for num in range(len(self.population)):
            temp_lst = []
            for i in range(self.n_param):
                temp_lst.append(random.choice(self.search_space[i]))
            zombie_list.append(temp_lst)

        zombie_array = np.array(zombie_list)
        pop_before_mutation[prob < sa_temp] = zombie_array[prob < sa_temp]
        pop_after_mutation = pop_before_mutation.tolist()  #population after mutation
        self.kids += pop_after_mutation
        # self.population += pop_after_mutation
        return
    
    def pipeline_2(self,sa_temp):
        self.kids = []
        while (len(self.kids) == 0):
            self.combination_selector()
            self.cross_over()
            self.mutate(sa_temp)
            self.kids = self.unique_identifier(self.kids,self.net_population_storage)
        self.net_population_storage += self.kids
        # self.population += next_gen
        # self.fitness_sorter()
        # self.spawn()

    def unique_identifier(self,population,reserve_population):
        temp_pop_st = reserve_population
        op_pop = []
        for i in population:
            if(i not in temp_pop_st):
                temp_pop_st.append(i)
                op_pop.append(i)
        return op_pop


    


    def pipeline(self,fitness_score,sa_temp):
        # self.spawn() - to spawn induviduals
        # self.fitness_score = np.sum(self.population , axis=1) - evaluation fitness 
        #To be done externally (above 2)
        # self.fitness_val.append(np.max(fitness_score))
        self.fitness_sorter()
        for i in range(self.n_families):
            self.combination_selector()
        self.cross_over()
        self.mutate(sa_temp) #max(0.1,1-i/sa_temp)

        return
        # the last 2 steps are to be done seperately
        # self.fitness_score = np.sum(self.population , axis=1)
        # self.fitness_sorter() 

# genetic algo sucessfull implementation (reference)    
# for i in range(n_generations):
#     GA_init.spawn()
#     GA_init.fitness_score = np.sum(GA_init.population , axis=1)
#     fitness_val.append(np.mean(GA_init.fitness_score))
#     GA_init.fitness_sorter()
#     for i in range(10):
#         GA_init.combination_selector()
#     GA_init.cross_over()
#     GA_init.mutate(max(0.1,1-i/n_generations))
#     GA_init.fitness_score = np.sum(GA_init.population , axis=1)
#     GA_init.fitness_sorter()