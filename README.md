# Refinement methods on CXR report generation model
This is an extended research on [Generating Radiology Reports via Memory-driven Transformer](https://arxiv.org/pdf/2010.16056.pdf) at EMNLP-2020.
### Our refinement methods
![image](https://hackmd.io/_uploads/S1gEnN-Fp.png)
### Our results
![image](https://hackmd.io/_uploads/BJYfnVbY6.png)
### How to use?
1. Download the datasets [iu_xray](https://drive.google.com/file/d/1I2NsXZx3BHNo22DOlDmhv6L5P_JsXoF_/view?usp=drive_link) and [mimic_cxr](https://drive.google.com/file/d/1KMO27Nu6zqxqV2r6RWHAyycIPI3px1sg/view?usp=drive_link).
2. Put them into the folder `R2Gen/data`.
3. Run `python main.py`.
### Our arguments
* You can modify our arguments in `R2Gen/main.py`.
* For the argument **data_src**, there are two valid input values:
    * **iu_xray**: This is the default dataset.
    * **standardized_iu_xray**: The program will preprocess the default dataset "iu_xray" using UMHF and put the results into the folder `R2Gen/data/standardized_iu_xray`.
* For the argument **whether_to_train**, there are two valid input values:
    * **True**: This is the default choice. The program will train "R2GenModel" and put the results into the folder `R2Gen/output/pth`.
    * **False**: Remember to download one of the pretrained models [model_iu_xray.pth](https://drive.google.com/file/d/12peL8cuV_3nOhdJZ9Aw_xaK9TBzf3Jmr/view?usp=drive_link) and [model_standardized_iu_xray.pth](https://drive.google.com/file/d/1vl8ZQ1qvVR5t-iGC1ZeCWRrBu_4ysWQG/view?usp=drive_link) according to the dataset you select and put it into the folder `R2Gen/output/pth`.
* For the argument **api_key**, there are two valid input values:
    * **empty**: This is the default choice.
    * **<your_api_key>**: Remember to replace it with your API key from OpenAI. The program will generate the refined reports using "TextEmbeddingModel".
### Input & output
* Input:
    * `R2Gen/data/iu_xray`
    * `R2Gen/data/mimic_cxr`
* Output:
    * `R2Gen/data/standardized_iu_xray`
    * `R2Gen/output/pth` is the checkpoint of the training result from "R2GenModel".
    * `R2Gen/output/r2gen_result` is the predictions from "R2GenModel".
    * `R2Gen/output/r2gen_score` is the evaluation metrics from "R2GenModel".
    * `R2Gen/output/text_embedding_result` is the predictions from "TextEmbeddingModel".
    * `R2Gen/output/text_embedding_score` is the evaluation metrics from "TextEmbeddingModel".
    * `R2Gen/output/union_result` is for analysis use.
* For more details, you can refer to [here](https://drive.google.com/drive/folders/1R9AiRrZMAYPk7dO11X-MIcXvTNqXlMfW?usp=drive_link).