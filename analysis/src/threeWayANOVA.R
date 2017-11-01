# repeated-measures three-way ANOVA
# expects wide data format, converts to long, prints anova, posthoc, descriptive stats, and simple charts

# run these lines of code the first time. once the packages are installed locally, you don't need to run these again
# install.packages("ggplot2")
# install.packages("grid")
# install.packages("plyr")
# install.packages("reshape")
# install.packages("ez")
# install.packages("nlme")
# install.packages("multcomp")
# install.packages("gridExtra")

# expect wide format with column names in format factor1_factor2_factor3_outputName
# factor1 should be value from withinLevels1 in the csv
# factor2 should be value from withinLevels2 in the csv
# factor3 should be value from withinLevels3 in the csv
##!! each of these columns should have the average from trials with combination of factor1 and factor2 and factor3 levels
##!! level names for factors must be unique

# ANOVA script can work with different amounts of levels for each factor, but the plotting only works if iv3 has 2 levels

### config input settings

datafilename="ReachStudy_3Way_Tech_OffsetSize_Distance/ReachStudy_ThreeWay_Tech_OffsetSize_Distance_Error.csv"  # csv file name

# Header name for participants
participantName = "p_ID"

# Factor names for repeated measures design
independentVariableName1 = "Technique" # for output/naming
withinLevels1 = c("translational", "interpolation") # needs to match first factor in csv column name
levelLabels1 = c("Trans", "Interp") # for renaming !!! Need to be in same order as withinLabels. This is for plotting

independentVariableName2 = "OffsetSize" # for output/naming
withinLevels2 = c("offset10", "offset14", "offset20", "offset30") # needs to match second factor in csv column name
levelLabels2 = c("offset10", "offset14", "offset20", "offset30") # for renaming !!! Need to be in same order as withinLabels. This is for plotting

independentVariableName3 = "Distance" # for output/naming
withinLevels3 = c("close", "far") # needs to match second factor in csv column name
levelLabels3 = c("Close", "Far") # for renaming !!! Need to be in same order as withinLabels. This is for plotting

outcomeName = "error"

# set some parameters for graphs
## outcomeName = "angleOffset"
yMin = 0
yMax = 1
yInterval = .1
yLabel = "Time"
chartTitle = "Technique x Offset"
saveFile = "ReachStudy_3Way_Tech_OffsetSize_Distance/three-way-Tech_OffsetSize_Distance_Error.jpg"
# requires a directory called "r_plots" is already created in directory

#ggsave(saveFile,width=8, height=6) #will only work after the ggplot code is run. wide


##### end of customization part #####

##### do the things ######

Data<-read.csv(datafilename, header = TRUE)

# new function for getting column by header
getColumnByName = function(dataframe, colName){return(dataframe[[which(colnames(dataframe) == colName)]])}

p_id_data = getColumnByName(Data, participantName)

# make sure subject identifier is not a number by prefixing with "p_"
Data[participantName] = paste("p", p_id_data, sep="_")


# Within independent factors/levels
withinCombos <- as.vector(outer(withinLevels1, withinLevels2, paste, sep="_"))
withinCombos <- as.vector(outer(withinCombos, withinLevels3, paste, sep="_"))
wiv <- paste(withinCombos, outcomeName, sep="_")


participantAmount = nrow(Data)
participantCases = length(wiv)
variableAmount = length(wiv)
variableCases = 1



# simple normality checks per condition (i.e., outcome for each factor)
i = 1 # !! Need to manually adjust per factor index. start with 1
outcome = getColumnByName(Data, wiv[i])

par(mfrow=c(2,2))
qqnorm(outcome)			#normal QQ plot (should be straight diagonal for normal)
hist(outcome,breaks=length(outcome))	#histogram
shapiro.test(outcome)
ks.test(outcome, "pnorm", mean=mean(outcome), sd=sd(outcome))
#Don't worry about ties warning\n"
#


#install.packages("reshape")
library("reshape")

#Convert wide shaped data to a long one
longData<-melt(Data, id.vars=participantName, measure.vars=c(wiv))

# Set appropriate names for participant, variable, value
names(longData)<-c(participantName, "combination", outcomeName)

