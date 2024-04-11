# organism: Human
# {"type": "vertebrate", "id": 1, "name": "Homo sapiens (GRCh38/hg38) - Human"}
import requests
import pandas as pd
import sys
import argparse

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

def get_offtarget_list(target_dict):
    total_gene_list = []
    total_target_list = []
    chromosome_list = []
    sequence_list = []
    region_list = []
    strand_list = []
    position_list = []
    mismatch_list = []

    for gene_id, target_list in target_dict.items():
        for target_id in target_list:
            url = f"http://www.rgenome.net/cpf1-database/genes/{gene_id}/targets/{target_id}/offtargets/"
            response = requests.get(url)
            if str(response.status_code)[:2] == "20":
                data = response.json()
                for offtarget in data['offtargets']:
                    total_gene_list.append(gene_id)
                    total_target_list.append(target_id)
                    chromosome_list.append(offtarget['chromosome'])
                    sequence_list.append(offtarget['sequence'])
                    region_list.append(offtarget['region'])
                    strand_list.append(offtarget['strand'])
                    position_list.append(offtarget['position'])
                    mismatch_list.append(offtarget['mismatch_count'])
            else:
                print("Error: Failed to retrieve gene list in gene_id: {gene_id}")
    
    df = pd.DataFrame({
        'gene_id': total_gene_list,
        'target_id': total_target_list,
        'chromosome': chromosome_list,
        'sequence': sequence_list,
        'region': region_list,
        'strand': strand_list,
        'position': position_list,
        'mismatch_count': mismatch_list
    })

    return df
    

def __main__(num1, num2):
    start_page_num = num1
    end_page_num = num2
    gene_list = get_gene_list(1, start_page_num, end_page_num)
    target_dict = get_target_list(gene_list)
    offtarget_df = get_offtarget_list(target_dict)
    print(offtarget_df.head())
    offtarget_df.to_csv(f"offtarget_data_page{start_page_num}_{end_page_num}.csv", index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script that gather Cpf1-Data base on page number")
    parser.add_argument("--start", required=True, type=int)
    parser.add_argument("--end", required=True, type=int)
    args = parser.parse_args()

    num1 = args.start
    num2 = args.end

    __main__(num1, num2)

