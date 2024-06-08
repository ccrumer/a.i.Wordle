import numpy as np
from images import replicate_client

def get_image_embedding(input):
    output = replicate_client.run(
        "andreasjansson/clip-features:75b33f253f7714a281ad3e9b28f63e3232d583716ef6718f2e46641077ea040a",
        input=input
    )
    return output[0]['embedding']

def cosine_similarity(embedding1, embedding2):
    dot_product = np.dot(embedding1, embedding2)
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)
    similarity = dot_product / (norm1 * norm2)
    return similarity

def compare_images(image1, image2):
    embedding1 = get_image_embedding({"inputs": image1})
    embedding2 = get_image_embedding({"inputs": image2})
    return cosine_similarity(embedding1, embedding2)

def guess_quality(similarity_score):
    if similarity_score < 0.65:
        return "Bad Guess"
    elif 0.65 <= similarity_score < 0.80:
        return "Fair Guess"
    elif 0.80 <= similarity_score < 0.90:
        return "Good Guess"
    else:
        return "Excellent Guess"