
import numpy as np

class MZDomain_Calibration:

    def __init__(self, mass_spectrum, selected_mass_peaks, include_isotopologue=False):

        self.mass_spectrum = mass_spectrum
        self.selected_mass_peaks = selected_mass_peaks
        self.load_variables(include_isotopologue)

    def load_variables(self, include_isotopologue):

        error = list()
        mz_exp = list()
        mz_theo = list()
        for mspeak in self.selected_mass_peaks:

            if not include_isotopologue:
                molecular_formulas = [
                    formula for formula in mspeak if not formula.is_isotopologue]
            else:
                molecular_formulas = mspeak

            for molecular_formula in molecular_formulas:
                mz_exp.append(mspeak.mz_exp)
                error.append(
                    molecular_formula._calc_assigment_mass_error(mspeak.mz_exp))
                mz_theo.append(molecular_formula.mz_theor)

        self.mz_theo = np.array(mz_theo)
        self.mz_exp = np.array(mz_exp)
        self.mz_exp_ms = np.array(
            [mspeak.mz_exp for mspeak in self.mass_spectrum])

    def linear(self, iteration=False):
        mz_exp = self.mz_exp
        mz_exp_ms = self.mz_exp_ms
        error = ((mz_exp-self.mz_theo)/self.mz_theo) * 1000000
        last_rms = np.sqrt(np.mean(error**2))
        while True:

            matrix = np.vstack([mz_exp, np.ones(len(mz_exp))]).T
            Aterm, Bterm = np.linalg.lstsq(matrix, self.mz_theo, rcond=None)[0]

            #matrix = np.vstack([mz_exp, np.power(mz_exp,2)]).T
            #Aterm, Bterm =  np.linalg.lstsq(matrix, self.mz_theo, rcond=None)[0]

            print("Aterm", Aterm)
            #mz_domain = Aterm / (self.freq_exp_ms + Bterm)
            mz_exp = (Aterm * mz_exp) + Bterm
            error = ((mz_exp-self.mz_theo)/self.mz_theo)*1000000
            rms = np.sqrt(np.mean(error**2))
            std = np.std(error)
            print('HEREEE', rms, std, Aterm, Bterm)
            if rms < last_rms:
                last_rms = rms
                mz_exp_ms = np.array(
                    [mspeak.mz_exp for mspeak in self.mass_spectrum])
                mz_domain = (Aterm * mz_exp_ms) + Bterm
                self.reset_mass_spec(mz_domain, Aterm, Bterm, 0)
                if not iteration:
                    break
            else:
                break

    def ledford_inverted_calibration(self, iteration=False):

        mz_exp = self.mz_exp
        mz_exp_ms = self.mz_exp_ms
        error = ((mz_exp-self.mz_theo)/self.mz_theo) * 1000000
        last_rms = np.sqrt(np.mean(error**2))
        while True:

            matrix = np.vstack([mz_exp, np.power(mz_exp, 2)]).T
            Aterm, Bterm = np.linalg.lstsq(matrix, self.mz_theo, rcond=None)[0]

            #matrix = np.vstack([mz_exp, np.power(mz_exp,2)]).T
            #Aterm, Bterm =  np.linalg.lstsq(matrix, self.mz_theo, rcond=None)[0]

            print("Aterm", Aterm)
            #mz_domain = Aterm / (self.freq_exp_ms + Bterm)
            mz_exp = (Aterm * (mz_exp)) + (Bterm * np.power((mz_exp), 2))
            error = ((mz_exp-self.mz_theo)/self.mz_theo)*1000000
            rms = np.sqrt(np.mean(error**2))
            std = np.std(error)
            print('HEREEE', rms, std, Aterm, Bterm)
            if rms < last_rms:
                last_rms = rms
                mz_exp_ms = np.array(
                    [mspeak.mz_exp for mspeak in self.mass_spectrum])
                mz_domain = (Aterm * (mz_exp_ms)) + \
                    (Bterm * np.power((mz_exp_ms), 2))
                self.reset_mass_spec(mz_domain, Aterm, Bterm, 0)
                if not iteration:
                    break
            else:
                break

    def quadratic(self, iteration=False):

        mz_exp = self.mz_exp
        mz_exp_ms = self.mz_exp_ms
        error = ((mz_exp-self.mz_theo)/self.mz_theo) * 1000000
        last_rms = np.sqrt(np.mean(error**2))
        while True:

            matrix = np.vstack(
                [mz_exp, np.power(mz_exp, 2), np.ones(len(mz_exp))]).T
            Aterm, Bterm, Cterm = np.linalg.lstsq(
                matrix, self.mz_theo, rcond=None)[0]

            #matrix = np.vstack([mz_exp, np.power(mz_exp,2)]).T
            #Aterm, Bterm =  np.linalg.lstsq(matrix, self.mz_theo, rcond=None)[0]

            print("Aterm", Aterm)
            #mz_domain = Aterm / (self.freq_exp_ms + Bterm)
            mz_exp = (Aterm * (mz_exp)) + \
                (Bterm * np.power((mz_exp), 2) + Cterm)
            error = ((mz_exp-self.mz_theo)/self.mz_theo)*1000000
            rms = np.sqrt(np.mean(error**2))
            std = np.std(error)
            print('HEREEE', rms, std, Aterm, Bterm)
            if rms < last_rms:
                last_rms = rms
                mz_exp_ms = np.array(
                    [mspeak.mz_exp for mspeak in self.mass_spectrum])
                mz_domain = (Aterm * (mz_exp_ms)) + \
                    (Bterm * np.power((mz_exp_ms), 2) + Cterm)
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
        
        #for indexes, mspeak in enumerate(self.mass_spectrum):
        #    mspeak.mz_cal = mz_domain[indexes] 
        self.mass_spectrum.mz_cal = mz_domain

