#import "utils.typ": *;

= Dice base system
Every Hero will start their turn by rolling five dice with the following faces:

#recipe(all) or (light, medium, heavy, wits, charm, might)

In addition to these dice each hero has automatic die face results that they may spend each turn, for example:

*Odysseus*
#recipe((wits, wits, might))

*Paris*
#recipe((charm, charm))
These icons can be spent on cards, combat, alliance, and other abilities on the hero cards. Over the course of the game the amount of cards

= Combat
Combat will have all of the same combos as diplomacy, the key difference is that instead of spending gifts towards the activation of combos, we instead have weapons that contribute to combos

= Diplomacy
To become an ally of a palace you need points equal to or greater than the rank of the palace. Or in other words you need to fill a number of buckets equal to one plus the palace rank with one of the following combos.

- Threat #recipe((might, might)) = 1 (However can't use #charm or #wits)
- Emotion #recipe((charm, charm)) = 1
- Reason #recipe((wits, wits)) = 1

Gifts
- #recipe((heavy,) * 5) = 1
- #recipe((medium,) * 4) = 1
- #recipe((light,) * 3) = 1

These gift values will be printed on the physical gifts instead of fame. For isntance a gift might have a value.

= Win conditions
Getting a one of these win conditions, and then sailing off of the edge of the board.

- Having the real Helen
- Having some large number of gifts points on your shif (ex. 4 gold)
- Five? allied regions
- Five? sacked palaces

= Combat
+ Base
#block()[
  #recipe((heavy, ) *3) = 1
  #recipe((medium, ) *3) = 2
  #recipe((light, ) *3) = 3
]
+ Weapons
#block()[
  #recipe((heavy, ) *3) = 1
  #recipe((medium, ) *3) = 2
  #recipe((light, ) *3) = 3

]


#show "hp": it => text(red)[#strong()[#it]]

#recipe((might, might)) = sunder
#par()[
  Remove an armor from this combat, then inflict 1hp, or 2hp no opponent has no armor
]
#recipe((might, charm)) = blood lust (Menelaos)
#par()[
  All subsequent attacks this combat are at +1hp
]
#recipe((charm, charm)) = cheap shot (Paris)
#par()[
  Opponent skips next roll
]
#recipe((wits, charm)) = disarm (Talthybios)
#par()[
  Remove a weapon from this combat or 1hp
]
#recipe((wits, wits)) = deflect
#par()[
  Deflect all recieved hp this round to opponent
]
#recipe((wits, might)) = feint (Odysseus)
#par()[
  Reroll these dice. Inflict 1hp.
]

*Special Character Combat Abilities*

Menelaos: #recipe((might, charm))

Whenever you roll bloodlust reroll the entire hand

Paris: #recipe((charm, charm))

Recover 1hp

Talthybios: #recipe((wits, charm))

Ignore all damage when disarming

Odysseus: #recipe((wits, might))

