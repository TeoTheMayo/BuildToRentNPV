class NPVModel(object):
    def __init__(self, units, sfUnit, rent, annualRentGrowth, vac, expRatio, expGrwothRate, acqPrice, renCosts, buildEff, yearlyIntRate, ammortization, hpr, ltc, exitCapRate, saleExpense, reqUnlRet):
        self.units = units
        self.sfUnit = sfUnit
        self.rent = rent
        self.annualRentGrowth = annualRentGrowth
        self.vac = vac
        self.expratio = expRatio
        self.expGrowthRate = expGrwothRate
        self.acqPrice = acqPrice
        self.renCosts = renCosts
        self.buildEff = buildEff
        self.yearlyInRate = yearlyIntRate
        self.ammortization = ammortization
        self.hpr = hpr
        self.ltc = ltc
        self.exitCapRate = exitCapRate
        self.saleExpense = saleExpense
        self.reqUnlRet = reqUnlRet
    
    def furtherAssumptions(self):
        #Acquisition Assumptions
        total_costs = self.acqPrice + self.renCosts
        leasable_sf = self.sfUnit * self.units
        gross_sf = leasable_sf * self.buildEff
        renCosts_per_sf = self.renCosts * gross_sf
        acquisitionAssumptions = [total_costs, leasable_sf, gross_sf, renCosts_per_sf]

        #Financing Assumptions
        loanAmount = total_costs * self.ltc
        equityAmount = total_costs - loanAmount
        annualDebtSer = 0#PMT(annualIntRate/12, Ammortization*12, -loanAmount)*12
        mortConstant = annualDebtSer/loanAmount
        financingAssumptions = [loanAmount, equityAmount, annualDebtSer, mortConstant]


    def proForma(self):
        listOfLists = []
        for i in range(self.hpr + 1):
            if i == 0:
                proFormaList = [0]
            else:
                potGrossIncome = self.units * self.sfUnit * self.rent * 12 * ( (1+self.annualRentGrowth)^(i - 1) )
                proFormaList = [i]


        return 
    