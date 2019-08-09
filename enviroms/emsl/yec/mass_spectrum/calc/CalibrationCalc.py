
from builtins import NotImplementedError

import numpy as np


class MZDomain_Calibration:

    
    def __init__(self, mass_spectrum, selected_mass_peaks):
        
        self.mass_spectrum = mass_spectrum
        self.selected_mass_peaks = selected_mass_peaks
        self.load_variables()

    def load_variables(self):
        
        error = list()
        mz_exp = list()
        mz_theo = list()
        for mspeak in self.selected_mass_peaks:
            
            for molecular_formula in mspeak:
                mz_exp.append(mspeak.mz_exp)
                error.append(molecular_formula._calc_assigment_mass_error(mspeak.mz_exp))
                mz_theo.append(molecular_formula.mz_theor)

        self.mz_theo = np.array(mz_theo)
        self.mz_exp = np.array(mz_exp)
        self.mz_exp_ms = np.array([mspeak.mz_exp for mspeak in self.mass_spectrum])        


    def linear(self, iteration=False):
        mz_exp = self.mz_exp
        mz_exp_ms = self.mz_exp_ms 
        error = ((mz_exp-self.mz_theo)/self.mz_theo) *1000000
        last_rms = np.sqrt(np.mean(error**2))
        while True:
            
            matrix = np.vstack([mz_exp, np.ones(len(mz_exp)) ]).T
            Aterm, Bterm =  np.linalg.lstsq(matrix, self.mz_theo, rcond=None)[0]
            
            #matrix = np.vstack([mz_exp, np.power(mz_exp,2)]).T
            #Aterm, Bterm =  np.linalg.lstsq(matrix, self.mz_theo, rcond=None)[0]
            
            print("Aterm", Aterm)
            #mz_domain = Aterm / (self.freq_exp_ms + Bterm) 
            mz_exp = (Aterm * mz_exp) + Bterm
            error = ((mz_exp-self.mz_theo)/self.mz_theo)*1000000
            rms = np.sqrt(np.mean(error**2))
            std = np.std(error)
            print ('HEREEE', rms, std, Aterm, Bterm)
            if rms < last_rms:
                 last_rms = rms
                 mz_exp_ms = np.array([mspeak.mz_exp for mspeak in self.mass_spectrum])        
                 mz_domain = (Aterm * mz_exp_ms) + Bterm
                 self.reset_mass_spec(mz_domain, Aterm, Bterm, 0)        
                 if not iteration:
                     break       
            else:
                break     

    def ledford_inverted_calibration(self, iteration=False):
        
        mz_exp = self.mz_exp
        mz_exp_ms = self.mz_exp_ms 
        error = ((mz_exp-self.mz_theo)/self.mz_theo) *1000000
        last_rms = np.sqrt(np.mean(error**2))
        while True:
            
            matrix = np.vstack([mz_exp, np.power(mz_exp,2) ]).T
            Aterm, Bterm =  np.linalg.lstsq(matrix, self.mz_theo, rcond=None)[0]
            
            #matrix = np.vstack([mz_exp, np.power(mz_exp,2)]).T
            #Aterm, Bterm =  np.linalg.lstsq(matrix, self.mz_theo, rcond=None)[0]
            
            print("Aterm", Aterm)
            #mz_domain = Aterm / (self.freq_exp_ms + Bterm) 
            mz_exp = (Aterm * (mz_exp)) + (Bterm * np.power((mz_exp), 2) )
            error = ((mz_exp-self.mz_theo)/self.mz_theo)*1000000
            rms = np.sqrt(np.mean(error**2))
            std = np.std(error)
            print ('HEREEE', rms, std, Aterm, Bterm)
            if rms < last_rms:
                 last_rms = rms
                 mz_exp_ms = np.array([mspeak.mz_exp for mspeak in self.mass_spectrum])        
                 mz_domain = (Aterm * (mz_exp_ms)) + (Bterm * np.power((mz_exp_ms), 2) )
                 self.reset_mass_spec(mz_domain, Aterm, Bterm, 0)   
                 if not iteration:
                    break       
            else:
                break     
        

    def quadratic(self, iteration=False):
        
        mz_exp = self.mz_exp
        mz_exp_ms = self.mz_exp_ms 
        error = ((mz_exp-self.mz_theo)/self.mz_theo) *1000000
        last_rms = np.sqrt(np.mean(error**2))
        while True:
            
            matrix = np.vstack([mz_exp, np.power(mz_exp,2), np.ones(len(mz_exp))]).T
            Aterm, Bterm, Cterm =  np.linalg.lstsq(matrix, self.mz_theo, rcond=None)[0]
            
            #matrix = np.vstack([mz_exp, np.power(mz_exp,2)]).T
            #Aterm, Bterm =  np.linalg.lstsq(matrix, self.mz_theo, rcond=None)[0]
            
            print("Aterm", Aterm)
            #mz_domain = Aterm / (self.freq_exp_ms + Bterm) 
            mz_exp = (Aterm * (mz_exp)) + (Bterm * np.power((mz_exp), 2) + Cterm)
            error = ((mz_exp-self.mz_theo)/self.mz_theo)*1000000
            rms = np.sqrt(np.mean(error**2))
            std = np.std(error)
            print ('HEREEE', rms, std, Aterm, Bterm)
            if rms < last_rms:
                 last_rms = rms
                 mz_exp_ms = np.array([mspeak.mz_exp for mspeak in self.mass_spectrum])        
                 mz_domain = (Aterm * (mz_exp_ms)) + (Bterm * np.power((mz_exp_ms), 2) + Cterm )
                 self.reset_mass_spec(mz_domain, Aterm, Bterm, Cterm)     
                 if not iteration:
                    break        
            else:
                break     
        '''
        matrix = np.vstack([self.mz_exp, np.power(self.mz_exp,2), np.ones(len(self.mz_exp))]).T
        Aterm, Bterm, Cterm =  np.linalg.lstsq(matrix, self.mz_theo, rcond=None)[0]
        print("Aterm", Aterm)
        #mz_domain = Aterm / (self.freq_exp_ms + Bterm) 
        self.mz_exp = (Aterm * (self.mz_exp)) + (Bterm * np.power((self.mz_exp), 2) + Cterm)
    
        mz_domain = (Aterm * (self.mz_exp_ms)) + (Bterm * np.power((self.mz_exp_ms), 2) + Cterm)
        self.reset_mass_spec(mz_domain, Aterm, Bterm, Cterm)
        '''
   
    def reset_mass_spec(self, mz_domain, Aterm, Bterm, Cterm):
        
        self.mass_spectrum._calibration_terms = (Aterm, Bterm, 0)
        for indexes, mspeak in enumerate(self.mass_spectrum):
            mspeak.mz_exp = mz_domain[indexes]


