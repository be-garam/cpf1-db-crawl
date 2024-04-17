# organism: Human
# {"type": "vertebrate", "id": 1, "name": "Homo sapiens (GRCh38/hg38) - Human"}
import requests
import pandas as pd
import sys
import argparse

def get_gene_list(organism_id, start_page_num, end_page_num):
    gene_list = []
    gene_dict = {}
    for page_num in range(start_page_num, end_page_num+1):
        url = f"http://www.rgenome.net/cpf1-database/organisms/{organism_id}/genes/?page={page_num}"
        response = requests.get(url)
        if str(response.status_code)[:2] == "20":
            data = response.json()
            for gene in data['genes']:
                gene_list += str(gene["id"])
                gene_dict[gene["id"]] = [gene["symbol"], gene["ensembl_id"], gene["biotype"], gene["description"]]
        else:
            print(f"Error: Failed to retrieve gene list in page{page_num}")
    return gene_list, gene_dict

def __main__(num1, num2):
    start_page_num = num1
    end_page_num = num2
    organism =  "Homo sapiens (GRCh38/hg38) - Human"
    # organism id: 1, "Homo sapiens (GRCh38/hg38) - Human"
    gene_list, gene_dict = get_gene_list(1, start_page_num, end_page_num)
    df = pd.DataFrame.from_dict(gene_dict, orient='index', columns=['symbol', 'ensembl_id', 'biotype', 'description'])
    df.to_csv('gene_data.csv')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script that gather Cpf1-Data base on page number")
    parser.add_argument("--start", required=True, type=int)
    parser.add_argument("--end", required=True, type=int)
    args = parser.parse_args()

    num1 = args.start
    num2 = args.end

    __main__(num1, num2)