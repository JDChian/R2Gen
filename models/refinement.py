import json
import openai
import numpy as np
import operator

class RefinementModel():
    def __init__(self, ann_path, data_path, api_key):
        self.ann_path = ann_path
        self.data_path = data_path
        self.api_key = api_key

        self.reference_sentences = []
        self.__load_reference_sentences()

        self.ground_truth_reports = {'train': [], 'val': [], 'test': []}
        self.target_reports = {'train': [], 'val': [], 'test': []}
        self.__load_data()

    def __load_reference_sentences(self):
        # input: self.ann_path
        # output: self.reference_sentences
        reference_reports = [
            "heart size and mediastinal contour are normal . pulmonary vascularity is normal . the right lung is clear . there is a <unk> <unk> left pleural effusion . no pneumothorax . limited right base <unk> density compatible with atelectasis . dextroscoliosis of the thoracic spine .",
            "no focal consolidation . no pneumothorax . no pleural effusions . heart size normal . cardio mediastinal silhouette is unremarkable ."
        ]
        for reference_report in reference_reports:
            self.reference_sentences += self.__report_to_sentences(reference_report)

    def __load_data(self):
        with open(self.data_path) as f:
            data = json.load(f)
        for mark in ['train', 'val', 'test']:
            self.ground_truth_reports[mark] = [item['ground_truth'] for item in data[mark]]
            self.target_reports[mark] = [item['report'] for item in data[mark]]

    def __report_to_sentences(self, report):
        sentences = report.split(' . ')
        sentences[-1] = sentences[-1].replace(' .', '')
        return sentences

    def __find_most_similar(self, sentence):
        # input: sentence, self.api_key
        # output: refined_sentence
        client = openai.OpenAI(
            api_key=self.api_key
        )
        ground_truths = self.reference_sentences
        ground_truths.append(sentence)
        resp = client.embeddings.create(
            input=ground_truths,
            model="text-embedding-ada-002"
        )
        embedding_vector = resp.data
        report_embedding = embedding_vector.pop()
        dots = list(map(lambda x:np.dot(report_embedding.embedding, x.embedding), embedding_vector))
        max_index, max_value = max(enumerate(dots), key=operator.itemgetter(1))
        refined_sentence = ground_truths[max_index]
        return refined_sentence

    def __sentences_to_report(self, sentences):
        report = ' . '.join(sentences)
        report += ' .'
        return report

    def refine(self):
        result = {'train': [], 'val': [], 'test': []}
        for mark in ['train', 'val', 'test']:
            refined_reports = []
            for target_report in self.target_reports[mark]:
                target_sentences = self.__report_to_sentences(target_report)
                refined_sentences = []
                for target_sentence in target_sentences:
                    refined_sentence = self.__find_most_similar(target_sentence)
                    refined_sentences.append(refined_sentence)
                refined_report = self.__sentences_to_report(refined_sentences)
                refined_reports.append(refined_report)
            result[mark] = [{'ground_truth': g, 'report': t, 'refined_report': r} for g, t, r in zip(self.ground_truth_reports[mark], self.target_reports[mark], refined_reports)]
        return result
