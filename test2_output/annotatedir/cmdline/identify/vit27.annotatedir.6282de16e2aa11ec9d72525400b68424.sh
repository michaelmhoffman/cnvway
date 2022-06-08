#!/usr/bin/env bash
/mnt/work1/users/home2/t114244uhn/miniconda3/envs/cnvway/bin/segway-task run viterbi test2_output/annotatedir/viterbi/viterbi027.bed chr6 41430000 43350001 30000 0 3 1 seg data/train-data.genomedata norm 0 False None None 1 -base 3 -cVitRegexFilter '^seg$' -cliqueTableNormalize 0.0 -componentCache F -cppCommandOptions '-DINPUT_PARAMS_FILENAME=test2_output/traindir/params/params.params -DCARD_SUPERVISIONLABEL=-1 -DCARD_SEG=3 -DCARD_SUBSEG=1 -DCARD_FRAMEINDEX=67 -DSEGTRANSITION_WEIGHT_SCALE=1.0' -deterministicChildrenStore F -eVitRegexFilter '^seg$' -fmt1 binary -fmt2 binary -hashLoadFactor 0.98 -inputMasterFile input.master -island T -iswp1 F -iswp2 F -jtFile test2_output/annotatedir/log/jt_info.txt -lst 100000 -mVitValsFile - -nf1 1 -nf2 0 -ni1 0 -ni2 1 -obsNAN T -of1 test2_output/annotatedir/observations/float32.list -of2 test2_output/annotatedir/observations/int.list -pVitRegexFilter '^seg$' -strFile segway.str -triFile test2_output/annotatedir/triangulation/segway.str.3.1.trifile -verbosity 0 -vitCaseSensitiveRegexFilter T
