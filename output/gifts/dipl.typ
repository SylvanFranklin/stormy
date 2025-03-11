#let pots = (
  "AMPHORAONE",
  "AMPHORATHREE",
  "AMPHORATWO",
  "CANAANITEAMPHORA",
  "CANAANITEAMPHORAALT",
)

#let war = (
  "COMMONSPEAR",
  "COMMONSWORD",
  "AXE",
  "SWORDS",
  "COMMONBOW",
)

#let gifts = (
  "ALMONDS",
  "AMPHORAONE",
  "AMPHORATHREE",
  "AMPHORATWO",
  "AXE",
  "BABOONS",
  "BEES",
  "BRACELET",
  "CANAANITEAMPHORA",
  "CANAANITEAMPHORAALT",
  "CANAANITEGOD",
  "CARNELIANBEADS",
  "CAT",
  "CEDAR",
  "CHIEFHERALD",
  "CLOTH",
  "COMMONBOW",
  "COMMONSPEAR",
  "COMMONSWORD",
  "COMMONTHORAX",
  "COPPERINGOT",
  "DATES",
  "EARRINGS",
  "EBONY",
  "EXPERTHELMSMAN",
  "FRUITS",
  "FUGITIVEDIVINER",
  "GLASSINGOTS",
  "GOAT",
  "GOLD",
  "GOLDCHALICE",
  "GOLDRHYTON",
  "GREAVES",
  "HEALERHEADINGHOME",
  "HELMET",
  "IRONKNIFE",
  "IVORYDUCK",
  "IVORYRAW",
  "JEWELRY",
  "LAPISLAZULICYLINDERSEAL",
  "LEKYTHION",
  "LYRE",
  "MASTERARCHER",
  "MASTERNAVIGATOR",
  "MUSICGIRLS",
  "MYCENEANJAR",
  "NECKLACE",
  "NEPENTHE",
  "OARS",
  "OLIVEOIL",
  "OSTRICHEGG",
  "POMEGRANITE",
  "RATS",
  "RESIN",
  "ROPE",
  "SCALE",
  "SCARABOFNEFERTITI",
  "SHIELDANDSPEAR",
  "SILVERHILTEDSWORD",
  "SINGER",
  "SLAVES",
  "SPICES",
  "STAND",
  "STATUE",
  "STONESCEPTER",
  "SWORDS",
  "SYMOSIUMBOWL",
  "TABLET",
  "THORAX",
  "TININGOT",
  "TORTOISESHELL",
  "TRIPODONE",
  "TRIPODTWO",
  "UNCOMMONSPEAR",
  "VESSELBLUE",
  "VESSELBLUETWO",
  "VESSELRED",
  "VESSELSILVER",
  "VESSELTALL",
  "WATER",
  "WHEAT",
)

#let key(parts) = {
  show grid.cell: set align(horizon + center)
  let cols = parts.map(part => image(part + ".png"))
  grid(
    stroke: 0pt, gutter: 2pt, columns: parts.len() * 2,
    ..cols
      .map(it => {
        grid.cell[#box(width: 2em)[= #it]]
      })
      .intersperse([=])
  )
}

#let recipe(value, parts) = {
  show grid.cell: set align(horizon + center)
  let cols = parts.map(part => image(part + ".png"))
  cols.push([\= #value])
  grid(
    stroke: 0pt, gutter: 4pt, columns: parts.len() + 1,
    ..cols.map(it => box(width: 2em)[= #it])
  )
}


= Stormy Diplomacy packages
// #recipe(3, ("ALMONDS",) * 4)
// #key(pots)
// #key(war)


#recipe(3, ("COPPERINGOT",) * 3)