class FreqDomain_Calibration:

    def __init__(self, mass_spectrum, selected_mass_peaks, include_isotopologue=False):

        self.selected_mspeaks = selected_mass_peaks
        error = list()
        freq_exp = list()
        mz_theo = list()
        mz_exp = list()

        for mspeak in selected_mass_peaks:

            if not include_isotopologue:
                molecular_formulas = [
                    formula for formula in mspeak if not formula.is_isotopologue]
            else:
                molecular_formulas = mspeak

            for molecular_formula in molecular_formulas:

                freq_exp.append(mspeak.freq_exp)
                error.append(
                    molecular_formula._calc_assigment_mass_error(mspeak.mz_exp))
                mz_theo.append(molecular_formula.mz_theor)
                mz_exp.append(mspeak.mz_exp)

        self.mz_exp = np.array(mz_exp)
        self.mz_theo = np.array(mz_theo)
        self.freq_exp = np.array(freq_exp)
        self.mass_spectrum = mass_spectrum
        self.freq_exp_ms = np.array(
            [mspeak.freq_exp for mspeak in mass_spectrum])

    def recal_mass_spec(self, mz_domain, Aterm, Bterm, Cterm):

        self.mass_spectrum._calibration_terms = (Aterm, Bterm, 0)
        
        #for indexes, mspeak in enumerate(self.mass_spectrum):
        #    mspeak.mz_cal = mz_domain[indexes] 
        self.mass_spectrum.mz_cal = mz_domain

    def linear(self):

        matrix = np.vstack([1/self.freq_exp, np.ones(len(self.freq_exp))]).T
        Aterm, Bterm = np.linalg.lstsq(matrix, self.mz_theo, rcond=None)[0]
        print("Aterm", Aterm)
        #mz_domain = Aterm / (self.freq_exp_ms + Bterm)
        mz_domain = (Aterm/self.freq_exp_ms) + Bterm
        self.recal_mass_spec(mz_domain, Aterm, Bterm, 0)

    def quadratic(self, iteration=False):

        mz_theo = self.mz_theo
        freq_exp = self.freq_exp
        mz_exp = self.mz_exp

        error = ((mz_exp-mz_theo)/mz_theo) * 1000000
        last_rms = np.sqrt(np.mean(error**2))
        while True:

            matrix = np.vstack(
                [1/freq_exp, 1/np.power(freq_exp, 2), np.ones(len(freq_exp))]).T
            Aterm, Bterm, Cterm = np.linalg.lstsq(
                matrix, self.mz_theo, rcond=None)[0]
            mz_exp = (Aterm / (freq_exp)) + \
                (Bterm / np.power((freq_exp), 2)) + Cterm
            error = ((mz_exp-mz_theo)/mz_theo)*1000000
            rms = np.sqrt(np.mean(error**2))
            std = np.std(error)
            print('HEREEE', rms, std, Aterm, Bterm)
            if rms < last_rms:
                last_rms = rms
                freq_exp = (Aterm + np.sqrt(np.power(-Aterm, 2) -
                                            (4*Cterm*(mz_exp-Bterm)))) / (2*mz_exp)

                mz_domain = (Aterm / (self.freq_exp_ms)) + \
                    (Bterm / np.power((self.freq_exp_ms), 2)) + Cterm
                self.recal_mass_spec(mz_domain, Aterm, Bterm, Cterm)
                if not iteration:
                    break
            else:
                break

    def ledford_calibration(self, iteration=False):

        mz_theo = self.mz_theo
        freq_exp = self.freq_exp
        mz_exp = self.mz_exp

        error = ((mz_exp-self.mz_theo)/self.mz_theo) * 1000000
        last_rms = np.sqrt(np.mean(error**2))
        while True:

            matrix = np.vstack([1/freq_exp, 1/np.power(freq_exp, 2)]).T
            Aterm, Bterm = np.linalg.lstsq(matrix, self.mz_theo, rcond=None)[0]

            mz_exp = (Aterm / (freq_exp)) + (Bterm / np.power((freq_exp), 2))
            error = ((mz_exp-mz_theo)/mz_theo)*1000000
            rms = np.sqrt(np.mean(error**2))
            std = np.std(error)
            print('HEREEE', rms, std, Aterm, Bterm)
            if rms < last_rms:
                last_rms = rms
                freq_exp = (Aterm + np.sqrt(np.power(-Aterm, 2) -
                                            (4*mz_exp-Bterm))) / (2*mz_exp)
                mz_domain = (Aterm / (self.freq_exp_ms)) + \
                    (Bterm / np.power((self.freq_exp_ms), 2))
                self.recal_mass_spec(mz_domain, Aterm, Bterm, 0)
                if not iteration:
                    break
            else:
                break

    def step_fit(self, steps=4):

        def f_to_mz(f, A, B, C, a): 
                return (A / f) + (B / np.power(f, 2)) + (C*a / np.power(f, 2))
        def mz_to_f(m, A, B, C): return (-A-m/B)
        
        tuple_indexs = [(i, i+steps) for i in range(0, len(self.selected_mspeaks)-steps, steps)]

        for current_index, tuple_index in enumerate(tuple_indexs):
            mspeak_ii, mspeak_fi = tuple_index
            freq_exp = list()
            mz_theor = list()
            mz_exp = list()
            abu = list()
            len_mono = len(range(mspeak_ii, mspeak_fi+1))
            len_iso =0
            
            for i in range(mspeak_ii, mspeak_fi+1):
               len_iso +=  len(self.selected_mspeaks[i][0].mspeak_indexes_isotopologues)
            
            for i in range(mspeak_ii, mspeak_fi+1):

                freq_exp.append(self.selected_mspeaks[i].freq_exp)
                mz_theor.append(self.selected_mspeaks[i][0].mz_theor)
                mz_exp.append(self.selected_mspeaks[i].mz_exp)
                abu.append(self.selected_mspeaks[i].abundance)
                
                mspeaks_iso_indexes = self.selected_mspeaks[i][0].mspeak_indexes_isotopologues    
                
                if len_iso == len_mono-1:
                    for iso_index in mspeaks_iso_indexes:
                    
                        freq_exp.append(self.mass_spectrum[iso_index].freq_exp)
                        mz_theor.append(self.mass_spectrum[iso_index][0].mz_theor)
                        mz_exp.append(self.mass_spectrum[iso_index].mz_exp)
                        abu.append(self.mass_spectrum[iso_index].abundance)    
                        
            
            freq_exp = np.array(freq_exp)
            mz_theor = np.array(mz_theor)
            mz_exp = np.array(mz_exp)
            abu = np.array(abu)

            if current_index == len(tuple_indexs)-1:
                ms_peaks_indexes = (self.selected_mspeaks[mspeak_ii].index, 0)
            elif current_index == 0:
                ms_peaks_indexes = (len(self.mass_spectrum)-1,
                                    self.selected_mspeaks[mspeak_fi].index-1)
            else:
                ms_peaks_indexes = (
                    self.selected_mspeaks[mspeak_ii].index, self.selected_mspeaks[mspeak_fi].index-1)

            final_index, start_index = ms_peaks_indexes
            
            #sub_TIC = sum([mspeak.abundance for mspeak in self.mass_spectrum[start_index:final_index]])
            
            #abundace term fails with lack of isotopologues
            
            if len_iso == len_mono-1:
                
                matrix = np.vstack([1/freq_exp, 1/np.power(freq_exp, 2), abu/np.power(freq_exp, 2)]).T
                A, B, C = np.linalg.lstsq(matrix, mz_theor, rcond=None)[0]
            else:
                
                matrix = np.vstack([1/freq_exp, 1/np.power(freq_exp, 2)]).T
                A, B = np.linalg.lstsq(matrix, mz_theor, rcond=None)[0]
                C = 0
            
            for mspeak in self.mass_spectrum[start_index:final_index]:
                mspeak.mz_cal = f_to_mz(
                    mspeak.freq_exp, A, B, C, 0)
        
        self.mass_spectrum.is_calibrated = True    