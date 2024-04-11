# organism: Human
# {"type": "vertebrate", "id": 1, "name": "Homo sapiens (GRCh38/hg38) - Human"}
import requests
import pandas as pd

def get_gene_list(organism_id, start_page_num, end_page_num):
    gene_list = []
    for page_num in range(start_page_num, end_page_num+1):
        url = f"http://www.rgenome.net/cpf1-database/organisms/{organism_id}/genes/?page={page_num}"
        response = requests.get(url)
        if str(response.status_code)[:2] == "20":
            data = response.json()
            gene_list += [i['id'] for i in data['genes']]
        else:
            print(f"Error: Failed to retrieve gene list in page{page_num}")
    return gene_list

def get_target_list(gene_list):
    target_dict = {}
    for gene_id in gene_list:
        url = f"http://www.rgenome.net/cpf1-database/genes/{gene_id}/targets/"
        response = requests.get(url)
        if str(response.status_code)[:2] == "20":
            data = response.json()
            target_list = [i['id'] for i in data['targets']]
            # print(target_list)
            target_dict[gene_id] = target_list
        else:
            print(f"Error: Failed to retrieve gene list in gene_id: {gene_id}")
    return target_dict

def get_offtarget_list(gene_id, target_id):
    url = f"http://www.rgenome.net/cpf1-database/genes/{gene_id}/targets/{target_id}/offtargets/"
    # print(url)
    response = requests.get(url)
    # print(response)
    if str(response.status_code)[:2] == "20":
        data = response.json()
        # print(data)
        offtarget_list = data['offtargets']
        return offtarget_list
    else:
        print("Error: Failed to retrieve gene list")
        return None

def __main__():
    gene_list = get_gene_list(1, 1, 1)
    target_dict = get_target_list(gene_list)
    print(target_dict)
    # offtarget_list = get_offtarget_list(gene_list[0]['id'], target_list[0])
    # print(offtarget_list)

if __name__ == "__main__":
    __main__()

