#import "utils.typ": *;

#set page(width: 8.5in, height: 5.5in, margin: 0.5em)
#let wits-color = color.rgb(43, 87, 96)
#let charm-color = color.rgb(126, 32, 33)
#let might-color = color.rgb(83, 95, 73)
#let thickness = 10pt

#let player = (name, title, accent, combat_ability_name, combat_ability_icons, general-ability) => [
  #set text(20pt)
  #show heading: set text(accent)
  #show strong: set text(accent)
  = #name
  #v(-0.2em)
  #title
  #v(-0.6em)
  #combat_ability_icons

  #place(top + right)[
    #block()[
      #place(center + horizon)[#box(width: 75%, height: 2em, fill: accent)]
      #grid(columns: 4, rows: 1, gutter: 3mm, ..for i in range(1, 5) {
          (
            block[
              #let length = 60% - (i - 1) * 15.3%
              #place(center + top, dy: 1em)[#box(width: thickness, height: length, fill: accent)]
              #orb(text(accent.transparentize(80%))[#i])],
          )
        })
    ]
  ]

  #for i in range(3) [
    #place(horizon + left, dy: -3.1em + 3em * i)[
      #place(horizon + left)[
        #line(length: 72% - i * 19.64%, stroke: thickness + accent)
      ]
      #box(width: 2.5em, height: 2.5em, stroke: 4pt, fill: white)[
        #place(center + horizon)[ ]
      ]
    ]
  ]

  #place(horizon + center, dy: 0.95em, dx: 8em)[
    #box(width: 3.8in, height: 1.9in, stroke: 4pt, fill: white)[#align(center + top)[
        #block(inset: 8pt)[
          Combat: *#combat_ability_name* (#combat_ability_icons)
          #v(-1em)
          #par(justify: true)[
            #general-ability
          ]
        ]
      ]]
  ]

  #place(bottom + center)[
    #set text(20pt, accent)
    #align(left)[#h(3.1em)#strong[Hit Points]]
    #set text(30pt, accent.transparentize(80%))
    #v(-0.8em)
    #grid(gutter: 1fr, columns: 6, rows: 1, ..for x in range(6) {
        (box(width: 1.25in, height: 1.25in, stroke: 4pt, fill: white)[#align(center + horizon)[#x]],)
      })
  ]
]

#player([Talthybius], [Chief Herald], navy, [Disarm], recipe((charm, wits)), [])
#pagebreak()
#player([Paris], [Trojan Hottie], maroon, [Cheap Shot], recipe((charm, charm)), [])
#pagebreak()
#player([Menelaus], [Placeholder], olive, [Bloodlust], recipe((charm, might)), [])
#pagebreak()
#player([Odysseus], [Crafty Leader], black, [Fient], recipe((might, wits)), [])
#pagebreak()
#player([Sam], [Some Guy], green, [Dissapear], recipe((might, might, might)), [])
