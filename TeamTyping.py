class PokeType(object):
    weaknesses = {
                  'normal' :['fighting'],
                  'fire' :['water', 'ground', 'rock'],
                  'water' :['grass', 'electric'],
                  'grass' :['fire', 'ice', 'poison', 'flying', 'bug'],
                  'electric' :['ground'],
                  'ice' :['fire', 'fighting', 'rock', 'steel'],
                  'fighting':['flying', 'psychic', 'fairy'],
                  'poison' :['ground', 'psychic'],
                  'ground' :['water', 'grass', 'ice'],
                  'flying' :['electric', 'ice', 'rock'],
                  'psychic' :['bug', 'ghost', 'dark'],
                  'bug' :['fire', 'flying', 'rock'],
                  'rock' :['water', 'grass', 'fighting', 'ground', 'steel'],
                  'ghost' :['ghost', 'dark'],
                  'dragon' :['ice', 'dragon', 'fairy'],
                  'dark' :['fighting', 'bug', 'fairy'],
                  'steel' :['fire', 'fighting', 'ground'],
                  'fairy' :['poison', 'steel']
                  }
    
    resistances = {'normal' :['none'],
                   'fire' :['fire', 'grass', 'ice', 'bug', 'steel', 'fairy'],
                   'water' :['fire', 'water', 'ice', 'steel'],
                   'grass' :['water', 'grass', 'electric', 'ground'],
                   'electric' :['electric', 'flying', 'steel'],
                   'ice' :['ice'],
                   'fighting':['bug', 'rock', 'dark'],
                   'poison' :['grass', 'fighting', 'poison', 'bug', 'fairy'],
                   'ground' :['poison', 'rock'],
                   'flying' :['grass', 'fighting', 'bug'],
                   'psychic' :['fighting', 'psychic'],
                   'bug' :['grass', 'fighting', 'ground'],
                   'rock' :['normal', 'fire', 'poison', 'flying'],
                   'ghost' :['poison', 'bug'],
                   'dragon' :['fire', 'water', 'grass', 'electric'],
                   'dark' :['ghost', 'dark'],
                   'steel' :['normal', 'grass', 'ice', 'flying', 'psychic', 'bug', 'rock', 'dragon', 'steel', 'fairy'],
                   'fairy' :['fighting', 'bug', 'dark']  }
    
    immunities = {'normal' : 'ghost' ,
                  'ground' : 'electric',
                  'flying' : 'ground',
                  'ghost' : ['normal', 'fighting'],
                  'dark' : 'psychic',
                  'steel' : 'poison' ,
                  'fairy' : 'dragon'}

    def __init__(self, *args):
        self.type = []
        self.weak = []
        self.resist = []
        self.immune = []
        for poke in args:
            Types = poke.split()
            for i in Types:
                self.type.append(i)
                for Type in PokeType.weaknesses[i]:
                    self.weak.append(Type)
                for Type in PokeType.resistances[i]:
                    self.resist.append(Type)
                if i in PokeType.immunities:
                    if  i == 'ghost':
                        for Type in PokeType.immunities[i]:
                            self.immune.append(Type)
                    else:
                        self.immune.append(PokeType.immunities[i])

    def __repr__(self):
        out = ''
        for e in self.type:
            out += e + ' '
        out = out[:-1]
        return out
    
    
class Team(object):

    def __init__(self, *args):
        self.team = []
        self.weak = {'normal' :0,
                   'fire' :0,
                   'water' :0,
                   'grass' :0,
                   'electric' :0,
                   'ice' :0,
                   'fighting':0,
                   'poison' :0,
                   'ground' :0,
                   'flying' :0,
                   'psychic' :0,
                   'bug' :0,
                   'rock' :0,
                   'ghost' :0,
                   'dragon' :0,
                   'dark' :0,
                   'steel' :0,
                   'fairy' :0  }
    
        for poke in args:
            store = None
            temp = poke.split()
            if len(temp) == 2:
                store = PokeType(temp[0], temp[1])
            else:
                store = PokeType(poke)
            self.team.append(store)
            for types in store.weak:
                self.weak[types] += 1
            for types in store.resist:
                if types == 'none':
                    continue        
                self.weak[types] += -1

        for poke in self.team:
            for Type in poke.immune:
                self.weak[Type] = 'immune'
            
        for types in self.weak:
            if self.weak[types] == 'immune':
                self.weak[types] == 0
            else:
                store = self.weak[types]
                self.weak[types] = float(2 ** store)

    def __repr__(self):
        out = ''
        for poke in self.team:
            out += str(poke) + ', '
        out = out[:-2]
        out += "\n"
        for Type in self.weak:
            out += Type + ': ' + str(self.weak[Type]) + '\n'
        return out

    def __add__(self, Poke):
        types = {}
        for i in Poke.weak:
            types[i] = 0
        for i in Poke.weak:
            types[i] += 1
        for i in Poke.resist:
            if i in types or i =='none':
                continue
            types[i] = 0
        for i in Poke.resist:
            if i == 'none':
                continue
            types[i] -= 1
        

        for i in types:
            if self.weak[i] == 'immune':
                continue
            self.weak[i] = float(self.weak[i] * (2 ** types[i]))
        for i in Poke.immune:
            self.weak[i] = 'immune'
        self.team.append(Poke)
        return self

    def __sub__(self, pokePos):
        del self.team[pokePos]
        c = None
        for i in self.team: 
            if self.team.index(i) == 0:
                c = Team(str(i))
            else:
                c += PokeType(str(i))
            
        return c
