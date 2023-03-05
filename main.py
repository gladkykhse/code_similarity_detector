import os
import json
import argparse
from typing import List
from pygments.lexers import guess_lexer_for_filename, guess_lexer
from pygments.token import Token
from pygments.util import ClassNotFound


parser = argparse.ArgumentParser()
parser.add_argument("--dir", default="NuGet.Client-dev", type=str, help="Path to the directory with code repositories")
parser.add_argument("--create_new", default=False, type=bool, help="True if you want to create new inverted index, false if you want to use the one you provided")
parser.add_argument("--filename", default="similar.cs", type=str, help="Name of the file to check similarity")
parser.add_argument("--text", default=None, type=str, help="Text for checking similarity")
parser.add_argument("--inverted_index_file", default="/app/config/inverted_index.json", type=str, help="File containing (or you want to save there) inverted index")
parser.add_argument("--index_file", default="/app/config/file_index.json", type=str, help="File containing (or you want to save there) indicies of files")


class InvertedIndex:
    def __init__(self) -> None:
        self._file_index = 1
        self._index_file = {}
        self._inverted_index = {}

    @property
    def index_file(self) -> dict:
        return self._index_file

    @property
    def inverted_index(self) -> dict:
        return self._inverted_index

    def _save_dict(self, dictionary: dict, dict_name: str) -> None:
        with open(dict_name, 'w') as file:
            json.dump(dictionary, file)

    def _load_dict(self, dict_name: str) -> dict:
        with open(dict_name) as file:
            data = json.load(file)
        return data


    def _create_index_files(self) -> None:
        '''
        Creating a map where key is an id of file and value is a path to this file
        '''
        for path, _, files in os.walk(args.dir):
            for file in files:
                file_path = os.path.join(path,file)
                self._index_file[self._file_index] = file_path
                self._file_index += 1

        if self._file_index == 1: raise RuntimeError("The directory is empty")

        self._save_dict(self._index_file, args.index_file)

    @staticmethod
    def tokenize_input(filename : str, code : str) -> List[str]:
        '''
        Getting the Token.Names of the given file
        '''
        tokens_list = []

        try:
            lexer = guess_lexer_for_filename(filename, code)
        except: return None
        try:
            tokens = lexer.get_tokens(code)
        except: return None
        for token, value in tokens:
            if token is Token.Name:
                tokens_list.append(value)

        return tokens_list


    def create_inverted_index(self, creating=True) -> None:
        '''
        Creating or loading an inverted index table: key is a token,
        value is a list of the id's of the documents containing this token
        '''
        if creating:
            self._create_index_files()
            for index in self._index_file:
                filename = self._index_file[index]
                with open(filename, "r") as file:
                    try:
                        code = file.read()
                    except: continue

                file_tokens = self.tokenize_input(filename, code)
                if file_tokens is not None:
                    for token in file_tokens:
                        if token in self._inverted_index:
                            if index != self._inverted_index[token][-1]:
                                self._inverted_index[token].append(index)
                        else:
                            self._inverted_index[token] = [index]
                else: continue

                self._save_dict(self._inverted_index, args.inverted_index_file)
        else:
            self._index_file = {int(key) : value for key, value in self._load_dict(args.index_file).items()}
            self._inverted_index = self._load_dict(args.inverted_index_file)




class FileSimilarity:
    def __init__(self, creating_inv_index=True) -> None:
        self.inv_index = InvertedIndex()
        self.inv_index.create_inverted_index(creating_inv_index)

    def check_similarity(self) -> str:
        '''
        Checking whether the given file is similar to another file in directory
        '''
        file_tokens = InvertedIndex.tokenize_input(args.filename, args.text)
        if file_tokens is None:
            return "Invalid input"
        file_tokens = list(dict.fromkeys(file_tokens))
        file_token_number = len(file_tokens)
        documents_with_tokens = {}
        for token in file_tokens:
            if token in self.inv_index.inverted_index:
                docs_containing_token = self.inv_index.inverted_index[token]
                for doc in docs_containing_token:
                    documents_with_tokens.setdefault(doc, 0)
                    documents_with_tokens[doc] += 1
        if not bool(documents_with_tokens):
            return "OK"
        greatest = max(documents_with_tokens, key=documents_with_tokens.get)
        if documents_with_tokens[greatest] / file_token_number >= 0.85:
            return self.inv_index.index_file[greatest]
        else:
            return "OK"



if __name__ == "__main__":
    args = parser.parse_args()
    similarity = FileSimilarity(args.create_new)
    print(similarity.check_similarity())

