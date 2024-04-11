# organism: Human
# {"type": "vertebrate", "id": 1, "name": "Homo sapiens (GRCh38/hg38) - Human"}
import requests

def get_gene_list(organism_id):
    url = f"http://www.rgenome.net/cpf1-database/organisms/{organism_id}/genes/?page=1"
    response = requests.get(url)
    if str(response.status_code)[:2] == "20":
        data = response.json()
        gene_list = data['genes']
        return gene_list
    else:
        print("Error: Failed to retrieve gene list")
        return None

def get_target_list(gene_id):
    url = f"http://www.rgenome.net/cpf1-database/genes/{gene_id}/targets/"
    response = requests.get(url)
    if str(response.status_code)[:2] == "20":
        data = response.json()
        target_list = [i['id'] for i in data['targets']]
        return target_list
    else:
        print("Error: Failed to retrieve gene list")
        return None

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
    gene_list = get_gene_list(1)
    target_list = get_target_list(gene_list[0]['id'])
    offtarget_list = get_offtarget_list(gene_list[0]['id'], target_list[0])
    print(offtarget_list)

if __name__ == "__main__":
    __main__()

