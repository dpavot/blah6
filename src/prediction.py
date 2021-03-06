import csv
import re


def get_fnu(curation_file, destination_file):
    """

    :param curation_file:
    :param destination_file:
    :return:
    """

    curation = open(curation_file, encoding = 'utf-8')
    curation_reader = csv.reader(curation, delimiter = ',')

    line_count = 0
    save_fnu = []

    for row in curation_reader:
        if line_count == 0:
            save_fnu.append(row[:10])
        else:
            try:  # to remove after completion
                if (row[10].lower() == 'false' and row[11].lower() == 'c') or (row[10].lower() == 'true' and row[11].lower() == 'i'):
                    save_fnu.append(row[:10])
            except IndexError:
                pass

        line_count += 1

    curation.close()

    destination = open(destination_file, 'w', encoding = 'utf-8')
    for annotation in save_fnu:
        elements = '\t'.join(annotation)
        destination.write(elements + '\n')

    destination.close()

    return len(save_fnu) - 1

#print(get_fnu('data/andre_incomplete_2171.csv', 'data/fnu_andre.tsv'))


def detect_false(corpus_file):
    """

    :param corpus_file:
    :return:
    """

    corpus = open(corpus_file, encoding='utf-8')
    corpus_reader = csv.reader(corpus, delimiter='\t')

    line_count = 0
    predictions = {}

    false_expressions = ['analyzed']

    for row in corpus_reader:
        if line_count == 0:
            predictions['header'] = '\t'.join(row)
        else:
            sentence = row[1]
            gene_entity = row[2]
            phenotype_entity = row[3]

            predict = 'U'

            for false_expression in false_expressions:
                patterns = ['(' + gene_entity + '|' + phenotype_entity + ')(.*?),(.*?),(.*?),(.*?)(' + gene_entity + '|' + phenotype_entity + ')',
                            'In' + '(.*?)' + false_expression + '(.*?)(' + gene_entity + '|' + phenotype_entity + ')(.*?)(' + gene_entity + '|' + phenotype_entity + ')']

                for pattern in patterns:
                    result = re.search(pattern, sentence)

                    if result:
                        predict = 'F'

            predictions['\t'.join(row)] = predict

        line_count += 1

    corpus.close()

    return predictions


def detect_negative(corpus_file):
    """

    :param corpus_file:
    :return:
    """

    corpus = open(corpus_file, encoding = 'utf-8')
    corpus_reader = csv.reader(corpus, delimiter = '\t')

    line_count = 0
    predictions = {}

    negative_expressions = ['are not', 'No', 'not associated', 'not be involved', 'dissociation']

    for row in corpus_reader:
        if line_count == 0:
            predictions['header'] = '\t'.join(row)
        else:
            sentence = row[1]
            gene_entity = row[2]
            phenotype_entity = row[3]

            predict = 'U'

            for negative_expression in negative_expressions:
                patterns = ['(' + gene_entity + '|' + phenotype_entity + ')(.*?)' + negative_expression + '(.*?)(' + gene_entity + '|' + phenotype_entity + ')',
                            '^' + negative_expression + '(.*?)(' + gene_entity + '|' + phenotype_entity + ')' + '(.*?)(' + gene_entity + '|' + phenotype_entity + ')']

                for pattern in patterns:
                    result = re.search(pattern, sentence)

                    if result:
                        predict = 'N'

            predictions['\t'.join(row)] = predict

        line_count += 1

    corpus.close()

    return predictions


def write_results_file(corpus_file, destination_file):
    """

    :param destination_file:
    :param corpus_file:
    """

    dict_negative = detect_negative(corpus_file)
    dict_false = detect_false(corpus_file)

    destination = open(destination_file, 'w', encoding = 'utf-8')
    destination.write(str(dict_negative['header'][:-1]) + '\tTYPE\n')

    for (k, v), (k2, v2) in zip(dict_negative.items(), dict_false.items()):

        if k == 'header':
            pass

        elif k == k2 and v == v2:
            destination.write(k + '\t' + v + '\n')

        elif k == k2 and v == 'N' and v2 == 'U':
            destination.write(k + '\t' + v + '\n')

        elif k == k2 and v2 == 'F' and v == 'U':
            destination.write(k + '\t' + v2 + '\n')

        elif k == k2 and v2 == 'F' and v == 'N':
            destination.write(k + '\t' + v2 + '\n')

    destination.close()

    return


def results_list(annotated_file):
    """

    :param annotated_file:
    :return:
    """

    annotations = open(annotated_file, 'r', encoding = 'utf-8')
    annotations_reader = csv.reader(annotations, delimiter = '\t')

    line_count = 0
    list_type = []

    for row in annotations_reader:
        if line_count == 0:
            pass
        else:
            list_type.append(row[10])

        line_count += 1

    annotations.close()

    return list_type


def precision(tp, fp):
    """

    :param tp:
    :param fp:
    :return:
    """

    return tp/(tp+fp)


def recall(tp, fn):
    """

    :param tp:
    :param fn:
    :return:
    """

    return tp / (tp + fn)


def f_measure(p, r):
    """

    :param p:
    :param r:
    :return:
    """

    print(p)
    print(r)
    print(2*((p*r)/(p+r)))
    return 2*((p*r)/(p+r))


def metrics(gold_standard_file, predictions_file):
    """

    :param gold_standard_file:
    :param predictions_file:
    :return:
    """

    list_gold_standard = results_list(gold_standard_file)
    list_predictions = results_list(predictions_file)

    true_count = 0
    false_count = 0

    tp_f_count = 0
    tp_n_count = 0
    tp_u_count = 0

    fp_f_count = 0
    fp_n_count = 0
    fp_u_count = 0

    fn_f_count = 0
    fn_n_count = 0
    fn_u_count = 0

    all_f_count = 0
    all_n_count = 0
    all_u_count = 0

    for i in range(len(list_gold_standard)):
        if list_gold_standard[i] == list_predictions[i]:
            if list_gold_standard[i] == 'F':
                tp_f_count += 1
            elif list_gold_standard[i] == 'N':
                tp_n_count += 1
            elif list_gold_standard[i] == 'U':
                tp_u_count += 1

            true_count += 1

        else:
            if list_predictions[i] == 'F':
                fp_f_count += 1
            elif list_gold_standard[i] == 'F':
                fn_f_count += 1

            if list_predictions[i] == 'N':
                fp_n_count += 1
            elif list_gold_standard[i] == 'N':
                fn_n_count += 1

            if list_predictions[i] == 'U':
                fp_u_count += 1
            elif list_gold_standard[i] == 'U':
                fn_u_count += 1

            false_count += 1

        if list_predictions[i] == 'F':
            all_f_count += 1

        elif list_predictions[i] == 'N':
            all_n_count += 1

        elif list_predictions[i] == 'U':
            all_u_count += 1

    f_f_score = f_measure(precision(tp_f_count, fp_f_count), recall(tp_f_count, fn_f_count))
    n_f_score = f_measure(precision(tp_n_count, fp_n_count), recall(tp_n_count, fn_n_count))
    u_f_score = f_measure(precision(tp_u_count, fp_u_count), recall(tp_u_count, fn_u_count))

    weighted_f1 = (all_f_count * f_f_score + all_n_count * n_f_score + all_u_count * u_f_score) / (all_f_count + all_n_count + all_u_count)

    return true_count, false_count, weighted_f1


#### RUN ####

def main():
    """

    """

    write_results_file('data/fnu.tsv', 'data/fnu_predictions.tsv')
    print(metrics('data/fnu_gold_standard.tsv', 'data/fnu_predictions.tsv'))


if __name__ == '__main__':
    main()