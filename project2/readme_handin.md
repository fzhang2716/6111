* Names: 
      Ruineng Li : rl3315, Frank Zhang : hz2716

* List of Files:
      readme
      project2.py
      requirement.txt

* A clear description of how to run your program.
  * besides the packages installed in instruction here http://www.cs.columbia.edu/~gravano/cs6111/Proj2/ ,we need to install the following pacakages:
    * sudo pip3 install openai
    * sudo pip3 install tqdm
  * execute the python file by:
    * move project2.py into SpanBERT folder
    * go into SpanBERT folder and execute: python3 project2.py -spanbert AIzaSyDm0Wcp0OqqLiWypz0ijCRMjkHZ2mYisJs 2d6a0e6f605702952 < open-ai key> 2 0.7 "bill gates microsoft" 10

* Internal Design Description
  * webpage extraction
    * we extract only the paragraphs in each webpage by using BeautifulSoup, such that it guarantees the first 10000 characters contain as many relevant information as it can.
  * iteration information extraction
    * For each iteration, the extraction process follows this workflow: first **process texts** to extract all sentences and their corresponding entities, then we only obtain the **entities of the required type** contains and the corresponding sentences, then we **obtain pairs** that follow the required relation types and feed them to the **relation extraction model**. The details for the functions in bold will be illustrated below.
    * The extracted tuples are then ordered by their confidence score, if "-spanbert" specified. We then first check the number of extracted tuples, if this number exceeds k, then we directly output top-k tuples. If not, we go through a loop to get a new query, we first check if the query has been used before, then the else-clause returns a query with the highest confidence score to extract tuples of required types again. 

* Step 3 Illustration
  * 3.a-3.c
  * 3.d is defined in function **process_texts**, we first use the spacy model to extract properties from the text extracted from the given webpage. Then we use the "sents" and "ent" properties to obtain the split sentences and their corresponding entities. To obtain entities of the required types, and their corresponding sentences, we define another function  **process_required_entities** to get only entities with their labels within the required types and the corresponding sentences using "label_".
  * 3.e-3.f is defined in function **process_required_pairs** and **process_relations**. This step is different for two models. We first check the model by its class and then extraction the relations with different processes. This is illustrated separatedly below.
    * SpanBERT: For required_pairs, we use a dictionary to classify all entities from the previous steps by their types, and we leverage the two lists, which contain all possible subject options, and all possible object options, respectively, to compute all possible combinations of the elements in the two lists. Then we obtain all the extracted pairs and feed them to the SpanBERT model. We record all the relations and their confidence scores. Then, for each extracted relation, we first check its confidence score and then decide whether to add it into X, the set of all extracted tuples. We track a set X and a dictionary X_with_scores, separately. X_with_scores is updated when a new tuple is extracted, or the confidence score of an existing tuple is updated. (Note that we don't have to check the duplication since this is done by using the set structure. Same below.)
    * GPT3: We follow the implementation of the reference code, such that we directly loop the sentences which contain required entities, and feed each whole text to the completion function and get the extracted relations. We record all relations using the set X.

* Google Custom Search Engine JSON API Key and Engine ID:
      Google Custom Search Engine JSON API Key: AIzaSyDm0Wcp0OqqLiWypz0ijCRMjkHZ2mYisJs
      Engine ID: 2d6a0e6f605702952
      
