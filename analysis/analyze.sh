# R CMD BATCH src/analyze.r results/results.txt
# rm -f Rplots.pdf
R CMD BATCH src/twoWayANOVA.R results/results.txt
Rscript src/threeWayANOVA.R
echo "Running src/analyze.r and outputting to results/results.txt (and generating figures if analyze.r has code for them)."
