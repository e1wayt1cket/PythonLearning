import hashlib, json, time

class Blockchain:
    def __init__(self):
        self.chain = []                 # 存储所有区块
        self.current_tx = []            # 当前区块待打包的交易
        # 创建创世区块
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        """生成新区块并追加到链"""
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_tx,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_tx = []            # 清空当前交易
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """向当前区块添加一笔交易"""
        self.current_tx.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        # 返回这笔交易将被打包进的区块高度
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """计算区块 SHA-256 哈希（字典按 key 排序保证一致性）"""
        block_str = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_str).hexdigest()

    @property
    def last_block(self):
        """获取链上最新区块"""
        return self.chain[-1]

    def is_valid(self):
        """简单校验链完整性：哈希指针是否断裂"""
        for i in range(1, len(self.chain)):
            cur, prev = self.chain[i], self.chain[i-1]
            if cur['previous_hash'] != self.hash(prev):
                return False
        return True

# -------------------- 使用示例 --------------------
if __name__ == '__main__':
    bc = Blockchain()                               # 1. 初始化链
    bc.new_transaction('Alice', 'Bob', 5)          # 2. 添加交易
    bc.new_block(proof=12345)                      # 3. 挖矿（任意 proof）
    bc.new_transaction('Bob', 'Charlie', 2)        # 4. 再一笔交易
    bc.new_block(proof=67890)                      # 5. 继续出块

    # 打印整条链
    for b in bc.chain:
        print('Block', b['index'], b['previous_hash'][:10]+'...', b['proof'])
    print('Chain valid?', bc.is_valid())