/************************************************************************
Stata .do file to analyze hangman data file

Data created using hangman simulation program: 
    https://github.com/angelinahli/hangman-solver
************************************************************************/

* replace hangman_data_dir before running
global hangman_data_dir = "~/Desktop/hangman"
global import_data = "$hangman_data_dir/hangman_data.csv"

clear all
set more off
log using $hangman_data_dir/hangman_summ_stats.txt, replace

*** (A) Basic summary stats ***

import delim using "$import_data", varnames(1) clear
gen num_unusual = cont_w + cont_k + cont_v + cont_x + cont_z + cont_j + cont_q

foreach varname in wrong len_word cont_unusual num_unusual {
    di "summ of `varname'"
    summ `varname'
}

*** (B) Data analysis ***

foreach varname in len_word cont_unusual num_unusual {
    di "does `varname' correlate with difficulty of guessing word?"
    reg wrong `varname'
}

log close
