# BLAH6: Annotation of Human Phenotype-Gene Relations - Identification of Negative Relations

Accessible negative results are relevant for researchers and clinicians not only to limit their search space but also to prevent the costly re-exploration of the hypothesis. However, most biomedical relation extraction data sets do not seek to distinguish between a false and a negative relation. A false relation should express a context where the entities are not related. In contrast, a negative relation should express a context where there is an affirmation of no association between the two entities. We propose to improve the distinction between these two concepts, by revising the false relations of the PGR corpus with regular expressions.
 
The first step was to create a sub-set of 84 false annotations within the PGR corpus. This sub-set was manually annotated to make the distinction between false and negative relations. 

#### Example of a false relation:

*The aCGH analysis revealed a pathogenic CNV in the 14q11.2 region, while targeted exome sequencing revealed pathogenic variants in genes associated with intellectual disability (HUWE1, **GRIN1**), including a gene coding for **mandibulofacial dysostosis** with microcephaly (EFTUD2).*

#### Example of a negative relation:

*The present findings did not identify copy number variation and mutations in **EDA**; therefore, excluding the possibility of EDA‑initiated **ectodermal dysplasia** syndrome.*

The manual annotation allowed for the assessment of common patterns in the two types of relations. False relations are often enumerations or an explanation of protocol that does not imply any type of relation. Negative relations are more regular, with words that imply negation of association, such as *non*, *no*, and *not* combined with *associated*, *involved*, and *dissociation*.

Application of regular expressions to catch false and negative examples that follow the previously mentioned patterns had some interesting results.
Test against the gold standard data set shows some improvements with 22 right detections.
