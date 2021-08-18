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
       Signaling_Cost = Education/Group #negative correlation of cost and productivity.
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
        
        #Consider the scenarios when the Signal is equal to Wage_Schedule at first
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
        #The first element can be considered as our main character. So, we need N-1.
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
    
    def __init__(self, Low, High, Wage_Schedule):
        self.Wage_Schedule=Wage_Schedule
        self.Low = Low
        self.High = High
       
    def Possible_Wage(self, Signal):
        Wage_Schedule = self.Wage_Schedule
        if(Signal >= Wage_Schedule):
          return self.High
        else:
          return self.Low

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
          return "The Group1(The normal) are urged to signal by market structure since Wage_Schedule < 1-q1: " + str(Wage_Schedule) + " < " + "1-" + str(q1)
      else: 
          return "Check if there is Separating Eqm."

#EOF
