import csv


def get_sentence_pubmed_id(data_set_file, sentence):
    """

    :param data_set_file:
    :param sentence:
    :return:
    """

    data_set = open(data_set_file, encoding = 'utf-8')
    data_set_reader = csv.reader(data_set, delimiter = '\t')

    line_count = 0
    dict_id_sentence = {}

    for row in data_set_reader:
        if line_count == 0:
            pass
        else:
            dict_id_sentence[row[1]] = row[0]

        line_count += 1

    data_set.close()

    return dict_id_sentence[sentence.replace('<span>&#44;</span>', ',').replace('</b>', '').replace('<b>', '')]




#print(get_sentence_pubmed_id('data/data_set.tsv', 'Deficiency of the extracellular matrix molecule FRAS1<span>&#44;</span> normally expressed by the ureteric bud<span>&#44;</span> leads to <b>bilateral</b> renal agenesis in humans with Fraser syndrome and blebbed (Fras1(bl/bl)) <b>mice</b>.'))