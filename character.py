"""
Chapitre 11.1

Classes pour représenter un personnage.
"""


import utils


class Weapon:
	"""
	Une arme dans le jeu.

	:param name:      Le nom de l'arme
	:param power:     Le niveau d'attaque
	:param min_level: Le niveau minimal pour l'utiliser
	"""

	UNARMED_POWER = 20
	
	# TODO: __init__
	def __init__(self, name, attacklv, minlv):
		self.__name = name
		self.attacklv = attacklv
		self.minlv = minlv

	# TODO: Propriétés
	@property
	def name(self):
		return self.__name
	
	def is_usable_by(self,user):
		return user.level >= self.minlv
		
	# TODO: use
	def use(self, user, opponent):
		# TODO: Caculer et appliquer le dommage en utilisant la méthode compute_damage
		#damage, crit = ...
		damage, crit = self.compute_damage(user,opponent)
		opponent.hp -= damage
		msg = ""
		if crit:
			msg += "Critical hit! "
		msg += f"{opponent.name} took {damage} dmg"
		return msg

	# TODO: compute_damage
	def compute_damage(self, attacker, defender):
		return utils.compute_damage_output(
			attacker.level,
			self.attacklv,
			attacker.attack,
			defender.defense,
			1/16,
			(0.85, 1.00)
		)
	# TODO: make_unarmed
	@classmethod
	def make_unarmed(cls):
		return cls("Unarmed",cls.UNARMED_POWER, 1)

class Character:
	"""
	Un personnage dans le jeu

	:param name:    Le nom du personnage
	:param max_hp:  HP maximum
	:param attack:  Le niveau d'attaque du personnage
	:param defense: Le niveau de défense du personnage
	:param level:   Le niveau d'expérience du personnage
	"""
	
	# TODO: __init__
	def  __init__(self, name, max_hp, attack, defense, level):
		self.__name = name
		self.__hp = max_hp
		self.__max_hp = max_hp
		self.attack = attack
		self.defense= defense
		self.level = level
		self.weapon = None
	# TODO: Propriétés
	@property
	def name(self):
		return self.__name
	@property
	def hp(self):
		return self.__hp
	
	@property
	def max_hp(self):
		return self.__max_hp
	
	@max_hp.setter
	def max_hp(self, value):
		self.__max_hp = value
		self.hp = self.hp
	
	@hp.setter
	def hp(self, val):
		self.__hp = utils.clamp(val, 0, self.__max_hp)

	@property
	def weapon(self):
		return self.__weapon
	
	@weapon.setter
	def weapon(self,value):
		if value is None:
			value = Weapon.make_unarmed()
		if not value.is_usable_by(self):
			raise ValueError(Weapon)
		self.__weapon = value

	def apply_turn(self, opponent):
		msg = f"{self.name} used {self.weapon.name}\n"
		msg += self.weapon.use(self, opponent)
		return msg