longData$factor1 = 0
for (item in withinLevels1){
  longData$factor1[grep(item, longData$combination)] = item
}

longData$factor2 = 0
for (item in withinLevels2){
  longData$factor2[grep(item, longData$combination)] = item
}

longData$factor3 = 0
for (item in withinLevels3){
  longData$factor3[grep(item, longData$combination)] = item
}

# rename factors to call them what we want
names(longData)<-c(names(longData)[1], names(longData)[2], names(longData)[3], independentVariableName1, independentVariableName2, independentVariableName3 )

# cast independent variable categories to factor (not string)
longData[, participantName] = as.factor(longData[, participantName])
longData[, independentVariableName1] = as.factor(longData[, independentVariableName1])
longData[, independentVariableName2] = as.factor(longData[, independentVariableName2])
longData[, independentVariableName3] = as.factor(longData[, independentVariableName3])


# need data copy with hard coded factor names for ezANOVA...hacky
longDataCopy = longData
names(longDataCopy)<-c("Participant_ID", "combination", "dvValue", "ivFactor1", "ivFactor2", "ivFactor3")


#install.packages("ez")
library(ez)

statsSummaryCombinations = ezStats(data = longDataCopy,
                 dv = dvValue,
                 wid = Participant_ID,
                 within = .(ivFactor1, ivFactor2, ivFactor3))

statsSummaryFactor1 = ezStats(data = longDataCopy,
                 dv = dvValue,
                 wid = Participant_ID,
                 within = .(ivFactor1))

statsSummaryFactor2 = ezStats(data = longDataCopy,
                 dv = dvValue,
                 wid = Participant_ID,
                 within = .(ivFactor2))

statsSummaryFactor3 = ezStats(data = longDataCopy,
                 dv = dvValue,
                 wid = Participant_ID,
                 within = .(ivFactor3))

#Means and standard deviations for iv1
paste("Summary for ", independentVariableName1)
statsSummaryFactor1

#Means and standard deviations for iv2
paste("Summary for ", independentVariableName2)
statsSummaryFactor2

#Means and standard deviations for iv3
paste("Summary for ", independentVariableName3)
statsSummaryFactor3

#Means and standard deviations for all conditions (combinations)
#paste("Summary for all combinations/conditions")
#statsSummaryCombinations

anova_output = ezANOVA(data = longDataCopy,
                 dv = dvValue,
                 wid = Participant_ID,
                 within = .(ivFactor1, ivFactor2, ivFactor3),
                 detailed = TRUE,
                 type = 3)

# ANOVA RESULTS
paste("ivFactor1 = ", independentVariableName1)
paste("ivFactor2 = ", independentVariableName2)
paste("ivFactor3 = ", independentVariableName3)
anova_output

## Posthoc Tests
## only report these for factors that had significant differences from the above ANOVA.
## two types of posthoc tests are below:
## (1) t tests with bonferroni correction and (2) Tukey tests
## be consistent with posthoc choice, and use it for the appropriate factor (factor1, factor2, or both depending on significant effects)


 # posthoc test: bonferroni t test for factor1
 pairwise.t.test(longDataCopy$dvValue,
                longDataCopy$ivFactor1,
                paired = TRUE,
                p.adjust.method = "bonferroni")

 # posthoc test: bonferroni t test for factor2
 pairwise.t.test(longDataCopy$dvValue,
                longDataCopy$ivFactor2,
                paired = TRUE,
                p.adjust.method = "bonferroni")

 # posthoc test: bonferroni t test for factor3
 pairwise.t.test(longDataCopy$dvValue,
                longDataCopy$ivFactor3,
                paired = TRUE,
                p.adjust.method = "bonferroni")

## posthoc test: Tukey
##first run as lme
#install.packages("nlme")
 library(nlme)
 lmeOutput = lme(dvValue ~ ivFactor1 * ivFactor2 * ivFactor3,
              random = ~1|Participant_ID,
              data = longDataCopy,
              method = "ML")

 ##then run the tukey on lme output
 #install.packages("multcomp")
 library(multcomp)
 tukey1 = glht(lmeOutput, linfct = mcp(ivFactor1= "Tukey", interaction_average=TRUE))
 summary(tukey1)
 tukey2 = glht(lmeOutput, linfct = mcp(ivFactor2= "Tukey", interaction_average=TRUE))
 summary(tukey2)
 tukey3 = glht(lmeOutput, linfct = mcp(ivFactor3= "Tukey", interaction_average=TRUE))
 summary(tukey3)

