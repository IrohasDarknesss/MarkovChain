# MarkovChain
マルコフ連鎖を用いた文章自動生成プログラム
Automatic sentence generation programme using Markov chains.

## バージョン(Version)
ver 0.1

## 使い方(How to use)

### 事前準備(Preparation)
まずは、事前準備として、テキストデータを集める。
集めたデータは何か新しくフォルダを作り、そこへ格納管理する。

次にDB作成のためのSQLファイルを作成する。
(特段オリジナルのアイデアがないなら、sqlファイルのコピペで大丈夫です。)

First, as a preliminary step, collect text data.
The collected data should be stored and managed in a new folder.

Next, create an SQL file for DB creation.
(If you don't have any original ideas, you can just copy and paste the sql file.)

### テキストデータの読み込み(Load Text data)
作成したデータセットを読み込ませ3つ組のデータを揃える。

The created dataset is read in and the three sets of data are aligned.

#### テキストを直に入れる場合(When the text is to be inserted directly.)
```
from chain_to_db import Nijigasaki
text = u"Put in Appropriately long sentences."
chain = Nijigasaki(text)
triplet_freqs = chain.make_triplet_freqs()
chain.save(triplet_freqs, True)
```

#### 複数データを読み込ませる場合(When multiple data are to be read in.)
```
(例:データセットがテキストファイルの場合)
(Ex: When the dataset is Text file)
from chain_to_db import Nijigasaki
import giob
    texts = glob.glob('./data/*.txt')
    for text in texts:
        with open(text, 'r', encoding='utf-8') as f:
            text = f.read()
            chain = Nijigasaki(text)
            triplet_freqs = chain.make_triplet_freqs()
            chain.save(triplet_freqs, True)
```

### 文章の生成(Text Genarate)
上記の準備が全てされていることが前提。
It's assumed that all the above preparations have been made.
```
from markov import Markov
generator = Markov()
print(generator.generate())
```


## 各ファイル(File names)
### README.md
このファイル
This File.

### chain_to_db.py
適当なテキストを与えて、そこから3つ組のチェーンを作成し、DBに保存するファイル。
A file from which given the appropriate text, a chain of triples is created, and stored in the DB.

### nijigasaki.sql
DB作成のためのSQLファイル。
SQL file for DB creation.

### markov.py
入力されたデータセットから実際にランダムで文章を生成するファイル。
A file that actually generates sentences at random from the input dataset.

### nijigasaki
作成された3つ組チェーンの情報が保存されているDBファイル。
DB file in which information on the three-pair chains created is stored.