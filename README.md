# BLAH6: Annotation of Human Phenotype-Gene Relations - Identification of Negative Relations

![alt text](https://github.com/dpavot/blah6/blob/master/proposal.png)

Accessible negative results are relevant for researchers and clinicians not only to limit their search space but also to prevent the costly re-exploration of the hypothesis. However, most biomedical relation extraction data sets do not seek to distinguish between a false and a negative relation. A false relation should express a context where the entities are not related. In contrast, a negative relation should express a context where there is an affirmation of no association between the two entities. Furthermore, when we are dealing with data sets created using distant supervision techniques, we also have some false negative relations that constitute undocumented/unknown relations. Unknown relations are good examples to further exploration by researchers and clinicians. We propose to improve the distinction between these two concepts, by revising the false relations of the PGR corpus with regular expressions. 

## Day 05/02/2020
 
The first step was to create a sub-set of 127 false annotations within the PGR corpus. This sub-set was manually annotated to make the distinction between false (F), negative (N), and unknown (U) relations. 

#### Example of a false relation (PMID 29307790):

- *The aCGH analysis revealed a pathogenic CNV in the 14q11.2 region, while targeted exome sequencing revealed pathogenic variants in genes associated with intellectual disability (HUWE1, **GRIN1**), including a gene coding for **mandibulofacial dysostosis** with microcephaly (EFTUD2).*

#### Example of a negative relation (PMID 28944914):

- *The present findings did not identify copy number variation and mutations in **EDA**; therefore, excluding the possibility of EDA‑initiated **ectodermal dysplasia** syndrome.*

#### Example of a unknown relation (PMID 26715604):

- *Here we discuss 'congenital disorders of autophagy' as an emerging subclass of inborn errors of metabolism by using the examples of six recently identified monogenic diseases: EPG5-related Vici syndrome, beta-propeller protein-associated neurodegeneration due to mutations in WDR45, **SNX14**-associated autosomal-recessive cerebellar ataxia and **intellectual disability** syndrome, and three forms of hereditary spastic paraplegia, SPG11, SPG15 and SPG49 caused by SPG11, ZFYVE26 and TECPR2 mutations, respectively.*

The manual annotation allowed for the assessment of common patterns for the false and negative types of relations:

- False relations are often enumerations or an explanation of protocol that does not imply any type of relation. 
- Negative relations are more regular, with words that imply negation of association, such as *non*, *no*, and *not* combined with *associated*, *involved*, and *dissociation*.

## Day 06/02/2020
 
Application of small sub set of regular expressions to catch false and negative examples that follow the previously mentioned patterns had some interesting results.

Test against the gold standard data set shows 53/127 (41.73%) detections.

## Day 07/02/2020

Application of a classifier without any tuning (neural network model): 23.08% accuracy.

Initial exploration of the identification of negative relations between human phenotypes and genes was partially successful. More manual work, building regular expressions, should boost these preliminary results.

#### Future Work:

- Evaluate on the entire PGR corpus.
- Application to other data sets. Negative relations in manually annotated data sets should be easier to detect since the unknown relations would be present. 
