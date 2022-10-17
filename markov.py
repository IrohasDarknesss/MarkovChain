import os
import sqlite3
import random
from chain_to_db import Nijigasaki

#文章生成クラス
class Markov(object): 
    
    def __init__(self, n=10):
        #初期化メソッド
        self.n = n

    def generate(self):
        #テキスト生成関数
        #DBが存在しない場合、例外を返す
        if not os.path.exists(Nijigasaki.DB_PATH):
            raise IOError('DB_PATH is not exist')

        #DBを開く
        connect = sqlite3.connect(Nijigasaki.DB_PATH)
        connect.row_factory = sqlite3.Row

        #生成される文章
        gen_txt = ""

        #指定の数だけ作成する
        for i in range(self.n):
            text = self._generate_sentence(connect)
            gen_txt += text

        #DBを閉じる
        connect.close()

        return gen_txt

    def _generate_sentence(self, connect):
        #ランダムに文章生成
        # 生成文章のリスト
        morphemes = []

        # はじまりを取得
        first_triplet = self._get_first_triplet(connect)
        morphemes.append(first_triplet[1])
        morphemes.append(first_triplet[2])

        # 文章を紡いでいく
        while morphemes[-1] != Nijigasaki.END:
            prefix1 = morphemes[-2]
            prefix2 = morphemes[-1]
            triplet = self._get_triplet(connect, prefix1, prefix2)
            morphemes.append(triplet[2])

        # 連結
        result = "".join(morphemes[:-1])

        return result
        
    def _get_chain_from_DB(self, connect, prefixes):
        #チェーンの情報をDBから取得
        #ベースとなるSQL
        sql = "select prefix1, prefix2, suffix, freq from nijigasaki where prefix1 = ?"

        if len(prefixes) == 2:
            sql += "and prefix2 = ?"

        #結果
        result = []

        #DBから取得
        cur = connect.execute(sql, prefixes)
        for row in cur:
            result.append(dict(row))

        return result

    def _get_first_triplet(self, connect):
        #文章のはじまりの3つ組をランダムに取得する

        # BEGINをprefix1としてチェーンを取得
        prefixes = (Nijigasaki.BEGIN,)

        # チェーン情報を取得
        chains = self._get_chain_from_DB(connect, prefixes)

        # 取得したチェーンから、確率的に1つ選ぶ
        triplet = self._get_probable_triplet(chains)

        return (triplet["prefix1"], triplet["prefix2"], triplet["suffix"])

    def _get_triplet(self, connect, prefix1, prefix2):
        #prefix1とprefix2からランダムにsuffixを取得
        #始点をprefix1にしてチェーンを取得
        prefixes = (prefix1, prefix2)

        #チェーンの情報を取得
        chains = self._get_chain_from_DB(connect, prefixes)

        #取得したチェーンから確率的に一つ選ぶ
        triplet = self._get_probable_triplet(chains)

        return(triplet["prefix1"], triplet["prefix2"], triplet["suffix"])

    def _get_probable_triplet(self, chains):
        #チェーンの中から確率的に一つ返す
        #確率配列
        probability = []

        #確率に合うようにインデックスに入れる
        for (index, chain) in enumerate(chains):
            for j in range (chain["freq"]):
                probability.append(index)

        #ランダムに一つ選ぶ
        chain_index = random.choice(probability)

        return chains[chain_index]

if __name__ == '__main__':
    generator = Markov()
    print(generator.generate())