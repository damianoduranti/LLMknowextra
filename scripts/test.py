import logging
from dl_concept import dl_concept
from ltl_process import ltl_process

logging.basicConfig(level=logging.INFO)

def main():

    # LTL trace verification 
    ltl_process('temp/unconstrained/output_pos5_neg5_symbolss_p_length30_sig.json', 5)

    # DL concept verification
    #dl_concept('data/DL_concept/strong_sep/1/1_instances.json', 'data/DL_concept/strong_sep/1/1_ontology.owl', 5)

if __name__ == '__main__':
    main()