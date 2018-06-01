
# coding: utf-8

# imports
import utils
from utils import *
import pickle
import re
from sklearn.preprocessing import scale
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.mixture import GaussianMixture, BayesianGaussianMixture

seed = 42

# create questionnaire from given list of verbs and their arguments
# (see list of arguments in arguments.txt)


def questionnaire(domain, verbs):

    #     # download corpus
    #     with open('ruwac_lines.pickle', 'rb') as f:
    #         lines = pickle.load(f)
    #     sentences = split_to_sentences(lines)

    # download corpus
    with open('ruwac_sentences.pickle', 'rb') as f:
        sentences = pickle.load(f)

    # download W2V model
    with open('W2V_RNC.pickle', 'rb') as f:
        W2V = pickle.load(f)

    # get contexts
    verb_contexts = {}
    for verb in verbs:
        verb_contexts[verb] = contexts(
            word=verb, sentences=sentences, window=2)

    verb_sentences = {}
    for verb in verbs:
        verb_sentences[verb] = contexts(
            word=verb, sentences=sentences, window='sent')

    verb_indexes = verbs_indexes(verb_contexts)

    arguments_labels = ['object', 'subject', 'second compliment']

    # get subjects
    subjects = {}
    for i, verb in enumerate(verb_contexts):
        subjects[verb] = get_lexemes_by_morphology(sentences=verb_contexts[verb], pos=[
                                                   'N'], case=['n'], syntactic=['предик'], indexes=verb_indexes[verb])

    # get objects
    objects = {}
    for i, verb in enumerate(verb_contexts):
        objects[verb] = get_lexemes_by_morphology(sentences=verb_contexts[verb], pos=[
                                                  'N'], case=['a'], syntactic=['1-компл'], indexes=verb_indexes[verb])

    # get second compliments
    compls2 = {}
    for i, verb in enumerate(verb_contexts):
        compls2[verb] = get_lexemes_by_morphology(sentences=verb_sentences[verb], pos=[
                                                  'N'], syntactic=['2-компл'], indexes=verb_indexes[verb])

    # get second compliments as Adposition Phrases
    PPs = {}
    for i, verb in enumerate(verb_contexts):
        PPs[verb] = get_preposition_phrases(
            verb_sentences[verb], indexes=verb_indexes[verb])
    PPs_collocations = {verb: [PP[0][0]+' '+PP[1][0] for PP in PPs[verb]]
                        for verb in PPs for PP in PPs[verb]}

    arguments = [objects, subjects, compls2]

    # write them down to .csv file
    write_arguments_to_csv(objects, '{}_objects'.format(domain))
    write_arguments_to_csv(subjects, '{}_subjects'.format(domain))
    write_arguments_to_csv(compls2, '{}_2compliments'.format(domain))
    write_arguments_to_csv(PPs_collocations, '{}_PPs'.format(domain))

    # contexts into math object
    final = {}
    for i, arg in enumerate(arguments):
 #       print(i, arg, arguments_labels[i])
        arg_vectors, arg_model = nouns_to_vectors(arg, W2V)

        X = arg_vectors
        X_scaled = scale(arg_vectors)
        X_scaled_pca = PCA(n_components=50).fit_transform(X_scaled)
        tsne = TSNE(n_components=2,
                    perplexity=5,  # 5-50
                    learning_rate=100  # 10-1000
                    )
        X_scaled_pca_tsne = tsne.fit_transform(X_scaled_pca)

        k = int(len(arg_model)/10)
        model = GaussianMixture(n_components=k, random_state=seed)
        model.fit(X_scaled_pca_tsne)
        clusters_labels = model.predict(X_scaled_pca_tsne)

        most_probable = {}
        for j in range(k):
            most_probable[j] = np.array(arg_model)[model.predict_proba(
                X_scaled_pca_tsne)[:, j].argsort()[-2:][::-1]]
    
        final[arguments_labels[i]] = [q[0] for q in most_probable.values()] + [q[1] for q in most_probable.values()]

    # save results
    with open('{}_contexts.pickle'.format(domain), 'wb') as f:
        pickle.dump(verb_contexts, f)
    with open('{}_sentences.pickle'.format(domain), 'wb') as f:
        pickle.dump(verb_sentences, f)
    with open('{}_objects.pickle'.format(domain), 'wb') as f:
        pickle.dump(objects, f)
    with open('{}_subjects.pickle'.format(domain), 'wb') as f:
        pickle.dump(subjects, f)
    with open('{}_2compls.pickle'.format(domain), 'wb') as f:
        pickle.dump(compls2, f)
    with open('{}_PPs.pickle'.format(domain), 'wb') as f:
        pickle.dump(PPs, f)
    write_arguments_to_csv(final, '{}_output'.format(domain))