### below is making plots

# only works if iv3 has 2 levels

#install.packages("ggplot2")
library("ggplot2")
library("grid")

# plyr used to adjust factor names to custom values for plots
#install.packages("plyr")
library(plyr)

# grab only the things with first level of iv3
plotCopy1 = longData[!(longData[independentVariableName3]==withinLevels3[2]),]
iv1 = plotCopy1[[independentVariableName1]]
iv2 = mapvalues(plotCopy1[[independentVariableName2]], from=withinLevels2, to=levelLabels2)
iv3 = mapvalues(plotCopy1[[independentVariableName3]], from=withinLevels3, to=levelLabels3)
dv1 = plotCopy1[[outcomeName]]

# BOX PLOT!
plot1 <- ggplot(plotCopy1, aes(y=dv1, x=mapvalues(iv1, from=withinLevels1, to=levelLabels1), fill=iv2)) +
   	geom_boxplot(outlier.size=2, lwd=1.0) +
   	coord_cartesian(ylim=c(yMin, yMax)) +
   	ggtitle(paste(chartTitle, levelLabels3[1], sep=": ")) +
   	scale_y_continuous(breaks=seq(yMin, yMax, yInterval), expand=c(0, 0)) +   labs(x=independentVariableName1, y=yLabel) +
   		theme(legend.title=element_blank(),
	   	legend.key.size=unit(1, "cm"),
	   	legend.text=element_text(size=16),
	   	plot.title=element_text(size=20, face="bold", hjust=0.5),
	   	axis.title.x=element_blank(),		# Use to remove x axis label/title
       	axis.text.x=element_text(size=18), # x axis tick label size/font
       	axis.title.y=element_text(size=20, margin=margin(t=0, r=5, b=0, l=0)), #move xaxis label from x axis
       	axis.text.y=element_text(size=18) # y axis category label size/font

       ) #close theme


# grab only the things with second level of iv3
plotCopy2 = longData[!(longData[independentVariableName3]==withinLevels3[1]),]
	civ1 = plotCopy2[[independentVariableName1]]
	civ2 = mapvalues(plotCopy2[[independentVariableName2]], from=withinLevels2, to=levelLabels2)
	civ3 = mapvalues(plotCopy2[[independentVariableName3]], from=withinLevels3, to=levelLabels3)
	cdv1 = plotCopy2[[outcomeName]]

# BOX PLOT!
plot2 <- ggplot(plotCopy2, aes(y=cdv1, x=mapvalues(civ1, from=withinLevels1, to=levelLabels1), fill=civ2)) +
   	geom_boxplot(outlier.size=2, lwd=1.0) +
   	coord_cartesian(ylim=c(yMin, yMax)) +
   	ggtitle(paste(chartTitle, levelLabels3[2], sep=": ")) +
   	scale_y_continuous(breaks=seq(yMin, yMax, yInterval), expand=c(0, 0)) +   labs(x=independentVariableName1, y=yLabel) +
   		theme(legend.title=element_blank(),
	   	legend.key.size=unit(1, "cm"),
	   	legend.text=element_text(size=16),
	   	plot.title=element_text(size=20, face="bold", hjust=0.5),
	   	axis.title.x=element_blank(),		# Use to remove x axis label/title
       	axis.text.x=element_text(size=18), # x axis tick label size/font
       	axis.title.y=element_text(size=20, margin=margin(t=0, r=5, b=0, l=0)), #move xaxis label from x axis
       	axis.text.y=element_text(size=18) # y axis category label size/font

       ) #close theme

require(gridExtra)
grid.arrange(plot1, plot2, ncol=2)
g <- arrangeGrob(plot1, plot2, ncol=2)

# automatically save graph to file. requires the output directory specified in "saveFile" has already been created
ggsave(saveFile,width=20, height=6, g)
