if(!("limma" %in% installed.packages()[,"Package"])){
  if (!require("BiocManager", quietly = TRUE))
    install.packages("BiocManager")
  
  BiocManager::install("limma")
}


library("limma")
print('running R script')

expression_ <- read.csv("interview_question/r_scripts/tmp_data/expression.csv")
metadata <- read.csv("interview_question/r_scripts/tmp_data/metadata.csv")
expression<- expression_
design <- model.matrix(formula(~0+group), data = metadata)
row.names(expression) <- expression$feature_id
expression$feature_id <- NULL


contrast.matrix <- makeContrasts(groupGroup1-groupGroup2, groupGroup2-groupGroup3, groupGroup3-groupGroup1, levels=design)


fit <- lmFit(expression, design = design)
fit2 <- contrasts.fit(fit, contrast.matrix)
fit2 <- eBayes(fit2)

write.csv(topTable(fit2, number = Inf), file = 'interview_question/r_scripts/tmp_data/limma_res.csv')

print('finished R script')

