class Candidate: 
    
    candidate1toN = []
    
    def __init__(self, Group, Low, High, Wage_Schedule):
        assert (Group in (1,2)), "The candidate is either low-type(Group=1) or high-type(Group=2)"
        self.Group = Group
        self.employer = Employer(Low, High, Wage_Schedule)
        
        #Push up to the class variable(Homogeneous Attribute)
        Candidate.Low = self.employer.Low
        Candidate.High = self.employer.High
        Candidate.Wage_Schedule = self.employer.Wage_Schedule
        
        #candidate is part of the market.
        Candidate.candidate1toN.append(self)
        
    #Simple instance method
    def Signaling_Cost(self, Education):
       assert (Education >= 0), "Education level is >=0"
       Group = self.Group
       Signaling_Cost = Education/Group #negative correlation of costs and productivity.
       return Signaling_Cost
    
    #It has to wait the additional class methods: q1 and Uniform_Payoff
    def Optimal_Education(self):
      
        #class variable
        Low = Candidate.Low
        High = Candidate.High
        Wage_Schedule = Candidate.Wage_Schedule
        Uniform_Payoff = Candidate.Uniform_Payoff
        
        #instance variable
        Group = self.Group
        
        #Self-Evaluation
        Net_Return_of_Signal1 = Low - 0/Group
        Net_Return_of_Signal2 = High - Wage_Schedule/Group
        Net_Return_of_Signal3 = Uniform_Payoff - Wage_Schedule/Group
        
        #Consider the scenarios when the Signal is equal to Wage_Schedule.
        
        #Targeting the Group2(The talent)
        if max(Uniform_Payoff,Net_Return_of_Signal2)==Net_Return_of_Signal2:
            self.Signal = Wage_Schedule
            return Wage_Schedule
        
        #Targeting the Group1(The normal)
        elif max(Net_Return_of_Signal1,Net_Return_of_Signal3)==Net_Return_of_Signal3:
            self.Signal = Wage_Schedule
            return Wage_Schedule
        else:
            self.Signal = 0
            return 0
     
    #The first mind of the candidate is about the Population.
    @classmethod
    def Population(cls, N=500): #N=500 is default
      
        from numpy.random import default_rng
        rng_seed = default_rng()
        
        #Every instance will be appended by the syntax `Candidate.candidate1toN.append(self)`
        #The first element can be considered as our main character. So, we need N-1
        #candidate.__class__.candidate1toN return N Candidate instance
        Other_candidates_Initiation = [
          Candidate(Low=cls.Low,
                    High=cls.High,
                    Wage_Schedule=cls.Wage_Schedule,
                    Group = int(rng_seed.integers(low=1, #inclusive
                                                   high=3, #exclusive
                                                   size=1))) for i in range(N-1)
        ]
        Population = len(Other_candidates_Initiation) + 1
        
        #Push up to the class variable(Homogeneous Attribute).
        cls.Population = Population
        return Population
    
    
    #With the Population, candidate may consider if the market is competitive.
    @classmethod
    def q1(cls):
        
        from numpy import mean
        proportion = mean([cls.candidate1toN[i].Group for i in range(cls.Population)])
        Group1_proportion = 2-proportion
        
        #Push up to the class variable
        cls.q1 = Group1_proportion 
        return Group1_proportion
      
    #With q1, candidate can evaluate the Uniform_Payoff
    @classmethod
    def Uniform_Payoff(cls): 
      
        Low = cls.Low
        High = cls.High
        q1 = cls.q1 
        Uniform_Payoff = Low*q1 + High*(1-q1)
        
        #Push up to the class variable, so the `Optimal_Education` method can be done.
        cls.Uniform_Payoff = Uniform_Payoff
        return Uniform_Payoff

#EOF

class Employer:
    #想要一般化的話，這邊可以多高薪要多高，低薪要多低。也更容易一般化 Google TSMC 等頂尖企業
    def __init__(self, Low, High, Wage_Schedule):
        self.Wage_Schedule=Wage_Schedule
        self.Low = Low
        self.High = High
       
     
    def Possible_Wage(self, Signal):
        Wage_Schedule = self.Wage_Schedule
         #In Spence, one candidate instance provide one signal, this is 1(employer) to N(candidates) game. But the concern comes from the reality that Signal is not a attribute belong to Employer. It's like a important, external information
        # Employer.Signal = Signal
        if(Signal >= Wage_Schedule):
          return self.High
        else:
          return self.Low
    
    def Check_Eqm(self, employer, candidate):
        # 看起來是可行的。但是權限大到基本上就是 Mr.JobMarket，用 Mr.JobMarket 的視角在看 Mr.JobMarket 操作的 Eqm-related methods，還在想要不要這樣。
        #Check_Eqm(self, employer, candidate)，employer 等於是自己。但是若寫
        #Check_Eqm(self, candidate)
        # self.jobmarket_result = JobMarket(employer=self, candidate) 會不對，是凸顯變成Mr.JobMarket事實
        self.jobmarket_result = JobMarket(employer, candidate)
    
    # 還有一個可能性是 Mr.JobMarket 做完 Eqm evaluation 之後，他單純借過來看，沒有 Input Arguments 作為阻擋或者 access friction，但是尚未確定是否做得到。
    #就是 NoAdditionalArguments in method instruction and after JobMarket.xxxmethod e.g.JobMarket.SeparatingEqm(NoAdditionalArguments), return true false and possible paste0 expression about the Group and Signal to mimic the realization after hiring the candidate instance.(But, build the JobMarket.SeparatingEqm... as soon as possible. )
    # def Check_Eqm(self, NoAdditionalArguments):
    #     self.jobmarket_result1 = JobMarket.SeparatingEqm(NoAdditionalArguments)
    #     self.jobmarket_result2 = JobMarket.Pooling1Eqm(NoAdditionalArguments)
    #     self.jobmarket_result3 = JobMarket.Pooling3Eqm(NoAdditionalArguments)

#EOF


class JobMarket:
  def __init__(self, employer, candidate):
    self.employer = employer
    self.candidate = candidate
  def Separating_Eqm(self):
    Group = self.candidate.Group
    Signal = self.candidate.Signal
    Wage_Schedule = self.employer.Wage_Schedule
    
    if ((Group == 1 and Signal == 0) or
       (Group == 2 and Signal == Wage_Schedule)):
        return "One more glance to check candidate from another Group(Type), therefore, the Separating Eqm will be more convincing."
    else:
        return "Check the scenario of Pooling Eqm."
      
  def Pooling_Eqm(self):
    q1 = self.candidate.__class__.q1
    Group = self.candidate.Group
    Signal = self.candidate.Signal
    Wage_Schedule = self.employer.Wage_Schedule

    if (Group == 2 and Signal == 0):
        return "The Group2(The talent) have no incentive to signal since q1*2 < Wage_Schedule: " + str(q1) + " * 2" + " < " + str(Wage_Schedule)
    elif (Group == 1 and Signal == Wage_Schedule):
        return "The Group1(The normal) are urged to signal by market structure since Wage_Schedule < 1-q1: " + str(Wage_Schedule) + "1-" + str(q1)
    else: 
        return "Check if there is Separating Eqm."
     
#EOF


#EOF





