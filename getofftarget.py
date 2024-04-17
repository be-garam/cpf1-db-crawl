# organism: Human
# {"type": "vertebrate", "id": 1, "name": "Homo sapiens (GRCh38/hg38) - Human"}
import requests
import pandas as pd
import sys
import argparse

def make_input(gene_id, gene_ansembl_id, target_dict):
    with open(f'{gene_ansembl_id}_input.txt', 'w') as file:
        organism =  "Homo sapiens (GRCh38/hg38) - Human"
        
        #check this
        path = f"path of {organism}"
        
        file.write(f"{path}\n")
        for id, value in target_dict.items(): 
            target = value[0]
            mistmatch_count_list = value[1:]
            for i in range(len(mistmatch_count_list)):
                if mistmatch_count_list[i] != 0:
                    file.write(f"{target} {i}\n")

def make_output(gene_ansembl_id, offtarget_df):
    with open(f'{gene_ansembl_id}_output.txt', 'w') as file:
        for row in offtarget_df.itertuples(index=False):
            file.write(' '.join(map(str, row)) + '\n')
    

def get_target_list(gene_id):
    target_dict = {}
    url = f"http://www.rgenome.net/cpf1-database/genes/{gene_id}/targets/"
    response = requests.get(url)
    if str(response.status_code)[:2] == "20":
        data = response.json()
        for target in data['targets']:
            target_dict[target["id"]] = [target["sequence"]] + target["offtarget_counts"]
    else:
        print(f"Error: Failed to retrieve gene list in gene_id: {gene_id}")
    return target_dict

def get_offtarget_list(gene_id, target_dict):
    total_gene_list = []
    total_target_list = []
    chromosome_list = []
    sequence_list = []
    region_list = []
    strand_list = []
    position_list = []
    mismatch_list = []

    for target_id in target_dict.keys():
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
    

def __main__(gene_id):
    df = pd.read_csv('gene_data.csv')
    df.rename(columns={"Unnamed: 0": "id"}, inplace=True)
    # print(df.head())
    gene_ansembl_id = df.loc[df['id'] == gene_id]["ensembl_id"].values[0]
    if gene_ansembl_id.empty:
        print("Error: Invalid gene_id")
        sys.exit(1)
    
    target_dict = get_target_list(gene_id)
    # print(target_dict)

    make_input(gene_id, gene_ansembl_id, target_dict)

    offtarget_df = get_offtarget_list(gene_id, target_dict)
    print(offtarget_df.head())
    offtarget_df.to_csv(f"{gene_ansembl_id}_output.csv", index=False)
    make_output(gene_ansembl_id, offtarget_df)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script that gather Cpf1-Data base on page number")
    parser.add_argument("--gene", required=True, type=int)
    # parser.add_argument("--mismatch", required=False, type=int)
    args = parser.parse_args()

    gene_id = args.gene
    # mismatch = args.mismatch

    # thining about using gene_data.csv is essential in this step
    # df = pd.read_csv('gene_data.csv')
    # #find gene_id row from gene_data.csv
    # gene_id = df.loc[df['gene_id'] == gene_id]

    # if gene_id.empty:
    #     print("Error: Invalid gene_id")
    #     sys.exit(1)

    # if mismatch > 2:
    #     print("Error: Mismatch value is too big")
    #     sys.exit(1)

    __main__(gene_id)

