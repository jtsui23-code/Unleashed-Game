class SaveState:
    def __init__(self, player):
        self.player = player
        self.upgrades = {
            'Attack': 0,
            'SP': 0,
            'Infection': 0,
            'FullHeal': 0
        }
        self.code = 0000000000

        self.currentFloor = 1
        self.currentCoin = 0
        self.totalCoin = 0
        self.hp = self.player.currentHp
        self.sp = self.player.currentSp
        self.host = self.player.currentHost

    def setSaveState(self, player, upgrades, currentFloor, currentCoin, totalCoin):
        self.player = player
        self.upgrades = upgrades
        self.currentFloor = currentFloor
        self.currentCoin = currentCoin
        self.totalCoin = totalCoin

    def getSaveState(self):
        return self.player, self.upgrades, self.currentFloor, self.currentCoin, self.totalCoin
    
    def saveCode(self):
        self.code = self.upgrades['Attack'] * 1000000000 + self.upgrades['SP'] * 100000000 + self.upgrades['Infection'] * 10000000 + self.upgrades['FullHeal'] * 1000000 + self.currentFloor * 100000 + self.currentCoin * 10000 + self.totalCoin * 1000 + self.hp * 100 + self.sp * 10 + self.host
        
