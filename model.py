import numpy as np
import numpy_financial as npf


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

        #ACQUISITION ASSUMPTIONS
        self.total_costs = self.acqPrice + self.renCosts
        self.leasable_sf = self.sfUnit * self.units
        self.gross_sf = self.leasable_sf * self.buildEff
        self.renCosts_per_sf = self.renCosts * self.gross_sf
        self.acquisitionAssumptions = [self.total_costs, self.leasable_sf, self.gross_sf, self.renCosts_per_sf]

        #Financing Assumptions
        self.loanAmount = self.total_costs * self.ltc
        self.equityAmount = self.total_costs - self.loanAmount
        self.annualDebtSer = (npf.pmt(self.yearlyInRate/12, self.ammortization*12, -self.loanAmount))*12#Make sure is correct
        self.mortConstant = self.annualDebtSer/self.loanAmount
        self.financingAssumptions = [self.loanAmount, self.equityAmount, self.annualDebtSer, self.mortConstant]

        #Exit Assumptions



    def proForma(self):
        listOfLists = {}
        for i in range(self.hpr + 2):
            if i == 0:
                leveredCashFlow = -self.equityAmount
                listOfLists[i] = 0
            else:
                potGrossIncome = self.units * self.sfUnit * self.rent * 12 * ( (1+self.annualRentGrowth)**(i - 1) )
                vacancyNumber = self.vac * potGrossIncome
                effGrossIncome = potGrossIncome - vacancyNumber
                if i == 1:
                    opexEffGross = effGrossIncome
                opExNumber = (self.expratio * opexEffGross * (1 + self.expGrowthRate)**(i -1))
                noi = effGrossIncome - opExNumber 
                debt_service = self.annualDebtSer
                cfaf = noi - debt_service

                dscr = noi/debt_service
                cashOnCashRet = cfaf / self.equityAmount
                listOfLists[i] = potGrossIncome, vacancyNumber, effGrossIncome, opExNumber, noi, debt_service, cfaf, dscr, cashOnCashRet

        
        
        
        salePrice = listOfLists[self.hpr+1][4]/self.exitCapRate
        salesExpense = salePrice*self.saleExpense
        proceeds = salePrice - salesExpense
        loanBalance = npf.fv(self.yearlyInRate/12, self.hpr*12, debt_service/12, -self.loanAmount)
        netCashFlow = proceeds - loanBalance

                

        return listOfLists, salePrice
        """
            
            
            

            """
            


        
    



if __name__ == '__main__':
    
    print(npf.pmt(.05/12, 25*12, -2400000) * 12)
    print(-npf.fv(.05/12, 5*12, 168362/12, -2400000))

    model1 = NPVModel(12, 1000, 2.05, .03, .06, .3, .01, 2000000, 1200000, .85, .05, 25, 5, .75, .068, .03, .08)
    print(model1.proForma())