class FreqDomain_Calibration:

    def __init__(self, mass_spectrum, selected_mass_peaks, include_isotopologue=False):
        
        self.selected_mass_peaks = selected_mass_peaks
        error = list()
        freq_exp = list()
        mz_theo = list()
        mz_exp = list()

        for mspeak in selected_mass_peaks:
            
            if not include_isotopologue:
                
                molecular_formulas = [formula for formula in mspeak if not formula.is_isotopologue]
                
            else:
                
                molecular_formulas = mspeak
            
                for molecular_formula in molecular_formulas:
                    
                    freq_exp.append(mspeak.freq_exp)
                    error.append(molecular_formula._calc_assigment_mass_error(mspeak.mz_exp))
                    mz_theo.append(molecular_formula.mz_theor)
                    mz_exp.append(mspeak.mz_exp)
                    
        
        self.mz_exp = np.array(mz_exp)
        self.mz_theo = np.array(mz_theo)
        self.freq_exp = np.array(freq_exp)
        self.mass_spectrum = mass_spectrum
        self.freq_exp_ms = np.array([mspeak.freq_exp for mspeak in mass_spectrum])

    def recal_mass_spec(self, mz_domain, Aterm, Bterm, Cterm):
        
        self.mass_spectrum._calibration_terms = (Aterm, Bterm, 0)
        for indexes, mspeak in enumerate(self.mass_spectrum):
            mspeak.mz_exp = mz_domain[indexes]
            
    def step_fit(self):
    
        raise NotImplementedError

    def linear(self):
        
        matrix = np.vstack([1/self.freq_exp, np.ones(len(self.freq_exp))]).T
        Aterm, Bterm =  np.linalg.lstsq(matrix, self.mz_theo, rcond=None)[0]
        print("Aterm", Aterm)
        #mz_domain = Aterm / (self.freq_exp_ms + Bterm) 
        mz_domain = (Aterm/self.freq_exp_ms) + Bterm 
        self.recal_mass_spec(mz_domain, Aterm, Bterm, 0)

    def quadratic(self, iteration=False):
        
        mz_theo = self.mz_theo
        freq_exp = self.freq_exp
        mz_exp = self.mz_exp
        
        error = ((mz_exp-mz_theo)/mz_theo) *1000000
        last_rms = np.sqrt(np.mean(error**2))
        while True:
            
            matrix = np.vstack([1/freq_exp, 1/np.power(freq_exp,2), np.ones(len(freq_exp))]).T
            Aterm, Bterm, Cterm =  np.linalg.lstsq(matrix, self.mz_theo, rcond=None)[0]
            mz_exp = (Aterm / (freq_exp)) + (Bterm / np.power((freq_exp), 2) )+ Cterm
            error = ((mz_exp-mz_theo)/mz_theo)*1000000
            rms = np.sqrt(np.mean(error**2))
            std = np.std(error)
            print ('HEREEE', rms, std, Aterm, Bterm)
            if rms < last_rms:
                last_rms = rms
                freq_exp = (Aterm + np.sqrt(np.power(-Aterm,2) - (4*Cterm*(mz_exp-Bterm)))) /(2*mz_exp)
                
                mz_domain = (Aterm / (self.freq_exp_ms)) + (Bterm / np.power((self.freq_exp_ms), 2) )+ Cterm
                self.recal_mass_spec(mz_domain, Aterm, Bterm, Cterm)
                if not iteration:
                    break       
            else:
                break     

    def ledford_calibration(self, iteration=False):
        
        mz_theo = self.mz_theo
        freq_exp = self.freq_exp
        mz_exp = self.mz_exp
        
        error = ((mz_exp-self.mz_theo)/self.mz_theo) *1000000
        last_rms = np.sqrt(np.mean(error**2))
        while True:
            
            matrix = np.vstack([1/freq_exp, 1/np.power(freq_exp,2)]).T
            Aterm, Bterm =  np.linalg.lstsq(matrix, self.mz_theo, rcond=None)[0]
            
            mz_exp = (Aterm / (freq_exp)) + (Bterm / np.power((freq_exp), 2))
            error = ((mz_exp-mz_theo)/mz_theo)*1000000
            rms = np.sqrt(np.mean(error**2))
            std = np.std(error)
            print ('HEREEE', rms, std, Aterm, Bterm)
            if rms < last_rms:
                 last_rms = rms
                 freq_exp = (Aterm + np.sqrt(np.power(-Aterm,2) - (4*mz_exp-Bterm))) /(2*mz_exp)
                 mz_domain = (Aterm / (self.freq_exp_ms)) + (Bterm / np.power((self.freq_exp_ms), 2))
                 self.recal_mass_spec(mz_domain, Aterm, Bterm, 0)
                 if not iteration:
                    break       
            else:
                break     
        
    def setfit_calibration(self):
        
        for mspeak in self.selected_mass_peaks:
           self.mass_spectrum[mspeak.index]
            

