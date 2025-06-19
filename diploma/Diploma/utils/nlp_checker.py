from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

tokenizer = AutoTokenizer.from_pretrained("mrm8488/bert-tiny-finetuned-fake-news-detection")
model = AutoModelForSequenceClassification.from_pretrained("mrm8488/bert-tiny-finetuned-fake-news-detection")

def predict_fake_news(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = F.softmax(outputs.logits, dim=1)
    real_prob = probs[0][1].item()  
    return real_prob  


