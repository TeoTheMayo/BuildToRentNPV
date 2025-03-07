import numpy as np
import numpy_financial as npf
from datetime import datetime
from dateutil.relativedelta import relativedelta

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

        self.listOfLists = {}
        for i in range(self.hpr + 2):
            if i == 0:
                self.listOfLists[i] = 0
            else:
                potGrossIncome = self.units * self.sfUnit * self.rent * 12 * ( (1+self.annualRentGrowth)**(i - 1) )
                vacancyNumber = self.vac * potGrossIncome
                effGrossIncome = potGrossIncome - vacancyNumber
                if i == 1:
                    opexEffGross = effGrossIncome
                opExNumber = (self.expratio *
                 opexEffGross * (1 + self.expGrowthRate)**(i -1))
                noi = effGrossIncome - opExNumber 
                debt_service = self.annualDebtSer
                cfaf = noi - debt_service

                dscr = noi/debt_service
                cashOnCashRet = cfaf / self.equityAmount

                proFormalist = potGrossIncome, vacancyNumber, effGrossIncome, opExNumber, noi, debt_service, cfaf, dscr, cashOnCashRet
                self.listOfLists[i] = proFormalist
        
        self.salePrice = self.listOfLists[self.hpr+1][4]/self.exitCapRate
        self.salesExpense = self.salePrice * self.saleExpense
        self.proceeds = self.salePrice - self.salesExpense
        self.loanBalance = npf.fv(self.yearlyInRate/12, self.hpr*12, debt_service/12, -self.loanAmount)
        self.netCashFlow = self.proceeds - self.loanBalance

        self.leveredCashFlow = []
        for i in range(self.hpr + 1):
            value = self.listOfLists[i]
            if isinstance(value, tuple) and i != self.hpr:
                self.leveredCashFlow.append(value[6])
            elif isinstance(value, tuple) and i == self.hpr:
                self.leveredCashFlow.append(value[6] + self.netCashFlow)  # Access the 7th element
            else:
                self.leveredCashFlow.append(-self.equityAmount)
        
        
        self.unleveredCashFlow = []
        for i in range(self.hpr + 1):
            value = self.listOfLists[i]
            if isinstance(value, tuple) and i != self.hpr:
                self.unleveredCashFlow.append(value[4])
            elif isinstance(value, tuple) and i == self.hpr:
                self.unleveredCashFlow.append(value[4] + self.proceeds)  # Access the 7th element
            else:
                self.unleveredCashFlow.append(-self.total_costs)
        
    def projectNPV(self):
        ppv = npf.npv(self.reqUnlRet, self.unleveredCashFlow) + self.total_costs
        return ppv

    def projectNPV(self):
        npv = npf.npv(self.reqUnlRet, self.unleveredCashFlow)
        return npv
    
    def projectUIRR(self):
        u_irr = npf.irr(self.unleveredCashFlow)
        return u_irr
    
    def projectLIRR(self):
        l_irr = npf.irr(self.leveredCashFlow)
        return l_irr

    def equityMultiple(self):
        negative = []
        index = -1
        leveredCF = self.leveredCashFlow #Prevent manipulating original list
        for i in leveredCF:
            index += 1
            if i <= 0:
                neg = float(leveredCF.pop(index))
                negative.append(neg)
        equityMult = (np.sum(leveredCF)) / np.sum(negative)
        return -equityMult
    
class SingleFamiliy(object):
    def __int__(self, build_size, land_size, purchase_date, renovation_months, holding_period, months_to_market, estimated_sale_date, purchase_price, closing_costs, due_dilignece_costs, construction_budget, sale_price, broker_commision, other_closing_costs, proerty_tax, insurance_monthly, loan_to_value, mortgage_int_rate, mort_term, monthly_rental_rate, var_opex, prop_manegment_fee, days_vacant, capital_reserve, ann_income_growth_rate, ann_expense_growth_rate, occupancy_month):
        self.build_size = build_size
        self.land_size = land_size
        self.purchase_date = purchase_date
        self.renovation_months = renovation_months
        self.holding_period = holding_period
        self.months_to_market = months_to_market
        self.investment_period = self.holding_period + self.renovation_months + self.months_to_market
        self.estimated_sale_price = estimated_sale_date#COME BACK, needs to be max of monthly cash flow
        self.purchase_price = purchase_price
        self.closing_costs = closing_costs
        self.due_diligence_costs  = due_dilignece_costs
        self.construction_budget = construction_budget#REFERENCE to another assumption sheet: Construction Budget
        self.sale_price = sale_price
        self.broker_commision = broker_commision
        self.other_closing_costs = other_closing_costs
        self.property_tax = proerty_tax
        self.insurance_monthly = insurance_monthly
        self.loan_to_value = loan_to_value
        self.loan_amount = self.purchase_price * self.loan_to_value
        self.mort_int_rate = mortgage_int_rate
        self.mort_term = mort_term
        self.monthly_payment = -(npf.pmt(self.mort_int_rate/12, self.mort_term*12, self.loan_amount)) 
        self.monthly_rental_rate = monthly_rental_rate
        self.var_opex = var_opex
        self.prop_management_fee = prop_manegment_fee
        self.days_vacant = days_vacant
        self.vacancy = self.days_vacant/365
        self.capital_reserves = capital_reserve
        self.ann_income_growth_rate = ann_income_growth_rate
        self.ann_expense_growth_rate = ann_expense_growth_rate
        self.occupancy_month = occupancy_month

    def monthlyCashFlow(self):
        return None




if __name__ == '__main__':
    
    #print(npf.pmt(.05/12, 25*12, -2400000) * 12)
    #print(-npf.fv(.05/12, 5*12, 168362/12, -2400000))

    model1 = NPVModel(12, 1000, 2.05, .03, .06, .3, .01, 2000000, 1200000, .85, .05, 25, 5, .75, .068, .03, .08)


    #print(-npf.pmt(.035/12, 30*12, 280000))
    #print(model1.projectNPV())
    #print(model1.equityMultiple())

    def returnListOfDates(investmentPeriod, PurchaseDate):
        #Incorporate ENDOFMONTH function
        new_text = PurchaseDate.split("/")
        year, month, day = int(new_text[-1]), int(new_text[0]), int(new_text[1])
        new_period = investmentPeriod + 1
        monthly_cash_flow_lib = []
        new_date = datetime(year, month, day)
        index = 0
        month_num = -1
        month -= 1
        while index < new_period:
            if month == 12:
                month = 1
                index += 1
                year += 1
                new_date = datetime(year, month, day) + relativedelta(day=31)
            else:
                month += 1
                index += 1
                new_date = datetime(year, month, day) + relativedelta(day=31)
            monthly_cash_flow_lib.append([new_date, index])
        
        return monthly_cash_flow_lib


        

    x = returnListOfDates(32, "1/1/2022")
    for i in x:
        print(i)

    