class SquareFittingAB:
    
    def __init__(self, eixo_f, eixo_mz, ):

        self.eixo_mz = np.array(eixo_mz)
        self.eixo_f = np.array(eixo_f)

    def criar_matrixY(self):

        y = []
        for i in range(len(self.eixo_mz)):
            y.append([self.eixo_mz[i]])

        return np.matrix(y)

    def criar_matrixX(self):
        x = []
        for i in range(len(self.eixo_f)):
            x.append([(1 / self.eixo_f[i]), (1 / (self.eixo_f[i] ** 2))])

        return np.matrix(x)

    def criar_transposta(self):
        X = self.criar_matrixX()
        Xt = X.T

        return Xt

    def segundo_membro(self):
        Xt = self.criar_transposta()
        XtY = Xt * self.criar_matrixY()
        return XtY

    def primeiro_membro(self):
        Xt = self.criar_transposta()
        XtX = Xt * self.criar_matrixX()

        return XtX.I

    def fitting(self):
        # retorna matrix 3x0 dos coeficientes da reta y = c + bx + a(x**2)
        return self.primeiro_membro() * self.segundo_membro()

    def print_equacao_cubica(self):
        # imprime a equcao de regressao na saida padrao
        a = self.fitting()[0]
        b = self.fitting()[1]

        print( "m/z = %f 1/f + %f 1/f**2" % (a, b))

    def return_mz(self, f):
        # retorna valor de y esperado da regrecao y = c + bx + a(x**2) 
        a = self.fitting()[0]
        b = self.fitting()[1]

        return np.array((a * (1 / f)) + (b * (1 / (f ** 2))))[0]

    def return_a(self):

        #print np.array(self.fitting())  # retorna o coeficiente a da equcao y = c + bx + a(x**2)
        return np.array(self.fitting()[0])[0][0]

    def return_b(self):
        # retorna o coeficiente b da equcao y = c + bx + a(x**2)

        return np.array(self.fitting()[1])[0][0]