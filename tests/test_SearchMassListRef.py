import os, sys
from pathlib import Path
sys.path.append(".")

from corems.molecular_formula.input.masslist_ref import ImportMassListRef
from corems.molecular_id.search.molecularFormulaSearch import SearchMolecularFormulas

import pytest

__author__ = "Yuri E. Corilo"
__date__ = "Jul 02, 2019"

def get_mass_spectrum():

    from corems.mass_spectrum.input.massList import ReadMassList

    file_location = Path.cwd() / "tests/tests_data/" / "ESI_NEG_ESFA.ascii"

    #polarity needs to be set or read from the file

    polariy = -1
   
    return ReadMassList(file_location, delimiter="  ").get_mass_spectrum(polariy, auto_process=True)
    
def test_search_imported_ref_files():

    mass_spectrum_obj = get_mass_spectrum()
    
    ref_file_location = os.path.join(os.getcwd(),  os.path.normcase("tests/tests_data/")) + "SRFA.ref"

    mf_references_list = ImportMassListRef(ref_file_location).from_bruker_ref_file()

    for mf in mf_references_list:

        print(mf.to_string_formated)
    
    ms_peaks_assigned = SearchMolecularFormulas().search_mol_formulas(mass_spectrum_obj, mf_references_list, find_isotopologues=False)

    assert (len(ms_peaks_assigned)) > 0


if __name__ == '__main__':
    
    test_search_imported_ref_files()