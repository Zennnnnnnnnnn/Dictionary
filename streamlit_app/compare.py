import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel
import torch

# Hàm để lấy embeddings từ mô hình GTE-Large
def get_embeddings(texts):
    tokenizer = AutoTokenizer.from_pretrained("thenlper/gte-large")
    model = AutoModel.from_pretrained("thenlper/gte-large")

    # Tokenize the input texts
    batch_dict = tokenizer(texts, max_length=512, padding=True, truncation=True, return_tensors='pt')
    
    with torch.no_grad():
        outputs = model(**batch_dict)
    
    # Average pooling
    last_hidden_states = outputs.last_hidden_state
    attention_mask = batch_dict['attention_mask']
    embeddings = average_pool(last_hidden_states, attention_mask)
    
    # Normalize embeddings
    embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
    
    return embeddings.numpy()

# Hàm để thực hiện average pooling trên các embeddings
def average_pool(last_hidden_states: torch.Tensor,
                 attention_mask: torch.Tensor) -> torch.Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]

'''
# Hàm để tìm cặp mô tả có độ tương đồng cao
def find_high_similarity_pairs(list1, list2, threshold=0.83):
    # Trích xuất Description từ từng đối tượng trong danh sách `list1` và `list2`
    descriptions1 = [item.get('Description', '') for item in list1]
    descriptions2 = [item.get('Description', '') for item in list2]

    if not descriptions1 or not descriptions2:
        raise ValueError("One of the description lists is empty.")

    # Lấy embeddings cho các mô tả trong cả hai danh sách
    embeddings1 = get_embeddings(descriptions1)
    embeddings2 = get_embeddings(descriptions2)

    if embeddings1.size == 0 or embeddings2.size == 0:
        raise ValueError("One of the embedding arrays is empty.")

    # Kiểm tra xem kích thước của các embeddings có khớp không
    if embeddings1.shape[1] != embeddings2.shape[1]:
        raise ValueError("Feature dimensions of embeddings do not match.")

    # Tính toán ma trận độ tương đồng giữa các embeddings
    try:
        similarities = cosine_similarity(embeddings1, embeddings2)
    except ValueError as e:
        raise ValueError(f"Error calculating cosine similarity: {e}")

    # In ma trận độ tương đồng với các giá trị > threshold
    filtered_similarities = np.where(similarities > threshold, similarities, 0)

    # Khởi tạo danh sách lưu trữ các cặp tương đồng cao
    pairs = []

    # Tạo hai tập hợp để theo dõi các chỉ số đã được ghép cặp
    matched1 = set()
    matched2 = set()

    # Duyệt qua từng hàng trong ma trận độ tương đồng
    for i, row in enumerate(similarities):
        # Duyệt qua từng cột trong hàng hiện tại
        for j, similarity in enumerate(row):
            # Kiểm tra nếu độ tương đồng lớn hơn ngưỡng và cả hai mô tả chưa được ghép cặp
            if similarity > threshold and i not in matched1 and j not in matched2:
                # Thêm các chỉ số vào các tập hợp đã được ghép cặp
                matched1.add(i)
                matched2.add(j)
                # Thêm cặp vào danh sách các cặp tương đồng cao
                pairs.append({
                    'Index_List1': i,
                    'Index_List2': j,
                    'Similarity': similarity
                })
                # In ra các cặp có độ tương đồng cao nhất
                print(f"Added pair: Index_List1={i}, Index_List2={j}, Similarity={similarity}")

    return pairs    # Trả về danh sách các cặp mô tả có độ tương đồng cao
'''
def find_high_similarity_pairs(list1, list2, threshold=0.83):
    # Ensure both lists are not empty
    if not list1 or not list2:
        raise ValueError("One or both of the description lists are empty.")
    
    # Extract descriptions and word types from both lists
    descriptions1 = {item.get('Description', ''): item.get('Word_type', '') for item in list1}
    descriptions2 = {item.get('Description', ''): item.get('Word_type', '') for item in list2}
    
    # Ensure descriptions are not empty
    if not descriptions1 or not descriptions2:
        raise ValueError("One or both of the description lists contain no descriptions.")
    
    # Create a dictionary to map word types to descriptions
    word_type_to_descriptions1 = {}
    word_type_to_descriptions2 = {}
    
    for desc, word_type in descriptions1.items():
        if word_type not in word_type_to_descriptions1:
            word_type_to_descriptions1[word_type] = []
        word_type_to_descriptions1[word_type].append(desc)
    
    for desc, word_type in descriptions2.items():
        if word_type not in word_type_to_descriptions2:
            word_type_to_descriptions2[word_type] = []
        word_type_to_descriptions2[word_type].append(desc)
    
    # Initialize list for storing high similarity pairs
    pairs = []
    
    # Iterate through common word types
    common_word_types = set(word_type_to_descriptions1.keys()).intersection(word_type_to_descriptions2.keys())
    
    for word_type in common_word_types:
        descriptions1_for_type = word_type_to_descriptions1[word_type]
        descriptions2_for_type = word_type_to_descriptions2[word_type]
        
        print(f"Comparing descriptions with word type '{word_type}':")
        print("Descriptions from list1:", descriptions1_for_type)
        print("Descriptions from list2:", descriptions2_for_type)
        
        # Get embeddings for both sets of descriptions
        embeddings1 = get_embeddings(descriptions1_for_type)
        embeddings2 = get_embeddings(descriptions2_for_type)
        
        # Print embeddings for debugging
        print("Embeddings from list1:", embeddings1)
        print("Embeddings from list2:", embeddings2)
        
        # Ensure embeddings are not empty and dimensions match
        if embeddings1.size == 0 or embeddings2.size == 0:
            raise ValueError("One of the embedding arrays is empty.")
        if embeddings1.shape[1] != embeddings2.shape[1]:
            raise ValueError("Feature dimensions of embeddings do not match.")
        
        # Calculate cosine similarity between the embeddings
        try:
            similarities = cosine_similarity(embeddings1, embeddings2)
        except ValueError as e:
            raise ValueError(f"Error calculating cosine similarity: {e}")
        
        # Print similarity matrix for debugging
        print("Similarity matrix:", similarities)
        
        # Filter similarities based on the threshold
        filtered_similarities = np.where(similarities > threshold, similarities, 0)
        print("Filtered similarities (threshold applied):", filtered_similarities)
        
        # Track matched indices
        matched1 = set()
        matched2 = set()
        
        # Create a list of all similarities with their indices
        similarity_pairs = []
        for i, row in enumerate(similarities):
            for j, similarity in enumerate(row):
                if similarity > threshold:
                    similarity_pairs.append((i, j, similarity))
        
        # Sort pairs by similarity in descending order
        similarity_pairs.sort(key=lambda x: x[2], reverse=True)
        
        # Match descriptions based on highest similarity
        for i, j, similarity in similarity_pairs:
            if i not in matched1 and j not in matched2:
                matched1.add(i)
                matched2.add(j)
                pairs.append({
                    'Index_List1': i,
                    'Index_List2': j,
                    'Similarity': similarity,
                    'Word_Type': word_type
                })
                print(f"Added pair: Index_List1={i}, Index_List2={j}, Similarity={similarity}, Word_Type={word_type}")
    
    return pairs
