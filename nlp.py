import torch
import torch.nn.functional as F
from transformers import pipeline
from transformers import AutoTokenizer, AutoModel


class NLPProcessor:
    def __init__(self):
        pass
    
    #Mean Pooling - Take attention mask into account for correct averaging
    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0] #First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    
    def cosine_similarity(self, embeddings: torch.Tensor):
        '''
        Computes cosine similarity between first row and the rest
        '''
        scores = []
        for emb in embeddings:
            scores.append(
                F.cosine_similarity(emb[0].unsqueeze(0), emb.unsqueeze(0)))
        return scores

    def similarity(self, text_list):
        # Load model 
        tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
        model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
        # Tokenize sentences
        encoded_input = tokenizer(text_list,
                                  padding=True,
                                  truncation=True,
                                  return_tensors='pt')
        # Compute token embeddings
        with torch.no_grad():
            model_output = model(**encoded_input)

        # Perform pooling
        sentence_embeddings = self.mean_pooling(model_output, encoded_input['attention_mask'])

        # Normalize embeddings
        sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)
        return sentence_embeddings


    def sentiment(self, text):
        sentitment_classifier = pipeline("text-classification",
                                         model="j-hartmann/emotion-english-distilroberta-base",
                                         return_all_scores=True)

        return sentitment_classifier(text)
    
        
    
