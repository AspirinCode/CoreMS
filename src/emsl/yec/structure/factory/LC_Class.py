'''
Created on Jun 12, 2019
'''
from emsl.yec.calc.LC_Calc import LC_Calculations
from emsl.yec.structure.factory.MassSpectrumClasses import MassSpecBase


__author__ = "Yuri E. Corilo"
__date__ = "Jun 25, 2019"


class LCMSBase(LC_Calculations):
    '''
    classdocs
    '''
    
    def __init__(self, sample_name):
        '''
        Constructor
        '''
        self.sample_name = sample_name
        self.retention_time_list = []
        self.scans_number_list = []
        self.tic_list = []
        
        self.ms  = {}
        '''
        key is scan number; value is MassSpectrum Class
        '''
                                      
    def set_mass_spectrum_for_scan(self,polarity, l_exp_mz, l_freq_centr, l_abundances, scan_number , noise_std, l_base_noise, l_signal_to_noise, l_charge, l_resolution, rt):
        
        self.ms[scan_number] = MassSpecBase(polarity,scan_number,noise_std, rt, l_exp_mz, l_freq_centr, l_abundances, l_base_noise, l_signal_to_noise, l_charge, l_resolution, )
         
    def get_mass_spec_by_scan_number(self,scan):
        
        return self.ms.get(scan)    
    
    def set_tic_list_from_data(self):
        
        self.set_tic_list([self.ms.get(i).get_sumed_peak_height() for i in self.get_scans_number()])
        
        #self.set_tic_list([self.ms.get(i).get_sumed_signal_to_noise() for i in self.get_scans_number()])
    
    def set_retention_time_from_data(self):
        
        retention_time_list = []
        
        for key_ms in sorted(self.ms.keys()):
            
            retention_time_list.append(self.ms.get(key_ms).rt)
       
        self.set_retention_time_list(retention_time_list)
        
        #self.set_retention_time_list(sorted(self.ms.keys()))
        
    def set_scans_number_from_data(self):
        self.set_scans_number_list(sorted(self.ms.keys()))
        
    def get_scans_number(self):
        
        return self.scans_number_list
    
    def get_retention_time(self):
        
        return self.retention_time_list
    
    def get_tic(self):
        
        return self.tic_list    
    
    def set_retention_time_list(self, lista):
        #self.retention_time_list = linspace(0, 80, num=len(self.scans_number_list))
        self.retention_time_list =  lista  
       
    def set_scans_number_list(self, lista):
        
        self.scans_number_list = lista      
        
    def set_tic_list(self, lista): 
        
        self.tic_list = lista
        
    def find_nearest_scan(self, rt):
        
        from numpy import abs as absolute
        from numpy import array
        
        #print  self.retention_time_list
        array_rt = array(self.retention_time_list)
        
        scan_index = (absolute(array_rt - rt)).argmin()
        
        real_scan = self.scans_number_list[scan_index]
        
        return real_scan +1 
               
 